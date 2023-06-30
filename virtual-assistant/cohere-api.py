import cohere
import dotenv
import os

dotenv.load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# authorize and instantiate the client object
co = cohere.Client(COHERE_API_KEY)


# generate a response based on the input from the command line interface
def response(input):
    response = co.generate(
        model="command",
        prompt=input,
        max_tokens=100,
        temperature=0.9,
        k=0,
        stop_sequences=[],
        return_likelihoods="NONE",
    )
    return response


def print_response(response):
    print("Response: {}".format(response.generations[0].text))


print_response(response("Who are you?\n"))
