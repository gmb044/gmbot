"""
Module de réflexion structurée pour GMBot
"""

REFLECTION_TEMPLATE = """
Applique le processus de raisonnement suivant à la demande de l'utilisateur :

### 1. Compréhension
Reformule le problème clairement. Identifie les objectifs et les contraintes.

### 2. Planification
Choisis la stratégie la plus adaptée (Chain-of-Thought, Tree-of-Thought, décomposition, preuve...).

### 3. Raisonnement détaillé
Développe la solution étape par étape avec justifications.

### 4. Auto-critique
Vérifie les erreurs potentielles, cas limites, cohérence logique.

### 5. Réponse finale
Donne la réponse claire, structurée et précise.

Demande de l'utilisateur :
{user_input}
"""


def build_reflection_prompt(user_input: str) -> str:
    return REFLECTION_TEMPLATE.format(user_input=user_input)
