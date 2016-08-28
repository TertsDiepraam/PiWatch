from .drawable import *

class GroupAttrs(AttrSet):
    def set_defaults(self):
        super().set_defaults()
        self.attrs.update(
            children=[]
        )


class Group(PiDrawable):
    DEFAULTATTRS = GroupAttrs()

    def add(self, *args):
        for child in args:
            self.children.append(child)
            if hasattr(self, 'parent'):
                child.setup(self.parent)
        if hasattr(self, 'parent'):
            self.set_position()

    def clear(self):
        self.children = []

    def setup(self, parent):
        self.parent = parent
        for child in self.children:
            child.setup(parent)
        self.set_position()

    def set_position(self):
        for child in self.chilren:
            child.set_position()
        self.rect = self.children[0].rect.unionall([child.rect for child in self.children[1:]])

    def draw(self, surface):
        if self.bg_color:
            surface.fill(self.bg_color, self.rect)
        for child in self.children:
            child.draw(surface)

class ListAttrs(GroupAttrs):
    def set_defaults(self):
        super().set_defaults()
        self.attrs.update(
            direction='down',
            padding=0,
        )

class List(Group):
    DEFAULTATTRS = ListAttrs()

    def set_position(self):
        offset_x = 0
        offset_y = 0
        if self.children:
            for child in self.children:
                if type(child) is str:
                    child = str_to_text(child)
                child.update(position=(self.position[0], self.position[1]+offset_x, self.position[2]+offset_y))
                if self.direction == 'down':
                    offset_y += child.rect.height + self.padding[0]
                elif self.direction == 'up':
                    offset_y -= child.rect.height - self.padding[0]
                elif self.direction == 'right':
                    offset_x += child.rect.width + self.padding[1]
                elif self.direction == 'left':
                    offset_x -= child.rect.width - self.padding[1]
                else:
                    raise AttributeError('List.direction must be up, down, left or right')
            self.rect = self.children[0].rect.unionall([child.rect for child in self.children[1:]])
        else:
            self.rect = None
