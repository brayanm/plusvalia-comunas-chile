import re
import pdfplumber
import pandas as pd
from pathlib import Path
import yaml
import os

base_path = '/opt/airflow'
avaluos_path = os.path.join(base_path, 'data', 'raw', 'avaluos')

config_path = "/opt/airflow/config/config.yaml"

def extract_avaluos():
    print("Extrayendo avalúos desde PDF...")

    # Leer config.yaml
    with open(config_path) as file:
        config = yaml.safe_load(file)

    comuna = config['comuna_objetivo']
    patron_pdf = config['pattern_avaluos'].format(comuna=comuna)
    pattern = re.compile(patron_pdf)

    pdf_dir = Path(avaluos_path)
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print("No se encontró PDF de avalúos en data/raw/avaluos/")
        return

    pdf_path = pdf_files[0]

    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    match = pattern.search(line)
                    if match:
                        comuna, manzana, predio, valor_pesos, valor_uf, fecha = match.groups()
                        rows.append({
                            "comuna": comuna,
                            "manzana": int(manzana),
                            "predio": int(predio),
                            "valor_pesos": int(valor_pesos.replace(".", "")),
                            "valor_uf": float(valor_uf.replace(".", "").replace(",", ".")),
                            "fecha": pd.to_datetime(fecha, dayfirst=True)
                        })

    avaluos_df = pd.DataFrame(rows)
    avaluos_df.drop_duplicates(inplace=True)
    avaluos_df.dropna(inplace=True)
    avaluos_df = avaluos_df[avaluos_df['valor_pesos'] > 0]

    output_path = Path("data/processed/avaluos.csv")
    avaluos_df.to_csv(output_path, index=False)

    print(f"Avalúos extraídos y guardados en {output_path}")

if __name__ == "__main__":
    extract_avaluos()

