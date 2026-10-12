#!/usr/bin/env python3
"""
GMBot - CLI
Chatbot puissant spécialisé en rédaction, réflexion, logique et mathématiques.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

load_dotenv()

console = Console()

# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.x.ai/v1")
MODEL = os.getenv("MODEL_NAME", "grok-4")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "16384"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.6"))
REFLECTION = os.getenv("REFLECTION_ENABLED", "true").lower() == "true"

if not API_KEY:
    console.print("[bold red]Erreur : OPENAI_API_KEY manquante dans .env[/bold red]")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Chargement du prompt système
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


def chat(messages: list) -> str:
    """Appel au modèle"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content


def reflect_and_answer(user_input: str, history: list) -> str:
    """Boucle de réflexion pour les questions complexes"""
    if not REFLECTION:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
            {"role": "user", "content": user_input}
        ]
        return chat(messages)

    # Prompt de réflexion
    reflection_prompt = f"""Analyse cette demande de l'utilisateur et détermine si elle nécessite un raisonnement approfondi (maths, énigme, logique, rédaction complexe, analyse).

Demande : {user_input}

Réponds uniquement par "COMPLEXE" ou "SIMPLE"."""

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": reflection_prompt}
    ]
    complexity = chat(messages).strip().upper()

    if "COMPLEXE" in complexity:
        # Raisonnement structuré
        think_prompt = f"""Voici la demande de l'utilisateur :

{user_input}

Applique strictement le processus de raisonnement en 5 étapes décrit dans ton prompt système.
Montre clairement chaque étape (Compréhension, Planification, Raisonnement, Auto-critique, Réponse finale)."""

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
            {"role": "user", "content": think_prompt}
        ]
        return chat(messages)
    else:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
            {"role": "user", "content": user_input}
        ]
        return chat(messages)


def main():
    console.print(Panel.fit(
        "[bold cyan]GMBot[/bold cyan] — Chatbot puissant (rédaction • réflexion • logique • maths)",
        border_style="cyan"
    ))
    console.print(f"[dim]Modèle : {MODEL} | Réflexion : {'activée' if REFLECTION else 'désactivée'}[/dim]\n")

    history = []

    while True:
        try:
            user_input = Prompt.ask("[bold green]Vous[/bold green]")
            if user_input.lower() in ("exit", "quit", "q", "sortir"):
                console.print("[yellow]Au revoir ![/yellow]")
                break

            if not user_input.strip():
                continue

            with console.status("[bold blue]GMBot réfléchit...[/bold blue]"):
                answer = reflect_and_answer(user_input, history)

            console.print()
            console.print(Panel(Markdown(answer), title="[bold cyan]GMBot[/bold cyan]", border_style="cyan"))
            console.print()

            # Mise à jour de l'historique
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": answer})

            # Limite l'historique pour éviter de dépasser le contexte (garder les 20 derniers échanges)
            if len(history) > 40:
                history = history[-40:]

        except KeyboardInterrupt:
            console.print("\n[yellow]Au revoir ![/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Erreur : {e}[/bold red]")


if __name__ == "__main__":
    main()
