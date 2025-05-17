import sys
import json
import os
import hashlib
import unicodedata
import re
import requests

# Configuration de l'API
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEFAULT_MODEL = "deepseek-chat"

def generate_ai_content(api_key, prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Erreur API: {str(e)}")
        return None

def build_ai_prompt(track_data, missing_fields):
    prompt = f"""Génère UNIQUEMENT un JSON avec les champs suivants : {', '.join(missing_fields)}.
Contexte musical :
- Titre : {track_data['title']}
- Album : {track_data['album']}
- Genre : {', '.join(track_data['genre'])}
- Mots-clés existants : {', '.join(track_data['keywords']) if track_data['keywords'] else 'Aucun'}
- Mood existant : {', '.join(track_data['mood']) if track_data['mood'] else 'Aucun'}
- Usage existant : {', '.join(track_data['usage']) if track_data['usage'] else 'Aucun'}
- Commentaire existant : {track_data['comment'] if track_data['comment'] else 'Aucun'}

Règles strictes :
1. Mood : 3-5 adjectifs ou expressions décrivant l'atmosphère émotionnelle
2. Usage : 3-5 cas d'utilisation concrets (ex: "Sport", "Concentration")
3. Comment : 1 phrase descriptive engageante en français
4. Story : 1 phrase littéraire intrigante en français (max 15 mots)
5. Format JSON uniquement, pas de commentaires"""

    return prompt

def enhance_with_ai(api_key, track):
    missing = [field for field in ['mood', 'usage', 'comment', 'story'] if not track.get(field) or (isinstance(track[field], list) and len(track[field]) == 0]
    
    if not missing:
        return track

    print(f"Génération IA pour : {track['title']}")
    print(f"Champs manquants : {', '.join(missing)}")

    prompt = build_ai_prompt(track, missing)
    ai_response = generate_ai_content(api_key, prompt)

    if not ai_response:
        return track

    try:
        ai_data = json.loads(ai_response.strip("```json\n").strip("```"))
        print("Réponse IA reçue avec succès")

        for field in missing:
            if field in ai_data:
                if isinstance(track[field], list):
                    track[field] = list(set(track[field] + ai_data[field]))  # Fusion des listes
                else:
                    track[field] = ai_data[field]
                print(f"Champ '{field}' mis à jour")
    except Exception as e:
        print(f"Erreur d'analyse JSON : {str(e)}")

    return track

# [Les fonctions existantes restent inchangées jusqu'à la fonction main...]

def main(type_music=None, csv_path=None, api_key=None):
    if not type_music:
        type_music = input("Type de musique (ex: soundchip): ").strip()
    if not csv_path:
        csv_path = input("Chemin du CSV: ").strip()
    if not api_key:
        api_key = input("Clé API Deepseek: ").strip()
    
    # [Le reste du traitement CSV reste inchangé...]
    
    # Après création des entries :
    print("\nDébut de l'amélioration IA...")
    for i, entry in enumerate(entries):
        entries[i] = enhance_with_ai(api_key, entry)
        print(f"Progression: {i+1}/{len(entries)} tracks traitées\n")

    # [Le reste de l'écriture JSON reste inchangé...]

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        main(*sys.argv[1:4])  # Accepte 3 arguments max
    else:
        print("Usage: python script.py <type_music> <fichier.csv> [api_key]")
        main()