# brain.py

from groq import Groq
import json
import os
import sys
import time

# =========================
# CONFIGURATION
# =========================
API_KEY = "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"  # <-- Apni Groq API key
client = Groq(api_key=API_KEY)
MEMORY_FILE = "memory.json"
MAX_MEMORY = 20  # last 20 messages stored

# =========================
# MEMORY FUNCTIONS
# =========================
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

# =========================
# TYPING EFFECT
# =========================
def typing_effect(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# =========================
# AI BRAIN FUNCTION
# =========================
def ask_ai(user_input):
    memory = load_memory()
    greetings = ["hello", "hi", "hey", "namaste"]

    # Save meaningful user input only
    if user_input.strip().lower() not in greetings:
        memory.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are AI CONSTRUCT AI.

Developer: Aditya
AI Architect & Guide: ChatGPT

Purpose:
Help people build AI assistants, chatbots, apps, and websites.

Rules:
- Short and friendly answers.
- Remember only meaningful user messages.
- Avoid repeating greetings unnecessarily.
- Avoid extra preambles unless specifically asked.
- Provide guidance step by step when requested.
"""
                }
            ] + memory[-MAX_MEMORY:]
        )

        ai_reply = response.choices[0].message.content.strip()

        # Save AI reply if not a greeting
        if ai_reply.lower() not in greetings:
            memory.append({"role": "assistant", "content": ai_reply})
            save_memory(memory)

        # Typing effect for the reply
        typing_effect(ai_reply)

        return ai_reply

    except Exception as e:
        error_msg = f"Brain error: {str(e)}"
        typing_effect(error_msg)
        return error_msg