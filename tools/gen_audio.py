#!/usr/bin/env python3
"""Records audio/lines.json with ElevenLabs and rebuilds audio/manifest.json.

  python3 tools/lines.py                         # refresh the sentence list
  ELEVENLABS_API_KEY=... python3 tools/gen_audio.py   # record missing files
  python3 tools/gen_audio.py --manifest-only     # only rebuild the manifest from files present

Voice: "Emily - Bright & Energetic" (young, American, female).
"""
import hashlib, json, os, re, sys, time, urllib.request

VOICE_ID = 'd8WcCpplp8meHt10UhL8'
MODEL_ID = 'eleven_multilingual_v2'
ROOT = os.path.join(os.path.dirname(__file__), '..', 'audio')

def key(t):  # must match normKey() in index.html
    return re.sub(r'\s+', ' ', t.strip().lower().replace('’', "'"))

def fname(t):
    k = key(t)
    slug = re.sub(r'[^a-z0-9]+', '-', k).strip('-')[:40] or 'x'
    return f"{slug}-{hashlib.sha1(k.encode()).hexdigest()[:6]}.mp3"

def tts(text, api_key):
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_22050_32',
        data=json.dumps({'text': text, 'model_id': MODEL_ID,
                         'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75, 'style': 0.3}}).encode(),
        headers={'xi-api-key': api_key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def main():
    lines = json.load(open(os.path.join(ROOT, 'lines.json')))
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    if '--manifest-only' not in sys.argv:
        if not api_key:
            sys.exit('Set ELEVENLABS_API_KEY (or use --manifest-only).')
        for i, t in enumerate(lines):
            path = os.path.join(ROOT, fname(t))
            if os.path.exists(path):
                continue
            for attempt in range(3):
                try:
                    open(path, 'wb').write(tts(t, api_key)); break
                except Exception as e:
                    print('retry', t, e); time.sleep(2 + attempt * 3)
            print(f'{i + 1}/{len(lines)} {t}')
    manifest = {key(t): fname(t) for t in lines if os.path.exists(os.path.join(ROOT, fname(t)))}
    json.dump(manifest, open(os.path.join(ROOT, 'manifest.json'), 'w'), ensure_ascii=False, indent=0, sort_keys=True)
    print(len(manifest), 'of', len(lines), 'sentences have a recording')

if __name__ == '__main__':
    main()
