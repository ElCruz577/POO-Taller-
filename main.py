# main.py
from clases import Empleado, Cliente, EquipoTaller, TareaMantenimiento, TareaAdministrativa
from archivos import GestorArchivos, registrarError

if __name__ == "__main__":
    print("--- 1. CREACIÓN DE OBJETOS ---")
    tecnico = Empleado("Juan Perez", "Mecánico Senior")
    cliente = Cliente("Empresa XYZ", "555-1234")
    equipo = EquipoTaller("SN-9988", "Torno CNC")
    
    tarea1 = TareaMantenimiento("Reparar motor", "2026-11-10", "Alta", equipo, tecnico, 30)
    tarea2 = TareaAdministrativa("Facturación", "2026-11-05", "Media", "Finanzas", True, cliente)
    
    print("\n--- 2. USO DE MÉTODOS DEL NEGOCIO ---")
    tarea1.marcarCompletada()
    print(tarea1.obtenerInfo())
    print(tarea2.obtenerInfo())
    print(tecnico.obtenerRol())

    print("\n--- 3. GUARDADO DE INFORMACIÓN ---")
    gestor = GestorArchivos("clientes_taller.txt")
    listaGuardar = [cliente, Cliente("Maria Lopez", "555-9876")]
    gestor.guardarClientes(listaGuardar)

    print("\n--- 4. CARGA DE INFORMACIÓN Y COMPROBACIÓN ---")
    listaCargada = gestor.cargarClientes()
    for c in listaCargada:
        print(f"Objeto recuperado -> Nombre: {c.nombre}, Teléfono: {c.telefono}")

    print("\n--- 5. PROVOCANDO ERRORES INTENCIONALES PARA EL LOG ---")
    
    try:
        with open("archivo_inventado.txt", "r") as f:
            contenido = f.read()
    except FileNotFoundError as e:
        print("Error provocado 1 capturado. Guardando en log...")
        registrarError(f"FileNotFoundError: {e}")

    try:
        precioIncorrecto = int("mil pesos")
    except ValueError as e:
        print("Error provocado 2 capturado. Guardando en log...")
        registrarError(f"ValueError: Texto en lugar de número - {e}")

    try:
        listaTemporal = ["Elemento 1"]
        falla = listaTemporal[5]
    except IndexError as e:
        print("Error provocado 3 capturado. Guardando en log...")
        registrarError(f"IndexError: Registro inexistente - {e}")
        
    print("\nEjecución finalizada. Revisa el archivo log_errores.txt y clientes_taller.txt")