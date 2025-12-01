FROM pytorch/torchserve:latest-cpu

RUN pip install --no-cache-dir transformers pillow numpy safetensors

WORKDIR /home/model-server

COPY config.properties .
COPY handler.py .
COPY model-store/ model-store/

EXPOSE 8080 8081

# Start TorchServe normally
CMD ["torchserve", "--start", "--model-store", "model-store", "--models", "clip.mar"]
