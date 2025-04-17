import geopandas as gpd
from pathlib import Path
import yaml
import pandas as pd
import os

base_path = '/opt/airflow'
manzanas_path = os.path.join(base_path, 'data', 'raw', 'manzana')
permisos_path = os.path.join(base_path, 'data', 'raw', 'permisos')
servicios_path = os.path.join(base_path, 'data', 'raw', 'servicios')

config_path = "/opt/airflow/config/config.yaml"

def extract_geodata():
    print("Cargando shapefiles y servicios...")

    # Leer config.yaml
    with open(config_path) as file:
        config = yaml.safe_load(file)

    comuna = config['comuna_objetivo']

    # Manzanas
    manzana_files = list(Path(manzanas_path).glob("*.shp"))
    if not manzana_files:
        print("No se encontró shapefile de manzanas")
        return
    manzanas = gpd.read_file(manzana_files[0])
    manzanas = manzanas[manzanas['N_COMUNA'] == comuna]
    manzanas = manzanas[manzanas.is_valid]
    manzanas.to_file("data/processed/manzanas.geojson", driver="GeoJSON")

    # Permisos
    permisos_files = list(Path(permisos_path).glob("*.shp"))
    permisos_list = [gpd.read_file(f) for f in permisos_files]
    permisos = pd.concat(permisos_list, ignore_index=True)
    permisos = permisos.dropna(subset=['geometry'])
    permisos = permisos[permisos.is_valid]
    permisos = permisos[permisos['GLOSA_COMU'] == comuna]
    permisos.to_file("data/processed/permisos.geojson", driver="GeoJSON")

    # Servicios
    servicios_files = list(Path(servicios_path).glob("*.geojson"))
    servicios_list = [gpd.read_file(f) for f in servicios_files]
    servicios = pd.concat(servicios_list, ignore_index=True)
    servicios = servicios.dropna(subset=['geometry'])
    servicios = servicios[servicios.is_valid]
    servicios.to_file("data/processed/servicios.geojson", driver="GeoJSON")

    print("Datos geoespaciales cargados y guardados en data/processed/")

if __name__ == "__main__":
    extract_geodata()

