from pathlib import Path
import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

REFERENCES_DIR = PROJ_ROOT / "references"
DOCS_DIR = PROJ_ROOT / "docs"

DVC_ROOT = PROJ_ROOT / '.dvc'

# Remote
DVC_REMOTE = os.getenv("DVC_REMOTE")
DVC_GDRIVE_CLIENT_ID = os.getenv("DVC_GDRIVE_CLIENT_ID")
DVC_GDRIVE_CLIENT_SECRET = os.getenv("DVC_GDRIVE_CLIENT_SECRET")

#URLs
URL_LIST = [
    {
        'url': 'https://files.conagua.gob.mx/aguasnacionales/TODOS%20LOS%20MONITOREOS.xlsb',
        'info': (
            "The information includes data on lotic, lentic, coastal, and underground water bodies, covering physicochemical "
            "and microbiological parameters according to the type of water body. These data are organized in an Excel file "
            "with three spreadsheets.\n\n"

            "First sheet: Contains details about the monitoring sites, such as key, name, aquifer, state, municipality, type "
            "of water body, latitude, longitude, among others.\n\n"

            "Second sheet: Presents the results of the monitoring, grouped by site, type of water body, date of completion, "
            "and the physicochemical and microbiological parameters recorded.\n\n"

            "Third sheet: Offers a dictionary that describes each parameter, indicating its key, name, and unit of measurement.\n\n"

            "The data was obtained from the National Water Commission (CONAGUA) (https://www.gob.mx/conagua/articulos/calidad-del-agua)"
            "dated August 6, 2024."
        ),
        'file': 'water_quality_raw_data.xlsb'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2013.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2013. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2013_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2014.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2014. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2014_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2015.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2015. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2015_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2016.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2016. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2016_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2017.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2017. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2017_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2018.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2018. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2018_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2019.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2019. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2019_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2020.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2020. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2020_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2021.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2021. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2021_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2022.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2022. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2022_raw_data.csv'
    },
    {
        'url': 'http://infosiap.siap.gob.mx/gobmx/datosAbiertos/Estadist_Produc_Pecuaria/cierre_2023.csv',
        'info': (
            "The information includes data on livestock production in the state of Sonora, Mexico, covering different species and products," 
            "as well as their volume and price. These data are organized in a CSV file containing records from 2023. \n\n"

            "The dataset includes the following columns: Año, Clave_Estado, Nombre_Estado, Clave_Municipio, Nombre_Municipio, Nombre_Especie," 
            "Clave_Producto, Nombre_Producto, Volumen, Precio y Valor Total"

            "Each record provides information on livestock production, including the type of product and its market value."

            "The data was obtained from the Mexican Agricultural Information System (SIAP) through the open data portal (http://infosiap.siap.gob.mx/gobmx/datosAbiertos_p.php)"
            "dated August 6, 2024."
        ),
        'file': 'livestock_2023_raw_data.csv'
    }
]

# Info
POLLUTANTS = ['OD_mg/L', 'DBO_TOT', 'DQO_TOT', 'COLI_FEC', 'E_COLI', 'N_TOT', 'P_TOT', 'TOX_D_48_UT', 'TOX_FIS_SUP_15_UT']
MUNICIPALITY = ['ARIZPE', 'BANÁMICHI', 'HUÉPAC', 'ACONCHI', 'SAN FELIPE', 'BAVIÁCORA', 'URES', 'CANANEA']


# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
