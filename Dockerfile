FROM python:3.7.5-alpine
WORKDIR /usr/src/upload
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY .env .env
COPY upload.py upload.py
CMD [ "python", "-u", "./upload.py" ]
