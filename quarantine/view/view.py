import pygame
import os
import quarantine.model as model
from .graphics import *
import logging



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

    def get_image(self, image_file_name: str, width: int = 32, height: int = 32):

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

                image = pygame.transform.scale(original_image, (width, height))
                smallest_size = image.get_bounding_rect()
                print(f'{image_file_name}:{image.get_rect()} smallest={smallest_size}')
                cropped_image = pygame.Surface((smallest_size.width, smallest_size.height))
                cropped_image.fill(transparent)
                cropped_image.blit(image, dest=(0,0), area= smallest_size)
                cropped_image.set_colorkey(transparent)
                #ImageManager.image_cache[image_file_name] = cropped_image
                ImageManager.image_cache[image_file_name] = original_image
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

    def process_event(self, new_event: model.Event):
        print("Default View Class event process:{0}".format(new_event))

    def draw(self):
        pass


class QMainFrame(View):
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    TRANSPARENT = (0, 255, 0)

    def __init__(self, model: model.QModel):

        super().__init__()

        self._debug = False

        self.model = model
        self.surface = None
        self.width = 600
        self.height = 600
        self._debug = False

    def initialise(self):

        super().initialise()

        print("Initialising {0}".format(__class__))

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(self.model.name)

        self.surface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)

        filename = QMainFrame.RESOURCES_DIR + "icon.png"

        try:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (32,32))
            pygame.display.set_icon(image)
        except Exception as err:
            print(str(err))

    def print(self):

        print("Printing Dark Work view...")

    def draw(self):
        
        self.surface.fill(Colours.RED)
        self.surface.fill((0, 255, 0))

        pane_rect = self.surface.get_rect()

        x = 0
        y = 0

        img = View.image_manager.get_image("quarantine.png")
        self.surface.blit(img, (x, y))

        img = View.image_manager.get_image("photo1.png")
        img_rect = img.get_rect()
        img_rect.center = self.surface.get_rect().center
        self.surface.blit(img, (img_rect.x, img_rect.y))


    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):

        super().tick()


    def process_event(self, new_event: model.Event):

        super().process_event(new_event)

