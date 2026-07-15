# --------Part 2: Project -- LLM Transform Pipeline---------
# For a technical issue I couldn't record a short video and instead I just added a screenshots folder to attach screenshots of the project of my terminal and also of 
# the data_pipeline with the processed blob.
#-------reflect-----

# I think the use of LLM here in this project was not necessary. We can get the same result using 
# simple code with if statements.
#  For example, we can classify the conditions as good, marginal, or bad for outdoor running based on temperature 
# # and precipitation using simple rules like:
#  if temperature > 10 and precipitation < 1:
#     condition = "good"
# elif temperature > 5 and precipitation < 3:
#     condition = "marginal"
# else:
#     condition = "bad"

#A rule-based approach would be faster, cheaper, and more
# consistent, while an LLM provides more flexibility but I think is not really needed here.

import json
import pandas as pd
from datetime import date
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential

ACCOUNT_URL =  "https://bouchaibctd2026sa.blob.core.windows.net"
CONTAINER = "pipeline-data"

#------Step 1: Read------------------------
# Download the raw weather data you uploaded in Week 9 from raw/<today>/weather.json. Parse the JSON and reshape the "hourly" parallel lists into a list of per-hour record dictionaries (each with "time", "temperature_2m", and "precipitation"). If today's date doesn't match when you uploaded in Week 9, use the fallback dataset.
#If you did not complete Week 9, a fallback dataset is available at assignments/resources/weather_raw.json -- load it with json.load() and reshape it the same way.





credential = DefaultAzureCredential()
container = ContainerClient(
    account_url = ACCOUNT_URL,
    container_name="pipeline-data",
    credential=credential
)

blob_path = "raw/2026-06-03/weather.json"


raw = container.download_blob(blob_path).readall()

weather_json = json.loads(raw.decode("utf-8"))

hourly = weather_json["hourly"]

records = [
    {
        "time": t,
        "temperature_2m": temp,
        "precipitation": precip
    }
    for t, temp, precip in zip(
        hourly["time"],
        hourly["temperature_2m"],
        hourly["precipitation"]
    )
]

df = pd.DataFrame(records)
print(f"Loaded {len(records)} hourly records")
print("\nFirst 5 rows:")
print(df.head())


#------Step 2: Transform---------
#For each record, call the OpenAI API to classify the conditions as good, marginal, or bad for outdoor running, 
# based on temperature and precipitation:
SYSTEM_PROMPT = (
    "You are classifying hourly weather conditions for outdoor running. "
    "Given a temperature in Celsius and a precipitation amount in mm, "
    "classify the conditions as exactly one of: good, marginal, or bad. "
    "Reply with that one word only -- no punctuation, no explanation."
)
# The user message for each record should be: "Temperature: <value>C, Precipitation: <value>mm".
# To keep costs and runtime manageable, process only the first 24 records (one day of hourly data).
#  Add a fallback: if the model's response is not one of the three valid labels, store "unknown" instead.
# Print a progress message every 6 records so you can see it running.


def make_user_message(record):
    return (
        f"Temperature: {record['temperature_2m']}C, "
        f"Precipitation: {record['precipitation']}mm"
    )

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

enriched = []
VALID_LABELS = {"good", "marginal", "bad"}
for i, record in enumerate(records[:24], start=1):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": make_user_message(record)}
        ]
    )

    raw_label = response.choices[0].message.content.strip().lower()

    label = raw_label if raw_label in VALID_LABELS else "unknown"

    enriched.append({
        **record,
        "conditions": label
    })

    if i % 6 == 0:
        print(f"Processed {i} records...")
#print(enriched)

#------Step 3: Write----

# Upload the enriched records (with the new "conditions" field) to processed/<today>/weather_classified.json 
# in Blob Storage. Use overwrite=True.
today = date.today().isoformat()  
processed_path = f"processed/{today}/weather_classified.json"
payload = json.dumps(enriched).encode("utf-8")
container.upload_blob(processed_path, payload, overwrite=True)
print(f"Uploaded {len(payload)} bytes to {processed_path}")

#-----Step 4: Spot-Check--------------------
# Download the processed blob, load it into a pandas DataFrame, and print:

# df["conditions"].value_counts()
# The first 5 rows of the DataFrame
processed_blob = container.download_blob(processed_path).readall()
processed_data = json.loads(processed_blob.decode("utf-8")) 
df = pd.DataFrame(processed_data)   
print(f'conditions value counts:\n{df["conditions"].value_counts()}')
print("\nFirst 5 rows:")
print(df.head())    

#-----Step 5: Save Output------
#Save the first 10 enriched records to outputs/first_10_records.json

output_path = "outputs/first_10_records.json"
output_payload = json.dumps(enriched[:10]).encode("utf-8")  
with open(output_path, "w") as f:
    json.dump(json.loads(raw.decode("utf-8")), f, indent=4)
print(f"Saved first 10 enriched records to {output_path}")

#----Step 6: Reflect-------

#Add a comment block at the top of project_10.py see the top of the page