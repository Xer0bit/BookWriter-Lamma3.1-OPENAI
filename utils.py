from langchain.chains import LLMChain
from langchain_ollama import OllamaLLM  # Import the Ollama LLM
import os

class BaseStructureChain:
    """
    A base class for creating LLM chains that generate different parts of the book's structure,
    such as the title, outline, and chapters.
    """
    PROMPT = ''

    def __init__(self) -> None:
        # Initialize the Llama 3.1 model
        self.llm = OllamaLLM(model="phi3:latest")

        # Create an LLMChain instance using the provided prompt template
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )
        self.chain.verbose = True

    def run(self, **kwargs):
        # Required keys that must be passed to the chain
        required_keys = {'subject', 'genre', 'author_description', 'profile', 'title', 'plot', 'chapter'}
        missing_keys = required_keys - kwargs.keys()

        # Raise an error if any required keys are missing
        if missing_keys:
            raise ValueError(f"Missing some input keys: {missing_keys}")

        return self.chain.predict(**kwargs)

class BaseEventChain:
    """
    A base class for creating LLM chains that generate content related to the book's events,
    such as key points, chapter content, and writing paragraphs.
    """
    PROMPT = ''

    def __init__(self) -> None:
        # Initialize the Llama 3.1 model
        self.llm = OllamaLLM(model="llama3.1:latest")

        # Create an LLMChain instance using the provided prompt template
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT,
        )
        self.chain.verbose = True

    def run(self, **kwargs):
        # Required keys that must be passed to the chain
        required_keys = {'subject', 'genre', 'author_description', 'profile', 'title', 'plot', 'summary', 'current_event'}
        missing_keys = required_keys - kwargs.keys()

        # Raise an error if any required keys are missing
        if missing_keys:
            raise ValueError(f"Missing some input keys: {missing_keys}")

        return self.chain.predict(**kwargs)
