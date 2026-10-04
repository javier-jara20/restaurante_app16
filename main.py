import tkinter as tk
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class RestauranteApp:
    def __init__(self, root_window: tk.Tk) -> None:
        self.root = root_window
        self.root.title("Restaurante App")
        self.root.geometry("500x450")

        # 1. Cargar datos usando ArchivoServicio
        archivo_servicio = ArchivoServicio()
        datos_productos = archivo_servicio.cargar_json("datos/productos.json")
        datos_usuarios = archivo_servicio.cargar_json("datos/usuarios.json")

        # 2. Instanciar RestauranteServicio enviando los datos cargados
        self.servicio = RestauranteServicio(
            datos_productos=datos_productos,
            datos_usuarios=datos_usuarios,
            archivo_servicio=archivo_servicio
        )

        self.vista_actual = None
        self.mostrar_login()

    def _limpiar_vista(self) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()

    def mostrar_login(self) -> None:
        self._limpiar_vista()
        self.vista_actual = LoginView(
            master=self.root,
            restaurante_servicio=self.servicio,
            on_login_success=self.mostrar_main
        )

    def mostrar_main(self, usuario_actual: Usuario) -> None:
        self._limpiar_vista()
        self.vista_actual = MainView(
            master=self.root,
            restaurante_servicio=self.servicio,
            on_logout=self.mostrar_login,
            usuario_actual=usuario_actual
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()