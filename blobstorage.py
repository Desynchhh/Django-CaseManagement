import os
from azure.storage.blob import ContainerClient, BlobServiceClient, BlobClient

class AzureStorage():
    def __init__(self):
        self.storage_account = os.environ.get('SKP_SAGSSTYRING_STORAGE_ACCOUNT')
        self.blob_service_client = BlobServiceClient.from_connection_string(
            os.environ.get('SKP_SAGSSTYRING_AZURE_STORAGE_CONNECTION_STRING')
        )


    def create_container(self, container_name:str):
        self.blob_service_client.create_container(container_name, public_access='blob')
    

    def delete_container(self, container_name:str):
        self.blob_service_client.delete_container(container_name)


    # UPLOAD A FILE TO THE CHOSEN CONTAINER
    def upload_blob(self, container:str, filepath) -> str:
        # Create a blob client using container's name and file's path
        blob_client = self.blob_service_client.get_blob_client(container, filepath)
        
        # Upload blob
        blob_client.upload_blob(filepath)
        
        # Return blob URL
        return self.generate_blob_url(container, filepath.name)


    def delete_blob(self, container:str, blob:str) -> None:
        blob_client = self.blob_service_client.get_blob_client(container, blob)
        blob_client.delete_blob()


    def generate_blob_url(self, container, blob):
        return f'https://{self.storage_account}.blob.core.windows.net/{container}/{blob}'


    def get_containers(self) -> list:
        containers = self.blob_service_client.list_containers()
        return [container.name for container in containers]


    def get_blobs(self, container:str) -> list:
        container_client = self.blob_service_client.get_container_client(container)
        blobs = container_client.list_blobs()
        return [blob.name for blob in blobs]

    
    # def download_blob(self, blob:str, local_path:str, local_file_name:str) -> None:
    #     download_path = os.path.join(local_path, local_file_name.replace('.jpg', '_DOWNLOAD.jpg'))
    #     print('Downloading blob to ' + download_path)
    #     blob_client = self.blob_service_client.get_blob_client(self.container, blob)
    #     with open(download_path, 'wb') as download_file:
    #         download_file.write(blob_client.download_blob().readall())


# TESTING
if __name__ == '__main__':
    #  SETUP
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_path = os.path.join('media', 'img')
    filepath = os.path.join(local_path, 'default.jpg')
    azure = AzureStorage()

    container = 'project-8'

    blobs = azure.get_blobs(container)
    azure._generate_blob_url(container, blobs[0])
