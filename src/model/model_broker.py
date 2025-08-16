##########
# The broker for the model, which is used to retrieve messages from the user.
# This file is part of LLM Safeguard.
##########

import pika
import logging
import json
import os, sys
from base_model import BaseModel
from src.broker.broker import Broker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelBroker(Broker):
    """
    Broker class for managing model interactions.
    This class is designed to retrieve messages from the user and interact with the model.
    """
    
    def __init__(self, input_queue_name='model_input_queue', output_queue_name='PI_input_queue', host='localhost'):
        super().__init__(input_queue_name, output_queue_name, 'model_input_exchange', 'PI_input_exchange', host)
        self.model = BaseModel()

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

            response = self.model.generate_response(input_text)
            logger.info(f"Generated response: {response}")

            # Send the response back to the user
            response_message = {
                'content': response,
                'type': 'model_response',
            }
            self.emit_message(response_message, message_type='model_response')
            logger.info("Response sent to user.")
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Reject message and requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

if __name__ == "__main__":
    # Example usage
    broker = ModelBroker()
    broker.setup_broker()
    logger.info("Model Broker is ready to receive messages.")
    
    # Start consuming messages
    try:
        broker.get_messages(broker.callback)
    except KeyboardInterrupt:
        logger.info("Model Broker stopped by user.")
        broker.close_connection()
