# Notes and questions: June 21st, 2023

## What I am trying to do:

So I started with the idea that we will have two separate containers -- one for the python scripts (app itself), and the other one for the data sources.

I have created a folder called `data`, and I have created a Dockerfile inside of that folder for the data sources. I have also created a Dockerfile for the python app in the `pythonProject`.

The challenge I am still facing right now is how to connect two different containers. The goal is to connect the CSV files from the data container to the scripts stored in the python app container.


## What I did so far:

Right now I have tried the following: 

in the pythonProject folder where the Dockerfile for the python app is contained, I run the following command to build the docker image for the python app:

```
docker build -t equipment-dashboard .
```

Then, I navigate to the data folder where the Dockerfile for the data sources is contained, and I run the following command to build the docker image for the data sources:

```
docker build -v data-for-the-dashboard .
```

Then, I navigate back to the pythonProject folder, and I run the following command to run the docker image for the python app:

```
docker run equipment-dashboard
```

I am getting the following error:

```
FileNotFoundError: [Errno 2] No such file or directory: '/data/user_cycle.csv'
```

## Questions:

1. How to make the connection between those two containers, so that the python app can access the data sources?
2. Should I try to start running the data container first, and then the python app? (upd: I have tried that too, didn't work out)

## Notes:

I have slightly modififed the python `dashboard.py` file where the path is '/data' instead of os.getcwd().
