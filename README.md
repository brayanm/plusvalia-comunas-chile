
# 📊 Análisis de Plusvalía en Comunas de Chile

Este proyecto propone un sistema abierto y reproducible para analizar el **potencial de plusvalía inmobiliaria en distintas comunas de Chile**. Comenzamos con **Valdivia** como comuna piloto, y la idea es extender este enfoque a otras comunas en el futuro.

## 🌱 ¿Por qué este proyecto?

El valor de una propiedad depende no solo de su precio actual, sino también de su capacidad de aumentar su valor en el tiempo. Este proyecto busca identificar, de forma transparente y basada en datos abiertos, las zonas con mayor potencial de plusvalía en distintas comunas chilenas.

## 📊 Tecnologías utilizadas

- **Python 3.11**
- **Apache Airflow**: Orquestación de flujos ETL
- **Pandas / GeoPandas**: Manipulación de datos y datos espaciales
- **Folium**: Visualización de mapas interactivos
- **Shapely**: Análisis geométrico
- **pdfplumber**: Extracción de datos desde PDF
- **Docker + Docker Compose**: Entorno de ejecución reproducible
- **Jupyter Notebook**: Visualización y exploración de resultados
- **YAML**: Configuración flexible del pipeline

## 📁 Estructura del proyecto

```
plusvalia-comunas-chile/
├── airflow/
│   ├── dags/
│   │   └── plusvalia_pipeline_dag.py
│   ├── docker-compose.yaml
│   └── requirements.txt
├── config/
│   └── config.yaml
├── data/
│   ├── raw/
│   │   ├── avaluos/
│   │   ├── manzana/
│   │   ├── permisos/
│   │   └── servicios/
│   └── processed/
│       ├── plusvalia_valdivia.geojson
│       └── plusvalia_valdivia.parquet
├── etl/
│   ├── extract_avaluos.py
│   ├── process_manzanas.py
│   ├── process_permisos.py
│   ├── process_servicios.py
│   └── calcular_score.py
├── notebooks/
│   └── plusvalia_visualizacion.ipynb
├── README.md
└── LICENSE
```
## 📊 Primer caso: Valdivia

Incluye:
- Extracción de avalúos fiscales desde PDFs del SII.
- Integración de permisos de edificación y servicios públicos.
- Cálculo de un **índice de plusvalía** por manzana.
- Visualización interactiva de zonas de alto y bajo potencial.

## 🚀 Cómo levantar el proyecto

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/brayanm/plusvalia_comunas_chile.git
   cd plusvalia-comunas-chile/airflow
   ```

2. **Construir e iniciar los contenedores**
   ```bash
   docker-compose up --build
   ```

3. **Acceder a la interfaz de Airflow**
   - URL: [http://localhost:8080](http://localhost:8080)
   - Usuario y contraseña preconfigurados en el `docker-compose.yaml`

4. **Ejecutar los DAGs desde la interfaz de Airflow**

5. **Visualizar resultados**
   - Corre localmente:
     ```bash
     jupyter notebook
     ```
   - Abre `notebooks/plusvalia_visualizacion.ipynb` para explorar el mapa interactivo.

## 📈 Próximos pasos

➡️ Incorporar nuevas comunas, comenzando por aquellas con mejor disponibilidad de datos abiertos.  
➡️ Mejorar el modelo de scoring incorporando variables socioeconómicas y ambientales.  
➡️ Publicar dashboards web para consulta pública.

## 📖 Licencia

Este proyecto se publica bajo la licencia **Creative Commons BY-NC-ND 4.0**  
[![CC BY-NC-ND 4.0](https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

