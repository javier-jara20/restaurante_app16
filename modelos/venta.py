class Venta:
    def __init__(self, usuario: str, producto: str, fecha: str) -> None:
        self.usuario = usuario
        self.producto = producto
        self.fecha = fecha

    def to_dict(self) -> dict:
        return {
            "usuario": self.usuario,
            "producto": self.producto,
            "fecha": self.fecha
        }