FROM python:3.9

WORKDIR /application
# adding the python script
ADD dashboard.py .
ADD application/ ./application
# installing dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# add the volume called csv-data-volume
# VOLUME ["/csv-data-volume/data"]

CMD ["python", "./dashboard.py"]