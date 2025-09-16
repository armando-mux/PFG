from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def send_file(local_file_path, container_name, blob_name):

    connect_str = ""

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

