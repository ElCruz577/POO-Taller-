# archivos.py
import datetime
from clases import Cliente

def registrarError(mensaje):
    """Genera el log con fecha y hora en modo 'a' (agregar) para no borrar anteriores."""
    fechaHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_errores.txt", "a", encoding="utf-8") as archivoLog:
        archivoLog.write(f"{fechaHora} | ERROR | {mensaje}\n")

class GestorArchivos:
    """Clase de persistencia para leer y guardar datos en archivos de texto."""
    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo

    def guardarClientes(self, listaClientes):
        """Escribe los objetos en el archivo de texto."""
        with open(self.nombreArchivo, "w", encoding="utf-8") as f:
            for cliente in listaClientes:
                f.write(f"{cliente.nombre},{cliente.telefono}\n")
        print(f"Datos guardados exitosamente en {self.nombreArchivo}")

    def cargarClientes(self):
        """Carga y reconstruye objetos desde el archivo de texto."""
        clientesReconstruidos = []
        try:
            with open(self.nombreArchivo, "r", encoding="utf-8") as f:
                for linea in f:
                    if linea.strip():
                        datos = linea.strip().split(",")
                        cliente = Cliente(datos[0], datos[1])
                        clientesReconstruidos.append(cliente)
            print("Datos cargados exitosamente.")
        except FileNotFoundError:
            print("El archivo no existe. Creando uno nuevo vacío...")
            with open(self.nombreArchivo, "w", encoding="utf-8") as f:
                pass
                
        return clientesReconstruidos