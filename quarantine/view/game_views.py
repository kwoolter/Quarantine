import quarantine.model as model
from .graphics import *


class LocationView(View):

    MODE_VISIBLE_OBJECT = "visible objects"
    MODE_OBJECT_CONTENTS = "object contents"

    def __init__(self, model: model.QModel, width:int =0, height=0):

        super().__init__()

        # Properties
        self.model = model
        self.width = width
        self.height = height
        self.bg_text = Colours.DARK_GREY
        self.fg_text = Colours.WHITE
        self.mode = LocationView.MODE_VISIBLE_OBJECT

        # Components
        self.next_location_selection = 0
        self.next_locations = []
        self.location_images = []

        self.objects_view = ObjectsView("Visible Objects", self.width, 110)
        self.object_contents_view = ObjectsView("Object Contents", self.width, 110)


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

        if new_event.name == model.Event.GAME_MODEL_CHANGED:
            object_list = self.model.get_objects_at_location()
            self.objects_view.initialise(object_list)
            self.object_contents_view.initialise(object_list)


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
        if self.mode == LocationView.MODE_VISIBLE_OBJECT:
            self.objects_view.set_selected_object(new_object_id, increment)
        elif self.mode == LocationView.MODE_OBJECT_CONTENTS:
            self.object_contents_view.set_selected_object(new_object_id, increment)

    def get_selected_object(self):
        if self.mode == LocationView.MODE_VISIBLE_OBJECT:
            return self.objects_view.get_selected_object()
        elif self.mode == LocationView.MODE_OBJECT_CONTENTS:
            return self.object_contents_view.get_selected_object()

    def set_mode(self, new_mode : str):

        if new_mode == LocationView.MODE_OBJECT_CONTENTS:
            obj = self.get_selected_object()
            if obj is not None and obj.get_property("IsContainer") is True:
                self.mode = new_mode
                self.object_contents_view.initialise(self.model.get_objects_at_location(obj.name))
        else:
            self.mode = new_mode


    def draw(self):
        self.surface.fill(Colours.BLACK)
        pane_rect = self.surface.get_rect()

        photo_img = self.location_images[self.location_image_selection]

        alpha = self.model.get_light_at_location()
        photo_img.set_alpha(alpha)

        self.surface.blit(photo_img, (0, 0))
        self.surface.blit(self.icon_img, (4,4))

        location = self.model.current_location

        x = pane_rect.centerx
        y = 18

        draw_text(self.surface,
                  msg=f"{location.name:^30}",
                  size=40,
                  x=x,
                  y=y,
                  fg_colour=self.fg_text,
                  bg_colour=self.bg_text)

        y+=20

        msg=str(self.model.timer)

        draw_text(self.surface,
                  msg=f"{msg:^30}",
                  size=16,
                  x=x,
                  y=y,
                  fg_colour=self.fg_text,
                  bg_colour=self.bg_text)

        obj_view = None
        if self.mode == LocationView.MODE_VISIBLE_OBJECT:
            obj_view = self.objects_view
        elif self.mode == LocationView.MODE_OBJECT_CONTENTS:
            obj_view = self.object_contents_view

        if obj_view is not None:
            obj_view.draw()
            obj_rect = obj_view.surface.get_rect()
            obj_rect.bottom = pane_rect.bottom
            self.surface.blit(obj_view.surface, obj_rect.topleft)

        icon_size = 64
        text_size = 16
        padding = 20

        y = obj_rect.top - icon_size - text_size - 4

        x = int(pane_rect.width + padding - len(self.next_locations) * (icon_size + text_size))/2

        for i, location in enumerate(self.next_locations):
            icon_file = location.get_property("Icon File")
            icon_img = View.image_manager.get_image(icon_file, width=icon_size, height=icon_size)
            self.surface.blit(icon_img, (x,y))

            icon_rect = icon_img.get_rect()
            icon_rect.topleft = (x,y)

            if i==self.next_location_selection:
                pygame.draw.rect(self.surface, Colours.RED, icon_rect, 4)
                
            draw_text(self.surface,
                      msg=f" {i+1}) {location.name} ",
                      x=icon_rect.centerx,
                      y=icon_rect.bottom + 10,
                      fg_colour=self.fg_text,
                      bg_colour=self.bg_text,
                      size = text_size)

            x+= icon_size + padding




class ObjectsView(View):

    def __init__(self, view_title:str ="Objects", width: int = 0, height=0):

        super().__init__()

        self.model = model
        self.width = width
        self.height = height
        self.view_title = view_title.title()
        self.bg = Colours.DARK_GREY
        self.fg = Colours.WHITE

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
            pass

    def get_selected_object(self):
        if len(self.objects) == 0:
            return None
        else:
            return self.objects[self.object_selection]

    def draw(self):
        self.surface.fill(self.bg)
        pane_rect = self.surface.get_rect()

        x = pane_rect.centerx
        y = 12

        draw_text(self.surface,
                  msg=self.view_title,
                  size=24,
                  x=x,
                  y=y,
                  bg_colour=self.bg,
                  fg_colour=self.fg
                  )

        icon_size = 64
        text_size = 16
        padding = 20

        x = int((pane_rect.width + padding - len(self.objects) * (icon_size + padding))/2)

        y = pane_rect.bottom - icon_size - text_size - 2

        for i, o in enumerate(self.objects):
            icon_file = o.get_property("Icon File")
            icon_img = View.image_manager.get_image(icon_file, width=icon_size, height=icon_size)
            self.surface.blit(icon_img, (x, y))

            icon_rect = icon_img.get_rect()
            icon_rect.topleft = (x, y)

            if i == self.object_selection:
                pygame.draw.rect(self.surface, Colours.RED, icon_rect, 4)

            if o.get_property("IsContainer") is True:

                contents = model.QObjectFactory.get_objects_by_location(o.name)

                draw_text(self.surface,
                          msg=f"+{len(contents)}",
                          x=icon_rect.x,
                          y=icon_rect.y + 10,
                          bg_colour=self.bg,
                          fg_colour=self.fg,
                          size=30,
                          centre=False)


            draw_text(self.surface,
                      msg=f"{i + 1}){o.description}",
                      x=icon_rect.centerx,
                      y=icon_rect.bottom + 10,
                      bg_colour=self.bg,
                      fg_colour=self.fg,
                      size=text_size)

            x += icon_size + padding

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
        y = 10

        draw_text(self.surface,
                  msg=f"Player {self.model.name}",
                  size=20,
                  x=x,
                  y=y)

        x = pane_rect.centerx
        y+= 20

        for property, val in self.model.properties.items():
            draw_text(self.surface,
                      msg=f"{property.title()} : {val}%",
                      size=16,
                      x=x,
                      y=y)
            y+=16

