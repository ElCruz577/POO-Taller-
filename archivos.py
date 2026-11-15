# archivos.py - Módulo de persistencia en archivo .txt y bitácora log_errores.txt

from datetime import datetime # Para registrar fecha y hora exacta en el log
from pathlib import Path # Visto en clase 12.1 para construir rutas en la carpeta actual
from clases import Empleado, Cliente, EquipoTaller, TareaMantenimiento, TareaAdministrativa, RegistroError

carpeta = Path(__file__).resolve().parent # Obtiene la carpeta donde está guardado este archivo .py
rutaLog = carpeta / "log_errores.txt" # Ruta del archivo log_errores.txt en la misma carpeta

def contarRegistros(): # Función vista en clase 12.2 para numerar cada error con enumerate
    """Cuenta cuántas líneas tiene log_errores.txt usando enumerate.""" # Docstring
    total = 0 # Inicia el contador en 0
    try: # Intenta abrir el log si ya existe
        with open(rutaLog, "r", encoding="utf-8") as f: # Abre en modo lectura con utf-8
            for total, linea in enumerate(f, start=1): # Cuenta los renglones empezando en 1
                pass # Avanza hasta la última línea
    except FileNotFoundError: # Si aún no existe el archivo log
        pass # Devuelve 0 y se creará al escribir el primer error
    return total # Retorna el total de líneas contadas

def registrarError(mensaje): # Función reutilizable llamada en TODOS los bloques except
    """Registra el error con número, fecha, hora y mensaje en modo 'a'.""" # Docstring
    numero = contarRegistros() + 1 # Número consecutivo del error
    fechaHora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Formato Año-Mes-Día Hora:Min:Seg
    with open(rutaLog, "a", encoding="utf-8") as archivoLog: # Modo 'a' agrega al final sin borrar
        archivoLog.write(f"{numero} | {fechaHora} | ERROR | {mensaje}\n") # Escribe el registro

class GestorArchivos: # Clase exclusiva de persistencia (guarda y reconstruye todos los datos de las 6 clases)
    """Gestiona el guardado, carga, consulta, modificación y baja de tareas.""" # Docstring
    def __init__(self, nombreArchivo): # Constructor que recibe el nombre del archivo .txt
        self.rutaArchivo = carpeta / nombreArchivo # Ruta completa a tareas_taller.txt
        self.listaTareas = [] # Lista en memoria donde viven los objetos de las tareas

    def guardarTareas(self): # Guarda todos los objetos en tareas_taller.txt con sus datos reales
        try: # Bloque try para proteger la escritura
            with open(self.rutaArchivo, "w", encoding="utf-8") as f: # Modo 'w' actualiza el archivo
                for t in self.listaTareas: # Recorre cada tarea registrada
                    if isinstance(t, TareaMantenimiento): # Si es Mantenimiento, guarda frecuenciaDias, técnico y equipo
                        f.write(f"Mantenimiento,{t.titulo},{t.fechaLimite},{t.prioridad},{t.completada},{t.frecuenciaDias},{t.tecnico.nombreCompleto},{t.equipo.numeroSerie}\n")
                    else: # Si es Administrativa, guarda el teléfono real del cliente, su nombre y el departamento
                        f.write(f"Administrativa,{t.titulo},{t.fechaLimite},{t.prioridad},{t.completada},{t.clienteRelacionado.telefono},{t.clienteRelacionado.nombre},{t.departamento}\n")
        except PermissionError as e: # Captura error de permisos (pedido en retroalimentación)
            registrarError(f"PermissionError al guardar: {e}") # Lo anota en log_errores.txt

    def cargarTareas(self): # Lee tareas_taller.txt y reconstruye los objetos exactos con sus datos
        self.listaTareas = [] # Limpia la lista antes de cargar
        try: # Intenta abrir tareas_taller.txt
            with open(self.rutaArchivo, "r", encoding="utf-8") as f: # Modo lectura con codificación utf-8
                for linea in f: # Lee línea por línea
                    if linea.strip() != "": # Ignora líneas en blanco
                        d = linea.strip().split(",") # Separa los datos por coma
                        datoExtra = d[5] if len(d) > 5 else "30" # Días (en Mantenimiento) o Teléfono (en Administrativa)
                        resp = d[6] if len(d) > 6 else "Juan Perez" # Recupera el técnico o cliente guardado
                        area = d[7] if len(d) > 7 else "General" # Recupera el equipo o departamento guardado
                        if d[0] == "Mantenimiento": # Reconstruye EquipoTaller, Empleado y TareaMantenimiento
                            eq = EquipoTaller(area, "Maquinaria") # Crea el objeto EquipoTaller con lo guardado
                            tec = Empleado(resp, "Técnico") # Crea el objeto Empleado con lo guardado
                            obj = TareaMantenimiento(d[1], d[2], d[3], eq, tec, int(datoExtra)) # Crea subclase 1
                        else: # Reconstruye Cliente (con su teléfono real guardado) y TareaAdministrativa
                            cli = Cliente(resp, datoExtra) # Crea el objeto Cliente con su nombre y teléfono reales
                            obj = TareaAdministrativa(d[1], d[2], d[3], area, True, cli) # Crea subclase 2
                        obj.completada = (d[4] == "True") # Restaura el estado booleano completada
                        self.listaTareas.append(obj) # Agrega el objeto reconstruido a la lista
        except FileNotFoundError as e: # Si el archivo aún no existe
            registrarError(f"FileNotFoundError: {e}") # Registra en log_errores.txt
            with open(self.rutaArchivo, "w", encoding="utf-8") as f: # Crea el archivo vacío
                pass # Se cierra automáticamente con with
        except PermissionError as e: # Si no hay permisos para leer el archivo
            registrarError(f"PermissionError al cargar: {e}") # Registra el error en el log
        return self.listaTareas # Devuelve la lista de objetos reconstruidos

    def agregarTarea(self, nuevaTarea): # Operación 1: Alta validando que no exista duplicado
        for t in self.listaTareas: # Recorre las tareas actuales
            if t.titulo.lower() == nuevaTarea.titulo.lower(): # Si el título ya está registrado
                raise RegistroError(f"La tarea '{nuevaTarea.titulo}' ya está registrada") # Lanza error propio
        self.listaTareas.append(nuevaTarea) # Agrega el objeto a la lista
        self.guardarTareas() # Guarda inmediatamente en tareas_taller.txt

    def buscarTarea(self, tituloBuscar): # Operación 2: Consulta por título
        for t in self.listaTareas: # Recorre la lista buscando el título
            if t.titulo.lower() == tituloBuscar.strip().lower(): # Si coincide
                return t # Devuelve el objeto encontrado
        raise RegistroError(f"No se encontró la tarea '{tituloBuscar}'") # Si no existe, lanza error propio

    def modificarTarea(self, tituloBuscar, nuevaTareaModificada): # Operación 3: Modificación completa
        for i, t in enumerate(self.listaTareas): # Busca la posición de la tarea con enumerate
            if t.titulo.lower() == tituloBuscar.strip().lower(): # Cuando encuentra la tarea por su título
                nuevaTareaModificada.completada = t.completada # Conserva si estaba Pendiente o Completada
                self.listaTareas[i] = nuevaTareaModificada # Reemplaza con todos los datos nuevos
                self.guardarTareas() # Guarda los cambios en tareas_taller.txt
                return # Termina el método con éxito
        raise RegistroError(f"No se encontró la tarea '{tituloBuscar}' para modificar") # Error si no existe

    def eliminarTarea(self, tituloBuscar): # Operación 4: Baja / Eliminación
        tarea = self.buscarTarea(tituloBuscar) # Verifica que la tarea exista
        self.listaTareas.remove(tarea) # Elimina el objeto de la lista
        self.guardarTareas() # Actualiza tareas_taller.txt