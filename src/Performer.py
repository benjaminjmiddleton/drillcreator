from enum import Enum

# class Instrument(Enum):
#     PICCOLO     = 1
#     FLUTE       = 2
#     CLARINET    = 3
#     ALTO_SAX    = 4
#     TENOR_SAX   = 5
#     BARI_SAX    = 6

#     TRUMPET     = 7
#     MELLOPHONE  = 8
#     TROMBONE    = 9
#     BARITONE    = 10
#     TUBA        = 11

#     SNARE       = 12
#     TENORS      = 13
#     BASS_DRUM   = 14
#     CYMBALS     = 15

#     GUARD       = 16

#     OTHER       = 17

# dictionary -- instrument: [group, radius]
# instrument_info = {
#     Instrument.PICCOLO: ['P', 1],
#     Instrument.FLUTE: ['F', 1],
#     Instrument.CLARINET: ['C', 1],
#     Instrument.ALTO_SAX: ['A', 1],
#     Instrument.TENOR_SAX: ['E', 1],
#     Instrument.BARI_SAX: ['X', 1],

#     Instrument.TRUMPET: ['T', 1],
#     Instrument.MELLOPHONE: ['M', 1],
#     Instrument.TROMBONE: ['R', 2],
#     Instrument.BARITONE: ['B', 1],
#     Instrument.TUBA: ['U', 1.5],

#     Instrument.SNARE: ['SD', 1],
#     Instrument.TENORS: ['TD', 1.5],
#     Instrument.BASS_DRUM: ['BD', 1.5],
#     Instrument.CYMBALS: ['CC', 1],

#     Instrument.GUARD: ['CG', 1],

#     Instrument.OTHER: ['-', 1],
# }

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