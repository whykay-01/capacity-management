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

Run the following command to build the docker image for the python application only (we will call the image `equipment-dashboard`):

```
docker build -t equipment-dashboard .
```

After building the docker image for the application, let us build the image for the data sources.

To do that, we need to navigate to the `data` folder:

```
cd data
```

Then, we run the following command to build the docker image for the data sources (we will call the image `data-for-the-dashboard`):

```
docker build -v data-for-the-dashboard .
```

Now, that we have created the images for the application and the data sources, we can run the application

```
cd ..
```

then, run the following command to run the docker image

```
docker run equipment-dashboard
```

FIXME: create two separate containers for the application and the data sources, and then connect them together. Use volumes for that.

# Working version
To build from scratch, run the following command in the working directory:

```
docker build -t my-dashboard-app .
```

And then, run the following command to run the docker image (make sure the port matches the one in the `dashboard.py` file):

```
docker run -p 8050:8050 --name dashboard-container my-dashboard-app
```

this command creates the `dashboard-container` container, and runs the `my-dashboard-app` image within the scope of the container.

FIXME: create a container, so that Docker doesn't have to generate the new container from the image every time we run the application.


