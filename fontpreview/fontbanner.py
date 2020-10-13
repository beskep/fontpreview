#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# fontbanner -- fontpreview
#
#     Copyright (C) 2020 Matteo Guadrini <matteo.guadrini@hotmail.it>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

# region imports
from .fontpreview import FontPreview, CALC_POSITION
from PIL import Image


# endregion

# region functions
def resize(image, size):
    """
    Resize image
    :param image: image to resize
    :param size: new size of image
    :return: Image
    """
    # Resize image
    return image.resize(size)


# endregion

# region classes
class FontBanner(FontPreview):
    """
    Class that represents the banner of a font
    """

    def __init__(self, font, orientation='landscape', bg_color='white', fg_color='black', mode='letter'):
        """
        Object that represents the banner of a font
        :param font: font file
        :param orientation: the orientation of the banner; 'landscape', 'portrait' or tuple(x,y)
        :param bg_color: background color
        :param fg_color: font color
        :param mode: the text inside the banner; 'letter','fontname', 'paragraph', 'alpha' and 'combination'
        """
        # Define properties
        FontPreview.__init__(self, font=font)
        self.set_orientation(orientation)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.mode = mode
        self.font_position = CALC_POSITION['center'](self.dimension, self.font.getsize(self.font_text))
        # Create default image
        self.set_mode(mode=mode)

    def __str__(self):
        """
        String representation of font banner
        :return: string
        """
        return FontPreview.__str__(self) + ",mode={mode}".format(mode=self.mode)

    def set_orientation(self, orientation, font_position='center'):
        """
        Set orientation of banner
        :param orientation: the orientation of the banner; 'landscape' or 'portrait'
        :param font_position: font position respect dimension of banner
        :return: None
        """
        # Calculate banner size
        if isinstance(orientation, tuple):
            self.dimension = orientation
            # Recalculate font position
            self.set_text_position(font_position)
            return None
        else:
            LANDSCAPE = (1653, 560)
            PORTRAIT = (560, 1653)
            if orientation == 'landscape':
                self.dimension = LANDSCAPE
            elif orientation == 'portrait':
                self.dimension = PORTRAIT
            else:
                raise ValueError('orientation is "landscape","portrait" or tuple(x,y)')
            # Recalculate font position
            self.set_text_position(font_position)

    def set_mode(self, mode, align='center'):
        """
        Set the text mode
        :param mode: mode that sets the text in the banner
        :param align: alignment of text. Available 'left', 'center' and 'right'
        :return: None
        """
        MODE = {
            'letter': 'a b c d e f\ng h i j k l\nm n o p q r\ns t u v w x y z',
            'alpha': 'Aa Bb Cc Dd Ee Ff\n1 2 3 4 5 6 7 8 9 0',
            'fontname': '{0}'.format(self.font.getname()[0]),
            'paragraph': 'Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit.',
            'combination': '{0}\n{1}'.format(self.font.getname(),
                                             'Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit.'
                                             ),
            'none': ''
        }
        # Verify is mode exists
        if mode in MODE:
            self.mode = mode
            self.font_text = MODE.get(mode)
            # Create default image
            self.draw(align=align)
        else:
            raise ValueError('mode is "letter", "alpha", "fontname", "paragraph" and "combination"')

    def add_image(self, image, position):
        """
        Adds an additional image to the banner
        :param image: path of image
        :param position: position of image
        :return: None
        """
        # Create image
        if isinstance(image, FontPreview):
            img = image.image
        else:
            img = Image.open(image)
        # Check if the image is bigger than the banner
        if img.size > self.dimension:
            width, height = self.dimension
            img = resize(img, (width // 2, height // 2))
        # Add image
        self.image.paste(img, position)


class FontWall:
    """
    Class that represents the wall of fonts
    """

    def __init__(self, fonts, max_width=3306, max_height=1120, max_tile=2, mode='horizontal'):
        """
        Object that represents the wall of fonts
        :param max_tile: maximum tile per row
        :param fonts: font list; string or FontPreview object
        :param max_width: maximum possible width for the wall
        :param max_height: maximum possible height for the wall
        :param mode: image alignment, 'horizontal' or 'vertical'
        """
        # Check if list contains string or FontPreview object
        if isinstance(fonts, list):
            self.fonts = []
            for font in fonts:
                if isinstance(font, FontPreview):
                    self.fonts.append(font)
                else:
                    _font = FontBanner(font)
                    self.fonts.append(_font)
        else:
            raise TypeError("'fonts' must be a list")
        # Other properties
        self.color_system = 'RGB'
        self.bg_color = 'white'
        self.max_width = max_width
        self.max_height = max_height
        self.mode = mode
        self.max_tile = max_tile
        # Build the wall
        self.wall = Image.new(self.color_system, (max_width, max_height), color=self.bg_color)
        self.draw(self.max_tile)

    def __concatenate(self, img1, img2, position):
        """
        Link multiple images to form a layout inside the wall
        :param img1: first image
        :param img2: second image
        :param position: paste positions
        :return: tuple
        """
        # Compose the wall
        if self.mode == 'horizontal':
            dst = Image.new(self.color_system, (img1.image.width + img2.image.width, img1.image.height))
            dst.paste(img1.image, (0, 0))
            dst.paste(img2.image, (img1.image.width, 0))
            self.wall.paste(dst, position)
        elif self.mode == 'vertical':
            dst = Image.new(self.color_system, (img1.image.width, img1.image.height + img2.image.height))
            dst.paste(img1.image, (0, 0))
            dst.paste(img2.image, (0, img1.image.height))
            self.wall.paste(dst, position)
        else:
            raise ValueError("the mode can be 'horizontal' or 'vertical'")
        return dst.size

    def draw(self, max_tile):
        """
        Draw wall with fonts on properties of this object
        :param max_tile: maximum tile per row
        :return: None
        """
        start_position = (0, 0)
        for f in range(0, len(self.fonts), max_tile):
            last_position = self.__concatenate(self.fonts[f], self.fonts[f + 1], start_position)
            print(start_position)
            start_position = (0, (start_position[1] + last_position[1]))

# endregion
