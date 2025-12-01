FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git build-essential

RUN pip install torch torchvision torchaudio transformers pytorch_lightning pillow safetensors torch-model-archiver

COPY build_model.py .
COPY handler.py ./handler.py

CMD ["python", "build_model.py"]
