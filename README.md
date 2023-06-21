# Yan's Repo

## Documentation for the pythonProject folder

```
cd pythonProject
```

Docker should be installed on the local machine

after navigating to the working directory (pythonProject), run the following command to build the docker image for the python app

```
docker build -t equipment-dashboard .
```

After building the docker image for the application, let us build the image for the data sources:

```
cd data
```

```
docker build -v data-for-the-dashboard .
```

Now, that we have created the images for the application and the data sources, we can run the application

```
cd ..
```

<!-- ```
docker-compose up
``` -->

then, run the following command to run the docker image

```
docker run equipment-dashboard
```
