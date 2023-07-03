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

Then, we need to create a volume mounted to the container. We will use the following command to start the process:

```bash
docker compose up -d  --build
```

To open the system in the browser, run the following command and click on the suggested localhost link:

```bash
docker compose logs -f
```