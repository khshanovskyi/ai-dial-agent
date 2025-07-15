FROM python:3.11-alpine

WORKDIR /app
COPY * /app
RUN pip install -r requirements.txt

EXPOSE 8010
CMD ["python", "server.py"]
