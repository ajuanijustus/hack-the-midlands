# Import from modules
from generateMIDI import generate_midi
from midiToMP3 import midi_to_mp3

# Import modules
import pygame
import os
import sys

class Button:
    def __init__(self, x, y, text, border=5):
        self.x = x
        self.y = y
        self.text = font.render(text, True, (0, 0, 0))
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.border = border
        self.inner_colour = 255
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x-self.border, self.y-self.border, self.width + 2*self.border, self.height + 2*self.border))
        pygame.draw.rect(screen, [self.inner_colour]*3, (self.x, self.y, self.width, self.height))

        screen.blit(self.text, (self.x, self.y))

    def hovered(self, x, y):
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height


# Define contant file name 
MIDI_FILENAME = "c_scale_withbass_random"

base_note = 60
scale_type = 'major'
chords_flag = False

generate_midi(MIDI_FILENAME, base_note, scale_type, chords_flag)
midi_to_mp3(MIDI_FILENAME)

"""path = os.getcwd()
midi_filename = os.path.join(path, "midiFiles", f"{MIDI_FILENAME}.mid")

pm = pretty_midi.PrettyMIDI(midi_filename)

for inst in pm.instruments:
    print(inst.notes)"""

# Get mp3 filename
path = os.getcwd()
mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")

# Initialise the mixer module
pygame.mixer.init()
pygame.font.init()

# Load the song
pygame.mixer.music.load(mp3_filename)

font = pygame.font.SysFont("Helvetica", 12)

# Set screen width and height
WIDTH, HEIGHT = (800, 600)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Button border
buttonGen = Button(10, 10, "Re-Generate", 5)
buttonChords = Button(10, 10, "Chords On", 5)

# Generating MIDI variables
base_note = 60
scale_type = 'major'
chords_flag = False

# Main interface loop
play = False
while True:
    # Manage each event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear the screen
    screen.fill((255, 255, 255))

    buttonGen.draw()
    buttonChords.draw()

    m_x, m_y = pygame.mouse.get_pos()

    if buttonGen.hovered(*pygame.mouse.get_pos()):
        buttonGen.inner_colour = 150
        if pygame.mouse.get_pressed()[0]:
            # Stop the music so that the file is no longer open
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            # Generate new set of notes
            generate_midi(MIDI_FILENAME, base_note, scale_type, chords_flag)
            midi_to_mp3(MIDI_FILENAME)

            # Load new midi file and start playing it
            mp3_filename = os.path.join(path, "mp3Files", f"{MIDI_FILENAME}.mp3")
            pygame.mixer.music.load(mp3_filename)

            play = False
    else:
        buttonGen.inner_colour = 255

    # Draw 4 lines
    for i in range(5):
        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT//2+30*i, WIDTH, 5))

    # If not already playing, play the notes
    if not play:
        pygame.mixer.music.play()
        play = True
    
    # Update the screen
    pygame.display.flip()