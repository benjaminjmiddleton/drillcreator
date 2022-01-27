from enum import IntEnum

import math

class yardline(IntEnum):
    A_END   = 1
    A5      = 2
    A10     = 3
    A15     = 4
    A20     = 5
    A25     = 6
    A30     = 7
    A35     = 8
    A40     = 9
    A45     = 10
    FIFTY   = 11
    B45     = 12
    B40     = 13
    B35     = 14
    B30     = 15
    B25     = 16
    B20     = 17
    B15     = 18
    B10     = 19
    B5      = 20
    B_END   = 21

# NCAA hash marks assumed for now
class hashmark(IntEnum):
    BSL = 0 # Back Sideline
    BH = 1 # Back Hash
    FH = 2 # Front Hash
    FSL = 3 # Front Sideline

class Coordinate:
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
        five_yards = field_width / 24
        _8to5 = five_yards / 8
        coord = (self.yardline + 1) * five_yards
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
        _8to5 = field_height / (28*3)
        coord = _8to5 * self.v_steps + self.hashmark * _8to5 * 28
        return math.floor(coord)

    def get_pixel_coords(self, field_width, field_height):
        return (self.get_x(field_width), self.get_y(field_height))