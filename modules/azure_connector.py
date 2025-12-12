"""
Azure & Databricks Connectivity Module
"""
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
from pyspark.sql import SparkSession
import logging

def get_key_vault_secret(secret_name, key_vault_url=None):
    """
    Securely retrieve a secret from Azure Key Vault using DefaultAzureCredential.
    """
    if not key_vault_url:
        key_vault_url = os.environ.get('KEY_VAULT_URL')
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value

def get_storage_file(container_name, blob_path, download_path, storage_account_url=None, storage_key=None):
    """
    Download a file from Azure Blob Storage to local filesystem.
    """
    if not storage_account_url:
        storage_account_url = os.environ.get('STORAGE_ACCOUNT_URL')
    if not storage_key:
        storage_key = os.environ.get('STORAGE_KEY')
    blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=storage_key)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
    with open(download_path, "wb") as f:
        f.write(blob_client.download_blob().readall())
    return download_path

def init_spark_session(app_name="ClinicalNLP"):
    """
    Initialize and return a Spark session for Azure Databricks.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    return spark
