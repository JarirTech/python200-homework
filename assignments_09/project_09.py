# video link: https://youtu.be/Zhw8YDl10vQ
# I couldn't finish the video, my computer got frozen and run out of memory, so I have to stop the video just attach 2 screenshots
#  of the container and the weather data that was uploaded to the container(see the outputs folder)

#Part 2: Project -- Extract + Load Pipeline

##Build project_09.py, a script that implements a complete Extract + Load pipeline using the Open-Meteo weather 
# API and Azure Blob Storage.

ACCOUNT_URL = "https://bouchaibctd2026sa.blob.core.windows.net"
#https://bouchaibctd2026sa.blob.core.windows.net
CONTAINER = "pipeline-data"

#Step 1: Extract
import requests
import json

url = (
     "https://api.open-meteo.com/v1/forecast"
    "?latitude=42.3584&longitude=-71.0598"
    "&hourly=temperature_2m,precipitation"
    "&forecast_days=7")



response = requests.get(url)
response.raise_for_status()
data = response.json()

#Step 2: Serialize-------------
payload = json.dumps(data).encode("utf-8")


#Step 3: Load---------

from datetime import date
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential

today = date.today().isoformat()  
blob_path = f"raw/{today}/weather.json"

credential = DefaultAzureCredential()
container = ContainerClient(
    account_url = ACCOUNT_URL,
    container_name="pipeline-data",
    credential=credential
)

container.upload_blob(blob_path, payload, overwrite=True)


# Print a confirmation message showing the blob path and the number of bytes uploaded.
print(f"Uploaded to {blob_path} ({len(payload)} bytes)")

#---Step 4: Verify--------------
#List all blobs in the container and print each one's name and size.
blobs = container.list_blobs()
for blob in blobs:
    print(f"Blob: {blob.name}, Size: {blob.size} bytes")

#----Step 5: Read Back--------

import io
import pandas as pd

raw = container.download_blob(blob_path).readall()
df = pd.DataFrame(json.loads(raw.decode("utf-8"))["hourly"])
print(f"\nFirst 5 rows:")
print(df.head())

# Save the downloaded JSON to outputs/weather_raw.json
with open("outputs/weather_raw.json", "w") as f:
    json.dump(json.loads(raw.decode("utf-8")), f, indent=4)
    

    