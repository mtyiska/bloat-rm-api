
# **GitHub Release Bloat Analyzer API**

A FastAPI service that analyzes GitHub repository release sizes over time by fetching release assets and computing deltas between versions.

---

## **🚀 Run Locally**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/mtyiska/bloat-rm-api.git
cd bloat-rm-api
```

### **2️⃣ Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the API**
```bash
uvicorn main:app --reload
```

The API will be available at:  
📍 **http://127.0.0.1:8000**

📌 **API Docs**: Open **http://127.0.0.1:8000/docs** in your browser.

---

## **🐳 Run with Docker**

### **1️⃣ Pull the Docker Image**
```bash
docker pull ghcr.io/mtyiska/fastapi-bloat-api:0.0.3
```

### **2️⃣ Run the Container**
```bash
docker run -d -p 8000:8000 ghcr.io/mtyiska/fastapi-bloat-api:0.0.3
```

📌 **Access the API**:  
🔗 **http://localhost:8000/docs** → Swagger API Documentation

---


> ⚠️ **Mac M1/M2 Users:** If you're on an Apple Silicon (ARM) machine, use the `--platform linux/amd64` flag to ensure compatibility.

```bash
docker run --platform linux/amd64 -d -p 8000:8000 ghcr.io/mtyiska/fastapi-bloat-api:0.0.3
```

#### **Verify the Container is Running**

Check running containers:

```bash
docker ps
```

You should see your `fastapi-bloat-api` container running.

#### **Test the API**


```bash
curl http://localhost:8000/docs
```

Or open your browser and visit:

🔗 **[http://localhost:8000/docs](http://localhost:8000/docs)** → This will display the **FastAPI interactive Swagger UI**.

#### **Stop & Remove the Container (Optional)**

If you want to stop the running container:

```bash
docker stop <container_id>
```

To remove the container:

```bash
docker rm <container_id>
```
