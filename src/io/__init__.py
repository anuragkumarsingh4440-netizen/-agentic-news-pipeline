"""Human I/O boundary: speech-in (ASR), speech-out (TTS), wake-word.

Every provider here implements a tiny interface (Interface Segregation), so a
local Whisper model and a cloud Deepgram call are interchangeable to the rest
of the app (Liskov). Swap them via config, not code.
"""
