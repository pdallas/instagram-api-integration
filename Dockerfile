FROM python:3
WORKDIR /app
ADD app /app
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python3","-u","app.py"]