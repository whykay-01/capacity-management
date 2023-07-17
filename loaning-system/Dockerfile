FROM python:3.11

# adding the python script
ADD dashboard.py .
ADD app/ ./app
ADD templates/ ./templates
# installing dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
# exposing the port we need
EXPOSE 8050
CMD ["python", "./dashboard.py"]