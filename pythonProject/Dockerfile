FROM python:3.9

WORKDIR /pythonProject

ADD dashboard.py .
ADD database.py .
ADD database_connection.py .

# installing the requirements for the python environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./dashboard.py"]