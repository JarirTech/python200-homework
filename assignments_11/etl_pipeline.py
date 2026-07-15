#=================Part 2: Project -- Full ETL Pipeline====================================


# video link: https://youtu.be/5u2LOLt85So
from prefect import task, flow
import requests
import json
from datetime import date
from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv
from openai import OpenAI


# =========Step 1: Extract task===================================================================


@task(retries=2, retry_delay_seconds=10)
def extract (latitude: float, longitude: float) -> dict:
    url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={latitude}&longitude={longitude}"
    "&hourly=temperature_2m,precipitation"
    "&forecast_days=7"
)

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print("Data extracted successfully.")
    return data


#=======================================================================================================
#============Step2: Transform task=========================================================================

#Decorated with @task
# Reshapes the "hourly" parallel lists into individual per-hour records
# Classifies the first 24 records (one day) using the OpenAI API with this system prompt:

# Falls back to "unknown" if the model returns an unexpected response
# Prints a progress message every 6 records
# Returns the list of enriched records


# 
load_dotenv()

ACCOUNT_URL = "https://bouchaibctd2026sa.blob.core.windows.net"

CONTAINER = "pipeline-data"

MAX_RECORDS = 24  # one day
SYSTEM_PROMPT = (
    "You are classifying hourly weather conditions for outdoor running."
    "Given a temperature in Celsius and a precipitation amount in mm,"
    "classify the conditions as exactly one of: good, marginal, or bad."
    "Reply with that one word only -- no punctuation, no explanation."
                )
VALID_LABELS = {"good", "marginal", "bad"}

@task
def transform(data: dict, max_records: int)-> list:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    hourly = data["hourly"]

    records = []
    for i in range(min(max_records, len(hourly["time"]))):
        records.append({
            "time": hourly["time"][i],
            "temperature_2m": hourly["temperature_2m"][i],
            "precipitation": hourly["precipitation"][i],
        })

    enriched = []

    for i, record in enumerate(records):
        user_msg = (
            f"Temperature: {record['temperature_2m']}C, "
            f"Precipitation: {record['precipitation']}mm"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ]
        )

        raw_label = response.choices[0].message.content.strip().lower()
        label = raw_label if raw_label in VALID_LABELS else "unknown"

        enriched.append({**record, "conditions": label})

        if (i + 1) % 6 == 0:
            print(f"  Classified {i + 1}/{len(records)} records")

    print(f"Transform complete: {len(enriched)} records enriched")
    return enriched

#=======================================================================================================
#--------step 3: load task---
# Decorated with @task
# Uploads the enriched records as JSON to final/<today>/weather_etl.json in your pipeline-data container
# Uses overwrite=True
# Prints a confirmation with the blob path and byte count
#
# 
@task
def load(records: list, blob_path: str) -> str:
    credential = DefaultAzureCredential()

    container = ContainerClient(
    account_url=ACCOUNT_URL,
    container_name=CONTAINER,
    credential=credential
    )
    

    payload = json.dumps(records).encode("utf-8")

    container.upload_blob(
        blob_path,
        payload,
        overwrite=True
    )

    print(f"Loaded {len(payload)} bytes to {blob_path}")
    return blob_path

#=================================================================

#----------------------Flow-------------------------------------------------
# Decorated with @flow(log_prints=True)
# Calls the three tasks in order
# Prints a completion message with the final blob path

@flow(log_prints=True)
def etl_pipeline(
    latitude: float = 42.3584, longitude: float = -71.0598): #Boston MA
    today = date.today().isoformat()

    blob_path = f"final/{today}/weather_etl.json"

    data = extract(latitude, longitude)

    enriched = transform(
        data,
        max_records=MAX_RECORDS
    )

    final_path = load(enriched, blob_path)
    print(f"Pipeline complete. Results at {final_path}")

if __name__ == "__main__":
    etl_pipeline()
    
      