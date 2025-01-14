#!/usr/bin/env python3
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

from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from PIL import Image

from .fontpreview import FontPreview


def resize(image, bg_image, ratio=1.2):
    """
    Resize image.

    :param image: image to resize
    :param bg_image: background image
    :return: Image object
    """
    # Check size of background image
    new_size = image.size
    while new_size > bg_image.size:
        width, height = new_size
        new_size = (int(width // ratio), int(height // ratio))

    # Resize image
    return image.resize(new_size)


class FontBanner(FontPreview):
    """
    Class that represents the banner of a font.
    """

    def __init__(
        self,
        font,
        orientation='landscape',
        bg_color='white',
        fg_color='black',
        mode='letter',
        font_size=64,
        color_system='RGB',
    ):
        """
        Object that represents the banner of a font.

        :param font: font file
        :param orientation: the orientation of the banner;
            'landscape', 'portrait' or tuple(x,y).
        :param bg_color: background color of preview. Default is 'white'.
        :param fg_color: foreground or font color of preview. Default is 'black'.
        :param mode: the text inside the banner; 'letter','fontname', 'paragraph',
            'alpha' and 'combination'.
        :param font_size: font size. Default is 64.
        :param color_system: color system string. Default is 'RGB'.
        """
        # Define properties
        FontPreview.__init__(
            self,
            font=font,
            bg_color=bg_color,
            fg_color=fg_color,
            font_size=font_size,
            color_system=color_system,
        )
        self.set_orientation(orientation)
        self.mode = mode
        self.set_text_position('center')

        # Create default image
        self.set_mode(mode=self.mode)

    def __str__(self):
        """
        String representation of font banner.

        :return: string
        """
        return FontPreview.__str__(self) + f',mode={self.mode}'

    def set_orientation(self, orientation, font_position='center'):
        """
        Set orientation of banner.

        :param orientation: the orientation of the banner; 'landscape' or 'portrait'
        :param font_position: font position respect dimension of banner
        :return: None
        """
        # Calculate banner size
        if isinstance(orientation, tuple):
            self.dimension = orientation
            # Recalculate font position
            self.set_text_position(font_position)
            return

        if orientation == 'landscape':
            self.dimension = (1653, 560)
        elif orientation == 'portrait':
            self.dimension = (560, 1653)
        else:
            msg = 'orientation is "landscape","portrait" or tuple(x,y)'
            raise ValueError(msg)

        # Recalculate font position
        self.set_text_position(font_position)

    def set_mode(
        self,
        mode: Literal['letter', 'alpha', 'fontname', 'combination', 'none'],
        align='center',
    ):
        """
        Set the text mode.

        :param mode: mode that sets the text in the banner
        :param align: alignment of text. Available 'left', 'center' and 'right'
        :return: None
        """
        modes = {
            'letter': 'a b c d e f\ng h i j k l\nm n o p q r\ns t u v w x y z',
            'alpha': 'Aa Bb Cc Dd Ee Ff\n1 2 3 4 5 6 7 8 9 0',
            'fontname': f'{self.font.getname()[0]}',
            'paragraph': 'Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit.',
            'combination': '{}\n{}'.format(
                self.font.getname(),
                'Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit.',
            ),
            'none': '',
        }
        # Verify is mode exists
        if mode in modes:
            self.mode = mode
            self.font_text = modes.get(mode)

            # Create default image
            self.draw(align=align)
        else:
            msg = 'mode is "letter", "alpha", "fontname", "paragraph" and "combination"'
            raise ValueError(msg)

    def add_image(self, image: str | Path | FontPreview, position):
        """
        Adds an additional image to the banner.

        :param image: path of image
        :param position: position of image
        :return: None
        """
        # Create image
        img = image.image if isinstance(image, FontPreview) else Image.open(image)
        if not img:
            raise ValueError(image)

        # Check if the image is bigger than the banner
        if img.size > self.dimension:
            img = resize(img, self.image)

        # Add image
        self.image.paste(img, position)


class FontLogo(FontPreview):
    """
    Class that represents the logo of a font.
    """

    def __init__(
        self,
        font,
        letters,
        size=(100, 100),
        bg_color='white',
        fg_color='black',
        font_size=64,
        color_system='RGB',
    ):
        """
        Object that represents the logo of a font.

        :param font: font file
        :param letters: One or two letters (or anything)
        :param size: size of logo square. Default is (100, 100)
        :param bg_color: background color of preview. Default is 'white'.
        :param fg_color: foreground or font color of preview. Default is 'black'.
        :param font_size: font size. Default is 64.
        :param color_system: color system string. Default is 'RGB'.
        """
        FontPreview.__init__(
            self,
            font=font,
            bg_color=bg_color,
            fg_color=fg_color,
            font_size=font_size,
            color_system=color_system,
        )
        # Check if the letters exceed the number 2
        if len(letters) > 2:  # noqa: PLR2004
            msg = 'letters can be maximum two'
            raise ValueError(msg)

        self.font_text = letters

        # Check maximum size
        self.__max_size(size)

        # Set letter position
        self.set_text_position('center')

        # Built a logo font
        self.draw()

    def __max_size(self, size):
        """
        Check maximum size.

        :param size: New size
        :return: None
        """
        max_size = ((75, 75), (100, 100), (150, 150), (170, 170))
        if size in max_size:
            self.dimension = size
        else:
            msg = f'The max size of the logo can be this: {max_size}'
            raise ValueError(msg)

    def new_size(self, size):
        """
        Define new size of FontLogo object.

        :param size: size of fontlogo object
        :return: None
        """
        # Check maximum size
        self.__max_size(size)

        # Built a logo font
        self.set_text_position('center')


class FontWall:
    """
    Class that represents the wall of fonts.
    """

    def __init__(
        self,
        fonts: Iterable[str | FontPreview],
        max_tile=2,
        mode: Literal['horizontal', 'vertical'] = 'horizontal',
    ):
        """
        Object that represents the wall of fonts.

        :param fonts: font list; string or FontPreview object
        :param max_tile: maximum tile per row/column
        :param mode: image alignment, 'horizontal' or 'vertical'
        """
        if mode not in {'horizontal', 'vertical'}:
            raise ValueError(mode)

        self.fonts = [f if isinstance(f, FontPreview) else FontBanner(f) for f in fonts]

        # Other properties
        self.color_system = 'RGB'
        self.bg_color = 'white'
        self.max_width = 0
        self.max_height = 0
        self.mode = mode
        self.max_tile = max_tile

        # Build the wall
        self.wall: Image.Image
        self.draw(self.max_tile)

    def __str__(self):
        """
        String representation of font wall.

        :return: string
        """
        return str([f'tile{i}={f}' for i, f in enumerate(self.fonts)])

    def __concatenate(self, fonts, position):
        """
        Link multiple images to form a layout inside the wall.

        :param fonts: list of FontPreview
        :param position: paste positions
        :return: tuple
        """
        # Get max width and height, presume horizontal
        if self.mode == 'horizontal':
            max_width = sum(font.image.width for font in fonts)
            max_height = max(font.image.height for font in fonts)
        else:
            max_width = max(font.image.width for font in fonts)
            max_height = sum(font.image.height for font in fonts)

        # Create background
        dst = Image.new(self.color_system, (max_width, max_height))
        start = 0
        for font in fonts:
            # Compose the row
            if self.mode == 'horizontal':
                dst.paste(font.image, (start, 0))
                start = font.image.width + start

            # Compose the column
            elif self.mode == 'vertical':
                dst.paste(font.image, (0, start))
                start = font.image.height + start

        self.wall.paste(dst, position)
        return dst.size

    def draw(self, max_tile):
        """
        Draw wall with fonts on properties of this object.

        :param max_tile: maximum tile per row
        :return: None
        """
        # Split fonts into maximum tile per row/column
        fonts = [
            self.fonts[i : i + max_tile] for i in range(0, len(self.fonts), max_tile)
        ]

        # Calculate max_width and max_height of wall
        max_width = []
        max_height = []
        for font in fonts:
            if self.mode == 'horizontal':
                max_width.append(sum(f.image.width for f in font))
                max_height.append(max(f.image.height for f in font))
            else:
                max_width.append(max(f.image.width for f in font))
                max_height.append(sum(f.image.height for f in font))
        if self.mode == 'horizontal':
            self.max_width = max(max_width)
            self.max_height = sum(max_height)
        else:
            self.max_width = sum(max_width)
            self.max_height = max(max_height)

        self.wall = Image.new(
            self.color_system, (self.max_width, self.max_height), color=self.bg_color
        )

        # Build the wall
        start_position = (0, 0)
        for font in fonts:
            if self.mode == 'horizontal':
                last_position = self.__concatenate(font, start_position)
                start_position = (0, (start_position[1] + last_position[1]))
            else:
                last_position = self.__concatenate(font, start_position)
                start_position = ((start_position[0] + last_position[0]), 0)

    def save(self, path=None):
        """
        Save the font wall.

        :param path: path where you want to save the font wall
        :return: None
        """
        path = path or Path() / 'fontwall.png'
        self.wall.save(path)

    def show(self):
        """
        Displays this image.

        :return: None
        """
        self.wall.show()
