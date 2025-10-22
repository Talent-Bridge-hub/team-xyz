#!/bin/bash
# UtopiaHire - Install Missing Dependencies
# Run this script to install all required packages

echo "=========================================="
echo "UtopiaHire - Dependency Installation"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: Please run this script from the Utopia root directory"
    exit 1
fi

echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python packages installed successfully"
else
    echo "❌ Failed to install Python packages"
    exit 1
fi

echo ""
echo "📥 Downloading NLTK data..."
python -c "
import nltk
print('Downloading punkt tokenizer...')
nltk.download('punkt', quiet=True)
print('✅ punkt downloaded')

print('Downloading stopwords...')
nltk.download('stopwords', quiet=True)
print('✅ stopwords downloaded')

print('Downloading averaged_perceptron_tagger...')
nltk.download('averaged_perceptron_tagger', quiet=True)
print('✅ averaged_perceptron_tagger downloaded')
"

if [ $? -eq 0 ]; then
    echo "✅ NLTK data downloaded successfully"
else
    echo "⚠️  Warning: NLTK data download may have issues"
fi

echo ""
echo "🧪 Testing imports..."
python -c "
try:
    import PyPDF2
    print('✅ PyPDF2')
except ImportError:
    print('❌ PyPDF2 - FAILED')

try:
    from docx import Document
    print('✅ python-docx')
except ImportError:
    print('❌ python-docx - FAILED')

try:
    from reportlab.lib.pagesizes import letter
    print('✅ reportlab')
except ImportError:
    print('❌ reportlab - FAILED')

try:
    import nltk
    print('✅ nltk')
except ImportError:
    print('❌ nltk - FAILED')

try:
    import fastapi
    print('✅ fastapi')
except ImportError:
    print('❌ fastapi - FAILED')

try:
    import psycopg2
    print('✅ psycopg2')
except ImportError:
    print('❌ psycopg2 - FAILED')
"

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start backend: cd backend && python -m uvicorn app.main:app --reload --port 8000"
echo "  2. Start frontend: cd frontend && npm run dev"
echo ""
