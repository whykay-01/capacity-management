from langchain import Cohere
import dotenv
import os

dotenv.load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# cohere = Cohere(model="gptd-instruct-tft", cohere_api_key=COHERE_API_KEY)

# response = cohere.generate("Hello, my name is Yan")
# print(response)

import cohere

co = cohere.Client(COHERE_API_KEY)
response = co.generate(
    model="command",
    prompt=input("Please enter a prompt: ") + "\n",
    max_tokens=100,
    temperature=0.9,
    k=0,
    stop_sequences=[],
    return_likelihoods="NONE",
)
print("Response: {}".format(response.generations[0].text))
