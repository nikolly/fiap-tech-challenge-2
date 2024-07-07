# IBOVESPA Data Capture and Upload to S3 Project

This script is part of the Tech Challenge created by the Machine Learning Engineering postgraduate course at FIAP.
It aims to capture data from the IBOVESPA index directly from the B3 website, transform it into a parquet file, and upload this file to an S3 bucket on AWS.

## Sumary

- [IBOVESPA Data Capture and Upload to S3 Project](#ibovespa-data-capture-and-upload-to-s3-project)
  - [Sumary](#sumary)
  - [Description](#description)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [AWS Credentials](#aws-credentials)
  - [Usage](#usage)
    - [Run the main script](#run-the-main-script)
    - [The script will](#the-script-will)

## Description

This project uses Selenium to automate navigation on the B3 website, where IBOVESPA data is extracted. The data is then processed and converted into a parquet file, which is subsequently uploaded to an S3 bucket on AWS.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your_user/your_repository.git
    cd your_repository
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/MacOS
    .venv\Scripts\activate  # Windows
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### AWS Credentials

Make sure to configure your AWS credentials. You can do this by setting up the ~/.aws/credentials file with your access credentials:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
aws_session_token= YOUR_SECRET_TOKEN
```

## Usage

### Run the main src/script

- python main.py

### The script will

- Configure the Selenium WebDriver.
- Navegato to the IBOVESPA page and capture the data.
- Process the data and save in a parquet file.
- Upload the parquet file to the specified S3 bucket.
