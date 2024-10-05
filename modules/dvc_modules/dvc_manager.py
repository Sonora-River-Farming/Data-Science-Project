from pathlib import Path
from loguru import logger
import subprocess
import sys
from dotenv import load_dotenv
from modules.config import PROCESSED_DATA_DIR, RAW_DATA_DIR, DVC_REMOTE

def check_dvc_repo(path = Path(".")):
    """Check if you are in a DVC repository."""
    dvc_path = Path(path) / ".dvc"

    # Check if the .dvc folder exists in the provided path
    if not dvc_path.exists():
        logger.warning(f"No DVC repository found. Initializing DVC repository...")
        
        # Start a DVC repository in the given directory
        try:
            subprocess.run(["dvc", "init"], check=True)
            logger.success(f"DVC repository initialized successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize DVC repository: {e}")
            raise RuntimeError("Failed to initialize DVC repository.") from e
    else:
        logger.info(f"DVC repository already exists.")


def add_dvc_remote(remote_name="origin", remote_url=DVC_REMOTE):
    """Check if a DVC remote exists, and add it if not."""
    try:
        # Check if the remote already exists
        result = subprocess.run(["dvc", "remote", "list"], capture_output=True, text=True, check=True)
        remotes = result.stdout.strip().splitlines()

        # Verifica si el remoto ya está configurado
        remote_exists = any(remote_name in remote for remote in remotes)
        if remote_exists:
            logger.info(f"DVC remote '{remote_name}' already exists.")
        else:
            logger.warning(f"No DVC remote found. Adding remote '{remote_name}'...")

            # Añadir el remoto si no está configurado
            subprocess.run(["dvc", "remote", "add", "-d", remote_name, remote_url], check=True)
            logger.success(f"DVC remote '{remote_name}' added successfully with URL: {remote_url}")
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check or add DVC remote: {e}")
        raise RuntimeError("Failed to add DVC remote.") from e


def add_file_to_dvc(file_path):
    """Add the file to DVC."""
    
    if not file_path.exists():
        logger.error(f"The file {file_path} does not exist.")
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    logger.info(f"Adding {file_path} to DVC...")
    try:
        subprocess.run(["dvc", "add", str(file_path)], check=True)
        logger.success(f"File {file_path} added to DVC successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error trying to add {file_path} to DVC: {e}")
        raise RuntimeError(f"Error trying to add {file_path} to DVC.") from e


def push_to_dvc_remote(remote_name="origin"):
    """Push changes to the DVC remote."""
    logger.info(f"Attempting to push to remote {DVC_REMOTE}...")
    try:
        subprocess.run(["dvc", "push", "-r", remote_name], check=True)
        logger.success(f"Data pushed successfully to {remote_name}.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error trying to push to remote {DVC_REMOTE}: {e}")
        raise RuntimeError(f"Failed to push to remote {remote_name}.") from e
""" 
if __name__ == "__main__":
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        
        # Ejecutar la función correspondiente según el argumento
        if function_name == "load_data":
            load_data()
        elif function_name == "clean_data":
            clean_data()
        elif function_name == "analyze_data":
            analyze_data()
        else:
            print(f"Function '{function_name}' not found.")
    else:
        print("No function name provided.") """