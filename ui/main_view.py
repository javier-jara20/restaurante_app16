import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from servicios.restaurante_servicio import RestauranteServicio
from modelos.usuario import Usuario


class MainView(tk.Frame):
    codigo_var: tk.StringVar
    nombre_var: tk.StringVar
    categoria_var: tk.StringVar
    precio_var: tk.StringVar
    stock_var: tk.StringVar
    tabla_productos: ttk.Treeview
    usuario_venta_var: tk.StringVar
    producto_venta_var: tk.StringVar
    tabla_ventas: ttk.Treeview
    usuario_venta_combo: ttk.Combobox
    producto_venta_combo: ttk.Combobox
    usuarios_venta_por_opcion: dict[str, str]
    productos_venta_por_opcion: dict[str, str]
    identificacion_usuario_var: tk.StringVar
    usuario_nombre_var: tk.StringVar
    usuario_correo_var: tk.StringVar
    usuario_contrasena_var: tk.StringVar
    usuario_rol_var: tk.StringVar
    usuario_rol_estado_var: tk.StringVar
    tabla_usuarios: ttk.Treeview
    usuario_rol_combo: ttk.Combobox
    logo_imagen: tk.PhotoImage
    icono_imagen: tk.PhotoImage

    def __init__(
        self,
        master,
        restaurante_servicio: RestauranteServicio,
        on_logout,
        usuario_actual: Usuario
    ):
        super().__init__(master)
        self.master = master
        self.servicio = restaurante_servicio
        self.on_logout = on_logout
        self.usuario_actual = usuario_actual
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.stock_var = tk.StringVar()
        self.usuario_venta_var = tk.StringVar()
        self.producto_venta_var = tk.StringVar()
        self.identificacion_usuario_var = tk.StringVar()
        self.usuario_nombre_var = tk.StringVar()
        self.usuario_correo_var = tk.StringVar()
        self.usuario_contrasena_var = tk.StringVar()
        self.usuario_rol_var = tk.StringVar()
        self.usuario_rol_estado_var = tk.StringVar()
        ruta_assets = Path(__file__).resolve().parent.parent / "assets"
        logo_original = getattr(self.master, "_restaurante_logo_original", None)
        if logo_original is None:
            logo_original = tk.PhotoImage(
                master=self.master,
                file=str(ruta_assets / "logo.png")
            )
            self.master._restaurante_logo_original = logo_original
        self.logo_imagen = logo_original.subsample(8, 8)
        self.icono_imagen = tk.PhotoImage(
            master=self.master,
            file=str(ruta_assets / "icono.png")
        ).subsample(16, 16)

        self.master.geometry("1180x760")
        self.master.minsize(900, 620)
        self.pack(fill="both", expand=True)
        self._crear_widgets()
        if self._es_administrador():
            self.bind("<Return>", lambda event: self._registrar_usuario())
            self.bind("<Escape>", lambda event: self._limpiar_formulario_usuario())

    def _es_administrador(self) -> bool:
        return self.usuario_actual.rol == "Administrador"

    def _crear_widgets(self):
        self._configurar_estilos()

        contenedor = ttk.Frame(self, style="App.TFrame")
        contenedor.pack(fill="both", expand=True)

        barra_lateral = ttk.Frame(
            contenedor,
            width=220,
            style="Sidebar.TFrame"
        )
        barra_lateral.pack(side="left", fill="y")
        barra_lateral.pack_propagate(False)

        ttk.Label(
            barra_lateral,
            text="RESTAURANTE",
            style="SidebarBrand.TLabel"
        ).pack(anchor="w", padx=22, pady=(30, 2))
        ttk.Label(
            barra_lateral,
            text="JARAMILLO",
            style="SidebarName.TLabel"
        ).pack(anchor="w", padx=22, pady=(0, 30))

        contenido = ttk.Frame(contenedor, padding=(26, 22), style="App.TFrame")
        contenido.pack(side="left", fill="both", expand=True)
        encabezado = ttk.Frame(contenido, style="App.TFrame")
        encabezado.pack(fill="x", pady=(0, 16))
        ttk.Label(
            encabezado,
            text="Panel de administración",
            style="PageTitle.TLabel"
        ).pack(side="left", anchor="center")
        tk.Label(
            encabezado,
            image=self.logo_imagen,
            bg="#f2f5f8",
            borderwidth=0
        ).pack(side="right")

        self.notebook = ttk.Notebook(contenido)
        self.notebook.pack(fill="both", expand=True)

        self.frame_productos = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(
            self.frame_productos,
            text=f"Productos ({self.servicio.cantidad_productos()})"
        )
        self._crear_seccion_productos()

        if self._es_administrador():
            self.frame_usuarios = ttk.Frame(self.notebook, padding=16)
            self.notebook.add(
                self.frame_usuarios,
                text=f"Usuarios ({self.servicio.cantidad_usuarios()})"
            )
            self._crear_seccion_usuarios(self.frame_usuarios)

        self.frame_ventas = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.frame_ventas, text="Ventas")
        self._crear_seccion_ventas()

        opciones = [
            ("🏠 Inicio", lambda: self.notebook.select(self.frame_productos), "Nav.TButton"),
            ("🍔 Productos", lambda: self.notebook.select(self.frame_productos), "Nav.TButton"),
            ("💰 Ventas", lambda: self.notebook.select(self.frame_ventas), "Nav.TButton"),
        ]
        if self._es_administrador():
            opciones.insert(
                1,
                (
                    "👥 Usuarios",
                    lambda: self.notebook.select(self.frame_usuarios),
                    "Nav.TButton"
                )
            )
        for texto, comando, estilo in opciones:
            boton = ttk.Button(
                barra_lateral,
                text=texto,
                command=comando,
                style=estilo
            )
            boton.pack(fill="x", padx=12, pady=3)

        ttk.Button(
            barra_lateral,
            text="Cerrar sesión",
            image=self.icono_imagen,
            compound="left",
            command=self.on_logout,
            style="Logout.TButton"
        ).pack(side="bottom", fill="x", padx=12, pady=18)

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("App.TFrame", background="#f2f5f8")
        estilo.configure("TFrame", background="#f2f5f8")
        estilo.configure("Sidebar.TFrame", background="#102a43")
        estilo.configure(
            "SidebarBrand.TLabel",
            background="#102a43",
            foreground="#e0b84f",
            font=("Arial", 10, "bold")
        )
        estilo.configure(
            "SidebarName.TLabel",
            background="#102a43",
            foreground="#ffffff",
            font=("Arial", 17, "bold")
        )
        estilo.configure(
            "Nav.TButton",
            background="#102a43",
            foreground="#f2f5f8",
            anchor="w",
            padding=(14, 11),
            borderwidth=0,
            font=("Arial", 10, "bold")
        )
        estilo.map(
            "Nav.TButton",
            background=[("active", "#1d4666"), ("disabled", "#102a43")],
            foreground=[("disabled", "#8093a5")]
        )
        estilo.configure(
            "PageTitle.TLabel",
            background="#f2f5f8",
            foreground="#183b56",
            font=("Arial", 20, "bold")
        )
        estilo.configure(
            "Primary.TButton",
            background="#1769aa",
            foreground="#ffffff",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Primary.TButton", background=[("active", "#12588f")])
        estilo.configure(
            "Gold.TButton",
            background="#c99a22",
            foreground="#ffffff",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Gold.TButton", background=[("active", "#a97f19")])
        estilo.configure(
            "Danger.TButton",
            background="#c0392b",
            foreground="#ffffff",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Danger.TButton", background=[("active", "#a93226")])
        estilo.configure(
            "Neutral.TButton",
            background="#dce4eb",
            foreground="#183b56",
            padding=(11, 8),
            borderwidth=0,
            font=("Arial", 9, "bold")
        )
        estilo.map("Neutral.TButton", background=[("active", "#c8d4de")])
        estilo.configure(
            "Logout.TButton",
            background="#c0392b",
            foreground="#ffffff",
            padding=(12, 10),
            borderwidth=0,
            font=("Arial", 10, "bold")
        )
        estilo.map("Logout.TButton", background=[("active", "#a93226")])
        estilo.configure("TNotebook", background="#f2f5f8", borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            background="#dce4eb",
            foreground="#183b56",
            padding=(14, 8),
            font=("Arial", 9, "bold")
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#ffffff")],
            foreground=[("selected", "#1769aa")]
        )
        estilo.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#263746",
            rowheight=32,
            font=("Arial", 10)
        )
        estilo.configure(
            "Treeview.Heading",
            background="#183b56",
            foreground="#ffffff",
            padding=(8, 9),
            font=("Arial", 9, "bold")
        )

    def _crear_seccion_productos(self):
        formulario = ttk.LabelFrame(
            self.frame_productos,
            text="Datos del producto",
            padding=14
        )
        formulario.pack(fill="x", pady=(0, 12))

        campos = (
            ("Código", self.codigo_var),
            ("Nombre", self.nombre_var),
            ("Categoría", self.categoria_var),
            ("Precio", self.precio_var),
            ("Stock", self.stock_var),
        )

        for columna, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(
                row=0, column=columna, padx=4, pady=(0, 4), sticky="w"
            )
            ttk.Entry(formulario, textvariable=variable, width=18).grid(
                row=1, column=columna, padx=4, sticky="ew"
            )

        for columna in range(len(campos)):
            formulario.columnconfigure(columna, weight=1)

        botones = ttk.Frame(self.frame_productos)
        botones.pack(fill="x", pady=(0, 10))
        ttk.Button(
            botones,
            text="➕ Registrar",
            command=self._registrar_producto,
            style="Primary.TButton"
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            botones,
            text="🔍 Cargar por código",
            command=self._cargar_producto,
            style="Gold.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="✏️ Actualizar",
            command=self._actualizar_producto,
            style="Primary.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="🗑️ Eliminar",
            command=self._eliminar_producto,
            style="Danger.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="🧹 Limpiar",
            command=self._limpiar_formulario,
            style="Neutral.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="↻ Refrescar",
            command=self._refrescar_productos,
            style="Neutral.TButton"
        ).pack(side="left", padx=6)

        tabla_frame = ttk.Frame(self.frame_productos)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=10
        )
        encabezados = {
            "codigo": "Código",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Stock",
        }
        for columna in columnas:
            self.tabla_productos.heading(columna, text=encabezados[columna])
            self.tabla_productos.column(columna, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=scrollbar.set)
        self.tabla_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._refrescar_productos()

    def _cargar_producto(self):
        codigo = self.codigo_var.get().strip()
        producto = self.servicio.buscar_producto(codigo)
        if producto is None:
            messagebox.showerror("Error", "No existe un producto con ese código.")
            return

        self.codigo_var.set(producto.codigo)
        self.nombre_var.set(producto.nombre)
        self.categoria_var.set(producto.categoria)
        self.precio_var.set(str(producto.precio))
        self.stock_var.set(str(producto.stock))

    def _crear_seccion_usuarios(self, frame_usuarios):
        formulario = ttk.LabelFrame(
            frame_usuarios,
            text="Datos del usuario",
            padding=14
        )
        formulario.pack(fill="x", pady=(0, 10))

        campos = (
            ("Identificación", self.identificacion_usuario_var),
            ("Nombre", self.usuario_nombre_var),
            ("Correo", self.usuario_correo_var),
            ("Contraseña", self.usuario_contrasena_var),
        )
        entradas = []
        for columna, (texto, variable) in enumerate(campos):
            ttk.Label(formulario, text=texto).grid(
                row=0, column=columna, padx=4, pady=(0, 4), sticky="w"
            )
            entrada = ttk.Entry(formulario, textvariable=variable, width=18)
            entrada.grid(row=1, column=columna, padx=4, sticky="ew")
            entradas.append(entrada)

        ttk.Label(formulario, text="Rol").grid(
            row=0, column=4, padx=4, pady=(0, 4), sticky="w"
        )
        self.usuario_rol_combo = ttk.Combobox(
            formulario,
            textvariable=self.usuario_rol_var,
            values=("Administrador", "Empleado", "Cliente"),
            state="readonly",
            width=18
        )
        self.usuario_rol_combo.grid(
            row=1, column=4, padx=4, sticky="ew"
        )
        self.usuario_rol_combo.bind(
            "<<ComboboxSelected>>",
            self._cambio_rol_usuario
        )
        for columna in range(5):
            formulario.columnconfigure(columna, weight=1)

        ttk.Label(
            formulario,
            textvariable=self.usuario_rol_estado_var
        ).grid(row=2, column=0, columnspan=5, sticky="w", padx=4, pady=(6, 0))

        botones = ttk.Frame(frame_usuarios)
        botones.pack(fill="x", pady=(0, 10))
        ttk.Button(
            botones,
            text="Registrar",
            command=self._registrar_usuario,
            style="Primary.TButton"
        ).pack(side="left", padx=(0, 6))
        ttk.Button(
            botones,
            text="Actualizar",
            command=self._actualizar_usuario,
            style="Gold.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="Eliminar",
            command=self._eliminar_usuario,
            style="Danger.TButton"
        ).pack(side="left", padx=6)
        ttk.Button(
            botones,
            text="Limpiar",
            command=self._limpiar_formulario_usuario,
            style="Neutral.TButton"
        ).pack(side="left", padx=6)

        tabla_frame = ttk.Frame(frame_usuarios)
        tabla_frame.pack(fill="both", expand=True)
        columnas = ("identificacion", "nombre", "usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=10
        )
        encabezados = {
            "identificacion": "Identificación",
            "nombre": "Nombre",
            "usuario": "Usuario",
            "rol": "Rol",
        }
        for columna in columnas:
            self.tabla_usuarios.heading(columna, text=encabezados[columna])
            self.tabla_usuarios.column(columna, width=150, anchor="center")
        self.tabla_usuarios.bind(
            "<<TreeviewSelect>>",
            self._seleccionar_usuario
        )

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_usuarios.yview
        )
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)
        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for widget in (*entradas, self.usuario_rol_combo, self.tabla_usuarios):
            widget.bind(
                "<Return>",
                lambda event: self._registrar_usuario(),
                add="+"
            )
            widget.bind(
                "<Escape>",
                lambda event: self._limpiar_formulario_usuario(),
                add="+"
            )

        self._refrescar_usuarios()

    def _cambio_rol_usuario(self, _evento=None):
        self.usuario_rol_estado_var.set(
            f"Rol seleccionado: {self.usuario_rol_var.get()}"
        )

    def _seleccionar_usuario(self, _evento=None):
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return

        identificacion = self.tabla_usuarios.item(
            seleccion[0],
            "values"
        )[0]
        usuario = self.servicio.buscar_usuario(identificacion)
        if usuario is None:
            messagebox.showerror(
                "Error",
                "No se encontró el usuario seleccionado."
            )
            return

        self.identificacion_usuario_var.set(usuario.identificacion)
        self.usuario_nombre_var.set(usuario.nombre)
        self.usuario_correo_var.set(usuario.correo)
        self.usuario_contrasena_var.set(usuario.contrasena)
        self.usuario_rol_var.set(usuario.rol)
        self.usuario_rol_estado_var.set("")

    def _registrar_usuario(self):
        resultado, mensaje = self.servicio.registrar_usuario(
            self.identificacion_usuario_var.get(),
            self.usuario_nombre_var.get(),
            self.usuario_correo_var.get(),
            self.usuario_contrasena_var.get(),
            self.usuario_rol_var.get()
        )
        self._refrescar_usuarios()
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._limpiar_formulario_usuario()

    def _actualizar_usuario(self):
        resultado, mensaje = self.servicio.actualizar_usuario(
            self.identificacion_usuario_var.get(),
            self.usuario_nombre_var.get(),
            self.usuario_correo_var.get(),
            self.usuario_contrasena_var.get(),
            self.usuario_rol_var.get()
        )
        self._refrescar_usuarios()
        self._mostrar_resultado(resultado, mensaje)

    def _eliminar_usuario(self):
        identificacion = self.identificacion_usuario_var.get().strip()
        if not identificacion:
            messagebox.showwarning(
                "Selección requerida",
                "Seleccione un usuario para eliminar."
            )
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este usuario?"
        ):
            return

        resultado, mensaje = self.servicio.eliminar_usuario(identificacion)
        self._refrescar_usuarios()
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._limpiar_formulario_usuario()

    def _limpiar_formulario_usuario(self):
        for variable in (
            self.identificacion_usuario_var,
            self.usuario_nombre_var,
            self.usuario_correo_var,
            self.usuario_contrasena_var,
            self.usuario_rol_var,
            self.usuario_rol_estado_var,
        ):
            variable.set("")
        seleccion = self.tabla_usuarios.selection()
        if seleccion:
            self.tabla_usuarios.selection_remove(*seleccion)
        self.tabla_usuarios.focus("")

    def _refrescar_usuarios(self):
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        for usuario in self.servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                "end",
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.correo,
                    usuario.rol
                )
            )

        self.notebook.tab(
            self.frame_usuarios,
            text=f"Usuarios ({self.servicio.cantidad_usuarios()})"
        )

    def _crear_seccion_ventas(self):
        formulario = ttk.LabelFrame(
            self.frame_ventas,
            text="Registrar venta",
            padding=14
        )
        formulario.pack(fill="x", pady=(0, 12))

        ttk.Label(formulario, text="Usuario").grid(
            row=0, column=0, padx=4, pady=(0, 4), sticky="w"
        )
        ttk.Label(formulario, text="Producto").grid(
            row=0, column=1, padx=4, pady=(0, 4), sticky="w"
        )
        self.usuario_venta_combo = ttk.Combobox(
            formulario,
            textvariable=self.usuario_venta_var,
            state="readonly"
        )
        self.usuario_venta_combo.grid(
            row=1, column=0, padx=4, sticky="ew"
        )
        self.producto_venta_combo = ttk.Combobox(
            formulario,
            textvariable=self.producto_venta_var,
            state="readonly"
        )
        self.producto_venta_combo.grid(
            row=1, column=1, padx=4, sticky="ew"
        )
        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        ttk.Button(
            formulario,
            text="Registrar venta",
            command=self.registrar_venta,
            style="Primary.TButton"
        ).grid(row=1, column=2, padx=(10, 4), sticky="ew")

        tabla_frame = ttk.Frame(self.frame_ventas)
        tabla_frame.pack(fill="both", expand=True)
        columnas = ("usuario", "producto", "fecha")
        self.tabla_ventas = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            height=12
        )
        encabezados = {
            "usuario": "Usuario",
            "producto": "Producto",
            "fecha": "Fecha"
        }
        for columna in columnas:
            self.tabla_ventas.heading(columna, text=encabezados[columna])
            self.tabla_ventas.column(columna, width=180, anchor="center")

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla_ventas.yview
        )
        self.tabla_ventas.configure(yscrollcommand=scrollbar.set)
        self.tabla_ventas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._actualizar_opciones_ventas()
        self._refrescar_ventas()

    def _actualizar_opciones_ventas(self):
        self.usuarios_venta_por_opcion = {
            f"{usuario.identificacion} - {usuario.nombre}": usuario.identificacion
            for usuario in self.servicio.listar_usuarios()
        }
        self.productos_venta_por_opcion = {
            f"{producto.codigo} - {producto.nombre}": producto.codigo
            for producto in self.servicio.listar_productos()
        }
        usuarios = tuple(self.usuarios_venta_por_opcion)
        productos = tuple(self.productos_venta_por_opcion)
        self.usuario_venta_combo.configure(values=usuarios)
        self.producto_venta_combo.configure(values=productos)
        if self.usuario_venta_var.get() not in usuarios:
            self.usuario_venta_var.set("")
        if self.producto_venta_var.get() not in productos:
            self.producto_venta_var.set("")

    def _refrescar_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        for venta in self.servicio.listar_ventas():
            self.tabla_ventas.insert(
                "",
                "end",
                values=(venta.usuario, venta.producto, venta.fecha)
            )

    def registrar_venta(self):
        opcion_usuario = self.usuario_venta_var.get()
        opcion_producto = self.producto_venta_var.get()
        identificacion = self.usuarios_venta_por_opcion.get(opcion_usuario)
        codigo = self.productos_venta_por_opcion.get(opcion_producto)

        if identificacion is None or codigo is None:
            messagebox.showwarning(
                "Selección requerida",
                "Seleccione un usuario y un producto."
            )
            return

        resultado, mensaje = self.servicio.registrar_venta(
            identificacion,
            codigo
        )
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._refrescar_ventas()
            self.usuario_venta_var.set("")
            self.producto_venta_var.set("")

    def _refrescar_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)

        for producto in self.servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"{producto.precio:.2f}",
                    producto.stock
                )
            )
        self.notebook.tab(
            self.frame_productos,
            text=f"Productos ({self.servicio.cantidad_productos()})"
        )
        if hasattr(self, "usuario_venta_combo"):
            self._actualizar_opciones_ventas()

    def _registrar_producto(self):
        try:
            precio = float(self.precio_var.get())
            stock = int(self.stock_var.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser decimal y el stock debe ser entero."
            )
            return

        resultado, mensaje = self.servicio.registrar_producto(
            self.codigo_var.get(),
            self.nombre_var.get(),
            self.categoria_var.get(),
            precio,
            stock
        )
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._refrescar_productos()
            self._limpiar_formulario()

    def _actualizar_producto(self):
        try:
            precio = float(self.precio_var.get())
            stock = int(self.stock_var.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser decimal y el stock debe ser entero."
            )
            return

        resultado, mensaje = self.servicio.actualizar_producto(
            self.codigo_var.get(),
            self.nombre_var.get(),
            self.categoria_var.get(),
            precio,
            stock
        )
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._refrescar_productos()

    def _eliminar_producto(self):
        codigo = self.codigo_var.get().strip()
        resultado, mensaje = self.servicio.eliminar_producto(codigo)
        self._mostrar_resultado(resultado, mensaje)
        if resultado:
            self._refrescar_productos()
            self._limpiar_formulario()

    def _mostrar_resultado(self, resultado, mensaje):
        if resultado:
            messagebox.showinfo("Operación exitosa", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def _limpiar_formulario(self):
        for variable in (
            self.codigo_var,
            self.nombre_var,
            self.categoria_var,
            self.precio_var,
            self.stock_var,
        ):
            variable.set("")