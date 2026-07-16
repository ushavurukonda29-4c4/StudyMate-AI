# ==========================================================
# AI STUDY TUTOR (GEMINI + GRADIO CHAT)
# SAFE VERSION FOR GITHUB
# ==========================================================

import os
import gradio as gr
from google import genai

# ==========================================================
# LOAD API KEY
# ==========================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("⚠️ GEMINI_API_KEY not set!")

client = genai.Client(api_key=API_KEY)

# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are a StudyMate AI, an intelligent tutor and educational assistant.

Instructions:
- Answer study-related questions clearly and accurately.
- Explain concepts in simple language.
- Provide step-by-step explanations.
- Use examples wherever needed.
- Provide complete and well-commented code if asked.
- Use headings, bullet points, or tables.
- Show all steps for numerical problems.
- Be polite, friendly, and professional.
"""

# ==========================================================
# CREATE CHAT SESSION
# ==========================================================

def create_chat():
    return client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_PROMPT}
    )

chat = create_chat()

# ==========================================================
# CHAT FUNCTION
# ==========================================================

def respond(message, history):
    global chat

    if not API_KEY:
        return "❌ API key missing. Please set GEMINI_API_KEY."

    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ==========================================================
# CLEAR CHAT
# ==========================================================

def clear_chat():
    global chat
    chat = create_chat()
    return [], ""

# ==========================================================
# GRADIO UI
# ==========================================================

with gr.Blocks(title="AI Study Tutor") as demo:

    gr.Markdown("# 📚 StudyMate AI")
    gr.Markdown("Ask any study-related question 👇")

    chatbot = gr.ChatInterface(fn=respond)

    clear_btn = gr.Button("🧹 Clear Chat")

    clear_btn.click(
        fn=clear_chat,
        outputs=[chatbot.chatbot, chatbot.textbox]
    )

# ==========================================================
# LAUNCH
# ==========================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
