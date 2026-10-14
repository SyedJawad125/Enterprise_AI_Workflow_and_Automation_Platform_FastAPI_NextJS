"""
test_groq.py
───────────
Test Groq API connection and list available models.

Usage:
    python test_groq.py

Requirements:
    - GROQ_API_KEY in .env file
    - groq package installed
"""
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("❌ Error: GROQ_API_KEY not found in .env file")
    print("Please add: GROQ_API_KEY=your_key_here to your .env file")
    exit(1)

try:
    client = Groq(api_key=api_key)
    models = client.models.list()
    print("✅ Successfully connected to Groq API!")
    print("\nYour available Groq models:")
    for m in models.data:
        print(f"  • {m.id}")
except Exception as e:
    print(f"❌ Error connecting to Groq API: {e}")
    exit(1)