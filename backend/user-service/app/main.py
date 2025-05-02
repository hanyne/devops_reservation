from app import create_app
from waitress import serve
from app.kafka_consumer import start_kafka_consumer

app = create_app()

# Démarrer le consommateur Kafka
start_kafka_consumer()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)