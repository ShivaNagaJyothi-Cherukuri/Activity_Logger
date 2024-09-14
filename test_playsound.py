from playsound import playsound
import os

# Path to your sound file
sound_file = 'sounds/notification_sound.mp3'

# Check if the file exists
if not os.path.exists(sound_file):
    print(f"Sound file not found: {sound_file}")
else:
    print("Playing sound...")
    playsound(sound_file)
    print("Sound played successfully.")

