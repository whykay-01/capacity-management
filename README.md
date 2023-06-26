# Yan's Repo

## Documentation for the pythonProject folder


Before we start, it is important to move to the working directory:

```
cd pythonProject
```

Let's first install the dependencies and create a virtual environment for the python app:

```
python3 -m venv .venv
```

Once the virtual environment is installed, let's activate it:

```
source .venv/bin/activate
```

Now, let's install the dependencies on our local machine:

```
pip install -r requirements.txt
```

##### NOTE: Docker should be installed on the local machine prior to deploying the application.

Run the following command to build the docker image for the python application only (we will call the image `my-dashboard-app`):

```
docker build -t my-dashboard-app .
```

And then, run the following command to run the docker image (make sure the port matches the one in the `dashboard.py` file):

```
docker run -p 8050:8050 --name dashboard-container my-dashboard-app
```

this command creates the `dashboard-container` container, and runs the `my-dashboard-app` image within the scope of the container.

FIXME: create a container, so that Docker doesn't have to generate the new container from the image every time we run the application.


