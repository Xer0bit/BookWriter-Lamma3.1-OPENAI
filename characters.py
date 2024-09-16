import os
from langchain.document_loaders import PyPDFLoader
from langchain.chains import LLMChain
from langchain_ollama import OllamaLLM  # Import the Ollama LLM

class MainCharacterChain:
    PROMPT = """
    You are provided with a professional profile document. 
    Summarize the person's credentials, background, and expertise in one or two sentences.
    Make sure to capture the most relevant details that align with the subject of the book.

    Profile Document: {text}

    Summary:"""

    def __init__(self) -> None:
        # Initialize the Llama 3.1 model
        self.llm = OllamaLLM(model="llama3.1:latest")
        
        # Create the LLM chain with the defined prompt
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )
        self.chain.verbose = True

    def load_profile(self, file_name):
        folder = './docs'
        file_path = os.path.join(folder, file_name)
        loader = PyPDFLoader(file_path)
        docs = loader.load_and_split()
        return docs

    def run(self, file_name):
        docs = self.load_profile(file_name)
        profile_text = '\n\n'.join([doc.page_content for doc in docs])
        summary = self.chain.predict(text=profile_text)  # Use predict instead of run
        return summary
