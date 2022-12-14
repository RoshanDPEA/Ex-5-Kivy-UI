import os

os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.animation import Animation

from datetime import datetime

from random import random
from kivy.clock import Clock
from kivy.properties import StringProperty
import pygame

#pygame.init()
from pidev.Joystick import Joystick

#stick = Joystick(0, False)
#print(stick.get_axis('x'), stick.get_axis('y'))

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Clock.schedule_interval(self.update_stick, 0.01)

    def backroundChangeMain(self):
        SCREEN_MANAGER.current = 'button'

    # def stickShow(self):
    # self.ids.stick.text = str(stick.get_axis('x')) + " " + str(stick.get_axis('y'))

    #def update_stick(self, dt):
    #    self.ids.stick1.x = self.width * stick.get_axis('x')
    #    self.ids.stick1.y = self.height * stick.get_axis('y')



    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def toggleMotor(self):
        if self.ids.mtr.text == 'motor off':
            self.ids.mtr.text = 'motor on'
        else:
            self.ids.mtr.text = 'motor off'

    def toggleText(self):
        if self.ids.btn.text == 'on':
            self.ids.btn.text = 'off'
        else:
            self.ids.btn.text = 'on'

    def counter(self):
        self.ids.cnt.i += 1
        self.ids.cnt.text = str(self.ids.cnt.i)

    def animate_it(self, widget, *args):
        # Define The Animation you want to do
        animate = Animation(
            background_color=(0, 0, 1, 1),
            duration=1)

        # Do second animation
        animate += Animation(
            size_hint=(1, 1))

        # Do Third animation
        animate += Animation(
            size_hint=(.5, .5))

        animate += Animation(
            pos_hint={"center_x": 0.1})

        animate += Animation(
            pos_hint={"center_x": 0.5})

        # Start The Animation
        animate.start(widget)

        # Create a callback
        animate.bind(on_complete=self.my_callback)

        SCREEN_MANAGER.current = 'button'

    def my_callback(self, *args):
        self.ids.my_label.text = "Wow! Look At That!"

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class Screen2(Screen):
    def imageToggle(self):
        SCREEN_MANAGER.current = 'main'

    def animate_it(self, widget, *args):
        # Define The Animation you want to do
        animate = Animation(
            background_color=(0, 0, 1, 1),
            duration=1)

        # Do second animation
        animate += Animation(
            size_hint=(1, 1))

        # Do Third animation
        animate += Animation(
            size_hint=(.5, .5))

        animate += Animation(
            pos_hint={"center_x": 0.1})

        animate += Animation(
            pos_hint={"center_x": 0.5})

        # Start The Animation
        animate.start(widget)

        # Create a callback
        animate.bind(on_complete=self.my_callback)

        SCREEN_MANAGER.current = 'main'

    def my_callback(self, *args):
        self.ids.my_label.text = "Wow! Look At That!"


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(Screen2(name='button'))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
