import base64
import functions_framework
import json
from google.cloud import bigquery

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    print(base64.b64decode(cloud_event.data["message"]["data"]))
    pubsub_message = base64.b64decode(cloud_event.data['message']['data']).decode('utf-8')
    print(pubsub_message)
    print(type(pubsub_message))
    data_json = json.loads(pubsub_message)
    print(data_json)
     #client = bigquery.Client()
     #table_id = "course-big-data-336218.curso_bigdata.vuelos"
     #errors = client.insert_rows_json(table_id, data_json)
     #if errors == []:
     #     print("New rows have been added.")
     #else:
     #     print("Encountered errors while inserting rows: {}".format(errors))



