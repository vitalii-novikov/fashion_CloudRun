FROM pytorch/torchserve:latest-cpu

RUN pip install --no-cache-dir transformers pillow numpy safetensors google-cloud-storage

WORKDIR /home/model-server

COPY config.properties .
COPY startup.sh .

EXPOSE 8080 8081

ENV MODEL_BUCKET=your-bucket-name

CMD ["bash", "startup.sh"]
