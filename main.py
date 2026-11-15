# main.py - Conecta las 6 clases y la persistencia con la interfaz gráfica Tkinter

import tkinter as tk # Librería gráfica estándar vista en clase 14.1
from tkinter import ttk, messagebox # ttk para Combobox/Treeview y messagebox para alertas (14.2)
from pathlib import Path # Para ubicar la imagen logo.png en la misma carpeta
from PIL import Image, ImageTk # Librería Pillow vista en clase 14.2 para cargar el logo
from clases import Empleado, Cliente, EquipoTaller, Tarea, TareaMantenimiento, TareaAdministrativa, RegistroError
from archivos import GestorArchivos, registrarError # Gestor de persistencia y función de bitácora

gestor = GestorArchivos("tareas_taller.txt") # Instancia global del gestor de archivos

# --- FUNCIONES DE EVENTOS DE LA INTERFAZ GRÁFICA ---

def actualizarTabla(): # Refresca las filas del listado Treeview
    for fila in tabla.get_children(): # Recorre las filas actuales de la tabla
        tabla.delete(fila) # Las borra para volver a dibujarlas sin duplicar
    for t in gestor.listaTareas: # Recorre los objetos guardados en el gestor
        tipo = "Mantenimiento" if isinstance(t, TareaMantenimiento) else "Administrativa" # Identifica el tipo
        estado = "Completada" if t.completada else "Pendiente" # Traduce booleano a texto
        tabla.insert("", "end", values=(t.titulo, tipo, t.fechaLimite, t.prioridad, estado)) # Inserta fila

def limpiarCampos(): # Limpia los cuadros de texto y reinicia los Combobox (visto en 14.2)
    entryTitulo.delete(0, "end") # Borra el cuadro de título
    entryFecha.delete(0, "end") # Borra el cuadro de fecha
    entryDiasTel.delete(0, "end") # Borra el cuadro de Días / Teléfono
    entryResponsable.delete(0, "end") # Borra el cuadro de Técnico / Cliente
    entryArea.delete(0, "end") # Borra el cuadro de Equipo / Departamento
    comboPrioridad.set("Selecciona una prioridad") # Reinicia Combobox de prioridad
    comboTipo.set("Selecciona un tipo") # Reinicia Combobox de tipo de tarea

def seleccionarFila(event): # Al hacer clic en la tabla, carga TODOS los datos reales de esa tarea
    seleccion = tabla.selection() # Obtiene la fila seleccionada con el mouse
    if seleccion: # Si hay una fila seleccionada
        valores = tabla.item(seleccion[0], "values") # Extrae (Tarea, Tipo, Fecha, Prioridad, Estado)
        tarea = gestor.buscarTarea(valores[0]) # Busca el objeto real en el gestor por su título
        limpiarCampos() # Limpia las cajas antes de rellenarlas
        entryTitulo.insert(0, tarea.titulo) # Coloca el título en entryTitulo
        entryFecha.insert(0, tarea.fechaLimite) # Coloca la fecha en entryFecha
        comboPrioridad.set(tarea.prioridad) # Coloca la prioridad en comboPrioridad
        if isinstance(tarea, TareaMantenimiento): # Si la tarea seleccionada es de Mantenimiento
            comboTipo.set("Mantenimiento") # Pone Mantenimiento en el Combobox de tipo
            entryDiasTel.insert(0, str(tarea.frecuenciaDias)) # Pone sus días reales de frecuencia
            entryResponsable.insert(0, tarea.tecnico.nombreCompleto) # Pone el nombre del técnico
            entryArea.insert(0, tarea.equipo.numeroSerie) # Pone el número de serie del equipo
        else: # Si la tarea seleccionada es Administrativa
            comboTipo.set("Administrativa") # Pone Administrativa en el Combobox de tipo
            entryDiasTel.insert(0, tarea.clienteRelacionado.telefono) # Pone el teléfono real del cliente
            entryResponsable.insert(0, tarea.clienteRelacionado.nombre) # Pone el nombre del cliente real
            entryArea.insert(0, tarea.departamento) # Pone el departamento real

def construirObjetoDesdeFormulario(): # Crea el objeto TareaMantenimiento o TareaAdministrativa con lo escrito en la GUI
    titulo = entryTitulo.get().strip() # Lee el título escrito
    fecha = entryFecha.get().strip() # Lee la fecha escrita
    textoDiasTel = entryDiasTel.get().strip() # Lee los días (Mantenimiento) o el teléfono (Administrativa)
    responsable = entryResponsable.get().strip() # Lee el Técnico o Cliente escrito por el usuario
    area = entryArea.get().strip() # Lee el Equipo o Departamento escrito por el usuario
    if titulo == "" or fecha == "" or textoDiasTel == "" or responsable == "" or area == "": # Valida vacíos
        raise ValueError("Todos los campos del formulario son obligatorios") # Lanza ValueError si falta alguno
    if comboPrioridad.current() == -1 or comboTipo.current() == -1: # Valida que hayan elegido en ambos Combobox (-1)
        raise ValueError("Debes elegir una prioridad y un tipo de tarea en las listas desplegables") # Lanza ValueError
    prioridad = comboPrioridad.get() # Obtiene la prioridad elegida
    if comboTipo.get() == "Mantenimiento": # Si el usuario eligió Mantenimiento en el Combobox
        dias = int(textoDiasTel) # Convierte a entero (lanza ValueError si escribieron letras)
        eqObj = EquipoTaller(area, "Maquinaria") # Crea el EquipoTaller con lo escrito en Equipo/Depto
        tecObj = Empleado(responsable, "Técnico") # Crea el Empleado con lo escrito en Técnico/Cliente
        return TareaMantenimiento(titulo, fecha, prioridad, eqObj, tecObj, dias) # Retorna subclase 1
    else: # Si el usuario eligió Administrativa en el Combobox
        cliObj = Cliente(responsable, textoDiasTel) # Crea el Cliente validando su nombre y su teléfono real
        return TareaAdministrativa(titulo, fecha, prioridad, area, True, cliObj) # Retorna subclase 2 con su Depto

def botonAgregar(): # Registra una nueva tarea con todos los datos personalizados de la GUI
    try: # Intenta construir el objeto y guardarlo
        nueva = construirObjetoDesdeFormulario() # Construye la tarea validando todos los campos
        gestor.agregarTarea(nueva) # Guarda en la lista y en tareas_taller.txt
        actualizarTabla() # Refresca la tabla Treeview
        limpiarCampos() # Limpia los cuadros de texto
        messagebox.showinfo("Éxito", "Tarea registrada correctamente.") # Confirma al usuario
    except (ValueError, TypeError, RegistroError) as error: # Captura vacíos, letras, rango o duplicados
        registrarError(f"{type(error).__name__} al agregar: {error}") # Registra el error en log_errores.txt
        messagebox.showerror("Error de validación", str(error)) # Muestra el error en messagebox

def botonConsultar(): # Busca una tarea por título y muestra sus datos completos con __str__()
    try: # Intenta buscar el título escrito
        tarea = gestor.buscarTarea(entryTitulo.get()) # Si no existe, lanza RegistroError
        messagebox.showinfo("Detalle de Tarea", str(tarea)) # Muestra toda la info polimórfica
    except RegistroError as error: # Captura búsqueda de registro inexistente
        registrarError(f"RegistroError en consulta: {error}") # Registra en log_errores.txt
        messagebox.showerror("No encontrado", str(error)) # Alerta al usuario

def botonModificar(): # Modifica fecha, prioridad, tipo, días/teléfono, técnico/cliente y equipo/depto
    try: # Intenta crear el objeto actualizado y reemplazarlo en el gestor
        modificada = construirObjetoDesdeFormulario() # Toma todos los cambios hechos en las cajas de texto
        gestor.modificarTarea(modificada.titulo, modificada) # Actualiza el objeto y guarda en tareas_taller.txt
        actualizarTabla() # Refresca la tabla
        messagebox.showinfo("Modificación", "Tarea actualizada correctamente con todos sus datos.") # Éxito
    except (ValueError, TypeError, RegistroError) as error: # Captura si el título no existe o hay datos inválidos
        registrarError(f"{type(error).__name__} al modificar: {error}") # Anota en log_errores.txt
        messagebox.showerror("Error al modificar", str(error)) # Muestra alerta de error

def botonCompletar(): # Marca una tarea existente como completada
    try: # Intenta buscar la tarea y cambiar su estado
        tarea = gestor.buscarTarea(entryTitulo.get()) # Busca por título
        tarea.marcarCompletada() # Usa el setter para cambiar _completada a True
        gestor.guardarTareas() # Guarda el cambio en tareas_taller.txt
        actualizarTabla() # Refresca la tabla visual
        messagebox.showinfo("Completada", f"Tarea '{tarea.titulo}' marcada como completada.") # Aviso
    except RegistroError as error: # Si no existe la tarea escrita
        registrarError(f"RegistroError al completar: {error}") # Registra en el log
        messagebox.showerror("Error", str(error)) # Alerta de error

def botonEliminar(): # Elimina la tarea seleccionada de la lista y de tareas_taller.txt
    try: # Intenta eliminar por título
        gestor.eliminarTarea(entryTitulo.get()) # Elimina de la lista y actualiza el archivo .txt
        actualizarTabla() # Quita la fila de la tabla
        limpiarCampos() # Limpia el formulario
        messagebox.showinfo("Eliminada", "Tarea eliminada correctamente.") # Confirmación
    except RegistroError as error: # Si intentan eliminar un registro inexistente
        registrarError(f"RegistroError al eliminar: {error}") # Registra en log_errores.txt
        messagebox.showerror("Error", str(error)) # Muestra alerta

def botonAyuda(): # Realiza cálculos matemáticos sobre la colección y muestra ayuda (rúbrica)
    total = len(gestor.listaTareas) # Total de tareas registradas
    completadas = 0 # Contador de tareas completadas
    for t in gestor.listaTareas: # Recorre la lista de tareas
        if t.completada: completadas += 1 # Suma 1 por cada tarea completada
    pendientes = total - completadas # Calcula tareas pendientes
    porcentaje = (completadas / total * 100) if total > 0 else 0.0 # Cálculo de porcentaje de avance
    messagebox.showinfo("Cálculos y Ayuda", f"--- CÁLCULOS DEL TALLER ---\nTotal: {total} | Completadas: {completadas} | Pendientes: {pendientes}\nAvance del taller: {porcentaje:.1f}%\n\nHaz clic en una fila para cargar sus datos, modificarla o eliminarla.")

# --- BLOQUE PRINCIPAL ---

if __name__ == "__main__": # Ejecución principal del sistema
    tecInicial = Empleado("Juan Perez", "Mecánico Senior") # Instancia Clase 1 (Empleado)
    cliInicial = Cliente("Empresa XYZ", "555-1234") # Instancia Clase 2 (Cliente)
    eqInicial = EquipoTaller("SN-9988", "Torno CNC") # Instancia Clase 3 (EquipoTaller)
    tecInicial.actualizarCargo("Jefe Mecánico") # Demuestra método actualizarCargo de Empleado
    tareaGen = Tarea("Ordenar almacén", "2026-11-18", "Baja") # Instancia Clase 4 (Tarea base)
    tareaGen.actualizarDatos("2026-11-22", "Media") # Demuestra el uso del método actualizarDatos de Tarea
    tareaMant = TareaMantenimiento("Reparar motor", "2026-11-10", "Alta", eqInicial, tecInicial, 30) # Clase 5
    tareaAdmin = TareaAdministrativa("Facturación", "2026-11-05", "Media", "Finanzas", True, cliInicial) # Clase 6
    print(tareaGen, "\n", tareaMant, "\n", tareaAdmin) # Imprime en consola usando __str__()

    # Pruebas de validaciones reales de las clases para log_errores.txt (corrige observaciones de Parte 2)
    try: Cliente("", "abc") # Error real 1: constructor rechaza vacíos y letras en teléfono
    except ValueError as e: registrarError(f"ValueError constructor Cliente: {e}") # Registra en log
    try: tareaGen.completada = "texto" # Error real 2: setter de completada rechaza no booleanos
    except TypeError as e: registrarError(f"TypeError setter completada: {e}") # Registra en log

    gestor.cargarTareas() # Carga las tareas desde tareas_taller.txt
    if len(gestor.listaTareas) == 0: # Si el archivo estaba vacío, guarda las tareas iniciales
        gestor.agregarTarea(tareaMant) # Guarda tarea de mantenimiento inicial
        gestor.agregarTarea(tareaAdmin) # Guarda tarea administrativa inicial

    # Comparación explícita entre objetos guardados y cargados (observación de Parte 2)
    tituloGuardado = gestor.listaTareas[0].titulo # Título en memoria antes de recargar
    gestor.cargarTareas() # Recarga desde tareas_taller.txt
    print("Comparación guardado vs cargado exitosa:", tituloGuardado == gestor.listaTareas[0].titulo)

    # --- VENTANA PRINCIPAL TKINTER (Boceto Figura 3 y estilo de clases 14.1 y 14.2) ---
    ventana = tk.Tk() # Crea la ventana principal
    ventana.title("Agenda de tareas pendientes") # Título de la ventana
    ventana.geometry("700x520") # Tamaño de la ventana
    ventana.resizable(False, False) # Tamaño fijo
    ventana.configure(bg="#F6F4EE") # Color de fondo de las diapositivas de clase

    tk.Label(ventana, text="Agenda de tareas pendientes", font=("Arial", 16, "bold"), bg="#F6F4EE").place(x=30, y=15)

    try: # Carga de logo.png exactamente como en el PDF 14.2
        rutaBase = Path(__file__).parent # Carpeta donde se encuentra el archivo .py
        rutaLogo = rutaBase / "Logoprograma.png" # Ruta del archivo logo.png
        imagen = Image.open(rutaLogo).resize((85, 50)) # Abre y ajusta el tamaño del logo
        imagenTk = ImageTk.PhotoImage(imagen) # Convierte la imagen para Tkinter
        etiquetaLogo = tk.Label(ventana, image=imagenTk, bg="#F6F4EE") # Crea etiqueta con la imagen
        etiquetaLogo.image = imagenTk # Mantiene la referencia a la imagen
        etiquetaLogo.place(x=555, y=8) # Coloca el logo arriba a la derecha sin tapar botones
    except Exception as error: # Si aún no has puesto logo.png en la carpeta
        registrarError(f"Error al cargar logo.png: {error}") # Lo registra en log_errores.txt
        tk.Label(ventana, text="[Logo Taller]", bg="#F6F4EE", fg="red").place(x=565, y=22) # Texto provisional

    # Etiquetas con ejemplos entre paréntesis y cuadros de entrada vacíos al iniciar
    tk.Label(ventana, text="Título (ej. Afinación):", font=("Arial", 10, "bold"), bg="#F6F4EE").place(x=30, y=60)
    entryTitulo = tk.Entry(ventana) # Cuadro de texto vacío para el título
    entryTitulo.place(x=215, y=60, width=220, height=24)

    tk.Label(ventana, text="Fecha (AAAA-MM-DD):", font=("Arial", 10, "bold"), bg="#F6F4EE").place(x=30, y=90)
    entryFecha = tk.Entry(ventana) # Cuadro de texto vacío para la fecha límite
    entryFecha.place(x=215, y=90, width=220, height=24)

    tk.Label(ventana, text="Prioridad:", font=("Arial", 10, "bold"), bg="#F6F4EE").place(x=30, y=120)
    comboPrioridad = ttk.Combobox(ventana, values=["Alta", "Media", "Baja"], state="readonly") # Combobox prioridad
    comboPrioridad.set("Selecciona una prioridad") # Texto guía inicial en Combobox
    comboPrioridad.place(x=215, y=120, width=220, height=24)

    tk.Label(ventana, text="Tipo de tarea:", font=("Arial", 10, "bold"), bg="#F6F4EE").place(x=30, y=150)
    comboTipo = ttk.Combobox(ventana, values=["Mantenimiento", "Administrativa"], state="readonly") # Elige subclase
    comboTipo.set("Selecciona un tipo") # Texto guía inicial en Combobox
    comboTipo.place(x=215, y=150, width=220, height=24)

    tk.Label(ventana, text="Días (1-365) / Teléfono:", font=("Arial", 10, "bold"), bg="#F6F4EE").place(x=30, y=180)
    entryDiasTel = tk.Entry(ventana) # Guarda Frecuencia (si es Mantenimiento) o Teléfono (si es Administrativa)
    entryDiasTel.place(x=215, y=180, width=220, height=24)

    tk.Label(ventana, text="Técnico / Cliente (Nombre):", font=("Arial", 10, "bold"), bg="#F6F4EE").place(x=30, y=210)
    entryResponsable = tk.Entry(ventana) # Cuadro vacío para escribir el nombre del Técnico o Cliente
    entryResponsable.place(x=215, y=210, width=220, height=24)

    tk.Label(ventana, text="Serie Equipo / Depto:", font=("Arial", 10, "bold"), bg="#F6F4EE").place(x=30, y=240)
    entryArea = tk.Entry(ventana) # Cuadro vacío para escribir la Serie del Equipo o el Departamento
    entryArea.place(x=215, y=240, width=220, height=24)

    frameBotones = tk.Frame(ventana, bg="#F6F4EE") # Frame contenedor de botones a la derecha
    frameBotones.place(x=465, y=68) # Ubicado debajo del logo para que no se encimen
    tk.Button(frameBotones, text="Agregar", command=botonAgregar, bg="#117A76", fg="white", width=18).pack(pady=3)
    tk.Button(frameBotones, text="Consultar", command=botonConsultar, width=18).pack(pady=3)
    tk.Button(frameBotones, text="Modificar", command=botonModificar, width=18).pack(pady=3)
    tk.Button(frameBotones, text="Marcar completada", command=botonCompletar, width=18).pack(pady=3)
    tk.Button(frameBotones, text="Eliminar", command=botonEliminar, bg="#B03A2E", fg="white", width=18).pack(pady=3)
    tk.Button(frameBotones, text="Ayuda / Cálculos", command=botonAyuda, width=18).pack(pady=3)

    tk.Label(ventana, text="Tareas registradas", font=("Arial", 11, "bold"), bg="#F6F4EE").place(x=30, y=280)
    columnas = ("Tarea", "Tipo", "Fecha", "Prioridad", "Estado") # Columnas del Treeview
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=8) # Tabla Treeview
    for col in columnas: # Configura encabezados y ancho
        tabla.heading(col, text=col)
        tabla.column(col, width=125)
    tabla.place(x=30, y=305, width=630, height=185)
    tabla.bind("<<TreeviewSelect>>", seleccionarFila) # Conecta clic con seleccionarFila

    actualizarTabla() # Carga las tareas en la tabla al abrir
    ventana.mainloop() # Mantiene la ventana abierta