from enum import Enum
import json

# dictionary: group: [instrument_name, radius]
INSTRUMENTS = {
    'P': ['Piccolo', 1],
    'F': ['Flute', 1],
    'C': ['Clarinet', 1],
    'A': ['Alto Sax', 1],
    'E': ['Tenor Sax', 1],
    'X': ['Bari Sax', 1],

    'T': ['Trumpet', 1],
    'M': ['Mellophone', 1],
    'R': ['Trombone', 2],
    'B': ['Baritone', 1],
    'U': ['Tuba', 1.5],

    'SD': ['Snare Drum', 1],
    'TD': ['Tenor Drum', 1.5],
    'BD': ['Bass Drum', 1.5],
    'CC': ['Cymbals', 1],

    'CG': ['Color Guard', 1],

    '-': ['Other', 1],
}

class Performer:
    def __init__(self, instrument, id):
        self.instrument = instrument
        self.id = id
    
    def group(self):
        return self.instrument

    def radius(self):
        return INSTRUMENTS[self.instrument][1]
    
    def performer_label(self):
        return self.group() + str(self.id)
    
    def instrument_name(self):
        return INSTRUMENTS[self.instrument][0]

    def toDict(self):
        return { "instrument": self.instrument, "id": self.id }
