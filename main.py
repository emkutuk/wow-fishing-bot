# -*- coding: utf-8 -*-
from cv2 import cv2
import numpy as np
import pyautogui
import time
import datetime
from PIL import ImageGrab


class WoWBot(object):
    threshold = 0.7
    image = cv2.imread("media/img-04.jpg", cv2.IMREAD_UNCHANGED)    
    locations = []
    oldLocation = []
    lastThrow = []

    def __init__(self):
        self.start_countdown()
        while True:            
            self.reset_lists()
            while self.match_found() is False:
                self.throw_pole()
                self.take_screenshot()
            self.catch_fish()

    def reset_lists(self):
        self.locations.clear()
        self.oldLocation.clear()
        self.lastThrow = datetime.datetime.now()

    def catch_fish(self):
        print(datetime.datetime.now().strftime(
            '%H:%M:%S') + "  Catching some fish...")
        while not self.match_found():
            self.take_screenshot()
        self.oldLocation = [self.locations[0][0], self.locations[0][1]]
        count = 0
        while True:
            self.take_screenshot()
            if not self.match_found():
                count += 1
                if count >= 1:
                    self.move_mouse_to_hook()
                    time.sleep(2)
                    return

    @staticmethod
    def throw_pole():
        print(datetime.datetime.now().strftime(
            '%H:%M:%S') + "  Throwing the pole...")
        pyautogui.press("1")
        time.sleep(2)

    def move_mouse_to_hook(self):
        pyautogui.moveTo(
            self.oldLocation[0] + 20,
            self.oldLocation[1] + 20,
            0.5)
        pyautogui.rightClick()
        print(datetime.datetime.now().strftime(
            '%H:%M:%S') + "  Caught the fish!")
        pyautogui.moveTo(pyautogui.size()[0] - 50, 20, 1)

    def match_found(self):
        if (datetime.datetime.now() - self.lastThrow).seconds > 30:
            print(datetime.datetime.now().strftime(
                '%H:%M:%S') + '  float lost, retrying')
            return False
        if len(self.locations) > 0:
            return True
        else:
            return False

    def take_screenshot(self):        
        template_image = cv2.cvtColor(
            np.array(
                ImageGrab.grab()),
            cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(
            template_image,
            self.image,
            cv2.TM_CCOEFF_NORMED)
        self.locations = np.where(result >= self.threshold)
        self.locations = list(zip(*self.locations[::-1]))

    @staticmethod
    def start_countdown():
        countdown = 3
        while countdown != 0:
            print("Bot is starting in " + str(countdown))
            time.sleep(1)
            countdown -= 1
        print(datetime.datetime.now().strftime(
            '%H:%M:%S') + "  Bot has started...")


WoWBot()
