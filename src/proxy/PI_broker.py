#######
# Prompt Injection Broker
#######

import pika
import json
import logging

from src.broker.broker import Broker
from PI_analyzer import PIAnalyzer  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PIBroker(Broker):
    """Broker class for managing prompt injection analysis.
    This class is designed to retrieve messages from the user by rabbitMQ
    """

    def __init__(self, input_queue_name='PI_output_queue', output_queue_name='model_input_queue', host='localhost'):
        """
        Initializing the proxy that interceps messages
        """
        super().__init__(input_queue_name, output_queue_name, 'PI_output_exchange', 'model_input_exchange', host)
        self.PI_analyzer = PIAnalyzer() 

    def callback(self, ch, method, properties, body):
        try:
            # Decode message
            message = json.loads(body.decode('utf-8'))
            logger.info(f"Received message: {message}")

            # Process message with the model
            input_text = message.get('content', '')
            if not input_text:
                logger.warning("Received empty input text. Skipping processing.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            safe_val = self.PI_analyzer.analyze(input_text)

            if safe_val:
                self.emit_message("prompt injection detected","PI_detected")
            
            else:
                self.emit_message(input_text, "PI_safe ")
            logger.info(f"Analyzed : {safe_val}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Reject message and requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)   

    def close_connection(self):
        """Close the RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")
    

if __name__ == "__main__":
    # Example usage
    broker = PIBroker()
    broker.setup_broker()
    broker.get_messages(broker.callback)
    broker.close_connection()