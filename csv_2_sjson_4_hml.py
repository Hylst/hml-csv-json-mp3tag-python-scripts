import sys
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

def format_json_lists(json_str):
    return re.sub(
        r'(\"(\w+)\": \[\n\s+)((".*?")(,\n\s+".*?")*)(\n\s+\])',
        lambda m: f'"{m.group(2)}": [{", ".join(re.findall(r'".*?"', m.group(3)))}]',
        json_str
    )

def main(type_music=None, csv_path=None):
    if not type_music:
        type_music = input("Type de musique (ex: soundchip): ").strip()
    if not csv_path:
        csv_path = input("Chemin du CSV: ").strip()
    
    json_path = os.path.splitext(csv_path)[0] + ".json"

    with open(csv_path, 'r', encoding='utf-16') as f:
        raw_content = f.read().lstrip('\ufeff')
        lines = [line.strip() for line in raw_content.split('\n') if line.strip()]
    
    # Vérification et nettoyage des en-têtes
    headers = [h.strip().lower().replace('\ufeff', '') for h in lines[0].split(';')]
    required = {'title', 'artist', 'album', 'year', 'genre', 'comment', 
               'filename', 'keywords', 'mood', 'usage', 'story', 'song', 
               'lyrics', 'note'}
    
    if missing := required - set(headers):
        print(f"ERREUR: Colonnes manquantes: {', '.join(sorted(missing))}")
        print(f"En-têtes détectés: {headers}")
        return

    entries = []
    for line in lines[1:]:
        values = line.split(';')
        if len(values) != len(headers):
            print(f"Ligne ignorée (nombre de colonnes incorrect): {line}")
            continue
            
        row = dict(zip(headers, values))
        try:
            filename = row['filename']
            entries.append({
                "id": generate_id(filename),
                "title": row['title'],
                "artist": row['artist'],
                "album": row['album'],
                "genre": parse_list(row['genre']),
                "coverArt": f"/music/{type_music}/{os.path.splitext(filename)[0]}.jpg",
                "audioSrc": f"/music/{type_music}/{filename}",
                "fileName": filename,
                "keywords": parse_list(row['keywords']),
                "year": row['year'],
                "comment": row['comment'],
                "lyrics": row.get('lyrics', ''),
                "mood": parse_list(row['mood']),
                "usage": parse_list(row['usage']),
                "story": row.get('story', ''),
                "song": int(row['song']) if row['song'].strip() else 0,
                "note": int(row['note']) if row['note'].strip() else 0
            })
        except KeyError as e:
            print(f"Erreur dans la ligne : {line}")
            print(f"Clé manquante: {e}")
            continue

    json_str = json.dumps({type_music: entries}, ensure_ascii=False, indent=2)
    json_str = format_json_lists(json_str)

    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_str)

    print(f"Succès: {len(entries)} titres convertis -> {json_path}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python script.py <type_music> <fichier.csv>")
        main()