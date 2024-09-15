FROM python:3.11.6

WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

ENTRYPOINT ["python", "main.py"]