from enum import IntEnum

import math

class yardline(IntEnum):
    # Integer associated with each value = (number of yards from the left of the field) * 5
    A_END   = 2
    A5      = 3
    A10     = 4
    A15     = 5
    A20     = 6
    A25     = 7
    A30     = 8
    A35     = 9
    A40     = 10
    A45     = 11
    FIFTY   = 12
    B45     = 13
    B40     = 14
    B35     = 15
    B30     = 16
    B25     = 17
    B20     = 18
    B15     = 19
    B10     = 20
    B5      = 21
    B_END   = 22

# NCAA hash marks assumed
class hashmark(IntEnum):
    BSL = 0 # Back Sideline
    BH = 1 # Back Hash
    FH = 2 # Front Hash
    FSL = 3 # Front Sideline

class Coordinate:
    STEPS_FROM_BSL_TO_BH = 28
    STEPS_FROM_BSL_TO_FH = 48
    STEPS_FROM_BSL_TO_FSL = 76

    TOTAL_H_YARDS = 120

    def __init__(self, h_steps, yardline, v_steps, hashmark):
        """
        @param h_steps: 8:5 steps off the yardline, Integer
                        A positive value corresponds to inside steps. A negative value corresponds to outside steps.
        @param yardline: which yardline the marcher is closest to, Enum
        @param v_steps: 8:5 steps off the hashmark, Integer
                        A positive value corresponds to steps towards FSL. A negative value corresponds ot steps towards BSL.
        @param hashmark: the hashmark or sideline the marcher is closest to
        """
        self.h_steps = h_steps
        self.yardline = yardline
        self.v_steps = v_steps
        self.hashmark = hashmark
    
    def get_x(self, field_width):
        """
        @func get_x returns the horizontal pixel value of the co-ordinate given field width
        @param field_width: width from back of endzone to back of endzone in pixels, Integer
        """
        five_yards = field_width / Coordinate.TOTAL_H_YARDS * 5
        _8to5 = five_yards / 8
        coord = (self.yardline) * five_yards
        if self.yardline <= 11: # if on side A
            coord += _8to5 * self.h_steps
        else: # if on side B
            coord -= _8to5 * self.h_steps
        return math.floor(coord)

    def get_y(self, field_height):
        """
        @func get_y returns the vertical pixel value of the co-ordinate given field width
        @param field_height: height from FSL to BSL in pixels, Integer
        """
        _8to5 = field_height / Coordinate.STEPS_FROM_BSL_TO_FSL
        if self.hashmark == hashmark.BSL:
            coord = _8to5 * self.v_steps
        elif self.hashmark == hashmark.BH:
            coord = _8to5 * self.v_steps + _8to5 * Coordinate.STEPS_FROM_BSL_TO_BH
        elif self.hashmark == hashmark.FH:
            coord = _8to5 * self.v_steps + _8to5 * Coordinate.STEPS_FROM_BSL_TO_FH
        elif self.hashmark == hashmark.FSL:
            coord = _8to5 * self.v_steps + _8to5 * Coordinate.STEPS_FROM_BSL_TO_FSL
        return math.floor(coord)

    def get_pixel_coords(self, field_size):
        return (self.get_x(field_size[0]), self.get_y(field_size[1]))

    def toDict(self):
        return {
            "h_steps": self.h_steps,
            "yardline": int(self.yardline),
            "v_steps": self.v_steps,
            "hashmark": int(self.hashmark)
        }
