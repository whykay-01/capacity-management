FROM python:3.9

WORKDIR /code
# adding the python script
ADD dashboard.py .
# TODO: technically we dont even need database and database_connection files
ADD database.py .
ADD database_connection.py .
# adding data files
ADD equipment_cycle.csv .
ADD non_unique_user_equipment.csv .
ADD unique_user_equipment.csv .
ADD test.csv .
ADD user_cycle.csv .
# installing the requirements for the python environment
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# COPY ./app /code/app
# COPY ./data /code/data
CMD ["python", "./dashboard.py"]