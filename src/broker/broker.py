##########
# Defining th emodel broker class for other modules to use
#########

import pika
import json
import logging


class Broker:
    """
    This class is designed to be a parent of other broker classes
    """

    def __init__(self, input_queue_name: str, output_queue_name: str, input_exchange: str, output_exchange: str, host='localhost'):
        self.input_queue_name = input_queue_name
        self.output_queue_name = output_queue_name
        self.input_exchange = input_exchange
        self.output_exchange = output_exchange
        self.host = host
        self.connection = None
        self.channel = None
        self.PI_analyzer = None
        
    def setup_broker(self):
        """Set up the broker to retrieve messages from the user."""
        try:
            # Establish connection to RabbitMQ server
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            
            
            # Declare the queue (creates if doesn't exist)
            self.channel.queue_declare(queue=self.input_queue_name, durable=True)
            self.channel.queue_bind(exchange=self.input_exchange, queue=self.input_queue_name)

            self.channel.queue_declare(queue=self.output_queue_name, durable=True)
            self.channel.queue_bind(exchange=self.output_exchange, queue=self.output_queue_name)

            logging.info(f"Connected to RabbitMQ broker at {self.host}")
            logging.info(f"Queue '{self.input_queue_name}' declared")

        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def get_messages(self, callback):
        """Retrieve messages from the user."""
        if not self.channel:
            raise RuntimeError("Broker not set up. Call setup_broker() first.")
        
        # Set up consumer
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.input_queue_name, on_message_callback=callback)

        logging.info("Waiting for messages. To exit press CTRL+C")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.close_connection()
        

    def emit_message(self, message_content, message_type):
        """Emit a message to RabbitMQ broker."""
        if not self.channel:
            self.setup_broker()
        
        message = {
            'content': message_content,
            'type': message_type,
        }
        
        try:
            self.channel.basic_publish(
                exchange=self.output_exchange,
                routing_key=self.output_queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  
                )
            )
            logging.debug(f"Message sent: {message_content}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise


    def close_connection(self):
        """Close the RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logging.info("RabbitMQ connection closed")