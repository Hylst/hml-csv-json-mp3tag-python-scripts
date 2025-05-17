# MP3Tag to JSON Converter with AI Enhancement

**Auteur** : Geoffroy Streit  
**Version** : 2.0  
**Date** : Octobre 2024

---

## 📖 Description

Ce script Python convertit des fichiers CSV (exportés depuis MP3Tag) en un catalogue JSON structuré, avec génération automatique de métadonnées manquantes via l'API Deepseek. Parfait pour gérer des collections musicales complexes.

## 🚀 Fonctionnalités

- **Conversion CSV -> JSON** automatisée
- **Amélioration IA** des champs manquants :
  - Mood (ambiance émotionnelle)
  - Usage (cas d'utilisation)
  - Commentaires descriptifs
  - Phrases artistiques (story)
- Génération d'**IDs uniques** pour chaque piste
- **Gestion avancée** des métadonnées musicales
- Support des **arguments CLI** et mode interactif

## 📥 Installation

1. **Prérequis** :
   - Python 3.10+
   - Clé API Deepseek

2. **Installation des dépendances** :

```bash
pip install requests python-dotenv
'''
🛠 Utilisation

Mode ligne de commande

'''bash
python csv_2_sjson_4_hml.py <type_music> <fichier.csv> [api_key]
'''
type_music : Catégorie musicale (ex: "soundchip", "streaming")

fichier.csv : Chemin vers le fichier CSV MP3Tag

api_key (optionnel) : Clé API Deepseek

Mode interactif
bash
python csv_2_sjson_4_hml.py
Exemple complet
bash
python csv_2_sjson_4_hml.py atari atari_tracks.csv sk-or-v1-abc123

🔧 Configuration

Clé API Deepseek :

Obtenez une clé sur Deepseek Console

Utilisation possible :

En argument CLI

Dans un fichier .env :

'''ini
DEEPSEEK_API_KEY=votre_cle_ici
📂 Structure des fichiers
.
├── csv_2_sjson_4_hml.py    # Script principal
├── input/                  # Exemple de CSV d'entrée
│   └── mp3tag_export.csv
├── output/                 # JSON générés
│   └── catalogue_musique.json
└── README.md               # Ce fichier
'''

📄 Format d'entrée CSV

Exemple minimal :

'''csv
Title;Artist;Album;Year;Genre;Comment;Filename;Keywords;Mood;Usage;Story;Song;Lyrics;Note
Brassman;hylst;Hylst Experiments;2009;rap, hip hop;;brassman.mp3;rap, brass;;Workout;;1;;180
'''

📦 Format de sortie JSON
'''json
{
  "atari": [
    {
      "id": "remote-brassman-1c8318",
      "title": "Brassman",
      "artist": "hylst",
      "album": "Hylst Experiments",
      "genre": ["rap", "hip hop"],
      "coverArt": "/music/atari/brassman.jpg",
      "audioSrc": "/music/atari/brassman.mp3",
      "fileName": "brassman.mp3",
      "keywords": ["rap", "brass", "street"],
      "year": "2009",
      "comment": "Mélange explosif cuivres/hip-hop généré par IA",
      "mood": ["énergique", "urbain"],
      "usage": ["Sport", "Entraînement"],
      "story": "Les cuivres sonnent la révolte des rues.",
      "song": 1,
      "note": 180
    }
  ]
}
'''

🤖 Détails techniques

Prompt IA

'''python
"""
Génère UNIQUEMENT un JSON avec :
- mood : 3-5 adjectifs d'ambiance
- usage : 3-5 cas d'utilisation
- comment : 1 phrase descriptive
- story : 1 phrase artistique (<15 mots)

Contexte :
Titre: {title}
Album: {album}
Genres: {genres}
Mots-clés: {keywords}
"""
'''

Gestion des erreurs
Vérification des colonnes CSV

Reconnexion automatique à l'API

Journalisation détaillée

🔄 Personnalisation

Personnalisez dans le code :

'''python
# Paramètres IA
AI_SETTINGS = {
    'temperature': 0.7,       # Créativité (0-1)
    'max_tokens': 400,        # Longueur max réponse
    'model': 'deepseek-chat'  # Modèle à utiliser
}
'''

# Structure des chemins
AUDIO_BASE_PATH = "/music"    # Base URL des fichiers
📜 Licence
Creative Commons BY-NC-SA 4.0

Développé avec ♥ par Geoffroy Streit