from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm
from dataset_modules.downloader import download_file
from dataset_modules.processor import process_data
from dvc_modules.dvc_manager import check_dvc_repo, add_dvc_remote
from modules.config import PROCESSED_DATA_DIR, RAW_DATA_DIR, URL_LIST

app = typer.Typer()

@app.command()
def main(
    #url: str = typer.Option(None, help="URL of the dataset to download"),
    #file: str = typer.Option(None, help="File name to save the dataset (optional)"),
    #input_path: Path = typer.Option(None, help="Optional path to save the dataset"),
    # output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
):
    # if input_path is None:
    #     if file is None:
    #         typer.echo("You must provide either a file name or an input path.")
    #         raise typer.Exit()
    #     input_path = RAW_DATA_DIR / file

    # Verificar si estamos en un repositorio DVC
    check_dvc_repo()

    # Check remote
    add_dvc_remote()   
    
    # Download files
    if URL_LIST:
        for url in URL_LIST:
            input_path = RAW_DATA_DIR / url['file']
            download_file(url=url['url'], info=url['info'], input_path=input_path)
        logger.success(f"All files have been downloaded successfully !")
    else:
        logger.error(f"URL_LIST is empty")
    
    # Process data
    process_data()

if __name__ == "__main__":
    app()
