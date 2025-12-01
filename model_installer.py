import os
import subprocess
from transformers import CLIPModel, CLIPProcessor

MODEL_NAME = "openai/clip-vit-base-patch32"

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(ROOT_DIR, "clip-model")
EXPORT_DIR = os.path.join(ROOT_DIR, "model-server", "model-store")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

print("📥 Downloading CLIP model:", MODEL_NAME)

model = CLIPModel.from_pretrained(MODEL_NAME)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)

model.save_pretrained(MODEL_DIR, safe_serialization=True)
processor.save_pretrained(MODEL_DIR)

print("📦 Creating clip.mar file...")

cmd = [
    "/home/nvupto/.local/bin/torch-model-archiver",
    "--model-name", "clip",
    "--version", "1.0",
    "--serialized-file", f"{MODEL_DIR}/model.safetensors",
    "--handler", "model-server/handler.py",
    "--extra-files", ",".join([
        f"{MODEL_DIR}/config.json",
        f"{MODEL_DIR}/preprocessor_config.json",
        f"{MODEL_DIR}/tokenizer_config.json",
        f"{MODEL_DIR}/merges.txt",
        f"{MODEL_DIR}/vocab.json",
        f"{MODEL_DIR}/special_tokens_map.json",
    ]),
    "--export-path", EXPORT_DIR,
    "--force",
]

subprocess.run(cmd, check=True)

print("🎉 Successfully created:", os.path.join(EXPORT_DIR, "clip.mar"))
