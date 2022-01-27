FROM python:3.9-slim-buster

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /app/
RUN cd /app && pip install -e .

WORKDIR /app/jj
#ENTRYPOINT ["python3","uploader.py"]
ENTRYPOINT ["./jj.py"]
