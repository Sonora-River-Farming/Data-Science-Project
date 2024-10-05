from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
import os
import urllib.request
import requests
import datetime
from dvc_modules.dvc_manager import add_file_to_dvc, push_to_dvc_remote

app = typer.Typer()

def download_file(url: str, info: str, input_path: Path):
    """
    Main command to download a dataset from a URL and save it to the specified file name.

    Args:
    - url: URL from which to download the dataset.
    - input_path: The path to save the downloaded dataset as.
    """
    
    SOURCE = url
    INPUT_PATH = input_path
    SUBDIR = INPUT_PATH.parent
    FILE_NAME = INPUT_PATH.name

    logger.info(f"Starting download from {SOURCE}")
    response = requests.get(SOURCE, stream=True)
    total_size = int(response.headers.get('content-length', 0))    

    # Check if the file already exists
    if not os.path.exists(INPUT_PATH):
        logger.info(f"File {FILE_NAME} not found. Starting download...")

        # Create subdirectory if it does not exist
        if not os.path.exists(SUBDIR):
            os.makedirs(SUBDIR)
            logger.info(f"Created directory {SUBDIR}")

        # Download the file from the link provided
        urllib.request.urlretrieve(SOURCE, INPUT_PATH)
        logger.success(f"Download completed: {INPUT_PATH}")

        with open(INPUT_PATH, 'wb') as file, tqdm(
            desc="Downloading",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(1024):
                bar.update(len(data))
                file.write(data)

        logger.success(f"Download completed: {INPUT_PATH}")

        # Create info file with dataset details
        INFO_FILE_NAME = FILE_NAME.split('.')[0] + ".txt"
        INFO_FILE_PATH = os.path.join(SUBDIR, INFO_FILE_NAME)
        logger.info(f"Creating {INFO_FILE_NAME} file with dataset details")

        with open(INFO_FILE_PATH, 'w') as f:
            f.write("Information from water quality monitoring sites operated by Conagua throughout the country\n\n")
            # info = info
            f.write(info + '\n')
            f.write("Downloaded on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("From: " + SOURCE + "\n")
            f.write("Name: " + FILE_NAME + "\n")
        logger.success(f"Info file {INFO_FILE_NAME} created at {SUBDIR}")
        
        # Add the downloaded file to DVC
        add_file_to_dvc(input_path)

        # Push to DVC remote
        push_to_dvc_remote()
    else:
        logger.info(f"File {FILE_NAME} already exists in the directory {SUBDIR}. Skipping download. ")

@app.command()
def download(url: str = typer.Argument(help="URL of the dataset to download"), 
             info: str = typer.Argument(help="Dataset additional information"), 
             input_path: Path = typer.Argument("Path to save the dataset")):
    """
    Download a file from a URL, providing additional information and the input path.
    """
    download_file(url, info, input_path)

if __name__ == "__main__":
    app()