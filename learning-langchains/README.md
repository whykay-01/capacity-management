# Walking through the learning process of adapring `langchain` python package.

First of all, I have to specify that there are 2 different versions of `langchain` package, one is written on python, and the other one is on JS. In this repo, I will be using the python version.

## What is `langchain`?

Langchain is a framework that allows the end-user to interact with a variety of Large Language Models (LLMs) to produce some high-level applications. The framework is designed to be modular, so that the user can easily add new LLMs to the framework. The framework is also designed to be extensible, so that the user can easily add new applications to the framework.

## How am I going to approach the installation of the package and work with it? 

First of all, the package is gigantic, and therefore I suggest to create a virtual environment. 

```
python3 -m venv .venv
```

Once the virtual environment is installed, let's activate it:

```
source .venv/bin/activate
```

Now, let's install the package on our local machine:

NOTE: there are couple of different packages available, and they all server a slighly different purpose. I will be using the `'langchain[all]'` package, which is the main most comprehensive package. To learn more about the different packages, please refer to the [official documentation](https://langchain-langchain.vercel.app/docs/get_started/installation).

NOTE2: the following command will be different for those who are not using `zsh` shell, so please consult the documentation first.

```
pip install 'langchain[all]'
```


