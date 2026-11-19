# Minik English

A playful English learning app for young kids, starring Ada.

Live: https://ersancaliskan.github.io/minik-english/

## Recorded voice (Angel)
Angel can speak with pre-recorded ElevenLabs audio instead of the device voice.
- `tools/lines.py` lists every sentence the app says → `audio/lines.json`
- `tools/gen_audio.py` records missing sentences and rebuilds `audio/manifest.json`
- The app plays a recording when the manifest has the sentence; anything else (e.g. sentences with the child's name) uses the device voice. Settings → "Angel's voice" switches between recorded and device voice.
