FROM python:3.8
WORKDIR /usr/src/myapp
COPY requirements.txt ./
COPY . /usr/src/myapp
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]
