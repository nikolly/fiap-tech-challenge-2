import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import boto3
from botocore.exceptions import NoCredentialsError
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def upload_to_s3(file_name, bucket, object_name=None) -> bool:
    """
    Upload a file to an S3 bucket

    Parameters:
    file_name (str): The name of the file to upload.
    bucket (str): The name of the S3 bucket to upload to.
    object_name (str, optional): The name of the object in the S3 bucket. If not provided, the file_name will be used as the object name.

    Returns:
    bool: True if the file was successfully uploaded, False otherwise.
    """
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def config_selenium():
    """
    Configures and returns a Selenium WebDriver instance with headless mode enabled.
    
    Returns:
        webdriver.Chrome: A Chrome WebDriver instance with headless mode enabled.
    """
    try:
        options = Options()
        options.add_argument("--headless")
        
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error configuring Selenium: {str(e)}")


def get_ibov_data(driver: webdriver.Chrome):
    """
    Retrieves data from the Ibovespa index page on the B3 website.

    Args:
    - driver (webdriver.Chrome): The Chrome webdriver instance.

    Returns:
    - dados (list): A list of lists containing the data from the table on the Ibovespa index page.
      Each inner list represents a row in the table, and each element in the inner list represents a column value.
    
    Exceptions:
    - NoSuchElementException: If an element is not found on the page.
    - TimeoutException: If the page loading times out.
    - Exception: For any other unexpected error.
    """    
    try:
        url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/ibov?language=pt-br'
        driver.get(url)
        time.sleep(5)
        
        filtro = driver.find_element(By.XPATH, '//*[@id="segment"]')
        filtro.click()
        
        driver.find_element(By.XPATH, '//*[@id="segment"]/option[2]').click()
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        driver.find_element(By.XPATH, '//*[@id="selectPage"]').click()
        
        driver.find_element(By.XPATH, '//*[@id="selectPage"]/option[4]').click()        
        time.sleep(5)
        
        tabela = driver.find_element(By.CSS_SELECTOR, 'table.table.table-responsive-sm.table-responsive-md')
        rows = tabela.find_elements(By.TAG_NAME, 'tr')

        dados = []
        for row in rows[2:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            cols = [col.text.strip() for col in cols]
            dados.append(cols)
        
        return dados

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        return None
    except TimeoutException as e:
        print(f"Timeout: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()
