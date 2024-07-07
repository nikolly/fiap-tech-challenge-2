import pandas as pd
from datetime import date
from functions import upload_to_s3, config_selenium, get_ibov_data

# Configure Selenium
driver = config_selenium()

# Retrieve Ibovespa data
ibov_data = get_ibov_data(driver)

if ibov_data:
    # Create a DataFrame with Ibovespa data and add the data_pregao column
    dt = pd.DataFrame(ibov_data)
    dt['data_pregao'] = date.today()
    
    # Rename the DataFrame columns
    header = ['setor', 'codigo', 'acao', 'tipo', 'qtd', 'part', 'part_acum', 'data_pregao']
    dt.columns = header

    # Convert qtd, part, part_acum columns to numeric
    numeric_columns = ['qtd', 'part', 'part_acum']
    dt[numeric_columns] = dt[numeric_columns].replace('\.', '', regex=True)
    dt[numeric_columns] = dt[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Save DataFrame in parquet file
    file_path = 'data/ibov.parquet'
    dt.to_parquet(file_path, index=False)
    
    # Upload the parquet file to AWS S3
    bucket_name = 'fiap-mlet'
    upload_to_s3(file_path, bucket_name, 'ibov.parquet')
