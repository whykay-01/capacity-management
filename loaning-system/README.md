## Quickstart Guide on Dockerizing the Loaning System Dashboard

Before we start, it is important to move to the working directory:

```
cd loaning-system
```

##### NOTE: Docker should be installed on the local machine prior to deploying the application.

Run the following command to build the docker image for the python application only (we will call the image `dashboard-image`):

```
docker build -t dashboard-image .
```

And then, run the following command to run the docker image (make sure the port matches the one in the `dashboard.py` file):

```
docker run -p 8050:8050 --name dashboard-container dashboard-image
```

this command creates the `dashboard-container` container, and runs the `dashboard-image` image within the scope of the container.