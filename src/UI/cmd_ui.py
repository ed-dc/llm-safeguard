####################
# The cmd Line interface, where the user will comunicate with the model
# Part of the LLM safeguard project
####################

import pika
import json
import logging



from UI_broker import UI_broker

class CmdUI():
    """
    Main class for CMD line UI

    with methods :
        - setup : set up the interface and get ready to show lines
        - warning : show error with specific message
        - assisant_line : add a line for the assistant
        - user_line : add user line
    """

    def __init__(self):
        self.broker = UI_broker()
        self.broker.setup_rabbitmq()

    
    def show_interface()