from gtts import gTTS
import pygame
import io

# Initialize pygame mixer
pygame.mixer.init()

# Marathi text
text = "नमस्कार! आपले स्वागत आहे."

# Create a gTTS object
tts = gTTS(text=text, lang='mr', slow=False)

# Save the speech to a temporary in-memory buffer
mp3_fp = io.BytesIO()
tts.write_to_fp(mp3_fp)

# Rewind the buffer to the beginning
mp3_fp.seek(0)

# Load the MP3 file from the buffer and play it
pygame.mixer.music.load(mp3_fp)
pygame.mixer.music.play()

# Keep the script running while the audio plays
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
