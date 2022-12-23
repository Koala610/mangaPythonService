FROM python:3.9
EXPOSE 8080
COPY ./ ./

RUN pip install -r requirements-prod.txt