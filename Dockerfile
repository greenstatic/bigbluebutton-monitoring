FROM python:3.7-stretch
EXPOSE 5000

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["bbb-mon/server.py"]