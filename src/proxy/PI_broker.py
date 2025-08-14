#######
# Prompt Injection Broker
#######

import pika
import json
import logging

class PIBroker:
    """Broker class for managing prompt injection analysis.
    This class is designed to retrieve messages from the user by rabbitMQ
    """

    def __init__(self, model, queue_name='PI_input_queue', host='localhost'):
        self.model = model
        self.queue_name = queue_name
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
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.queue_bind(exchange='PI_exchange', queue=self.queue_name)

            logging.info(f"Connected to RabbitMQ broker at {self.host}")
            logging.info(f"Queue '{self.queue_name}' declared")
            
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def get_messages(self):
        """Retrieve messages from the user."""
        if not self.channel:
            raise RuntimeError("Broker not set up. Call setup_broker() first.")
        
        # Set up consumer
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

        logging.info("Waiting for messages. To exit press CTRL+C")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.close_connection()
        
    def callback(self, ch, method, properties, body):
        try:
            # Decode message
            message = json.loads(body.decode('utf-8'))
            logging.info(f"Received message: {message}")

            # Process message with the model
            # You can add your prompt injection analysis logic here
            

            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
                
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            # Reject message and requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


    def close_connection(self):
        """Close the RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logging.info("RabbitMQ connection closed")

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    model = None  # Replace with your model instance
    broker = PIBroker(model)
    broker.setup_broker()
    broker.get_messages()
    broker.close_connection()