from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
import pandas as pd
from typing import Optional

console = Console()
CSV_FILE = "aprendices.csv"


def crear_aprendiz(nombre: str, apellido: str, direccion: str, telefono: int, ficha: int) -> None:
    """
    Crea o agrega un aprendiz al archivo CSV.

    Args:
        nombre (str): Nombre del aprendiz.
        apellido (str): Apellido del aprendiz.
        direccion (str): Dirección del aprendiz.
        telefono (int): Teléfono del aprendiz.
        ficha (int): Ficha del aprendiz.

    Returns:
        None
    """
    nuevo = pd.DataFrame([{
        "Nombre": nombre,
        "Apellido": apellido,
        "Dirección": direccion,
        "Teléfono": telefono,
        "Ficha": ficha
    }])

    try:
        df = pd.read_csv(CSV_FILE, dtype={"Teléfono": int, "Ficha": int})
        df = pd.concat([df, nuevo], ignore_index=True)
    except FileNotFoundError:
        df = nuevo

    df.to_csv(CSV_FILE, index=False)

    success_text = Text()
    success_text.append("✓ ", style="bold green")
    success_text.append(f"Aprendiz {nombre} {apellido} agregado correctamente", style="white")

    console.print(
        Panel.fit(
            Align.center(success_text),
            border_style="dim white",
            padding=(1, 2)
        )
    )


def leer_aprendices() -> pd.DataFrame:
    """
    Lee y devuelve el contenido del archivo CSV con los aprendices.
    """
    try:
        df = pd.read_csv(CSV_FILE, dtype={"Teléfono": int, "Ficha": int})

        if not df.empty:
            # Crear tabla minimalista
            table = Table(
                show_header=True,
                header_style="bold dim_white",
                border_style="dim white",
                show_lines=False,
                padding=(0, 1)
            )

            # Añadir columnas
            table.add_column("#", justify="center", style="dim cyan", width=4)
            for col in df.columns:
                table.add_column(col, justify="left", style="white")

            # Añadir filas
            for idx, row in df.iterrows():
                table.add_row(str(idx), *[str(val) for val in row.values])

            # Panel para la tabla
            console.print(
                Panel.fit(
                    table,
                    title="[dim white]📋 Directorio de Aprendices[/dim white]",
                    border_style="dim white",
                    padding=(0, 1)
                )
            )
        else:
            empty_text = Text()
            empty_text.append("📭 ", style="dim yellow")
            empty_text.append("No hay registros disponibles", style="dim white")

            console.print(
                Panel.fit(
                    Align.center(empty_text),
                    border_style="dim white",
                    padding=(1, 2)
                )
            )
        return df

    except FileNotFoundError:
        empty_text = Text()
        empty_text.append("📭 ", style="dim yellow")
        empty_text.append("No hay registros disponibles", style="dim white")

        console.print(
            Panel.fit(
                Align.center(empty_text),
                border_style="dim white",
                padding=(1, 2)
            )
        )
        return pd.DataFrame(columns=["Nombre", "Apellido", "Dirección", "Teléfono", "Ficha"])


def actualizar_aprendiz_por_indice(indice: int, columna: str, nuevo_valor) -> bool:
    """
    Actualiza el valor de una columna específica de un aprendiz por índice.

    Args:
        indice (int): Índice del aprendiz en el DataFrame.
        columna (str): Nombre de la columna a actualizar.
        nuevo_valor: Nuevo valor para la columna.

    Returns:
        bool: True si se actualizó, False si no se encontró.
    """
    try:
        df = pd.read_csv(CSV_FILE, dtype={"Teléfono": int, "Ficha": int})
    except FileNotFoundError:
        error_text = Text()
        error_text.append("⚠ ", style="dim yellow")
        error_text.append("No hay registros para actualizar", style="dim white")

        console.print(
            Panel.fit(
                Align.center(error_text),
                border_style="dim white",
                padding=(1, 2)
            )
        )
        return False

    if indice < 0 or indice >= len(df):
        error_text = Text()
        error_text.append("✗ ", style="dim red")
        error_text.append(f"Índice {indice} no encontrado", style="white")

        console.print(
            Panel.fit(
                Align.center(error_text),
                border_style="dim white",
                padding=(1, 2)
            )
        )
        return False

    if columna not in df.columns:
        error_text = Text()
        error_text.append("✗ ", style="dim red")
        error_text.append(f"Columna '{columna}' no válida", style="white")

        console.print(
            Panel.fit(
                Align.center(error_text),
                border_style="dim white",
                padding=(1, 2)
            )
        )
        return False

    if columna in ["Teléfono", "Ficha"]:
        try:
            nuevo_valor = int(nuevo_valor)
        except ValueError:
            error_text = Text()
            error_text.append("✗ ", style="dim red")
            error_text.append(f"'{columna}' debe ser un número entero", style="white")

            console.print(
                Panel.fit(
                    Align.center(error_text),
                    border_style="dim white",
                    padding=(1, 2)
                )
            )
            return False

    df.at[indice, columna] = nuevo_valor
    df.to_csv(CSV_FILE, index=False)

    success_text = Text()
    success_text.append("✓ ", style="bold green")
    success_text.append(f"Registro actualizado correctamente", style="white")

    console.print(
        Panel.fit(
            Align.center(success_text),
            border_style="dim white",
            padding=(1, 2)
        )
    )
    return True


def mostrar_header():
    """Muestra un header minimalista para la aplicación"""
    header_text = Text()
    header_text.append("SENA ", style="bold white")
    header_text.append("• ", style="dim white")
    header_text.append("Directorio de Aprendices", style="dim white")

    console.print(
        Panel.fit(
            Align.center(header_text),
            border_style="dim white",
            padding=(0, 2)
        )
    )
    console.print()  # Espacio en blanco


def menu():
    """
    Muestra un menú interactivo minimalista para gestionar el directorio de aprendices.
    """
    while True:
        console.clear()
        mostrar_header()

        # Crear el menú centrado
        menu_content = Text()
        menu_content.append("\n")
        menu_content.append("Menú Principal\n", style="bold dim_white")
        menu_content.append("\n")
        menu_content.append("1 ", style="bold cyan")
        menu_content.append("• Crear aprendiz", style="dim white")
        menu_content.append("\n")
        menu_content.append("2 ", style="bold cyan")
        menu_content.append("• Ver aprendices", style="dim white")
        menu_content.append("\n")
        menu_content.append("3 ", style="bold cyan")
        menu_content.append("• Actualizar aprendiz", style="dim white")
        menu_content.append("\n")
        menu_content.append("4 ", style="bold cyan")
        menu_content.append("• Salir", style="dim white")
        menu_content.append("\n")

        # Panel del menú completamente centrado
        console.print(
            Panel.fit(
                Align.center(menu_content),
                border_style="dim white",
                padding=(1, 4)
            )
        )
        console.print()  # Espacio adicional

        # Input sin dimensiones visibles
        opcion = Prompt.ask(
            "[dim white]Seleccione una opción[/dim white]",
            choices=["1", "2", "3", "4"]
        )

        if opcion == "1":
            console.print()  # Espacio
            console.print(Panel.fit(
                Align.center("[dim white]👤 Crear Nuevo Aprendiz[/dim white]"),
                border_style="dim white",
                padding=(0, 2)
            ))
            console.print()

            try:
                nombre = Prompt.ask("[dim white]Nombre[/dim white]")
                apellido = Prompt.ask("[dim white]Apellido[/dim white]")
                direccion = Prompt.ask("[dim white]Dirección[/dim white]")
                telefono = IntPrompt.ask("[dim white]Teléfono[/dim white]")
                ficha = IntPrompt.ask("[dim white]Ficha[/dim white]")
                crear_aprendiz(nombre, apellido, direccion, telefono, ficha)
            except ValueError:
                error_text = Text()
                error_text.append("✗ ", style="dim red")
                error_text.append("Teléfono y ficha deben ser números", style="white")

                console.print(
                    Panel.fit(
                        Align.center(error_text),
                        border_style="dim white",
                        padding=(1, 2)
                    )
                )

            Prompt.ask("[dim white]Presione Enter para continuar[/dim white]", default="")

        elif opcion == "2":
            console.print()  # Espacio
            leer_aprendices()
            Prompt.ask("[dim white]Presione Enter para continuar[/dim white]", default="")

        elif opcion == "3":
            console.print()  # Espacio
            df = leer_aprendices()
            if not df.empty:
                console.print()
                try:
                    indice = IntPrompt.ask("[dim white]Índice del aprendiz a actualizar[/dim white]")
                    columnas = list(df.columns)
                    columna = Prompt.ask(
                        "[dim white]Columna a actualizar[/dim white]",
                        choices=columnas
                    )
                    nuevo_valor = Prompt.ask(f"[dim white]Nuevo valor para {columna}[/dim white]")
                    actualizado = actualizar_aprendiz_por_indice(indice, columna, nuevo_valor)
                except ValueError:
                    error_text = Text()
                    error_text.append("✗ ", style="dim red")
                    error_text.append("Entrada inválida", style="white")

                    console.print(
                        Panel.fit(
                            Align.center(error_text),
                            border_style="dim white",
                            padding=(1, 2)
                        )
                    )
            Prompt.ask("[dim white]Presione Enter para continuar[/dim white]", default="")

        elif opcion == "4":
            farewell_text = Text()
            farewell_text.append("👋 ", style="dim white")
            farewell_text.append("¡Hasta luego!", style="white")

            console.print(
                Panel.fit(
                    Align.center(farewell_text),
                    border_style="dim white",
                    padding=(1, 2)
                )
            )
            break


if __name__ == "__main__":
    menu()