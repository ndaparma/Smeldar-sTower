import sys
import time
from playsound import playsound
def player_input():
  playerInput = input().upper().strip()
  print('\n')
  return playerInput

def print_slow(str, typingActive):
  if typingActive == "ON":
    for char in str:
      time.sleep(.01)
      sys.stdout.write(char)
      sys.stdout.flush()
    print('')
  else:
    print(str)

def play_sound_effect(soundFile, SoundsOn):
  if SoundsOn == "ON":
    playsound(soundFile)
  else:
    pass