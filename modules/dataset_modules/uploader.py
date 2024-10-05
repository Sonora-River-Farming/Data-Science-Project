import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
from tqdm import tqdm
from loguru import logger

def write_parquet(df, output_path, chunk_size=100):
    """
    Function to save a DataFrame to a Parquet file.

    Args:
    df (pd.DataFrame): The DataFrame to be saved.
    output_path (str): Full path of the Parquet file where the DataFrame will be saved.
    chunk_size (int): Size of the chunk to write the Parquet in parts. Default is 100 rows
    """

    try:
        # Convertir el DataFrame a una tabla de Arrow
        table = pa.Table.from_pandas(df)
        total_rows = len(df)
        
        logger.info(f"Starting to write Parquet file to {output_path} with {total_rows} rows.")

        # Create the Parquet writer
        with pq.ParquetWriter(output_path, table.schema) as writer:
            # Start progress bar
            with tqdm(total=total_rows, desc="Writing Parquet", unit="rows") as bar:
                for start in range(0, total_rows, chunk_size):
                    end = min(start + chunk_size, total_rows)
                    
                    # Create a data chunk
                    chunk = table.slice(start, end - start)
                    
                    # Write the chunk to the Parquet file
                    writer.write_table(chunk)
                    
                    # Update progress bar
                    bar.update(end - start)

                    logger.debug(f"Written rows {start} to {end} to Parquet.")

        logger.success(f"Parquet file successfully written to {output_path}.")
    
    except Exception as e:
        logger.error(f"Error while writing Parquet file: {str(e)}")
        raise

def write_csv(df, output_path, chunk_size=100):
    """
    Function to save a DataFrame to a CSV file.

    Args:
    df (pd.DataFrame): The DataFrame to be saved.
    output_path (str): Full path of the CSV file where the DataFrame will be saved.
    chunk_size (int): Size of the chunk to write the CSV in parts. Default is 100 rows
    """

    try:
        total_rows = len(df)
        logger.info(f"Starting to write CSV file to {output_path} with {total_rows} rows.")

        # Abrir el archivo CSV
        with open(output_path, 'w') as f:
            # Escribir los encabezados (header)
            df.head(0).to_csv(f, index=False)
            
            # Barra de progreso para el proceso
            with tqdm(total=total_rows, desc="Writing CSV", unit="rows") as bar:
                for start in range(0, total_rows, chunk_size):
                    end = min(start + chunk_size, total_rows)
                    
                    # Escribir un chunk (parte) del DataFrame
                    df.iloc[start:end].to_csv(f, header=False, index=False)
                    
                    # Actualizar la barra de progreso
                    bar.update(end - start)
                    
                    logger.debug(f"Written rows {start} to {end} to CSV.")

        logger.success(f"CSV file successfully written to {output_path}.")
    
    except Exception as e:
        logger.error(f"Error while writing CSV file: {str(e)}")
        raise

