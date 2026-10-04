# Restaurante App

## Autor
Efren Jaramillo

## Descripción
Restaurante App es una aplicación de escritorio desarrollada en Python con Tkinter para gestionar un restaurante. Permite iniciar sesión, administrar productos, registrar ventas y gestionar usuarios mediante roles.

## Objetivo
El proyecto busca aplicar programación orientada a objetos, arquitectura modular, interfaces gráficas con Tkinter, persistencia de información mediante archivos JSON y manejo de eventos.

## Funcionalidades

### Login
- Inicio de sesión mediante identificación y contraseña.
- Validación de las credenciales mediante `RestauranteServicio`.
- Identificación del usuario autenticado para determinar sus permisos.
- Manejo de roles.

### Usuarios
En la Semana 16 se incorporó un CRUD completo para la gestión de usuarios:
- Registrar, consultar, actualizar y eliminar usuarios.
- Limpiar el formulario.
- Seleccionar registros mediante un `Treeview` y cargar los datos del usuario seleccionado en el formulario.
- Asignar los roles Administrador, Empleado y Cliente.
- Solo el Administrador puede acceder a la gestión administrativa de usuarios.
- La contraseña no se muestra en el `Treeview`.

### Productos
- Registrar productos.
- Consultar y listar productos.
- Buscar o cargar un producto mediante su código.
- Actualizar y eliminar productos.
- Limpiar el formulario.
- Validar los datos del producto.

### Ventas
- Seleccionar un usuario y un producto.
- Registrar una venta.
- Mostrar las ventas en un `Treeview`.
- Guardar las ventas en `ventas.json`.
- Recuperar las ventas al iniciar nuevamente la aplicación.

## Roles

| Rol | Acceso |
|---|---|
| Administrador | Gestión administrativa de usuarios y funciones de la aplicación |
| Empleado | Acceso a las funciones permitidas, sin gestión administrativa de usuarios |
| Cliente | Acceso a las funciones permitidas, sin gestión administrativa de usuarios |

## Eventos utilizados
En la Semana 16 se implementaron los siguientes eventos:

- `command=` para ejecutar acciones desde los botones.
- `<<TreeviewSelect>>` mediante `bind()` para seleccionar usuarios.
- `<Return>` mediante `bind()` para registrar desde el teclado.
- `<Escape>` mediante `bind()` para limpiar el formulario.
- `<<ComboboxSelected>>` mediante `bind()` para detectar el cambio de rol.

El flujo general de una acción es:

**Usuario → componente → evento/callback → RestauranteServicio → ArchivoServicio → JSON → actualización de interfaz.**

## Arquitectura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
├── main.py
└── README.md
```

## Tecnologías utilizadas
- Python
- Programación Orientada a Objetos
- Tkinter
- ttk
- JSON
- Git y GitHub

## Persistencia de datos
- `productos.json` almacena los productos.
- `usuarios.json` almacena los usuarios, sus contraseñas y roles.
- `ventas.json` almacena las ventas.
- `ArchivoServicio` se encarga de leer y guardar los archivos JSON.
- La interfaz no accede directamente a los archivos JSON; las operaciones se realizan mediante los servicios.

## Recursos visuales
La carpeta `assets` contiene los recursos visuales utilizados por la aplicación, como el logo y el icono.

## Cómo ejecutar el proyecto
1. Tener Python instalado.
2. Abrir una terminal en la carpeta raíz del proyecto.
3. Ejecutar:

```bash
python main.py
```
