from quarantine.model import QModel
from .graphics import *


class LocationView(View):

    def __init__(self, model: QModel, width:int =0, height=0):

        super().__init__()

        self.model = model
        self.width = width
        self.height = height

    def initialise(self, model: QModel):
        super().initialise()
        self.surface = pygame.Surface((self.width, self.height))

        icon_file = self.model.current_location.get_property("Icon File")
        image_file = self.model.current_location.get_property("Image File")

        self.icon_img = View.image_manager.get_image(icon_file, width=64, height=64)
        self.photo_img = View.image_manager.get_image(image_file, width=self.width)

    def draw(self):
        self.surface.fill(Colours.BLUE)
        pane_rect = self.surface.get_rect()


        self.surface.blit(self.photo_img, (0, 0))

        self.surface.blit(self.icon_img, (10,10))

        location = self.model.current_location

        x = pane_rect.centerx
        y = 18

        draw_text(self.surface,
                  msg=f"{location.name:^30}",
                  size=40,
                  x=x,
                  y=y)

        y+=30

        msg=str(self.model.timer)

        draw_text(self.surface,
                  msg=f"{msg:^30}",
                  size=16,
                  x=x,
                  y=y)

        x = 10
        y = 300
        icon_size = 64

        for location in self.model.current_location.linked_locations.values():
            icon_file = location.get_property("Icon File")
            icon_img = View.image_manager.get_image(icon_file, width=icon_size, height=icon_size)
            self.surface.blit(icon_img, (x,y))
            x+= icon_size + 10





