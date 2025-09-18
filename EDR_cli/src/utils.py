from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import socket
import sys

""" def send_file(local_file_path, container_name, blob_name):

    connect_str = ""

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

"""

# Esta funcion esta pensada para usarla en la generacion de datos con MV infectadas. En vez de usar un share de 
# azure, se pasa por un socket normal a otra MV con la que tiene una red interna (así se evita la conexcion a internet)

def send_file(local_file_path, container_name, blob_name):
    host = "10.0.0.1"
    port = 50001
    try:
        with open(local_file_path, 'rb') as file:
            file_data = file.read()
        
        filename = os.path.basename(local_file_path)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(filename.encode() + b'|||')
            s.sendall(file_data)
        
        print(f"Archivo enviado: {local_file_path}")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False
