#CASO DE ESTUDIO: LISTA DE RESPRODUCCIÓN (PLAYLIST)#

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class Song:
    title: str
    artist: str
    duration: str

    def display(self) -> str:
        parts = [self.title]
        if self.artist:
            parts.append(f"by {self.artist}")
        if self.duration:
            parts.append(f"[{self.duration}]")
        return " ".join(parts)


class SongNode:
    __slots__ = ("song", "prev", "next")

    def __init__(self, song: Song) -> None:
        self.song: Song = song
        self.prev: Optional[SongNode] = None
        self.next: Optional[SongNode] = None


class Playlist:
    def __init__(self) -> None:
        self.head: Optional[SongNode] = None
        self.tail: Optional[SongNode] = None
        self.current: Optional[SongNode] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def _append_node(self, node: SongNode) -> None:
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self._size += 1

    def add_song(self, song: Song, make_current: bool = False) -> None:
        node = SongNode(song)
        self._append_node(node)
        if self.current is None or make_current:
            self.current = node

    def insert_after_current(self, song: Song, make_current: bool = True) -> None:
        if self.is_empty() or self.current is None:
            self.add_song(song, make_current=True)
            return
        node = SongNode(song)
        next_node = self.current.next
        self.current.next = node
        node.prev = self.current
        node.next = next_node
        if next_node is not None:
            next_node.prev = node
        else:
            self.tail = node
        self._size += 1
        if make_current:
            self.current = node

    def _unlink_node(self, node: SongNode) -> None:
        prev_node = node.prev
        next_node = node.next
        if prev_node is not None:
            prev_node.next = next_node
        else:
            self.head = next_node
        if next_node is not None:
            next_node.prev = prev_node
        else:
            self.tail = prev_node
        if self.current is node:
            self.current = next_node or prev_node
        node.prev = node.next = None
        self._size -= 1

    def remove_by_title(self, title: str) -> bool:
        cursor = self.head
        title_lower = title.lower()
        while cursor is not None:
            if cursor.song.title.lower() == title_lower:
                self._unlink_node(cursor)
                return True
            cursor = cursor.next
        return False

    def remove_current(self) -> bool:
        if self.current is None:
            return False
        self._unlink_node(self.current)
        return True

    def clear(self) -> None:
        cursor = self.head
        while cursor is not None:
            nxt = cursor.next
            cursor.prev = cursor.next = None
            cursor = nxt
        self.head = self.tail = self.current = None
        self._size = 0

    def play_next(self) -> Optional[Song]:
        if self.current is None:
            return None
        if self.current.next is not None:
            self.current = self.current.next
        return self.current.song

    def play_previous(self) -> Optional[Song]:
        if self.current is None:
            return None
        if self.current.prev is not None:
            self.current = self.current.prev
        return self.current.song

    def jump_to(self, index: int) -> Optional[Song]:
        if index < 1 or index > self._size:
            return None
        cursor = self.head
        for _ in range(index - 1):
            assert cursor is not None
            cursor = cursor.next
        self.current = cursor
        return self.current.song if cursor is not None else None

    def iter_songs(self) -> Iterable[SongNode]:
        cursor = self.head
        while cursor is not None:
            yield cursor
            cursor = cursor.next


def prompt_song_details() -> Song:
    title = prompt_non_empty("Titulo de la cancion: ")
    artist = input("Artista (opcional): ").strip()
    duration = input("Duracion, por ejemplo 3:45 (opcional): ").strip()
    return Song(title=title, artist=artist, duration=duration)


def prompt_non_empty(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Debe ingresar un valor.")


def choose_option() -> str:
    print(
        """
Opciones:
1. Anadir cancion al final
2. Insertar cancion despues de la actual y reproducirla
3. Eliminar cancion por titulo
4. Eliminar cancion actual
5. Siguiente cancion
6. Cancion anterior
7. Mostrar cancion actual
8. Mostrar lista completa
9. Saltar a posicion especifica
10. Vaciar playlist
0. Salir
""".strip()
    )
    return input("Seleccione una opcion: ").strip()


def display_playlist(playlist: Playlist) -> None:
    if playlist.is_empty():
        print("La playlist esta vacia.")
        return
    print("\nPlaylist:")
    for index, node in enumerate(playlist.iter_songs(), start=1):
        marker = "->" if node is playlist.current else "  "
        print(f"{marker} {index:02d}. {node.song.display()}")
    print()


def display_current(playlist: Playlist) -> None:
    if playlist.current is None:
        print("No hay cancion reproduciendose.")
    else:
        print(f"Reproduciendo: {playlist.current.song.display()}")


def main() -> None:
    playlist = Playlist()
    handlers = {
        "1": lambda: playlist.add_song(prompt_song_details(), make_current=False),
        "2": lambda: playlist.insert_after_current(prompt_song_details(), make_current=True),
        "3": lambda: handle_remove_by_title(playlist),
        "4": lambda: handle_remove_current(playlist),
        "5": lambda: handle_play_next(playlist),
        "6": lambda: handle_play_previous(playlist),
        "7": lambda: display_current(playlist),
        "8": lambda: display_playlist(playlist),
        "9": lambda: handle_jump_to(playlist),
        "10": lambda: handle_clear(playlist),
    }

    print("Bienvenido a la playlist interactiva.")
    while True:
        option = choose_option()
        if option == "0":
            print("Hasta luego. Disfruta la musica.")
            break
        handler = handlers.get(option)
        if handler is None:
            print("Opcion no valida. Intente de nuevo.")
            continue
        handler()


def handle_remove_by_title(playlist: Playlist) -> None:
    if playlist.is_empty():
        print("No hay canciones para eliminar.")
        return
    title = prompt_non_empty("Titulo exacto a eliminar: ")
    if playlist.remove_by_title(title):
        print(f"Se elimino '{title}'.")
    else:
        print(f"No se encontro '{title}'.")


def handle_remove_current(playlist: Playlist) -> None:
    if playlist.remove_current():
        print("Cancion actual eliminada.")
        display_current(playlist)
    else:
        print("No hay cancion actual para eliminar.")


def handle_play_next(playlist: Playlist) -> None:
    song = playlist.play_next()
    if song is None:
        print("Playlist vacia. Agregue canciones primero.")
    else:
        print(f"Siguiente: {song.display()}")


def handle_play_previous(playlist: Playlist) -> None:
    song = playlist.play_previous()
    if song is None:
        print("Playlist vacia. Agregue canciones primero.")
    else:
        print(f"Anterior: {song.display()}")


def handle_jump_to(playlist: Playlist) -> None:
    if playlist.is_empty():
        print("Playlist vacia. Agregue canciones primero.")
        return
    try:
        position = int(prompt_non_empty("Posicion a reproducir (1-n): "))
    except ValueError:
        print("Ingrese un numero valido.")
        return
    song = playlist.jump_to(position)
    if song is None:
        print("Posicion fuera de rango.")
    else:
        print(f"Reproduciendo posicion {position}: {song.display()}")


def handle_clear(playlist: Playlist) -> None:
    if playlist.is_empty():
        print("La playlist ya esta vacia.")
        return
    confirmation = input("Seguro que desea vaciar la playlist? (s/N): ").strip().lower()
    if confirmation == "s":
        playlist.clear()
        print("Playlist vaciada.")
    else:
        print("Operacion cancelada.")


if __name__ == "__main__":
    main()
