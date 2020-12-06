from quarantine.model import QModel
from .graphics import *


class LocationView(View):

    def __init__(self, model: QModel, width:int =0, height=0):

        super().__init__()

        self.model = model
        self.width = width
        self.height = height

        self.next_location_selection = 0
        self.next_locations = []

        self.objects_view = ObjectsView(self.model, self.width, 100)


    def initialise(self):
        super().initialise()

        self.surface = pygame.Surface((self.width, self.height))

        icon_file = self.model.current_location.get_property("Icon File")
        image_file = self.model.current_location.get_property("Image File")

        self.icon_img = View.image_manager.get_image(icon_file, width=64, height=64)
        self.photo_img = View.image_manager.get_image(image_file, width=self.width, height=self.height)

        self.next_locations = sorted(list(self.model.current_location.linked_locations.values()), key=lambda k:k.name )
        self.set_next_location(0)

        self.objects_view.initialise()

    def set_next_location(self, new_location_id : int, increment:bool = False):

        print(f"in:{new_location_id}")

        if increment is True:
            new_location_id = self.next_location_selection + new_location_id

        new_location_id -= 1

        self.next_location_selection = max(0,min(new_location_id, len(self.next_locations)-1))

        print(f"in:{new_location_id} out:{self.next_location_selection}")

    def get_selected_new_location(self):
        return self.next_locations[self.next_location_selection]

    def set_selected_object(self, new_object_id: int, increment: bool = False):
        self.objects_view.set_selected_object(new_object_id, increment)

    def draw(self):
        self.surface.fill(Colours.BLUE)
        pane_rect = self.surface.get_rect()

        self.surface.blit(self.photo_img, (0, 0))
        self.surface.blit(self.icon_img, (4,4))

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

        icon_size = 64
        text_size = 16

        y = pane_rect.bottom - icon_size - text_size - 16

        for i, location in enumerate(self.next_locations):
            icon_file = location.get_property("Icon File")
            icon_img = View.image_manager.get_image(icon_file, width=icon_size, height=icon_size)
            self.surface.blit(icon_img, (x,y))

            icon_rect = icon_img.get_rect()
            icon_rect.topleft = (x,y)

            if i==self.next_location_selection:
                pygame.draw.rect(self.surface, Colours.RED, icon_rect, 4)
                
            draw_text(self.surface,
                      msg=f"{i+1}){location.name}",
                      x=icon_rect.centerx,
                      y=icon_rect.bottom + 10,
                      bg_colour=Colours.BLUE,
                      size = text_size)

            x+= icon_size + 10

        self.objects_view.draw()
        self.surface.blit(self.objects_view.surface, (0, pane_rect.bottom - 200))


class ObjectsView(View):

    def __init__(self, model: QModel, width: int = 0, height=0):

        super().__init__()

        self.model = model
        self.width = width
        self.height = height

        self.object_selection = 0
        self.objects = []

    def initialise(self):
        super().initialise()

        self.surface = pygame.Surface((self.width, self.height))

        self.objects = self.model.get_objects_at_location()
        self.set_selected_object(0)

    def set_selected_object(self, new_object_id: int, increment: bool = False):

        if increment is True:
            new_object_id = self.next_location_selection + new_object_id

        new_object_id -= 1

        self.object_selection = max(0, min(new_object_id, len(self.objects) - 1))


    def get_selected_object(self):
        return self.objects[self.object_selection]

    def draw(self):
        self.surface.fill(Colours.GREEN)
        pane_rect = self.surface.get_rect()

        x = pane_rect.centerx
        y = 18

        draw_text(self.surface,
                  msg="Objects",
                  size=30,
                  x=x,
                  y=y)

        x = 10

        icon_size = 64
        text_size = 16

        y = pane_rect.bottom - icon_size - text_size - 16

        for i, o in enumerate(self.objects):
            icon_file = o.get_property("Icon File")
            icon_img = View.image_manager.get_image(icon_file, width=icon_size, height=icon_size)
            self.surface.blit(icon_img, (x, y))

            icon_rect = icon_img.get_rect()
            icon_rect.topleft = (x, y)

            if i == self.object_selection:
                pygame.draw.rect(self.surface, Colours.RED, icon_rect, 4)

            draw_text(self.surface,
                      msg=f"{i + 1}){o.name}",
                      x=icon_rect.centerx,
                      y=icon_rect.bottom + 10,
                      bg_colour=Colours.BLUE,
                      size=text_size)

            x += icon_size + 10

