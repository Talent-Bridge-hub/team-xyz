#!/bin/bash
# Startup script for UtopiaHire API
# Ensures proper PYTHONPATH and starts the FastAPI server

cd /home/firas/Utopia
source venv/bin/activate

export PYTHONPATH="/home/firas/Utopia:$PYTHONPATH"

echo "🚀 Starting UtopiaHire API..."
echo "📍 PYTHONPATH: $PYTHONPATH"
echo "🌐 Server will be available at: http://127.0.0.1:8000"
echo "📚 API Docs: http://127.0.0.1:8000/docs"
echo ""

# Start the FastAPI server with uvicorn
cd /home/firas/Utopia/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
