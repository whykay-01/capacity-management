# Walking through the learning process of adapring `langchain` python package.

First of all, I have to specify that there are 2 different versions of `langchain` package, one is written on python, and the other one is on JS. In this repo, I will be using the python version.

#### What is `langchain`?

Langchain is a framework that allows the end-user to interact with a variety of Large Language Models (LLMs) to produce some high-level applications. The framework is designed to be modular, so that the user can easily add new LLMs to the framework. The framework is also designed to be extensible, so that the user can easily add new applications to the framework.

#### How am I going to approach the installation of the package and work with it?

First of all, the package is gigantic, and therefore I suggest to create a virtual environment.

```
python3 -m venv venv
```

Once the virtual environment is installed, let's activate it:

```
source venv/bin/activate
```

Now, let's install the package on our local machine:

- NOTE: there are couple of different packages available, and they all server a slighly different purpose. I will be using the `'langchain[all]'` package, which is the main most comprehensive package. To learn more about the different packages, please refer to the [official documentation](https://langchain-langchain.vercel.app/docs/get_started/installation).

- NOTE2: the following command will be different for those who are not using `zsh` shell, so please consult the documentation first.

```
pip install 'langchain[all]' --use-pep517
```

Side notes:

In this repo I am focusing on the creation of the [agents](https://langchain-langchain.vercel.app/docs/modules/agents/) and exploring how does the storage unit works within the scope of language chains. Viable plan for today would be:

1. Create a simple agent that will be able to interact with the storage unit.
2. Create a simple storage unit that will be able to store the data.
3. Report back on the progress and then start working on specific tasks.

Side notes p.2:

1. All the functions and classes are available in [github repo](https://github.com/hwchase17/langchain/blob/master/langchain/), so I will be using them as a reference point. All the classes available for the functionality are also available there.

# IMPORTANT

pip uninstall langflow

# RESOURCES

https://github.com/scrapy/scrapy?ref=blog.apify.com
https://docs.scrapy.org/en/latest/intro/tutorial.html

# RESOURCES

| #   | Name/desc of the source                                                                                                                                                              |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | [How to use Redis DB for embeddings](https://community.openai.com/t/using-redis-for-embeddings/23517)                                                                                |
| 2   | [Langchain tutorial](https://www.youtube.com/watch?v=au2WVVGUvc8&ab_channel=LiamOttley)                                                                                              |
| 3   | [Embeddings with Hugging Face](https://github.com/ToxyBorg/Hugging-Face-Hub-Langchain-Document-Embeddings)                                                                           |
| 4   | [Using HuggingFace, OpenAI, and Cohere models with Langchain](https://medium.com/the-techlife/using-huggingface-openai-and-cohere-models-with-langchain-db57af14ac5b)                |
| 5   | [Redis Docs](https://redis.io/docs/about/)                                                                                                                                           |
| 6   | [More on preprocessing data before embeddings](https://www.kaggle.com/code/christofhenkel/how-to-preprocessing-when-using-embeddings)                                                |
| 7   | [Sample work](https://github.com/HaxyMoly/Vicuna-LangChain/)                                                                                                                         |
| 8   | [Sample work2](https://developer.mozilla.org/en-US/blog/introducing-ai-help/)                                                                                                        |
| 9   | [Medable](https://www.mendable.ai/pricing)                                                                                                                                           |
| 10  | [Building search engines](https://dev.to/mage_ai/how-to-build-a-search-engine-with-word-embeddings-56jd)                                                                             |
| 11  | [Codebase for the semantic search](https://github.com/czhu12/semantic-search/blob/master/search.py)                                                                                  |
| 12  | [Build a Personal Search Engine Web App using Open AI Text Embeddings](https://medium.com/@avra42/build-a-personal-search-engine-web-app-using-open-ai-text-embeddings-d6541f32892d) |
| 13  | [Harnessing the Falcon 40B Model, the Most Powerful Open-Source LLM](https://towardsdatascience.com/harnessing-the-falcon-40b-model-the-most-powerful-open-source-llm-f70010bc8a10)  |
