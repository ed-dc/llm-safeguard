#########
# MAIN function of the safeguard project
#########


from UI.cmd_ui import CmdUI
from model.base_model import BaseModel
from proxy.PI_analyzer import PIAnalyzer
import logging


class MainSafeguard():
    """
    Main class for the safeguard project
    """
    
    def __init__(self):
        self.ui = CmdUI()
        self.model = BaseModel()
        self.proxy = PIAnalyzer()

    def process_input(self, user_input):
        """
        Process user input through the proxy and model.
        """
        if self.proxy.analyze(user_input) == 1:
            self.ui.warning("Prompt injection detected! Input rejected.")
            return None
        else:
            response = self.model.generate_response(user_input)
            return response


    def run(self):
        """
        Method to run the main function of the safeguard project
        """
        self.ui.setup()
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("Goodbye!")
                    break
                elif user_input.lower() == 'reset':
                    self.ui.reset()
                    continue
                elif user_input.lower() == 'help':
                    self.ui.show_help()
                    continue
                elif user_input == '':
                    continue
                
                #Process input and get response
                response = self.process_input(user_input)
                if response:
                    self.ui.assistant_line(response)
                

            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                self.ui.warning(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("Starting LLM Safeguard Application")
    safeguard_app = MainSafeguard()
    safeguard_app.run()