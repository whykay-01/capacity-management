from langchain.llms import Cohere
import dotenv
import os

dotenv.load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

cohere = Cohere(model="command", cohere_api_key=COHERE_API_KEY)
response = cohere("Tell me a joke.")
print(response)
