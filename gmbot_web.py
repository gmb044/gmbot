#!/usr/bin/env python3
"""
GMBot - Interface Web (Gradio)
"""

import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.x.ai/v1")
MODEL = os.getenv("MODEL_NAME", "grok-4")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "16384"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.6"))
REFLECTION = os.getenv("REFLECTION_ENABLED", "true").lower() == "true"

if not API_KEY:
    raise ValueError("OPENAI_API_KEY manquante dans .env")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


def chat_fn(message, history):
    """Fonction principale de chat pour Gradio"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )

    return response.choices[0].message.content


demo = gr.ChatInterface(
    fn=chat_fn,
    title="GMBot 🤖",
    description="Chatbot puissant spécialisé en **rédaction**, **réflexion**, **logique**, **énigmes** et **mathématiques complexes**.\n\nCompatible grand contexte • Raisonnement structuré • Style Claude-level",
    theme=gr.themes.Soft(primary_hue="cyan", secondary_hue="blue"),
    examples=[
        "Rédige un article de blog engageant sur l'avenir de l'IA en 2027",
        "Résous étape par étape : intégrale de (x² * e^x) dx",
        "Voici une énigme : Un homme regarde une photo et dit 'Frères et sœurs, je n'en ai point, mais le père de cet homme est le fils de mon père'. Qui est sur la photo ?",
        "Explique-moi le théorème de Banach-Tarski de façon accessible mais rigoureuse",
        "Améliore ce texte pour le rendre plus professionnel et percutant : [colle ton texte]",
    ],
    cache_examples=False,
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
