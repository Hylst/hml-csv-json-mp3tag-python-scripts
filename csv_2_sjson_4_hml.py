import sys
import csv
import json
import os
import hashlib
import unicodedata
import re

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def generate_id(filename):
    base = os.path.splitext(filename)[0]
    clean_base = slugify(base)
    hash_part = hashlib.md5(filename.encode()).hexdigest()[:6]
    return f"remote-{clean_base}-{hash_part}"

def parse_list(value):
    return [item.strip() for item in value.split(',') if item.strip()]

def main(type_music=None, csv_path=None):
    # Configuration via arguments ou prompts
    if not type_music:
        type_music = input("Entrez le type de musique (ex: soundchip): ").strip()
    if not csv_path:
        csv_path = input("Entrez le chemin du fichier CSV: ").strip()
    
    json_path = os.path.splitext(csv_path)[0] + ".json"

    # Lecture et traitement du CSV
    with open(csv_path, 'r', encoding='utf-16') as f:
        raw_content = f.read().lstrip('\ufeff')
        lines = [line.strip() for line in raw_content.split('\n') if line.strip()]
    
    headers = [h.strip().lower() for h in lines[0].split(';')]
    required = {'title', 'artist', 'album', 'year', 'genre', 'comment', 
               'filename', 'keywords', 'mood', 'usage', 'story', 'song', 
               'lyrics', 'note'}
    
    if missing := required - set(headers):
        print(f"ERREUR: Colonnes manquantes: {', '.join(sorted(missing))}")
        return

    entries = []
    for line in lines[1:]:
        values = line.split(';')
        if len(values) != len(headers):
            continue
            
        row = dict(zip(headers, values))
        filename = row['filename']
        
        entry = {
            "id": generate_id(filename),
            "title": row.get('title', ''),
            "artist": row.get('artist', ''),
            "album": row.get('album', ''),
            "genre": parse_list(row.get('genre', '')),
            "coverArt": f"/music/{type_music}/{os.path.splitext(filename)[0]}.jpg",
            "audioSrc": f"/music/{type_music}/{filename}",
            "fileName": filename,
            "keywords": parse_list(row.get('keywords', '')),
            "year": row.get('year', ''),
            "comment": row.get('comment', ''),
            "lyrics": row.get('lyrics', ''),
            "mood": parse_list(row.get('mood', '')),
            "usage": parse_list(row.get('usage', '')),
            "story": row.get('story', ''),
            "song": int(row.get('song', 0)) if row.get('song', '').strip() else 0,
            "note": int(row.get('note', 0)) if row.get('note', '').strip() else 0
        }
        entries.append(entry)

    # Écriture avec formatage personnalisé
    with open(json_path, 'w', encoding='utf-8') as f:
        json_str = json.dumps(
            {type_music: entries},
            ensure_ascii=False,
            indent=2,
            separators=(',', ': '),
            default=lambda o: o.__dict__
        )
        # Optimisation du formatage des listes
        json_str = re.sub(r'(\[\n\s+)(".+?")(\n\s+\])', r'\1\2\3', json_str)
        f.write(json_str)

    print(f"Conversion réussie! {len(entries)} titres exportés dans {json_path}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Utilisation: python script.py [type_music] [fichier.csv]")
        main()