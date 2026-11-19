# Minik English

A playful English learning app for young kids, starring Ada.

Live: https://ersancaliskan.github.io/minik-english/

## Recorded voice (Angel)
Angel speaks with pre-recorded ElevenLabs audio (voice: "Emily - Bright & Energetic", eleven_v4) instead of the device voice. All 1224 sentences are recorded.
- `tools/lines.py` lists every sentence the app says → `audio/lines.json`
- `tools/gen_audio.py` records missing sentences and rebuilds `audio/manifest.json`
- The app plays a recording when the manifest has the sentence; anything else (e.g. sentences with the child's name) uses the device voice. Settings → "Angel's voice" switches between recorded and device voice.
