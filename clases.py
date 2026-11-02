# clases.py

class Empleado:
    """Representa al personal técnico o administrativo del taller."""
    def __init__(self, nombreCompleto, cargo):
        self._nombreCompleto = nombreCompleto
        self._cargo = cargo

    @property
    def nombreCompleto(self):
        return self._nombreCompleto
        
    def obtenerRol(self):
        return f"Rol: {self._cargo}"

class Cliente:
    """Representa a un cliente del taller que solicita servicios."""
    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre
        
    @property
    def telefono(self):
        return self._telefono

    def contactarCliente(self):
        return f"Llamando al {self._telefono}..."

class EquipoTaller:
    """Representa la maquinaria del taller que recibe mantenimiento."""
    def __init__(self, numeroSerie, tipoEquipo):
        self._numeroSerie = numeroSerie
        self._tipoEquipo = tipoEquipo

    @property
    def numeroSerie(self):
        return self._numeroSerie

    def registrarUso(self):
        return f"Equipo {self._tipoEquipo} en uso."

class Tarea:
    """Clase base genérica que modela una tarea del taller."""
    def __init__(self, titulo, fechaLimite, prioridad):
        self._titulo = titulo
        self._fechaLimite = fechaLimite
        self._prioridad = prioridad
        self._completada = False

    @property
    def titulo(self):
        return self._titulo

    @property
    def completada(self):
        return self._completada

    @completada.setter
    def completada(self, estado):
        if not isinstance(estado, bool):
            raise ValueError("El estado debe ser True o False")
        self._completada = estado

    def marcarCompletada(self):
        self.completada = True

    def obtenerInfo(self):
        estado = "Completada" if self.completada else "Pendiente"
        return f"Tarea: {self.titulo} | Estado: {estado}"

class TareaMantenimiento(Tarea):
    """Subclase para trabajos físicos, asocia Empleado y EquipoTaller."""
    def __init__(self, titulo, fechaLimite, prioridad, equipo, tecnico, frecuenciaDias):
        super().__init__(titulo, fechaLimite, prioridad)
        self._equipo = equipo  
        self._tecnico = tecnico  
        self._frecuenciaDias = frecuenciaDias

    def programarMantenimiento(self):
        return f"Mantenimiento cada {self._frecuenciaDias} días."

    def obtenerInfo(self):
        infoBase = super().obtenerInfo()
        return f"{infoBase} | Técnico: {self._tecnico.nombreCompleto} | Equipo: {self._equipo.numeroSerie}"

class TareaAdministrativa(Tarea):
    """Subclase para trámites de oficina, asocia Cliente."""
    def __init__(self, titulo, fechaLimite, prioridad, departamento, requiereAprobacion, clienteRelacionado):
        super().__init__(titulo, fechaLimite, prioridad)
        self._departamento = departamento
        self._requiereAprobacion = requiereAprobacion
        self._clienteRelacionado = clienteRelacionado  

    def archivarDocumento(self):
        return f"Archivado en {self._departamento}."

    def obtenerInfo(self):
        infoBase = super().obtenerInfo()
        return f"{infoBase} | Depto: {self._departamento} | Cliente: {self._clienteRelacionado.nombre}"