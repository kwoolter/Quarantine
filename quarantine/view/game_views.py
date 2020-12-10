import quarantine.model as model
from .graphics import *


class LocationView(View):

    def __init__(self, model: model.QModel, width:int =0, height=0):

        super().__init__()

        # Properties
        self.model = model
        self.width = width
        self.height = height

        # Components
        self.next_location_selection = 0
        self.next_locations = []
        self.location_images = []

        self.objects_view = ObjectsView("Visible Objects", self.width, 100)


    def initialise(self):

        super().initialise()

        self.surface = pygame.Surface((self.width, self.height))

        icon_file = self.model.current_location.get_property("Icon File")
        self.icon_img = View.image_manager.get_image(icon_file, width=64, height=64)

        image_files = self.model.current_location.get_property("Image File")
        self.location_images = []
        for file_name in image_files.split(","):
            photo_img = View.image_manager.get_image(file_name.strip(), width=self.width, height=self.height)
            self.location_images.append(photo_img)

        self.set_location_image(0)

        self.next_locations = sorted(list(self.model.current_location.linked_locations.values()), key=lambda k:k.name )
        self.set_next_location(0)

        object_list = self.model.get_objects_at_location()
        self.objects_view.initialise(object_list)

    def process_event(self, new_event: model.Event):
        self.objects_view.process_event(new_event)

    def set_location_image(self, image_number : int, increment : bool = False, wrap: bool = True):

        if increment is True:
            image_number = self.location_image_selection + image_number
            if wrap is True:
                if image_number >= len(self.location_images):
                    image_number = 0
                elif image_number < 0:
                    image_number = len(self.location_images) - 1

        self.location_image_selection = max(0, min(len(self.location_images) - 1, image_number))

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

    def get_selected_object(self):
        return self.objects_view.get_selected_object()

    def draw(self):
        self.surface.fill(Colours.BLUE)
        pane_rect = self.surface.get_rect()

        photo_img = self.location_images[self.location_image_selection]

        self.surface.blit(photo_img, (0, 0))
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

    def __init__(self, view_title:str ="Objects", width: int = 0, height=0):

        super().__init__()

        self.model = model
        self.width = width
        self.height = height
        self.view_title = view_title.title()

        self.object_selection = 0
        self.objects = []

    def initialise(self, object_list:list):
        super().initialise()

        self.surface = pygame.Surface((self.width, self.height))

        self.objects = object_list
        self.set_selected_object(0)

    def set_selected_object(self, new_object_id: int, increment: bool = False):

        if increment is True:
            new_object_id = self.next_location_selection + new_object_id

        new_object_id -= 1

        self.object_selection = max(0, min(new_object_id, len(self.objects) - 1))

    def process_event(self, new_event: model.Event):
        if new_event.name == model.Event.GAME_MODEL_CHANGED:
            self.initialise()


    def get_selected_object(self):
        return self.objects[self.object_selection]

    def draw(self):
        self.surface.fill(Colours.WHITE)
        pane_rect = self.surface.get_rect()

        x = pane_rect.centerx
        y = 18

        draw_text(self.surface,
                  msg=self.view_title,
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
                      bg_colour=Colours.WHITE,
                      fg_colour=Colours.BLUE,
                      size=text_size)

            x += icon_size + 10

class PlayerView(View):

    def __init__(self, model: model.QPlayer, width: int = 0, height=0):

        super().__init__()

        self.model = model
        self.width = width
        self.height = height


    def initialise(self):
        super().initialise()

        self.surface = pygame.Surface((self.width, self.height))

    def process_event(self, new_event: model.Event):
        pass

    def draw(self):
        self.surface.fill(Colours.BLACK)
        pane_rect = self.surface.get_rect()

        x = pane_rect.centerx
        y = 18

        draw_text(self.surface,
                  msg=f"Player {self.model.name}",
                  size=30,
                  x=x,
                  y=y)

        x = pane_rect.centerx
        y+= 30

        for property, val in self.model.properties.items():
            draw_text(self.surface,
                      msg=f"{property} : {val}",
                      size=24,
                      x=x,
                      y=y)
            y+=20

