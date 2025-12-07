# 👗 Fashion CLIP Inference System  
A fully containerized, production-ready image embedding & fashion recommendation service powered by **OpenAI CLIP**, **TorchServe**, **FastAPI**, **Streamlit**, and **Google Cloud Run**.

This project provides an end-to-end pipeline for generating vector embeddings from fashion images using CLIP, wrapping them into an API, and serving them via a lightweight frontend. Everything is designed for cloud-native, scalable, serverless deployment.

---

## 🚀 Features

### 🔍 Image Embedding with CLIP
- Uses **OpenAI CLIP ViT-B/32**  
- Automatically downloads and packages the model  
- Generates a TorchServe-ready `.mar` file using safe serialization (`safetensors`)

### 🖥 FastAPI Backend
- Wraps TorchServe predictions into a clean REST API  
- Environment-configurable (local & Cloud Run)

### 🎨 Streamlit Frontend
- User uploads an image  
- Calls the API to generate embeddings  
- Fully Cloud Run–compatible  

### ☁ Cloud-Native Architecture
- Each service runs independently on **Google Cloud Run**  
- Auto-scalable serverless deployment  
- Built via `gcloud builds submit`

### 🔧 Simple Model Installation
A standalone script `model_installer.py` downloads the CLIP model, exports it as `clip.mar`, and saves it directly into:

model-server/model-store/clip.mar

No buckets, no gsutil, no startup scripts.

---

## 🏗 Project Structure

fashion_CloudRun/
│
├── model_installer.py        # Downloads CLIP + creates .mar file
├── install_model.ipynb       # Jupyter notebook alternative
├── README.md
│
├── model-server/
│   ├── Dockerfile
│   ├── handler.py
│   ├── config.properties
│   └── model-store/
│       └── clip.mar
│
├── api/
│   ├── Dockerfile
│   ├── main.py
│   └── ...
│
└── frontend/
    ├── Dockerfile
    ├── app.py
    └── ...

---

## 🔧 Local Setup

### 1. Clone the repository
git clone <your-repo-url>
cd fashion_CloudRun

### 2. Install the CLIP model and create `.mar`
python3 model_installer.py

This generates:
model-server/model-store/clip.mar

---

## 🐳 Build Docker Images via Cloud Build

### Build model server (TorchServe)
gcloud builds submit model-server --tag gcr.io/$GOOGLE_CLOUD_PROJECT/model-server

### Build API
gcloud builds submit api --tag gcr.io/$GOOGLE_CLOUD_PROJECT/api

### Build frontend
gcloud builds submit frontend --tag gcr.io/$GOOGLE_CLOUD_PROJECT/frontend

---

## ☁️ Deploy to Google Cloud Run

### 1. Deploy TorchServe model server
gcloud run deploy model-server \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/model-server \
  --memory=2Gi \
  --concurrency=1 \
  --allow-unauthenticated \
  --region=europe-west3

### 2. Deploy API
gcloud run deploy api \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/api \
  --set-env-vars TORCHSERVE_URL=https://<model-server-url>/predictions/clip \
  --allow-unauthenticated \
  --region=europe-west3

### 3. Deploy frontend
gcloud run deploy frontend \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/frontend \
  --set-env-vars API_URL=https://<api-url> \
  --allow-unauthenticated \
  --region=europe-west3

---

## 🌐 Environment Variables

Each component supports a `.env` file:

TORCHSERVE_URL=https://model-server-xxxxx.run.app/predictions/clip
API_URL=https://api-xxxxx.run.app

---

## 🔄 End-to-End Workflow

1. User uploads an image via Streamlit  
2. Frontend sends the image to FastAPI  
3. FastAPI forwards the request to TorchServe  
4. TorchServe runs CLIP ViT-B/32 and returns embeddings  
5. Frontend displays results  

---

## 🧪 Testing the model server manually

curl -X POST \
  -F "data=@test.jpg" \
  https://model-server-xxxxx.run.app/predictions/clip

---

## ⚙ Recommended Cloud Run Settings

Setting        | Value      
----------------|------------
Memory         | **1–2 GiB** 
CPU            | 1 vCPU     
Concurrency    | **1**      
Min Instances  | 0 or 1     
Max Instances  | 1–3        

TorchServe + CLIP requires >600 MB RAM.  
Cloud Run default 512 MiB will fail.

---

## 🛠 Tech Stack

- CLIP ViT-B/32  
- TorchServe  
- FastAPI  
- Streamlit  
- Docker / Cloud Build  
- Google Cloud Run  

---

## 🙌 About

This project demonstrates a complete cloud-native ML inference pipeline, including model packaging, scalable architecture, REST API serving, and frontend integration. Designed as a portfolio-grade example of deploying modern ML models in production.
