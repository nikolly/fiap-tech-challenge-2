import pandas as pd
from datetime import datetime
from functions import upload_to_s3, config_selenium, get_ibov_data

# Configure Selenium
driver = config_selenium()
print("Selenium configured")

# Retrieve Ibovespa data
ibov_data = get_ibov_data(driver)
print("Ibovespa data retrieved")

if ibov_data:
    # Create a DataFrame with Ibovespa data and add the data_pregao column
    dt = pd.DataFrame(ibov_data)
    dt['data_pregao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Rename the DataFrame columns
    header = ['setor', 'codigo', 'acao', 'tipo', 'qtd', 'part', 'part_acum', 'data_pregao']
    dt.columns = header

    # Convert qtd, part, part_acum columns to numeric
    numeric_columns = ['qtd', 'part', 'part_acum']
    dt[numeric_columns] = dt[numeric_columns].replace('\.', '', regex=True)
    dt[numeric_columns] = dt[numeric_columns].replace('\,', '.', regex=True)
    dt[numeric_columns] = dt[numeric_columns].apply(pd.to_numeric, errors='coerce')
    print("DataFrame created")

    # Save DataFrame in parquet file
    file_path = 'data/ibov.parquet'
    dt.to_parquet(file_path, index=False)
    print("Parquet file created")
    
    # Upload the parquet file to AWS S3
    bucket_name = 'fiap-mlet'
    upload_to_s3(file_path, bucket_name, 'ibov.parquet')
    print("File uploaded to S3")
