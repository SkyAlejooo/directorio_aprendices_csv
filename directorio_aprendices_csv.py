import pandas as pd
from typing import Optional

CSV_FILE = "aprendices.csv"


def crear_aprendiz(nombre: str, apellido: str, direccion: str, telefono: str, ficha: str) -> None:
    """
    Crea o agrega un aprendiz al archivo CSV.

    Args:
        nombre (str): Nombre del aprendiz.
        apellido (str): Apellido del aprendiz.
        direccion (str): Dirección del aprendiz.
        telefono (str): Teléfono del aprendiz.
        ficha (str): Ficha del aprendiz.

    Returns:
        None
    """
    nuevo = pd.DataFrame([{
        "Nombre": nombre,
        "Apellido": apellido,
        "Direccion": direccion,
        "Telefono": telefono,
        "Ficha": ficha
    }])

    try:
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, nuevo], ignore_index=True)
    except FileNotFoundError:
        df = nuevo

    df.to_csv(CSV_FILE, index=False)
    print(f"✅ Aprendiz {nombre} {apellido} agregado correctamente.")


def leer_aprendices() -> pd.DataFrame:
    """
    Lee y devuelve el contenido del archivo CSV con los aprendices.

    Returns:
        pd.DataFrame: DataFrame con los datos de los aprendices.
    """
    try:
        df = pd.read_csv(CSV_FILE)
        print("📋 Lista de aprendices cargada correctamente.")
        return df
    except FileNotFoundError:
        print("⚠ No hay registros aún.")
        return pd.DataFrame(columns=["Nombre", "Apellido", "Direccion", "Telefono", "Ficha"])


def actualizar_aprendiz(nombre: str, apellido: str, direccion: Optional[str] = None,
                        telefono: Optional[str] = None, ficha: Optional[str] = None) -> bool:
    """
    Actualiza la información de un aprendiz según su nombre y apellido.

    Args:
        nombre (str): Nombre del aprendiz.
        apellido (str): Apellido del aprendiz.
        direccion (Optional[str]): Nueva dirección.
        telefono (Optional[str]): Nuevo teléfono.
        ficha (Optional[str]): Nueva ficha.

    Returns:
        bool: True si se actualizó, False si no se encontró.
    """
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print("⚠ No hay registros para actualizar.")
        return False

    mask = (df["Nombre"] == nombre) & (df["Apellido"] == apellido)
    if not mask.any():
        print(f"❌ Aprendiz {nombre} {apellido} no encontrado.")
        return False

    if direccion:
        df.loc[mask, "Direccion"] = direccion
    if telefono:
        df.loc[mask, "Telefono"] = telefono
    if ficha:
        df.loc[mask, "Ficha"] = ficha

    df.to_csv(CSV_FILE, index=False)
    print(f"✅ Aprendiz {nombre} {apellido} actualizado correctamente.")
    return True


if __name__ == "__main__":
    # Ejemplo de uso manual (puedes comentar esto en producción)
    crear_aprendiz("Mariana", "Zapata", "Calle 20b # 20a 28", "3208916055", "2993648")
    print(leer_aprendices())
    actualizar_aprendiz("Alejandro", "Botia", telefono="3138534161")
    print(leer_aprendices())