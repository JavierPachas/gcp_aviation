# Real-Time Flight Data Pipeline on GCP

An event-driven streaming data pipeline that ingests real-time flight data from the [AviationStack API](https://aviationstack.com/dashboard) into BigQuery using Google Cloud Pub/Sub and Cloud Functions.

## Architecture

```
┌──────────────────┐      ┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│  AviationStack   │ ───▶ │  Publisher   │ ───▶ │   Pub/Sub       │ ───▶ │    Cloud     │
│      API         │      │  (Notebook)  │      │     Topic       │      │   Function   │
└──────────────────┘      └──────────────┘      └─────────────────┘      └──────┬───────┘
                                                                                 │
                                                                                 ▼
                                                                         ┌──────────────┐
                                                                         │   BigQuery   │
                                                                         │    Table     │
                                                                         └──────────────┘
```

**Flow:**
1. A publisher script (`aviationstack_extract_data.ipynb`) fetches real-time flight data from the AviationStack API.
2. Each flight record is published as a message to a Pub/Sub topic.
3. A Cloud Function (`main.py`) subscribes to the topic, decodes the message, and streams it into BigQuery.

## Tech Stack

- **Cloud Provider:** Google Cloud Platform (GCP)
- **Messaging:** Cloud Pub/Sub
- **Compute:** Cloud Functions (Python, Pub/Sub-triggered)
- **Data Warehouse:** BigQuery
- **Data Source:** [AviationStack API](https://aviationstack.com/)
- **Language:** Python 3

## Repository Structure

```
gcp_aviation/
├── aviationstack_extract_data.ipynb   # Publisher: fetches API data & publishes to Pub/Sub
├── main.py                            # Cloud Function: subscribes & writes to BigQuery
├── requirements.txt                   # Cloud Function dependencies
└── README.md
```

## Prerequisites

- A Google Cloud project with billing enabled
- The following GCP APIs enabled:
  - Cloud Pub/Sub API
  - Cloud Functions API
  - BigQuery API
- An [AviationStack API key](https://aviationstack.com/dashboard) (free tier available)
- `gcloud` CLI installed and authenticated

## Setup

### 1. Create the Pub/Sub topic

```bash
gcloud pubsub topics create flights-topic
```

### 2. Create the BigQuery dataset and table

```bash
bq mk --dataset your_project_id:aviation_data
bq mk --table your_project_id:aviation_data.flights \
  flight_date:STRING,flight_status:STRING,departure_airport:STRING,arrival_airport:STRING,airline_name:STRING,flight_number:STRING
```

> Adjust the schema to match the fields you extract from the AviationStack response.

### 3. Deploy the Cloud Function

```bash
gcloud functions deploy flights-ingest \
  --runtime python39 \
  --trigger-topic flights-topic \
  --entry-point hello_pubsub \
  --source .
```

### 4. Run the publisher

Open `aviationstack_extract_data.ipynb` in Jupyter or Colab, set your API key and GCP project ID, and execute the cells to start publishing flight data.

## How It Works

**Publisher (`aviationstack_extract_data.ipynb`):**
- Calls the AviationStack API endpoint to retrieve real-time flight data
- Parses and structures each flight record
- Publishes messages to the Pub/Sub topic using the `google-cloud-pubsub` client

**Subscriber (`main.py`):**
- Triggered automatically when a new message arrives on the Pub/Sub topic
- Decodes the base64-encoded message payload
- Parses the JSON and streams the row into BigQuery using `insert_rows_json`

## Use Cases

This architectural pattern generalizes well beyond flight data to any use case that requires:
- Real-time ingestion from a third-party REST API
- Decoupled, event-driven processing
- Auto-scaling compute without managing servers
- Analytics-ready storage in a data warehouse

## Notes

- The BigQuery write logic in `main.py` is currently commented out for demo purposes. Uncomment and update `table_id` before deploying to production.
- Be mindful of AviationStack free-tier rate limits (100 requests/month on the free plan).
- Consider adding dead-letter topic configuration for failed message handling in production.

## Possible Extensions

- Add **Cloud Scheduler** to trigger the publisher on a fixed interval (e.g., every 5 minutes)
- Build a **Looker Studio** dashboard on top of the BigQuery table for live flight monitoring
- Add **dbt** transformations to clean and model the raw flight data
- Implement **schema validation** with Pydantic before publishing
- Migrate the publisher to a **Cloud Run** service for full serverless orchestration

## Author

Maintained by [Javier Pachas](https://github.com/JavierPachas).

## License

MIT
