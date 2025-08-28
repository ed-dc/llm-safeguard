####################
# The cmd Line interface, where the user will comunicate with the model
# Part of the LLM safeguard project
####################

import json
import logging




class CmdUI():
    """
    Main class for CMD line UI

    with methods :
        - setup : set up the interface and get ready to show lines
        - warning : show error with specific message
        - assisant_line : add a line for the assistant
        - user_line : add user line
        - reset : reset all the lines
    """

    def setup(self):
        """
        Method to setup the interface
        """
        print("Welcome to the LLM safeguard project")
        print("Type 'exit' to exit the program")
        print("Type 'reset' to reset the conversation")
        print("Type 'help' to see the help message")
        print("Type your message and press enter to send it")
        print("--------------------------------------------------")

    def warning(self, message):
        """
        Show error with specific message
        """
        print(f"⚠️  WARNING: {message}")

    def assistant_line(self, message):
        """
        Add a line for the assistant
        """
        print(f"🤖 Assistant: {message}\n")

    def reset(self):
        """
        Reset all the lines
        """
        print("\n" * 50)  # Clear screen
        print("Conversation reset!")
        print("--------------------------------------------------")

    def show_help(self):
        """
        Show help message
        """
        print("\nAvailable commands:")
        print("  exit  - Exit the program")
        print("  reset - Reset the conversation")
        print("  help  - Show this help message")
        print("--------------------------------------------------")

    


