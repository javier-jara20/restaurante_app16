class Usuario:

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        contrasena: str,
        rol: str
    ) -> None:

        if not identificacion.strip():
            raise ValueError(
                "La identificación no puede estar vacía."
            )

        if not nombre.strip():
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if not correo.strip():
            raise ValueError(
                "El correo no puede estar vacío."
            )

        if not contrasena.strip():
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

        if rol not in ("Administrador", "Empleado", "Cliente"):
            raise ValueError(
                "El rol debe ser Administrador, Empleado o Cliente."
            )

        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol

    def mostrar_informacion(self) -> str:
        return (
            f"Identificación: {self.identificacion}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Rol: {self.rol}"
        )

    def to_dict(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "rol": self.rol
        }