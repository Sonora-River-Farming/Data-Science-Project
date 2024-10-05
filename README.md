# Sonora River Farming

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Overview

This project focuses on analyzing the impact of pollution in the Sonora River on farming activities in affected areas. It automates the process of downloading, processing, and tracking large datasets related to water quality and livestock production using DVC (Data Version Control) for version control.

## Requirements
You will need the following to run the project:
* Python 3.12+
* virtualenv
* pip
* dvc with Google Drive support
* A .env file with the correct configuration (described below)

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         modules and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── modules   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes modules a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset_modules         <- Scripts for dataset management (download, process, upload)
    │   ├── __init__.py         <- Makes dataset_modules a Python package
    │   ├── downloader.py       <- Script for downloading datasets from URLs
    │   ├── processor.py        <- Script for processing and cleaning datasets
    │   └── uploader.py         <- Script for saving datasets in Parquet or CSV format
    │
    ├── dvc_modules             <- Scripts for DVC automation and management
    │   └── dvc_manager.py      <- Script for managing DVC repository, remote setup, and pushing files
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```



## Environment Setup
### Configuration .env file

Ensure the .env file contains the following:

```
    DVC_REMOTE=<Your_Google_Drive_Remote_URL>
```

This DVC_REMOTE will specify the Google Drive remote storage URL used by DVC for data versioning.

### Configuration Details in config.py
**URL_LIST:** This list contains the datasets that are downloaded and processed. Each entry includes a URL, metadata about the file, and the file name.

**POLLUTANTS:** Defines a list of pollutant parameters to be analyzed from water quality datasets. These include parameters like dissolved oxygen (OD_mg/L), total nitrogen (N_TOT), and more.

**MUNICIPALITY:** Defines a list of municipalities in Sonora state, Mexico, where the analysis will focus. The data related to these regions will be filtered and processed.

### Setup DVC remote with Google Drive
Follow these steps to create your own Google Cloud project and generate OAuth credentials for your GDrive remotes to connect to Google Drive.

https://dvc.org/doc/user-guide/data-management/remote-storage/google-drive#using-a-custom-google-cloud-project-recommended

## Running the Project

1. Set up the environment:
```bash
    make create_environment
```

2. Install required packages:
```bash
    make requirements
```

3. Download and Process Data: To download and process the data automatically with DVC tracking:
```bash
    make data
```

4. To download the data separately and process it later:
```bash
    make download
    make process
```

## Makefile Commands

Here are the available commands in the Makefile:

* ```make create_environment```: Sets up a Python virtual environment.

* ```make requirements```: Installs all required Python packages from requirements.txt.

* ```make data```: Downloads, processes, and tracks the datasets with DVC. This is the main command that automates the entire data pipeline from downloading, processing, and pushing data to remote storage via DVC.

* ```make download```: Downloads the raw datasets listed in the URL_LIST (in config.py) and saves them in data/raw. This step can be executed separately from processing if needed.

* ```make process```: Processes the downloaded datasets, generating cleaned versions in data/processed. It processes files listed in the URL_LIST from config.py.

* ```make dvc```: Initializes DVC and configures the remote storage as specified in .env.

### Key Make Commands in Detail
```make data```

* This command runs the entire data pipeline: it downloads the datasets, processes them, and pushes the results to the DVC remote. It’s a single command for fully automating the workflow from start to finish.

```make download```

* Downloads the raw data from the URLs defined in URL_LIST in config.py. It supports various formats, including .xlsb and .csv, and the files are saved in the data/raw folder. Metadata for each file is also generated.

```make process```

* Reads, cleans, and processes the raw datasets listed in config.py. It generates cleaned versions of the data in Parquet format, which are saved in the data/processed directory. Data quality reports are also generated for each dataset.

## DVC Integration

DVC is used to manage and track the datasets. Below are the key commands for DVC:

* Initialize DVC:
```bash
    dvc init
```

* Add DVC Remote: Configured with Google Drive remote:
```bash
    dvc remote add -d myremote gdrive://<your-folder-id>
```

* Track a File: Track downloading or processing data with DVC:
```bash
    dvc add data/raw/water_quality_raw_data.xlsb
```

* Push Data to Remote: Push tracked data to the remote storage:
```bash
    dvc push
```

## Data Profile Report
Data profiling reports will be available through the following GitHub Pages links:
* **Livestock report:** https://sonora-river-farming.github.io/Data-Science-Project/livestock_report.html
* **Water quality report:** https://sonora-river-farming.github.io/Data-Science-Project/water_report.html

These reports provide a comprehensive analysis of the datasets, including:

* Descriptive statistics: Summary of key characteristics of each variable, such as mean, median, standard deviation, etc.
* Data distributions: Graphical visualizations showing how the values ​​of each variable are distributed.
* Null values: Identification and percentage of missing data in each column.
* Correlations: Analysis of the relationship between the different variables.
Duplicate detection: Number of duplicate records in the dataset.

## License

This project is licensed under the MIT License.