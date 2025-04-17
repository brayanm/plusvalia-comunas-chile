from pathlib import Path
import geopandas as gpd
import pandas as pd

def guardar_resultados():
    print("Consolidando resultados finales...")

    # Leer resultados procesados
    geojson_path = Path("data/processed/plusvalia_valdivia.geojson")
    parquet_path = Path("data/processed/plusvalia_valdivia.parquet")

    if not geojson_path.exists() or not parquet_path.exists():
        print("No se encuentran los archivos procesados para guardar resultados.")
        return

    # Solo los mostramos como comprobación (ya están guardados en transform_cruces)
    df_geojson = gpd.read_file(geojson_path)
    df_parquet = pd.read_parquet(parquet_path)

    print(f"{len(df_geojson)} manzanas exportadas a GeoJSON.")
    print(f"{len(df_parquet)} registros exportados a Parquet.")
    print(f"Archivos disponibles en data/processed/")

if __name__ == "__main__":
    guardar_resultados()