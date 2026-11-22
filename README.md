# Minik English

A playful English learning app for young kids, starring Ada.

Live: https://ersancaliskan.github.io/minik-english/

## Recorded voice (Angel)
Angel speaks with pre-recorded ElevenLabs audio (voice: "Emily - Bright & Energetic", eleven_v4) instead of the device voice. All 1224 sentences are recorded.
- `tools/lines.py` lists every sentence the app says → `audio/lines.json`
- `tools/gen_audio.py` records missing sentences and rebuilds `audio/manifest.json`
- The app plays a recording when the manifest has the sentence; anything else (e.g. sentences with the child's name) uses the device voice.

## Pıtır (meraklı baykuş)
Kids' Q&A app in Turkish: the child asks out loud, the owl Pıtır answers by age (4–5 / 6–8) and shows Wikipedia pictures and videos.
Live: https://ersancaliskan.github.io/minik-english/pitir/
- Answers come live from Claude (key `sk-ant-…`) or ChatGPT (key `sk-…`), entered once on the parent screen and kept only on the device.
- Optional ElevenLabs key for the voice (default voice Çiçek); otherwise the device's Turkish voice.
