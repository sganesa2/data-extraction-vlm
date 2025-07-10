import logging
import datetime
from datetime import timedelta
from dataclasses import dataclass
from typing import Optional, ByteString

from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient, 
    generate_blob_sas, 
    BlobSasPermissions
)

class SFTPStorage:
    def __init__(self, connection_string:str, container_name:str):
        self.connection_string = connection_string
        self.container_name = container_name
    
    def __enter__(self)->ContainerClient:
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str=self.connection_string)
        return self.blob_service_client.get_container_client(container=self.container_name)
    
    def __exit__(self,type,value,traceback):
        self.blob_service_client.close()

@dataclass
class BlobStorageUtils:
    container_name:str
    connection_string: Optional[str] = None
    account_name:Optional[str] = None
    account_key:Optional[str] = None

    def _upload_single_file_to_blob(self, blob_path:str, data: ByteString, container_client:ContainerClient)->None:
        blob_exists = container_client.get_blob_client(blob=blob_path).exists()
        if blob_exists:
            container_client.delete_blob(blob_path)
        blob_client = container_client.upload_blob(name=blob_path,data=data)
        uploaded_blob_status = blob_client.exists()
        logging_str = f"Blob name:{blob_client.blob_name} has been created with Status:{uploaded_blob_status}"
        logging.error(logging_str)
    
    def _upload_files_to_blob(self, blob_mapping:dict[str,ByteString], container_client:ContainerClient)->None:
        for blob_path, data in blob_mapping.items():
            self._upload_single_file_to_blob(blob_path, data, container_client)

    def _get_single_blob_sas_url(self, blob_path:str, expiration_hours:int = 1)->str:
        if not (self.account_key and self.account_name and self.container_name):
            raise Exception("Missing parameters for generating blob sas url!")
        
        sas_token = generate_blob_sas(account_name=self.account_name, 
                                    container_name=self.container_name,
                                    blob_name=blob_path,
                                    account_key=self.account_key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.datetime.now(datetime.timezone.utc) + timedelta(hours=expiration_hours))
        logging_str = f"SAS Token created for Blob name:{blob_path}"
        logging.error(logging_str)
        return 'https://'+self.account_key+'.blob.core.windows.net/'+self.container_name+'/'+blob_path+'?'+sas_token

    def _get_multiple_blob_sas_urls(self, blob_paths:list[str])->list[str]:
        return list(map(self._get_single_blob_sas_url, blob_paths))

    def upload_blob_and_get_sas_urls(self, blob_mapping:dict[str,ByteString])->list[str]:
        with SFTPStorage(self.connection_string, self.container_name) as container_client:
            self._upload_files_to_blob(blob_mapping, container_client)
            urls = self._get_multiple_blob_sas_urls(list(blob_mapping.keys()))
            if len(urls)==0:
                raise Exception("NO SAS URLS CREATED!")
            return urls
            
