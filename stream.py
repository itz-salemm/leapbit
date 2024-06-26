import pandas as pd
import sys
import time
import logging
import json
from confluent_kafka import Producer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        sys.exit(1)

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def stream_to_kafka(config):
    try:
        local_dataset_path = config["local_dataset_path"]
        topic = config["topic"]
        kafka_endpoint = config["kafka_endpoint"]
        kafka_user = config["kafka_user"]
        kafka_pass = config["kafka_pass"]
        batch_size = config.get("batch_size", 1000)
        sleep_time = config.get("sleep_time", 0.01)

        # Confluent Kafka producer configuration
        conf = {
            'bootstrap.servers': kafka_endpoint,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanism': 'PLAIN',
            'sasl.username': kafka_user,
            'sasl.password': kafka_pass
        }

        producer = Producer(**conf)

        # Read the local dataset
        if local_dataset_path.endswith('.csv'):
            data = pd.read_csv(local_dataset_path)
            logger.info("CSV file loaded.")
        elif local_dataset_path.endswith('.parquet'):
            data = pd.read_parquet(local_dataset_path)
            logger.info("Parquet file loaded.")
        else:
            raise ValueError("Unsupported file format. Only CSV and Parquet files are supported.")

        # Start timer
        start = time.time()

        # Send data in batches
        for i in range(0, len(data), batch_size):
            batch_data = data.iloc[i:i + batch_size]
            for index, row in batch_data.iterrows():
                message = row.to_json().encode("utf-8")
                producer.produce(topic, message, callback=delivery_report)
            producer.flush()  # Ensure all messages are sent
            time.sleep(sleep_time)

        # End timer
        end = time.time()
        elapsed = end - start

        logger.info("Data sent to Kafka cluster")
        logger.info(f"It took {round(elapsed, 2)} seconds to stream this dataset containing {len(data)} rows")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        producer.flush()  # Ensure all messages are sent before closing


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python stream.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    config = load_config(config_file)
    stream_to_kafka(config)
