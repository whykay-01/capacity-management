## Quickstart Guide on Dockerizing the Loaning System Dashboard

Before we start, it is important to move to the working directory:

```
cd loaning-system
```

##### NOTE: Docker should be installed on the local machine prior to deploying the application.

### Step 1

Run the following command to build the docker image for the python application only (we will call the image `dashboard-image`):

```bash
docker build -t dashboard-image .
```
### Step 2

We need to create the container for the image. We will use the following command to create the container:

```bash
docker create --name dashboard-with-volume dashboard-image
```
where `dashboard-with-volume` is the name of the container, and `dashboard-image` is the name of the image.

### Step 3

Then, we need to create a volume for the container. We will use the following command to create the volume:

```bash
docker volume create csv-data-volume
```
where `csv-data-volume` is the name of the volume.

Now that we have an empty container, let's put the CSV files with our data inside of it. We will use the following command to copy the CSV files into the container:

```bash
docker compose up -d  --build
```

```bash
docker compose logs -f
```

### Step 4

And then, run the following command to run the docker image (make sure the port matches the one in the `dashboard.py` file):

```bash
docker run -p 8050:8050 --name dashboard-with-volume  dashboard-image
```

this command creates the `dashboard-with-volume ` container, and runs the `dashboard-image` image within the scope of the container.