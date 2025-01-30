# Compliance Policy Checker

Analyzes web content against compliance policies.

## Features
- Automated compliance analysis using Groq's Llama model
- Real-time streaming compliance checks
- Detailed violation reporting with severity levels
- Support for custom compliance policies
- RESTful API with FastAPI backend
- Interactive Streamlit frontend

## Live at
http://13.233.69.2:8501/

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+ (for frontend development)
- Virtual Environment

### Backend Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create logs directory
mkdir -p logs
```

### Environment Variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Running the Application

### Start Backend Server
```bash
# Start Gunicorn server in daemon mode
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8050 app.main:app \
    --daemon \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --pid logs/gunicorn.pid \
    --capture-output \
    --log-level info
```

### Start Frontend
```bash
# Run Streamlit frontend in background
nohup streamlit run frontend.py &
```

## Server Management

### Check Server Status
```bash
# Check if processes are running
ps aux | grep gunicorn
ps aux | grep streamlit

# View logs
tail -f logs/access.log  # Backend access logs
tail -f logs/error.log   # Backend error logs
```

### Stop Servers
```bash
# Stop backend
kill $(cat logs/gunicorn.pid)

# Stop frontend
pkill -f "streamlit run frontend.py"
```

## API Endpoints

### Check Compliance
```bash
POST /check-compliance
Content-Type: application/json

{
    "webpage_url": "https://example.com",
    "policy_url": "https://policy-document-url.com"
}
```

### Health Check
```bash
GET /health
```

## Testing
```bash
# Run test suite
python test_api.py
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[MIT License](LICENSE)

## Support
For support, please open an issue in the repository or contact the development team.