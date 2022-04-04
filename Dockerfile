FROM ubuntu:latest
FROM python:3.8
WORKDIR /usr/src/myapp
COPY /tasks/requirements.txt ./
COPY /tasks/. /usr/src/myapp
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]
