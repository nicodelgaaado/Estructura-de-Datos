"""Script interactivo para gestionar una lista de tareas pendientes usando una lista enlazada simple."""

# Definicion de clases ----------------------------------------------------

class NodoTarea:
    """Representa un nodo de la lista enlazada con todos los datos de una tarea."""

    def __init__(self, id_tarea, titulo, descripcion, prioridad, estado,
                 fecha_creacion, fecha_vencimiento, responsable, tags,
                 notas_adicionales):
        # Campos informativos de la tarea
        self.id_tarea = id_tarea
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = estado
        self.fecha_creacion = fecha_creacion
        self.fecha_vencimiento = fecha_vencimiento
        self.responsable = responsable
        self.tags = tags
        self.notas_adicionales = notas_adicionales
        # Enlace al siguiente nodo de la lista
        self.next = None

    def coincide_tag(self, tag_busqueda):
        """Verifica si el tag buscado existe dentro de la lista de tags."""
        tag_normalizado = tag_busqueda.strip().lower()
        return any(tag_normalizado == tag.lower() for tag in self.tags)

    def coincide_titulo(self, titulo_busqueda):
        """Compara el titulo del nodo con el titulo buscado (ignorando mayusculas)."""
        return self.titulo.lower() == titulo_busqueda.strip().lower()


class ListaTareas:
    """Implementa la lista enlazada simple que almacena los nodos de tareas."""

    def __init__(self):
        self.head = None

    def agregar_tarea(self, id_tarea, titulo, descripcion, prioridad, estado,
                      fecha_creacion, fecha_vencimiento, responsable, tags,
                      notas_adicionales):
        """Agrega una nueva tarea al final de la lista si el id no esta repetido."""
        if self._contiene_id(id_tarea):
            print(f"Ya existe una tarea con el id '{id_tarea}'. Usa otro identificador.")
            return False

        nueva_tarea = NodoTarea(
            id_tarea=id_tarea,
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            estado=estado,
            fecha_creacion=fecha_creacion,
            fecha_vencimiento=fecha_vencimiento,
            responsable=responsable,
            tags=tags,
            notas_adicionales=notas_adicionales,
        )

        if self.head is None:
            self.head = nueva_tarea
            return True

        actual = self.head
        while actual.next:
            actual = actual.next
        actual.next = nueva_tarea
        return True

    def buscar_por_tag(self, tag):
        """Muestra todas las tareas que contienen el tag indicado."""
        if self.head is None:
            print("No hay tareas registradas.")
            return

        actual = self.head
        encontradas = []
        while actual:
            if actual.coincide_tag(tag):
                encontradas.append(actual)
            actual = actual.next

        if not encontradas:
            print(f"No se encontraron tareas con el tag '{tag}'.")
            return

        print(f"\nTareas con el tag '{tag}':")
        print("-" * 70)
        for indice, tarea in enumerate(encontradas, start=1):
            self._imprimir_tarea(tarea, indice)

    def buscar_por_titulo(self, titulo):
        """Busca y muestra la primera tarea cuyo titulo coincide exactamente."""
        if self.head is None:
            print("No hay tareas registradas.")
            return

        actual = self.head
        while actual:
            if actual.coincide_titulo(titulo):
                print("\nTarea encontrada:")
                print("-" * 70)
                self._imprimir_tarea(actual)
                return
            actual = actual.next

        print(f"No se encontro ninguna tarea con el titulo '{titulo}'.")

    def mostrar_todas(self):
        """Recorre la lista y muestra todas las tareas almacenadas."""
        if self.head is None:
            print("No hay tareas para mostrar.")
            return

        print("\nListado completo de tareas:")
        print("-" * 70)
        actual = self.head
        indice = 1
        while actual:
            self._imprimir_tarea(actual, indice)
            actual = actual.next
            indice += 1

    def _contiene_id(self, id_busqueda):
        """Revisa si ya existe una tarea con el id indicado."""
        actual = self.head
        while actual:
            if actual.id_tarea == id_busqueda:
                return True
            actual = actual.next
        return False

    def _imprimir_tarea(self, tarea, indice=None):
        """Imprime una tarea con un formato claro y alineado."""
        etiqueta_indice = f"Tarea {indice}" if indice is not None else "Tarea"
        print(f"{etiqueta_indice}")
        print(f"  Id             : {tarea.id_tarea}")
        print(f"  Titulo         : {tarea.titulo}")
        print(f"  Descripcion    : {tarea.descripcion}")
        print(f"  Prioridad      : {tarea.prioridad}")
        print(f"  Estado         : {tarea.estado}")
        print(f"  Fecha creacion : {tarea.fecha_creacion}")
        print(f"  Fecha vencim.  : {tarea.fecha_vencimiento}")
        print(f"  Responsable    : {tarea.responsable}")
        tags_formateados = ", ".join(tarea.tags) if tarea.tags else "(sin tags)"
        print(f"  Tags           : {tags_formateados}")
        notas = tarea.notas_adicionales or "(sin notas)"
        print(f"  Notas          : {notas}")
        print("-" * 70)


# Funciones auxiliares ----------------------------------------------------

def solicitar_datos_tarea():
    """Solicita al usuario los campos necesarios para crear una tarea."""
    print("\nIngresa los datos de la nueva tarea")
    print("-" * 70)
    id_tarea = input("Id de la tarea: ").strip()
    titulo = input("Titulo de la tarea: ").strip()
    descripcion = input("Descripcion de la tarea: ").strip()
    prioridad = input("Prioridad (Alta, Media, Baja u otra): ").strip()
    estado = input("Estado (Pendiente, En progreso, Completada, etc.): ").strip()
    fecha_creacion = input("Fecha de creacion: ").strip()
    fecha_vencimiento = input("Fecha de vencimiento: ").strip()
    responsable = input("Responsable: ").strip()
    tags_entrada = input("Tags (separados por comas): ").strip()
    notas_adicionales = input("Notas adicionales: ").strip()

    tags = [tag.strip() for tag in tags_entrada.split(",") if tag.strip()]
    return (
        id_tarea,
        titulo,
        descripcion,
        prioridad,
        estado,
        fecha_creacion,
        fecha_vencimiento,
        responsable,
        tags,
        notas_adicionales,
    )


def mostrar_menu():
    """Despliega el menu principal en la consola."""
    print("\n=== Gestor de Tareas Pendientes ===")
    print("1. Agregar tarea")
    print("2. Buscar tarea por titulo")
    print("3. Buscar tareas por tag")
    print("4. Mostrar todas las tareas")
    print("5. Salir")


def ejecutar_aplicacion():
    """Ejecuta el ciclo principal de interaccion con el usuario."""
    lista_tareas = ListaTareas()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opcion (1-5): ").strip()

        if opcion == "1":
            (
                id_tarea,
                titulo,
                descripcion,
                prioridad,
                estado,
                fecha_creacion,
                fecha_vencimiento,
                responsable,
                tags,
                notas_adicionales,
            ) = solicitar_datos_tarea()

            if not id_tarea or not titulo:
                print("El id y el titulo son obligatorios. Intenta nuevamente.")
                continue

            agregado = lista_tareas.agregar_tarea(
                id_tarea=id_tarea,
                titulo=titulo,
                descripcion=descripcion,
                prioridad=prioridad,
                estado=estado,
                fecha_creacion=fecha_creacion,
                fecha_vencimiento=fecha_vencimiento,
                responsable=responsable,
                tags=tags,
                notas_adicionales=notas_adicionales,
            )
            if agregado:
                print("Tarea agregada correctamente.")
        elif opcion == "2":
            titulo = input("\nIntroduce el titulo de la tarea a buscar: ").strip()
            if titulo:
                lista_tareas.buscar_por_titulo(titulo)
            else:
                print("Debes ingresar un titulo para buscar.")
        elif opcion == "3":
            tag = input("\nIntroduce el tag a buscar: ").strip()
            if tag:
                lista_tareas.buscar_por_tag(tag)
            else:
                print("Debes ingresar un tag para buscar.")
        elif opcion == "4":
            lista_tareas.mostrar_todas()
        elif opcion == "5":
            print("Saliendo del gestor de tareas. Hasta luego!")
            break
        else:
            print("Opcion no valida. Por favor elige una opcion entre 1 y 5.")


# Punto de entrada --------------------------------------------------------

if __name__ == "__main__":
    ejecutar_aplicacion()
