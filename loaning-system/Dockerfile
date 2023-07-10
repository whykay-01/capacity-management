FROM python:3.9

WORKDIR /application
# adding the python script
ADD dashboard.py .
ADD app/ ./app
ADD templates/ ./templates
# installing dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python", "./dashboard.py"]