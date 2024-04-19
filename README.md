# Streaming Static Data to Kafka

## Overview:

This Python script enables the transformation of static data (CSV or Parquet) into a continuous stream, which is then seamlessly streamed to Kafka. Real-time data processing is facilitated through this process, providing users with the ability to perform analytics, monitoring, and more on streaming data.

## Features:

1. **Easy Configuration:** Users can specify the file path, Kafka topic, and credentials in a JSON configuration file, making it simple to set up and customize the streaming process.
2. **Batch Processing:** The script supports sending data in batches, improving performance and efficiency during transmission to Kafka.
3. **Robust Error Handling:** Comprehensive error handling ensures smooth operation, even in challenging environments, providing reliability and stability to the streaming process.
4. **Detailed Logging:** Extensive logging functionality offers visibility into the streaming process, facilitating troubleshooting, monitoring, and performance optimization.

## Installation:

1. Ensure you have Python installed on your system.
2. Install required dependencies using pip:

```bash
pip install pandas confluent_kafka
```

## Usage:

1. Create a configuration file (`config.json`) based on the provided `config_example.json` template with the following parameters:

- `local_dataset_path`: Path to the local dataset file (CSV or Parquet).
- `topic`: Kafka topic to which data will be streamed.
- `kafka_endpoint`: Kafka bootstrap server endpoint (e.g., hostname:port).
- `kafka_user`: Username for authentication with the Kafka cluster.
- `kafka_pass`: Password for authentication with the Kafka cluster.
- `batch_size` (optional): Number of messages to send in each batch (default is 1000).
- `sleep_time` (optional): Time to sleep between sending each batch (default is 0.01 seconds).

2. Execute the script by running:

```bash
python stream_to_kafka.py config.json
```

## Example Configuration File (`config_example.json`):

```json
{
  "local_dataset_path": "data.csv",
  "topic": "stream-this-dataset",
  "kafka_endpoint": "talented-cow-10356-eu1-kafka.upstash.io:9092",
  "kafka_user": "my_kafka_user",
  "kafka_pass": "my_kafka_password",
  "batch_size": 1000,
  "sleep_time": 0.01
}
```

## Dependencies

- Pandas: For reading CSV and Parquet files.
- confluent_kafka: Python client for interacting with Kafka.

## Note:

Ensure that the Kafka cluster is accessible and configured correctly with the provided credentials. The script is designed to handle both CSV and Parquet file formats for the input dataset. Users can customize batch size and sleep time parameters based on their specific requirements.
