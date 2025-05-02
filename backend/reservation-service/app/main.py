from . import create_app
from .kafka_handler import start_kafka_consumer
import threading
import sys
import traceback
import logging
import os
from waitress import serve

# Configurer le logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = create_app()

# Lancer le consommateur Kafka dans un thread séparé
logger.info("Starting Kafka consumer thread...")
try:
    kafka_thread = threading.Thread(target=start_kafka_consumer)
    kafka_thread.daemon = True
    kafka_thread.start()
except Exception as e:
    logger.error(f"Failed to start Kafka consumer thread: {e}")
    traceback.print_exc(file=sys.stdout)

if __name__ == '__main__':
    # Vérifier si on est en mode développement ou production
    if os.getenv('FLASK_ENV') == 'development':
        logger.info("Running in development mode with Flask debug server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.info("Running in production mode with Waitress...")
        serve(app, host='0.0.0.0', port=5000, threads=4)