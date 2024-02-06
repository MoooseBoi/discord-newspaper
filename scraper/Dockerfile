FROM python:3.12
WORKDIR /app
COPY . .

RUN ls -al

RUN pip install -r requirments.txt

CMD ["python", "-u", "main.py"]
