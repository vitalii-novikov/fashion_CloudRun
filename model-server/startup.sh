#!/bin/bash
set -e

echo "⬇️ Downloading clip.mar from GCS"
gsutil cp gs://$MODEL_BUCKET/clip.mar /home/model-server/model-store/clip.mar

echo "🚀 Starting TorchServe"
torchserve --start --ncs \
  --model-store /home/model-server/model-store \
  --ts-config /home/model-server/config.properties \
  --models clip=clip.mar

