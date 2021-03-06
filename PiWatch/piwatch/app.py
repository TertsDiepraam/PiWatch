"""Defines the classes for the construction of PiWatch-apps."""
import os

from .event import EventHandler
from .event import EventListener


class Activity(EventListener):
    """Represents one "page" of an application. This contains Drawables.
    """
    def __init__(self, name):
        self.name = name
        self.objects = []  # later objects are drawn OVER earlier objects
        EventListener.__init__(self)

    def add(self, *args):
        for object in args:
            self.objects.append(object)

    def clear(self):
        self.objects = []

    def setup(self, parent):
        for object in self.objects:
            object.setup(parent)

    def draw(self, surface):
        for object in self.objects:
            if object.visible:
                object.draw(surface)


class App(EventHandler):
    """The object that represents the app itself. Used for screen-filling graphical applications.
    """
    def __init__(self, name='app', bg_color=(0, 0, 0), icon=None):
        self.name = name
        self.icon = icon
        self.bg_color = bg_color
        self.activities = {}
        self.mainactivity = 'main'
        self.current_activity = None
        self.folder = ('apps' + os.sep + name.lower() + os.sep).replace(' ', '_')
        EventHandler.__init__(self)
        self.started = False

    def start(self, parent):
        self.parent = parent
        self.set_activity('main')
        self.started = True

    def add(self, *args):
        for activity in args:
            self.activities[activity.name] = activity

    def draw(self, surface):
        self.current_activity.draw(surface)

    def get_event_listeners(self):
        d1 = self.event_listeners.copy()
        d1_keys = d1.keys()
        d2 = self.current_activity.get_event_listeners().items()
        for key, value in d2:
            if key in d1_keys:
                d1[key] += value
            else:
                d1[key] = value
        return d1

    def set_activity(self, act_name):
        self.current_activity = self.activities[act_name]
        self.current_activity.setup(self.parent)


class Overlay(App):
    """Represents a little bit of graphical information, drawn over the main application.
    It is just an alias for App.
    """
    pass


class Service(EventHandler):
    """Represents a non-graphical application, which is run in the background.
    """
    def __init__(self, name='Anonymous Service'):
        self.name = name
        EventHandler.__init__(self)

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def pause(self):
        raise NotImplementedError()
