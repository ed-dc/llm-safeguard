############
# The model class for the LLM safeguard project
# This class is designed to be the base model for the LLM safeguard project.
# It provides methods to interact with the model and perform various operations.
############


import sys, os
import logging
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Env variable 
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'openai/gpt-oss-20b')
if not NVIDIA_API_KEY:
    logging.error("NVIDIA_API_KEY environment variable is not set.")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

##  Way to choose wich model to use
# available_models = [model for model in ChatNVIDIA.get_available_models() 
#      if ("mistral" in model.id or "meta/llama" in model.id) 
#          and model.model_type in ('chat', None)]

# print(f"Available models: {[model.id for model in available_models]}")



class BaseModel:
    """
    Base class for the LLM safeguard project model.
    
    """

    def __init__(self):
        self.model = ChatNVIDIA(
            model=MODEL_NAME,  
            api_key=NVIDIA_API_KEY)
        self.output_parser = StrOutputParser()
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. You try your best to answer the user's questions."),
                ("user", "{input}"),
            ]
        )
        self.chain = self.prompt_template | self.model | self.output_parser
    
    def generate_response(self, input_text):
        """
        Generate a response from the model based on the input text.
        
        Args:
            input_text (str): The input text to generate a response for.
        
        Returns:
            str: The generated response from the model.
        """
        try:
            logging.debug(f"Generating response for input: {input_text}")
            if not input_text:
                logging.warning("Input text is empty. Returning default response.")
                return "Please provide a valid input."
            inst_out = ""
            chat_gen = self.chain.stream({"input": input_text})

            for token in chat_gen:
                inst_out += token
            return inst_out
        
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "An error occurred while generating the response."
        

# if __name__ == "__main__":
    
#     # I choose a mistral model
#     model = ChatNVIDIA(
#         model='openai/gpt-oss-20b',
#         api_key=NVIDIA_API_KEY)

#     model_instance = BaseModel(model)
#     input_text = "What is the capital of France?"
#     response = model_instance.generate_response(input_text)
#     print(f"Response: {response}")