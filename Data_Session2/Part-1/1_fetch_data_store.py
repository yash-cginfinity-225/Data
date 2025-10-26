# Imports
import requests
import pandas as pd

# Fetch data 
url = "https://api.artic.edu/api/v1/artworks"
params = {
    "page": 2,
    "limit": 20,
}
response = requests.get(url, params=params)
data = response.json()

# Process data
artworks = data["data"]
df = pd.DataFrame([
    {
        "id": art["id"],
        "title": art["title"],
        "artist_display": art["artist_display"],
        "date_display": art["date_display"],
        "medium_display": art["medium_display"],
        "image_url": art["image_id"]
            and f"https://www.artic.edu/iiif/2/{art['image_id']}/full/843,/0/default.jpg"
            or None,
    }
    for art in artworks
])
df.to_csv("artworks_data.csv", index=False)

# Display first few rows
print(df.head())