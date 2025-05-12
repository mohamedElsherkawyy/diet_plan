FROM python:3.11

RUN apt-get update && apt-get install -y git-lfs
WORKDIR /app
COPY . .
RUN git lfs install && git lfs pull
RUN pip install -r requirements.txt

CMD ["python", "main.py"]