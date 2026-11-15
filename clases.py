# clases.py - Módulo con las 6 clases del negocio, herencia, validaciones y excepción propia

class RegistroError(Exception): # Excepción propia heredada de Exception (pedida por la profesora)
    """Excepción propia para tareas duplicadas o inexistentes.""" # Docstring obligatorio por rúbrica
    pass # Hereda todo el funcionamiento de Exception

class Empleado: # Clase 1 de negocio: personal del taller
    """Representa al personal técnico o administrativo del taller.""" # Docstring de la clase
    def __init__(self, nombreCompleto, cargo): # Constructor con validación de campos vacíos
        if nombreCompleto.strip() == "" or cargo.strip() == "": # Revisa que no envíen textos en blanco
            raise ValueError("Nombre y cargo del empleado son obligatorios") # Lanza error si están vacíos
        self._nombreCompleto = nombreCompleto.strip() # Atributo privado (_) para el nombre
        self._cargo = cargo.strip() # Atributo privado (_) para el cargo

    @property # Decorador GETTER: permite leer empleado.nombreCompleto sin exponer el atributo privado
    def nombreCompleto(self): # Función getter del nombre
        return self._nombreCompleto # Devuelve el atributo privado _nombreCompleto

    @property # Decorador GETTER para leer el cargo
    def cargo(self): # Función getter del cargo
        return self._cargo # Devuelve el atributo privado _cargo

    def actualizarCargo(self, nuevoCargo): # Método que modifica el cargo del empleado
        if nuevoCargo.strip() == "": # Valida que el nuevo cargo no venga vacío
            raise ValueError("El nuevo cargo no puede estar vacío") # Lanza ValueError si está vacío
        self._cargo = nuevoCargo.strip() # Actualiza el atributo privado _cargo

    def obtenerRol(self): # Método propio de Empleado que consulta sus atributos
        return f"{self._nombreCompleto} ({self._cargo})" # Retorna nombre y cargo

    def __str__(self): # Método especial que convierte el objeto en texto al usar print() o str()
        return f"Empleado: {self.obtenerRol()}" # Reutiliza obtenerRol()

class Cliente: # Clase 2 de negocio: clientes del taller
    """Representa a un cliente del taller que solicita servicios.""" # Docstring de la clase
    def __init__(self, nombre, telefono): # Constructor que corrige la observación Cliente("", "abc")
        if nombre.strip() == "": # Impide que el nombre esté vacío
            raise ValueError("El nombre del cliente no puede estar vacío") # Lanza ValueError
        if not telefono.replace("-", "").strip().isdigit(): # Verifica que el teléfono solo tenga números
            raise ValueError("El teléfono solo debe contener números") # Bloquea letras como "abc"
        self._nombre = nombre.strip() # Guarda el nombre privado
        self._telefono = telefono.strip() # Guarda el teléfono privado

    @property # Decorador GETTER para leer el nombre del cliente
    def nombre(self): # Función getter de nombre
        return self._nombre # Retorna _nombre

    @property # Decorador GETTER para leer el teléfono
    def telefono(self): # Función getter de telefono
        return self._telefono # Retorna _telefono

    def contactarCliente(self): # Método de negocio que devuelve la información de contacto del cliente
        return f"{self._nombre} (Tel: {self._telefono})" # Retorna nombre y teléfono

    def __str__(self): # Método especial para mostrar el objeto Cliente como texto
        return f"Cliente: {self.contactarCliente()}" # Retorna los datos del cliente

class EquipoTaller: # Clase 3 de negocio: maquinaria del taller
    """Representa la maquinaria del taller que recibe mantenimiento.""" # Docstring de la clase
    def __init__(self, numeroSerie, tipoEquipo): # Constructor de EquipoTaller
        if numeroSerie.strip() == "" or tipoEquipo.strip() == "": # Valida que no haya campos vacíos
            raise ValueError("Serie y tipo de equipo son obligatorios") # Lanza ValueError
        self._numeroSerie = numeroSerie.strip() # Atributo privado número de serie
        self._tipoEquipo = tipoEquipo.strip() # Atributo privado tipo de equipo
        self._enUso = False # Estado interno para saber si la máquina está en mantenimiento

    @property # Decorador GETTER para leer el número de serie
    def numeroSerie(self): # Función getter de numeroSerie
        return self._numeroSerie # Retorna _numeroSerie

    @property # Decorador GETTER para leer el tipo de equipo
    def tipoEquipo(self): # Función getter de tipoEquipo
        return self._tipoEquipo # Retorna _tipoEquipo

    def registrarUso(self): # Método que cambia el estado interno de la máquina a True (en uso)
        self._enUso = True # Modifica el atributo privado _enUso
        return f"{self._tipoEquipo} [Serie: {self._numeroSerie}]" # Retorna tipo y serie

    def __str__(self): # Método especial para imprimir EquipoTaller con print()
        return f"Equipo: {self.registrarUso()}" # Retorna la información del equipo

class Tarea: # Clase 4 de negocio (SUPERCLASE / PADRE): base para las tareas
    """Clase base genérica que modela una tarea del taller.""" # Docstring de la superclase
    def __init__(self, titulo, fechaLimite, prioridad): # Constructor padre
        if titulo.strip() == "" or fechaLimite.strip() == "" or prioridad.strip() == "": # Valida vacíos
            raise ValueError("Título, fecha y prioridad son obligatorios") # Lanza ValueError si falta algo
        self._titulo = titulo.strip() # Atributo privado título
        self._fechaLimite = fechaLimite.strip() # Atributo privado fecha límite
        self._prioridad = prioridad.strip() # Atributo privado prioridad
        self._completada = False # Inicia como False (Pendiente)

    @property # Decorador GETTER para título
    def titulo(self): # Permite leer tarea.titulo
        return self._titulo # Retorna _titulo

    @property # Decorador GETTER para fechaLimite
    def fechaLimite(self): # Permite leer tarea.fechaLimite
        return self._fechaLimite # Retorna _fechaLimite

    @property # Decorador GETTER para prioridad
    def prioridad(self): # Permite leer tarea.prioridad
        return self._prioridad # Retorna _prioridad

    @property # Decorador GETTER para el booleano completada
    def completada(self): # Permite leer tarea.completada
        return self._completada # Retorna True o False

    @completada.setter # Decorador SETTER: valida antes de asignar tarea.completada = valor
    def completada(self, estado): # Recibe el nuevo valor booleano
        if not isinstance(estado, bool): # Verifica con isinstance que sea booleano (True o False)
            raise TypeError("El estado debe ser True o False") # Lanza TypeError si envían texto o número
        self._completada = estado # Actualiza el atributo privado _completada

    def marcarCompletada(self): # Método de negocio para completar la tarea
        self.completada = True # Usa el setter para cambiar a True

    def actualizarDatos(self, nuevaFecha, nuevaPrioridad): # Método base para modificar fecha y prioridad
        if nuevaFecha.strip() == "" or nuevaPrioridad.strip() == "": # Valida que no estén vacíos
            raise ValueError("La nueva fecha y prioridad son obligatorias") # Lanza ValueError
        self._fechaLimite = nuevaFecha.strip() # Actualiza _fechaLimite
        self._prioridad = nuevaPrioridad.strip() # Actualiza _prioridad

    def obtenerInfo(self): # Reúne todos los atributos de la clase padre
        estado = "Completada" if self._completada else "Pendiente" # Texto según el booleano
        return f"Tarea: {self._titulo} | Fecha: {self._fechaLimite} | Prioridad: {self._prioridad} | Estado: {estado}"

    def __str__(self): # Método especial para imprimir Tarea con print()
        return self.obtenerInfo() # Retorna obtenerInfo()

class TareaMantenimiento(Tarea): # Clase 5 (SUBCLASE 1): hereda de Tarea
    """Subclase para trabajos físicos, asocia Empleado y EquipoTaller.""" # Docstring
    def __init__(self, titulo, fechaLimite, prioridad, equipo, tecnico, frecuenciaDias): # Constructor hijo
        super().__init__(titulo, fechaLimite, prioridad) # Llama al constructor padre con super()
        if not isinstance(frecuenciaDias, int): # Valida que los días sean un entero
            raise TypeError("La frecuencia debe ser un número entero") # Lanza TypeError
        if frecuenciaDias < 1 or frecuenciaDias > 365: # Valida rango entre 1 y 365 días
            raise ValueError("La frecuencia debe estar en un rango de 1 a 365 días") # Lanza ValueError
        self._equipo = equipo # Asociación: guarda objeto EquipoTaller
        self._tecnico = tecnico # Asociación: guarda objeto Empleado
        self._frecuenciaDias = frecuenciaDias # Guarda días de frecuencia

    @property # Decorador GETTER para leer el objeto equipo
    def equipo(self): # Permite acceder a tarea.equipo
        return self._equipo # Retorna _equipo

    @property # Decorador GETTER para leer el objeto tecnico
    def tecnico(self): # Permite acceder a tarea.tecnico
        return self._tecnico # Retorna _tecnico

    @property # Decorador GETTER para leer frecuenciaDias
    def frecuenciaDias(self): # Permite leer tarea.frecuenciaDias
        return self._frecuenciaDias # Retorna _frecuenciaDias

    def programarMantenimiento(self): # Método propio de TareaMantenimiento
        return f"Cada {self._frecuenciaDias} días en {self._equipo.registrarUso()}" # Usa EquipoTaller

    def obtenerInfo(self): # POLIMORFISMO: sobrescribe obtenerInfo() agregando técnico, equipo y frecuencia
        return f"{super().obtenerInfo()} | Tipo: Mantenimiento | Técnico: {self._tecnico.obtenerRol()} | {self.programarMantenimiento()}"

    def __str__(self): # Método especial para imprimir TareaMantenimiento
        return self.obtenerInfo() # Retorna la información polimórfica

class TareaAdministrativa(Tarea): # Clase 6 (SUBCLASE 2): hereda de Tarea
    """Subclase para trámites de oficina, asocia Cliente.""" # Docstring
    def __init__(self, titulo, fechaLimite, prioridad, departamento, requiereAprobacion, clienteRelacionado):
        super().__init__(titulo, fechaLimite, prioridad) # Inicializa atributos heredados con super()
        if departamento.strip() == "": # Valida que departamento no esté vacío
            raise ValueError("El departamento es obligatorio") # Lanza ValueError
        if not isinstance(requiereAprobacion, bool): # Valida que requiereAprobacion sea booleano
            raise TypeError("requiereAprobacion debe ser True o False") # Lanza TypeError
        self._departamento = departamento.strip() # Guarda departamento privado
        self._requiereAprobacion = requiereAprobacion # Guarda booleano de aprobación
        self._clienteRelacionado = clienteRelacionado # Asociación: guarda objeto Cliente

    @property # Decorador GETTER para leer el departamento en la GUI
    def departamento(self): # Permite leer tarea.departamento
        return self._departamento # Retorna _departamento

    @property # Decorador GETTER para leer el cliente asociado en la GUI
    def clienteRelacionado(self): # Permite leer tarea.clienteRelacionado
        return self._clienteRelacionado # Retorna _clienteRelacionado

    def archivarDocumento(self): # Método propio que usa _requiereAprobacion y contactarCliente()
        aprob = "Con aprobación" if self._requiereAprobacion else "Sin aprobación" # Usa _requiereAprobacion
        return f"Depto: {self._departamento} ({aprob}) | Cliente: {self._clienteRelacionado.contactarCliente()}"

    def obtenerInfo(self): # POLIMORFISMO: sobrescribe obtenerInfo() con datos administrativos
        return f"{super().obtenerInfo()} | Tipo: Administrativa | {self.archivarDocumento()}"

    def __str__(self): # Método especial para imprimir TareaAdministrativa
        return self.obtenerInfo() # Retorna obtenerInfo()