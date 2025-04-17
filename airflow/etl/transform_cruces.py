import geopandas as gpd
import pandas as pd
import numpy as np
import yaml
from pathlib import Path

config_path = "/opt/airflow/config/config.yaml"

def transformar_datos():
    print("Procesando cruces y cálculo de score...")

    with open(config_path) as file:
        config = yaml.safe_load(file)

    buffer_m = config['buffer_metros']
    crs_utm = config['crs_utm']

    # Cargar datos procesados
    manzanas = gpd.read_file("data/processed/manzanas.geojson")
    permisos = gpd.read_file("data/processed/permisos.geojson")
    servicios = gpd.read_file("data/processed/servicios.geojson")
    avaluos_df = pd.read_csv("data/processed/avaluos.csv")

    # Agrupar avaluos por manzana
    avaluos_agg = avaluos_df.groupby('manzana')['valor_pesos'].sum().reset_index(name='avaluo_total')

    # Spatial join permisos → manzanas
    permisos = permisos.to_crs(manzanas.crs)
    permisos_en_manzana = gpd.sjoin(permisos, manzanas, predicate="within")
    permisos_agg = permisos_en_manzana.groupby('COD_MANZAN').size().reset_index(name='num_permisos')

    # Reproyectar manzanas a UTM
    manzanas_proj = manzanas.to_crs(epsg=crs_utm)
    centroides = manzanas_proj.copy()
    centroides["geometry"] = centroides.geometry.centroid
    buffers = centroides.copy()
    buffers["geometry"] = centroides.geometry.buffer(buffer_m)

    # Servicios en buffer
    servicios_proj = servicios.to_crs(epsg=crs_utm)
    servicios_en_radio = gpd.sjoin(servicios_proj, buffers, predicate="within")
    conteo_servicios = servicios_en_radio.groupby("COD_MANZAN").size().reset_index(name="servicios_cercanos")

    # Unificar todo
    df = manzanas.merge(avaluos_agg, left_on='COD_MANZAN', right_on='manzana', how='left')
    df = df.merge(permisos_agg, on='COD_MANZAN', how='left')
    df = df.merge(conteo_servicios, on='COD_MANZAN', how='left')

    df[['avaluo_total', 'num_permisos', 'servicios_cercanos']] = df[['avaluo_total', 'num_permisos', 'servicios_cercanos']].fillna(0)

    # Calcular score
    df['score'] = (
        np.log1p(df['avaluo_total']) +
        2 * df['num_permisos'] +
        1.5 * df['servicios_cercanos']
    )

    df.to_file("data/processed/plusvalia_valdivia.geojson", driver='GeoJSON')
    df.drop(columns='geometry').to_parquet("data/processed/plusvalia_valdivia.parquet")

    print("Datos procesados y guardados en data/processed/")

if __name__ == "__main__":
    transformar_datos()