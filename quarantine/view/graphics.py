import pygame
import logging
import os

class Colours:
    # set up the colours
    BLACK = (0, 0, 0)
    BROWN = (128, 64, 0)
    WHITE = (255, 255, 255)
    RED = (237, 28, 36)
    DARK_RED = (100, 0, 0)
    GREEN = (34, 177, 76)
    DARK_GREEN = (0, 100, 0)
    BLUE = (63, 72, 204)
    DARK_GREY = (40, 40, 40)
    GREY = (128, 128, 128)
    LIGHT_GREY = (200,200,200)
    GOLD = (255, 201, 14)
    YELLOW = (255, 255, 0)
    TRANSPARENT = (255, 1, 1)

def draw_text(surface, msg, x, y, size=32, fg_colour=Colours.WHITE, bg_colour=Colours.BLACK, alpha: int = 255,
              centre: bool = True):
    font = pygame.font.Font(None, size)
    if bg_colour is not None:
        text = font.render(msg, 1, fg_colour, bg_colour)
    else:
        text = font.render(msg, 1, fg_colour)
    textpos = text.get_rect()

    if centre is True:
        textpos.centerx = x
    else:
        textpos.x = x

    textpos.centery = y
    surface.blit(text, textpos)
    surface.set_alpha(alpha)


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        textpos = image.get_rect()
        textpos.centerx = rect.centerx
        textpos.y = y

        surface.blit(image, (textpos))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except Exception as err:
            print('Unable to load spritesheet image:', filename)
            raise err

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle=None, colorkey=None):
        if rectangle is None:
            rectangle = self.sheet.get_rect()
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, depth=24)
        key = (0, 255, 0)
        image.fill(key)
        image.set_colorkey(key)
        image.blit(self.sheet, (0, 0), rect)

        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class ImageManager:
    DEFAULT_SKIN = "default"
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    image_cache = {}
    skins = {}
    sprite_sheets = {}
    initialised = False

    def __init__(self):
        pass

    def initialise(self):
        if ImageManager.initialised is False:
            self.load_skins()
            self.load_sprite_sheets()

    def get_image(self, image_file_name: str, width: int = 0, height: int = 0):

        transparent = pygame.Color(255, 22, 33)

        if image_file_name not in ImageManager.image_cache.keys():

            if image_file_name in self.sprite_sheets.keys():
                file_name, rect = self.sprite_sheets[image_file_name]
                filename = ImageManager.RESOURCES_DIR + file_name
                logging.info("Loading image {0} from {1} at {2}...".format(image_file_name, filename, rect))

                image_sheet = spritesheet(filename)
                original_image = image_sheet.image_at(rect)
            else:
                filename = ImageManager.RESOURCES_DIR + image_file_name
                logging.info("Loading image {0}...".format(filename))
                image_sheet = spritesheet(filename)
                original_image = image_sheet.image_at()

            try:

                img_rect = original_image.get_rect()

                if width == 0:
                    width = img_rect.width
                if height == 0:
                    height = img_rect.height

                image = pygame.transform.scale(original_image, (width, height))
                smallest_size = image.get_bounding_rect()
                print(f'{image_file_name}:{image.get_rect()} smallest={smallest_size}')
                cropped_image = pygame.Surface((smallest_size.width, smallest_size.height))
                cropped_image.fill(transparent)
                cropped_image.blit(image, dest=(0,0), area= smallest_size)
                cropped_image.set_colorkey(transparent)
                ImageManager.image_cache[image_file_name] = cropped_image
                #ImageManager.image_cache[image_file_name] = original_image
                logging.info("Image {0} loaded and scaled to {1}x{2} and cached.".format(filename, width, height))

            except Exception as err:
                print(str(err))

        return self.image_cache[image_file_name]

    def load_skins(self):

        new_skin_name = ImageManager.DEFAULT_SKIN
        new_skin = (new_skin_name, {

            "EMPTY": None,

        })

        ImageManager.skins[new_skin_name] = new_skin

    def get_skin_image(self, tile_name: str, skin_name: str = DEFAULT_SKIN, tick=0, width: int = 32, height: int = 32):

        if skin_name not in ImageManager.skins.keys():
            raise Exception("Can't find specified skin {0}".format(skin_name))

        name, tile_map = ImageManager.skins[skin_name]

        if tile_name not in tile_map.keys():
            name, tile_map = ImageManager.skins[ImageManager.DEFAULT_SKIN]
            if tile_name not in tile_map.keys():
                raise Exception("Can't find tile name '{0}' in skin '{1}'!".format(tile_name, skin_name))

        tile_file_names = tile_map[tile_name]

        image = None

        if tile_file_names is None:
            image = None
        elif isinstance(tile_file_names, tuple):
            if tick == 0:
                tile_file_name = tile_file_names[0]
            else:
                tile_file_name = tile_file_names[tick % len(tile_file_names)]

            image = self.get_image(image_file_name=tile_file_name, width=width, height=height)

        else:
            image = self.get_image(tile_file_names, width=width, height=height)

        return image

    def load_sprite_sheets(self):

        sheet_file_name = "tiles64x64.png"
        for i in range(0, 7):
            self.sprite_sheets["tiles64:{0}.png".format(i)] = (sheet_file_name, (i * 64, 0, 64, 64))

class View():
    image_manager = ImageManager()

    def __init__(self, width: int = 0, height: int = 0):
        self._debug = False
        self.tick_count = 0
        self.height = height
        self.width = width
        self.surface = None

    def initialise(self):
        pass

    def tick(self):
        self.tick_count += 1

    def debug(self, debug_on: bool = None):

        if debug_on is None:
            self._debug = not self._debug
        else:
            self._debug = debug_on

    def draw(self):
        pass
