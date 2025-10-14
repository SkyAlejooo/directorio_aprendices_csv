import os
import pandas as pd
from directorio_aprendices_csv import crear_aprendiz, leer_aprendices, actualizar_aprendiz, CSV_FILE


def setup_function():
    """Crea un entorno limpio antes de cada prueba."""
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)


def test_crear_y_leer_aprendiz():
    crear_aprendiz("Pedro", "Sanchez", "Carrera 16", "3102532301", "2993548")
    df = leer_aprendices()
    assert not df.empty
    assert df.iloc[0]["Nombre"] == "Pedro"
    assert df.iloc[0]["Ficha"] == "2993548"


def test_actualizar_aprendiz():
    crear_aprendiz("Mariana", "Botia", "Calle 28", "3152489653", "2996584")
    actualizado = actualizar_aprendiz("Maria", "Lopez", telefono="3201452358")
    assert actualizado is True

    df = leer_aprendices()
    assert df.iloc[0]["Telefono"] == "3222222222"


def test_actualizar_inexistente():
    actualizado = actualizar_aprendiz("Pedro", "Torres", telefono="3111111111")
    assert actualizado is False