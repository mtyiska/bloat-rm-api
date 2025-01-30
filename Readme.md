# **GitHub Release Bloat Analyzer API**

A FastAPI service to analyze the size changes ("bloat") of GitHub repository releases over time by fetching release assets and computing deltas between versions.

## **Setup & Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/mtyiska/bloat-rm-api.git
cd github-bloat-analyzer
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the project root and add:
```
GITHUB_API_BASE=https://api.github.com/repos
```

If you have a GitHub token to bypass rate limits, add:
```
GITHUB_TOKEN=your_personal_access_token
```

### **5. Run the API**
```bash
uvicorn main:app --reload
```

The API will be available at:  
📍 **http://127.0.0.1:8000**

## **Usage**

### **Check Release Size Changes**
Make a `GET` request to:
```
http://127.0.0.1:8000/api/v1/{owner}/{repo}/bloat?start={start_version}&end={end_version}
```

Example:
```bash
curl "http://127.0.0.1:8000/api/v1/apache/airflow/bloat?start=2.8.3&end=2.9.2"
```

### **Swagger API Documentation**
Visit **http://127.0.0.1:8000/docs** for interactive API documentation.

## **Project Structure**
```
/github-bloat-analyzer
│── apis/
│   ├── bloat_controller.py    # API routes
│── utils.py                    # Helper functions
│── config/settings.py          # Configuration
│── main.py                     # App entry point
│── requirements.txt             # Dependencies
│── .env                         # Environment variables (not committed)
│── README.md                    # Project documentation
```

# bloat-api
# bloat-api
# bloat-rm-api
# bloat-rm-api
