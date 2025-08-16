#########
# Proxy for PI (Prompt injection) analysis
#########


from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



class PIAnalyzer:
    """Proxy class for analyzing prompt injections in a model.
    This class is designed to interface with a model to
    analyze and detect prompt injections. It provides a method to
    analyze a given prompt and return the results of the analysis.
    """

    def __init__(self):
        """
        Initializing the model, taking an open source model from hugging face
        """
        tokenizer = AutoTokenizer.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")
        model = AutoModelForSequenceClassification.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")
        self.model = pipeline(
                        "text-classification",
                        model=model,
                        tokenizer=tokenizer,
                        truncation=True,
                        max_length=512,
                        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
                        )
    
    def analyze(self,prompt :str):
        """
        Method to analyze a specific prompt
        return 0 or 1:
        0 for no injection and 1 for injection detected.
        """
        
        if type(prompt) != str:
            raise TypeError(f"Prompt should be an str not a {type(prompt)}")

        result = self.model(prompt)
        injection_type = result[0]["label"]
        logger.info(f"Result from analyze is : {injection_type}")
        if injection_type == "SAFE":
            return 0
        return 1

# if __name__ == "__main__":
#     analyzer = PIAnalyzer()
#     print(analyzer.analyze("I love cats"))

    
