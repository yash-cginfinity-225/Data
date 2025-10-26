import requests
import pandas as pd
from azure.storage.blob import BlobServiceClient

# Fetch data from API
url = "https://api.artic.edu/api/v1/artworks"
params = {"page": 1, "limit": 20}
response = requests.get(url, params=params)
data = response.json()["data"]

# Convert to DataFrame
df = pd.DataFrame([
    {
        "id": art["id"],
        "title": art["title"],
        "artist": art["artist_display"],
        "date": art["date_display"],
        "medium": art["medium_display"],
        "image_url": art["image_id"] and f"https://www.artic.edu/iiif/2/{art['image_id']}/full/843,/0/default.jpg" or None
    }
    for art in data
])

# Upload CSV to Azure Blob Storage
connect_str = "***********"
container_name = "mycontainer"
blob_name = "artworks.csv"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

csv_bytes = df.to_csv(index=False).encode('utf-8')
container_client.upload_blob(name=blob_name, data=csv_bytes, overwrite=True)

print("CSV uploaded!")