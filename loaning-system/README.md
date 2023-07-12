## Explanation of the Loaning System Dashboard and the Codebase

To start deploying the system, one has to understand the codebase and the structure of the system. The system is divided into multiple parts. Before we dive into the codebase, I want to empathize that the system is built using the following technologies:

1. Flask for the backend -- API referencing
2. Simple bootstrap templates for the frontend -- HTML, CSS, and JS (CSS and JS part are rather small chuncks of code embedded in the HTML files)
3. Python for the backend -- data processing and data visualization, namely the `pandas` and `plotly` libraries.

- Q: What is different in this project from the previous dashboard?

The previous dashboard was built using the `dash` library, which is a python library for building interactive dashboards. However, the `dash` library is not compatible with the `flask` library. Therefore, I had to build a separate flask application for the dashboard. The `flask` application is located in the `app` folder.

I have completely restructured and decomposed the codebase. Previous code was a mess contained in one function in the `dashboard.py` file, therefore it was hard to maintain. I have decomposed the codebase into multiple files and folders. The main file which connects everything is still the `dashboard.py` file. However, the code is now more readable and maintainable as it is rather a collection of functions inside of modules.

In additional to the "invisible difference," I have added the following features to the dashboard:

1. The dashboard is now responsive to the screen size. It is now possible to view the dashboard even on mobile devices if required.
2. There is a user interface for the file upload.
3. The file upload system is excessively robust, as it allows you not only to upload the file, but also generates all the other intermediary files required for the dashboard to work properly.

## Quickstart Guide on Dockerizing the Loaning System Dashboard

##### NOTE: Docker should be installed on the local machine prior to deploying the application.

Before we start, it is important to move to the working directory:

```
cd loaning-system
```

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
