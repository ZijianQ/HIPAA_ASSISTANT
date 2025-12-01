FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install streamlit ollama

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
