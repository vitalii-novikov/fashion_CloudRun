# 👗 Fashion CLIP Inference System  
A fully containerized, production-ready image embedding & fashion recommendation service powered by **OpenAI CLIP**, **TorchServe**, **FastAPI**, **Streamlit**, **Annoy (Spotify)**, and **Google Cloud Run**.

This project provides an end-to-end pipeline for generating vector embeddings from fashion images using CLIP, storing them in an approximate nearest neighbors index (Annoy), exposing them via an API, and serving results through a frontend UI.  
The system is cloud-native, serverless, fully containerized, and ready for production-scale inference.

---

## 🚀 Features

### 🔍 Image Embedding with CLIP
- Uses **OpenAI CLIP ViT-B/32**  
- Automatically downloads and packages the model  
- Generates a TorchServe-ready `.mar` file using safe serialization (`safetensors`)

### 🧠 ANN Recommendations Using Annoy (Spotify)
- Fast approximate nearest neighbor search  
- Index rebuilt and persisted offline  
- Real-time querying for image similarity  
- Suitable for millions of vectors with minimal memory  
- Cloud Run–friendly: runs purely in-memory without GPU requirements

### 🖥 FastAPI Backend
- Wraps TorchServe predictions  
- Exposes `/predict` or `/recommend` endpoints  
- Loads Annoy index for fast similarity search  
- Returns nearest-neighbor items using CLIP embeddings

### 🎨 Streamlit Frontend
- Image upload  
- API interaction  
- Displays predicted embedding + recommended similar items  
- Minimal, clean UI

### ☁ Cloud-Native Architecture
- Three independent Cloud Run services:
  - `model-server` (TorchServe)
  - `api` (FastAPI + Annoy index)
  - `frontend` (Streamlit)
- Fully serverless  
- Auto-scalable  
- Built with Cloud Build

### 🔧 Simple Model Installation
A standalone script `model_installer.py` downloads CLIP, packages it as `clip.mar`, and places it into:

model-server/model-store/clip.mar

This avoids buckets, gsutil, or any complex tooling.

---

## 🏗 Project Structure

fashion_CloudRun/  
│  
├── model_installer.py            # Downloads CLIP + creates .mar file  
├── build_annoy_index.py          # Builds Annoy similarity index  
├── install_model.ipynb           # Notebook alternative  
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
│   ├── annoy_index.ann            
│  
└── frontend/  
    ├── Dockerfile  
    ├── app.py  
  
---  

## 🔧 Local Setup

### 1. Clone the repository
git clone <your-repo-url>
cd fashion_CloudRun

### 2. Install the CLIP model and create `.mar`
python3 model_installer.py

This generates:
model-server/model-store/clip.mar

## 3. Use your Cloud Run to run the project

---

## 🔄 End-to-End Workflow

1. User uploads an image via Streamlit  
2. Frontend sends the image to FastAPI  
3. FastAPI calls TorchServe to compute CLIP embedding  
4. Annoy index returns similar items instantly  
5. Results displayed to the user  

---

## 🧠 Annoy Recommendation Engine Details

- Uses cosine similarity on CLIP embeddings  
- Persistent `.ann` index file    
- Loads extremely fast on Cloud Run (few MB)  
- Ideal for serverless inference scenarios

---

## ⚙ Recommended Cloud Run Settings

Setting        | Value      
----------------|------------
Memory         | **1–2 GiB** 
CPU            | 1 vCPU     
Concurrency    | **1**      
Min Instances  | 0 or 1     
Max Instances  | 1–3        

TorchServe + CLIP requires >600 MB RAM, so Cloud Run default 512 MiB will fail.

---

## 🛠 Tech Stack

- CLIP ViT-B/32  
- TorchServe  
- FastAPI  
- Streamlit  
- Annoy (Spotify) for recommendations  
- Docker / Cloud Build  
- Google Cloud Run  

---

## 🙌 About

This project demonstrates a fully cloud-native ML inference pipeline, combining CLIP embeddings with an efficient approximate nearest neighbor search system (Annoy) to build real-time image similarity recommendations.  
