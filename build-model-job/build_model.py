import os
import subprocess
from transformers import CLIPModel, CLIPProcessor

OUTPUT_DIR = "/app/output"
MODEL_DIR = "/app/clip-model-safe"
MAR_EXPORT = "/app/mar-out"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(MAR_EXPORT, exist_ok=True)

print("📥 Downloading CLIP model...")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model.save_pretrained(MODEL_DIR, safe_serialization=True)
processor.save_pretrained(MODEL_DIR)

print("📦 Creating .mar file")
cmd = [
    "torch-model-archiver",
    "--model-name", "clip",
    "--version", "2.0",
    "--serialized-file", f"{MODEL_DIR}/model.safetensors",
    "--handler", "handler.py",
    "--extra-files",
        ",".join([
            f"{MODEL_DIR}/config.json",
            f"{MODEL_DIR}/preprocessor_config.json",
            f"{MODEL_DIR}/tokenizer_config.json",
            f"{MODEL_DIR}/merges.txt",
            f"{MODEL_DIR}/vocab.json",
            f"{MODEL_DIR}/special_tokens_map.json",
        ]),
    "--export-path", MAR_EXPORT,
    "--force"
]

subprocess.run(cmd, check=True)

print("🎉 .mar file created: /app/mar-out/clip.mar")

print("⬆️ Uploading to Google Cloud Storage...")
bucket = os.environ["MODEL_BUCKET"]

subprocess.run([
    "gsutil", "cp", "/app/mar-out/clip.mar", f"gs://{bucket}/clip.mar"
], check=True)

print("✨ Upload completed!")
