from datetime import datetime

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:

    def __init__(
        self,
        datos_productos: list[dict],
        datos_usuarios: list[dict],
        archivo_servicio: ArchivoServicio
    ) -> None:

        self.archivo_servicio = archivo_servicio

        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.ventas: list[Venta] = []

        self.cargar_productos(datos_productos)
        self.cargar_usuarios(datos_usuarios)
        self.cargar_ventas()

    # -------------------------------------------------
    # CARGA DE DATOS
    # -------------------------------------------------

    def cargar_productos(self, datos_productos: list[dict]) -> None:
        """Convierte los registros JSON en objetos Producto."""

        self.productos.clear()

        for registro in datos_productos:
            producto = Producto(
                codigo=str(registro.get("codigo", "")).strip(),
                nombre=str(registro.get("nombre", "")).strip(),
                categoria=str(registro.get("categoria", "")).strip(),
                precio=float(registro.get("precio", 0)),
                stock=int(registro.get("stock", 0))
            )

            self.productos.append(producto)

    def cargar_usuarios(self, datos_usuarios: list[dict]) -> None:
        """Convierte los registros JSON en objetos Usuario."""

        self.usuarios.clear()

        for registro in datos_usuarios:
            usuario = Usuario(
                identificacion=str(
                    registro.get("identificacion", "")
                ).strip(),
                nombre=str(
                    registro.get("nombre", "")
                ).strip(),
                correo=str(
                    registro.get("correo", "")
                ).strip(),
                contrasena=str(
                    registro.get("contrasena", "")
                ).strip(),
                rol=str(
                    registro.get("rol", "Cliente")
                ).strip()
            )

            self.usuarios.append(usuario)

    def cargar_ventas(self) -> None:
        """Carga las ventas guardadas y crea sus objetos de dominio."""

        self.ventas = [
            Venta(
                usuario=str(registro.get("usuario", "")),
                producto=str(registro.get("producto", "")),
                fecha=str(registro.get("fecha", ""))
            )
            for registro in self.archivo_servicio.cargar_ventas()
        ]

    # -------------------------------------------------
    # LOGIN
    # -------------------------------------------------

    def validar_usuario(
        self,
        identificacion: str,
        clave: str
    ) -> Usuario | None:
        """Valida si un usuario existe y si la contraseña es correcta."""

        for usuario in self.usuarios:
            if (
                usuario.identificacion == identificacion.strip()
                and usuario.contrasena == clave.strip()
            ):
                return usuario

        return None

        

    # -------------------------------------------------
    # CONSULTAS
    # -------------------------------------------------

    def listar_productos(self) -> list[Producto]:
        return self.productos

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def listar_ventas(self) -> list[Venta]:
        return self.ventas

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Busca un producto mediante su código."""

        for producto in self.productos:
            if producto.codigo == codigo:
                return producto

        return None

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        """Busca un usuario mediante su identificación."""

        identificacion = identificacion.strip()

        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario

        return None

    # -------------------------------------------------
    # PERSISTENCIA
    # -------------------------------------------------

    def guardar_productos(self) -> None:
        """Guarda los productos actuales en productos.json."""

        datos = [
            producto.to_dict()
            for producto in self.productos
        ]

        self.archivo_servicio.guardar_json(
            "datos/productos.json",
            datos
        )

    def guardar_usuarios(self) -> None:
        """Guarda los usuarios actuales en usuarios.json."""

        datos = [usuario.to_dict() for usuario in self.usuarios]

        self.archivo_servicio.guardar_json(
            "datos/usuarios.json",
            datos
        )

    def guardar_ventas(self) -> None:
        datos = [venta.to_dict() for venta in self.ventas]
        self.archivo_servicio.guardar_ventas(datos)

    # -------------------------------------------------
    # REGISTRAR PRODUCTO
    # -------------------------------------------------

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> tuple[bool, str]:

        codigo = codigo.strip()
        nombre = nombre.strip()
        categoria = categoria.strip()

        if not codigo or not nombre or not categoria:
            return False, "Todos los campos son obligatorios."

        if self.buscar_producto(codigo) is not None:
            return False, "Ya existe un producto con ese código."

        try:
            nuevo_producto = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=float(precio),
                stock=int(stock)
            )

        except ValueError as error:
            return False, str(error)

        self.productos.append(nuevo_producto)
        self.guardar_productos()

        return True, "Producto registrado correctamente."

    # -------------------------------------------------
    # ACTUALIZAR PRODUCTO
    # -------------------------------------------------

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> tuple[bool, str]:

        producto_existente = self.buscar_producto(codigo.strip())

        if producto_existente is None:
            return False, "No existe un producto con ese código."

        nombre = nombre.strip()
        categoria = categoria.strip()

        if not nombre or not categoria:
            return False, "El nombre y la categoría son obligatorios."

        try:
            producto_actualizado = Producto(
                codigo=producto_existente.codigo,
                nombre=nombre,
                categoria=categoria,
                precio=float(precio),
                stock=int(stock)
            )

        except ValueError as error:
            return False, str(error)

        posicion = self.productos.index(producto_existente)
        self.productos[posicion] = producto_actualizado

        self.guardar_productos()

        return True, "Producto actualizado correctamente."

    # -------------------------------------------------
    # ELIMINAR PRODUCTO
    # -------------------------------------------------

    def eliminar_producto(self, codigo: str) -> tuple[bool, str]:

        producto = self.buscar_producto(codigo.strip())

        if producto is None:
            return False, "No existe un producto con ese código."

        self.productos.remove(producto)
        self.guardar_productos()

        return True, "Producto eliminado correctamente."

    # -------------------------------------------------
    # GESTIÓN DE USUARIOS
    # -------------------------------------------------

    def registrar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str
    ) -> tuple[bool, str]:

        identificacion = identificacion.strip()
        nombre = nombre.strip()
        correo = correo.strip()
        contrasena = contrasena.strip()
        rol = rol.strip()

        if not all((identificacion, nombre, correo, contrasena, rol)):
            return False, "Todos los campos son obligatorios."

        if self.buscar_usuario(identificacion) is not None:
            return False, "Ya existe un usuario con esa identificación."

        try:
            nuevo_usuario = Usuario(
                identificacion=identificacion,
                nombre=nombre,
                correo=correo,
                contrasena=contrasena,
                rol=rol
            )
        except ValueError as error:
            return False, str(error)

        self.usuarios.append(nuevo_usuario)

        try:
            self.guardar_usuarios()
        except (OSError, TypeError, ValueError) as error:
            self.usuarios.remove(nuevo_usuario)
            return False, f"No se pudo guardar el usuario: {error}"

        return True, "Usuario registrado correctamente."

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str
    ) -> tuple[bool, str]:

        usuario_existente = self.buscar_usuario(identificacion)

        if usuario_existente is None:
            return False, "No existe un usuario con esa identificación."

        try:
            usuario_actualizado = Usuario(
                identificacion=usuario_existente.identificacion,
                nombre=nombre.strip(),
                correo=correo.strip(),
                contrasena=contrasena.strip(),
                rol=rol.strip()
            )
        except ValueError as error:
            return False, str(error)

        posicion = self.usuarios.index(usuario_existente)
        self.usuarios[posicion] = usuario_actualizado

        try:
            self.guardar_usuarios()
        except (OSError, TypeError, ValueError) as error:
            self.usuarios[posicion] = usuario_existente
            return False, f"No se pudo guardar el usuario: {error}"

        return True, "Usuario actualizado correctamente."

    def eliminar_usuario(self, identificacion: str) -> tuple[bool, str]:

        usuario = self.buscar_usuario(identificacion)

        if usuario is None:
            return False, "No existe un usuario con esa identificación."

        administradores = sum(
            usuario.rol == "Administrador"
            for usuario in self.usuarios
        )
        if usuario.rol == "Administrador" and administradores == 1:
            return False, "No se puede eliminar al único administrador."

        posicion = self.usuarios.index(usuario)
        self.usuarios.remove(usuario)

        try:
            self.guardar_usuarios()
        except (OSError, TypeError, ValueError) as error:
            self.usuarios.insert(posicion, usuario)
            return False, f"No se pudo guardar el usuario: {error}"

        return True, "Usuario eliminado correctamente."

    def registrar_venta(
        self,
        identificacion_usuario: str,
        codigo_producto: str
    ) -> tuple[bool, str]:
        usuario = next(
            (
                usuario
                for usuario in self.usuarios
                if usuario.identificacion == identificacion_usuario.strip()
            ),
            None
        )
        if usuario is None:
            return False, "El usuario seleccionado no existe."

        producto = self.buscar_producto(codigo_producto.strip())
        if producto is None:
            return False, "El producto seleccionado no existe."

        venta = Venta(
            usuario=usuario.nombre,
            producto=producto.nombre,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.ventas.append(venta)
        self.guardar_ventas()

        return True, "Venta registrada correctamente."