from pathlib import Path
import os
import pandas as pd
import re
import pyarrow as pa
import pyarrow.parquet as pq
import typer
import git
from loguru import logger
from tqdm import tqdm
from ydata_profiling import ProfileReport
from .uploader import write_parquet, write_csv
from dvc_modules.dvc_manager import add_file_to_dvc, push_to_dvc_remote
from modules.config import PROCESSED_DATA_DIR, RAW_DATA_DIR, INTERIM_DATA_DIR, REFERENCES_DIR, DOCS_DIR, URL_LIST, MUNICIPALITY, POLLUTANTS

app = typer.Typer()

def process_data():
    livestock_list = []
    WATER_QUALITY_DATA = 'water_quality_raw_data.xlsb'

    if URL_LIST:    
        for f in URL_LIST:
            FILE_NAME = f['file']
            INPUT_PATH = Path(RAW_DATA_DIR) / FILE_NAME

            # Check if the file already exists
            if not os.path.exists(INPUT_PATH):
                logger.warning(f"File {FILE_NAME} not found. Download it first")
                raise RuntimeError("File not found. Download it first")

            if FILE_NAME == WATER_QUALITY_DATA:
                water_process(FILE_NAME)
            elif re.match(r'^livestock_\d{4}.*\.csv$', FILE_NAME):
                RAW_LIVESTOCK_DATA_DIR = RAW_DATA_DIR / FILE_NAME
                logger.info(f"Starting reading file {FILE_NAME}")
                
                with tqdm(total=len(URL_LIST)-1, desc="Processing files", unit="file") as pbar:
                    livestock = pd.read_csv(RAW_LIVESTOCK_DATA_DIR, encoding='ISO-8859-1')
                    if not livestock.empty:
                        livestock_list.append(livestock)
                    logger.success(f"Reading file {FILE_NAME} completed")
                    pbar.update(1)
                
        if livestock_list:
            livestock_process(livestock_list)                

        logger.success(f"Data processing completed")
    else:
        logger.warning(f"URL_LIST is empty")


def water_process(file):
    FILE_NAME = file
    OUTPUT_FILE = 'water_quality_tidy_data.parquet'
    WATER_RAW_DATA_DIR = RAW_DATA_DIR / FILE_NAME
    WATER_PROCESSED_DATA_DIR = PROCESSED_DATA_DIR / OUTPUT_FILE 
    WATER_RAW_DATA_REFERENCES_FILE = 'water_quality_raw_data_references.csv'
    WATER_PROCESSED_DATA_REFERENCES_FILE = 'water_quality_tidy_data_references.csv'
    WATER_RAW_DATA_REFERENCES_DIR = REFERENCES_DIR / WATER_RAW_DATA_REFERENCES_FILE
    WATER_PROCESSED_DATA_REFERENCES_DIR = REFERENCES_DIR / WATER_PROCESSED_DATA_REFERENCES_FILE
    WATER_DOC_DIR = DOCS_DIR / 'water_report.html'

    excel_file = pd.ExcelFile(WATER_RAW_DATA_DIR, engine='pyxlsb')
    sheet_names = excel_file.sheet_names
    df_water_site = pd.DataFrame()
    df_water_result = pd.DataFrame()
    df_water_dic = pd.DataFrame()

    logger.info(f"Starting reading file {FILE_NAME}")

    # Separate the sheets in DataFrame
    with tqdm(total=len(sheet_names), desc="Reading sheets", unit="sheet") as pbar:
        for sheet in range(len(sheet_names)):
            if sheet == 0:
                df_water_site = pd.read_excel(WATER_RAW_DATA_DIR, engine='pyxlsb', sheet_name=sheet)
            elif sheet == 1:
                df_water_result = pd.read_excel(WATER_RAW_DATA_DIR, engine='pyxlsb', sheet_name=sheet)
            elif sheet == 2:
                df_water_dic = pd.read_excel(WATER_RAW_DATA_DIR, engine='pyxlsb', sheet_name=sheet)
            pbar.update(1)

    logger.success(f"Reading file {FILE_NAME} completed")
    logger.info(f"Starting data processing: merging data frames, filtering according to established criteria, selection, cleaning and conversion of columns")

    # Merging df_water_site and df_water_result DataFrames using 'CLAVE SITIO' as the key.
    df_water_merged = pd.merge(
        df_water_site, 
        df_water_result, 
        on='CLAVE SITIO', 
        how='inner'
    )

    # Select the columns required for the study
    df_water_merged_filtered = df_water_merged[
        ['CLAVE SITIO', 'ESTADO', 'MUNICIPIO', 'CUERPO DE AGUA', 'TIPO CUERPO DE AGUA', 'SUBTIPO CUERPO AGUA', 'LATITUD', 'LONGITUD'] + 
        POLLUTANTS
    ]
    
    # Filter the DataFrame to obtain only the records of the water bodies that are not "COASTAL" of the affected municipalities of the state of Sonora.
    df_water_filtered_sonora = df_water_merged_filtered[
        (df_water_merged['ESTADO'] == 'SONORA') &
        (df_water_merged['MUNICIPIO'].isin(MUNICIPALITY))   
    ]
    df_water_filtered_sonora = df_water_filtered_sonora[
        ~df_water_filtered_sonora['TIPO CUERPO DE AGUA'].str.contains('COSTERO', na=False)
    ]

    # Clean the columns of pollutants by removing the '>' and '<' symbols and converting them to numeric
    for column in POLLUTANTS:
        if column in df_water_filtered_sonora.columns:
            df_water_filtered_sonora[column] = df_water_filtered_sonora[column].astype(str)
            df_water_filtered_sonora[column] = (
                df_water_filtered_sonora[column]
                .str.replace('<', '', regex=False)
                .str.replace('>', '', regex=False)
            )
            df_water_filtered_sonora[column] = pd.to_numeric(df_water_filtered_sonora[column], errors='coerce')

    # Save new DataFrame to a Parquet file
    logger.info(f"Saving file {OUTPUT_FILE}")
    write_parquet(df_water_filtered_sonora, WATER_PROCESSED_DATA_DIR, 10)
    
    logger.info(f"Saving dictionaries")

    # Save dictionary of original data
    write_csv(df_water_dic, WATER_RAW_DATA_REFERENCES_DIR, 5)
    
    # Save dictionary of new DataFrame
    df_water_tidy_dic = df_water_dic[df_water_dic['CLAVE PARÁMETRO'].isin(POLLUTANTS)]
    write_csv(df_water_tidy_dic, WATER_PROCESSED_DATA_REFERENCES_DIR, 5)

    # Create the data profile report and save the report as an HTML file
    handle_dvc(WATER_PROCESSED_DATA_DIR)
    
    # Create the data profile report and upload to GitHub
    logger.info(f"Creating data profile report and pushing to GitHub")
    profile_data(df_water_filtered_sonora, WATER_DOC_DIR, title="Data Profile Report: Data Quality")
    upload_report(WATER_DOC_DIR)

    logger.success(f"Tasks successfully completed for file {WATER_DOC_DIR}")

  
def livestock_process(file_list):
    # FILE_NAME = file
    # RAW_LIVESTOCK_DATA_DIR = RAW_DATA_DIR / FILE_NAME
    OUTPUT_FILE = 'livestock_tidy_data.parquet'
    LIVESTOCK_RAW_DATA_DIR = RAW_DATA_DIR / OUTPUT_FILE 
    LIVESTOCK_PROCESSED_DATA_DIR = PROCESSED_DATA_DIR / OUTPUT_FILE
    LIVESTOCK_RAW_DATA_REFERENCES_FILE = 'livestock_raw_data_references.csv'
    LIVESTOCK_RAW_DATA_REFERENCES_DIR = REFERENCES_DIR / LIVESTOCK_RAW_DATA_REFERENCES_FILE
    LIVESTOCK_DOC_DIR = DOCS_DIR / 'livestock_report.html'

    valores_cmun = ['Huepac', 'Ures', 'Aconchi', 'Arizpe', 'Banámichi', 'Baviácora ', 'Cananea', 'San Felipe de Jesús']
    especies_permitidas = ['Bovino', 'Caprino', 'Porcino', 'Ovino']
    nuevos_nombres = {
        'Anio': 'Año',
        'Cveestado': 'Clave_Estado',
        'Nomestado': 'Nombre_Estado',
        'Nomddr': 'Nombre_DDR',
        'Cvempio': 'Clave_Municipio',
        'Nommunicipio': 'Nombre_Municipio',
        'Nomespecie': 'Nombre_Especie',
        'Cveproducto': 'Clave_Producto',
        'Nomproducto': 'Nombre_Producto',
        'Volumen': 'Volumen',
        'Precio': 'Precio',
        'Valor': 'Valor Total'
    }

    livestock_merged = pd.concat(file_list, ignore_index=True)

    # Filtrar la tabla donde CMUN está en la lista especificada
    livestock_filtered = livestock_merged[livestock_merged['Nommunicipio'].isin(valores_cmun)]

    # Mantener solo las especies permitidas
    livestock_filtered = livestock_filtered[livestock_filtered['Nomespecie'].isin(especies_permitidas)]

    # Eliminar las columnas especificadas
    livestock_filtered = livestock_filtered.drop(columns=['Cveddr', 'Cveespecie', 'Peso', 'Asacrificado', 'Nomddr'])

    # Rename columns and change data types for better handling
    livestock_filtered.rename(columns=nuevos_nombres, inplace=True)

    # Reemplazar comas y espacios en blanco, pero mantener el formato
    def clean_value(value):
        if isinstance(value, str):
            return value.replace(',', '').strip()  # Limpiar comas y espacios
        return value

    # Aplicar la limpieza a las columnas
    livestock_filtered['Volumen'] = livestock_filtered['Volumen'].apply(clean_value)
    livestock_filtered['Precio'] = livestock_filtered['Precio'].apply(clean_value)
    livestock_filtered['Valor Total'] = livestock_filtered['Valor Total'].apply(clean_value)

    # Convertir a float, pero manejar los errores
    def safe_float_conversion(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return value  # Mantener el valor original si no se puede convertir

    # Aplicar la conversión
    livestock_filtered['Volumen'] = livestock_filtered['Volumen'].apply(safe_float_conversion)
    livestock_filtered['Precio'] = livestock_filtered['Precio'].apply(safe_float_conversion)
    livestock_filtered['Valor Total'] = livestock_filtered['Valor Total'].apply(safe_float_conversion)

    # Cambiar tipos de datos a int
    livestock_filtered['Año'] = livestock_filtered['Año'].astype(int)
    livestock_filtered['Clave_Estado'] = livestock_filtered['Clave_Estado'].astype(int)
    livestock_filtered['Clave_Municipio'] = livestock_filtered['Clave_Municipio'].astype(int)
    livestock_filtered['Clave_Producto'] = livestock_filtered['Clave_Producto'].astype(int)

    # Save new DataFrame to a Parquet file
    logger.info(f"Saving file {OUTPUT_FILE}")
    write_parquet(livestock_filtered, LIVESTOCK_PROCESSED_DATA_DIR, 100)

    # Create the data profile report and save the report as an HTML file
    handle_dvc(LIVESTOCK_PROCESSED_DATA_DIR)

    # Create the data profile report and upload to GitHub
    logger.info(f"Creating data profile report and pushing to GitHub")
    profile_data(livestock_filtered, LIVESTOCK_DOC_DIR, title="Data Profile Report: Livestock Data")
    upload_report(LIVESTOCK_DOC_DIR)

    logger.success(f"Tasks successfully completed for file {LIVESTOCK_DOC_DIR}.")

def profile_data(df, path, title):
    # Create the data profile report
    profile = ProfileReport(df, title=title, explorative=True)

    # Save the report as an HTML file
    profile.to_file(path)

def upload_report(path):
    try:
        repo_path = Path(path).parent.parent
        repo = git.Repo(repo_path)
        repo.git.add('docs/')
        repo.index.commit(f"chore: update data profile report")
        origin = repo.remote(name='origin')
        origin.push()
        
        logger.success(f"Report successfully uploaded to GitHub.")
    
    except Exception as e:
        logger.error(f"An error occurred while creating or uploading the report: {e}")

def handle_dvc(file_path, remote='origin'):
    # Add the downloaded file to DVC
    add_file_to_dvc(file_path)

    # Push to DVC remote
    push_to_dvc_remote(remote_name=remote)

@app.command()
def process():
    """
    Processes all downloaded files found in the URL_LIST list.
    """
    process_data()

if __name__ == "__main__":
    app()

