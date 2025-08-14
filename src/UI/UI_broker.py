#########
# UI Broker
#########

import pika
import json
import logging


class UI_broker:
    """
    Broker class for managing user interface interactions.
    This class is designed to emit messages to the user via RabbitMQ.
    """

    def __init__(self, queue_name='PI_input_queue', host='localhost'):
        self.queue_name = queue_name
        self.host = host
        self.connection = None
        self.channel = None

    def setup_rabbitmq(self):
        """Set up RabbitMQ connection for emitting messages."""
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.queue_bind(exchange='PI_exchange', queue=self.queue_name)
            logging.info(f"RabbitMQ connection established for UI")
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def emit_message(self, message_content, message_type='user_input'):
        """Emit a message to RabbitMQ broker."""
        if not self.channel:
            self.setup_rabbitmq()
        
        message = {
            'content': message_content,
            'type': message_type,
        }
        
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  
                )
            )
            logging.info(f"Message sent: {message_content}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise

    def close_rabbitmq_connection(self):
        """Close RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logging.info("RabbitMQ connection closed")