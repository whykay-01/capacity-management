# Explanation of the Loaning System Dashboard and the Codebase

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

# Quickstart Guide on Dockerizing the Loaning System Dashboard

### NOTE: Please run the follwing commands in the terminal to ensure that you have Docker installed on your system:

```
brew update
brew install docker
```

### NOTE: This is the guide for the Mac users.

Before we start, it is important to move to the working directory:

```
cd loaning-system
```

To deploy, please modify the .env file first. You have to change `ADMIN_ACCESS_TOKEN` to the md5-ed version of your password. To do so, please run the following command in the terminal:

```bash
echo -n "YOUR_PASSWORD" | md5
```

Then copy the hashed version of your password, and run the follwing command:

Create .env file from example.env and change the values

```bash
cp example.env .env
```

Now, set the `ADMIN_ACCESS_TOKEN` to the hashed version of your password which we copied earlier. To do this, run the following command:

```bash
vim .env
```

Or simply open the newly created `.env` file in your favorite text editor and change the value of `ADMIN_ACCESS_TOKEN` to the hashed version of your password.

After the environment variables are set, run the following command to deploy the system:

```bash
docker compose up -d  --build
```

To open the system in the browser, run the following command and click on the suggested localhost link:

```bash
docker compose logs -f
```

# Demo

Click [here](https://drive.google.com/file/d/1UKXMfQVqtk0NGlanh6DNLxfgmebsqEZ0/view?usp=sharing) to see the video demonstration of the system.

# How did I add the image to the server?

1. I have created a Dockerfile in the root directory of the project.

2. I have created a docker image using the following command:

```bash
docker build -t dashboard-image .
```

3. I tagged the image using the following command:

```bash
docker tag dashboard-image whykay01/loaning-system
```

4. I have pushed the image to the docker hub using the following command:

```bash
docker push whykay01/loaning-system
```

# Now to run the files, you have to run the following commands:

```bash
docker pull whykay01/loaning-system
```

```bash
docker run -d -p 8050:8050 -v <YOUR_PATH_TO_THE_DATA_FOLDER>:/data --name dashboard_container whykay01/loaning-system
```

in this example: `/Users/yan/git-repos/capacity-management/loaning-system/data` is the path to my data file, however, you have to change it to your path to the data file.

```bash
docker logs -f dashboard_container
```

```bash
docker stop dashboard_container
```

```bash
docker start dashboard_container
```
