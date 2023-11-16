import json
# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError
import gspread
from google.oauth2.service_account import Credentials
from botocore.exceptions import NoCredentialsError


def get_secret():

    secret_name = "qontak_data_sheet_credential"
    region_name = "ap-southeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
        

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.

def clear_worksheet(secret, spreadsheet_name, worksheet_name):
    # Authentikasi dengan Google Sheets menggunakan berkas kredensial
    gc = gspread.service_account_from_dict(secret)

    # Membuka spreadsheet berdasarkan nama
    spreadsheet = gc.open(spreadsheet_name)

    # Memilih worksheet berdasarkan nama
    worksheet = spreadsheet.worksheet(worksheet_name)

    # Baca semua data dari worksheet
    data = worksheet.get_all_values()

    # Simpan header (baris pertama)
    header = data[0]

    # Hapus semua baris selain header
    worksheet.clear()

    # Tambahkan kembali header sebagai satu-satunya baris
    worksheet.append_row(header)

def lambda_handler(event, context):
    secret_name = 'qontak_data_sheet_credential'  # Ganti dengan nama rahasia yang sesuai
    spreadsheet_name = 'Copy of Qontak Data'
    
    # Mengambil rahasia dari AWS Secrets Manager
    secret = json.loads(get_secret(secret_name))

    # Mendapatkan daftar worksheet dalam spreadsheet
    gc = gspread.service_account_from_dict(secret)
    spreadsheet = gc.open(spreadsheet_name)
    worksheets = spreadsheet.worksheets()

    # Menghapus data dari setiap worksheet dan menyisakan satu baris sebagai header
    for worksheet in worksheets:
        clear_worksheet(secret, spreadsheet_name, worksheet.title)

    return {
        "statusCode": 200,
        "body": json.dumps("Data berhasil dihapus dan header disisakan.")
    }