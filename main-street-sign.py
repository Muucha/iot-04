# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Robotics Inc, and all authors'
__license__   = 'All Rights Reserved'


from time import sleep

from mvnc import mvncapi as mvnc
import numpy as np
import cv2

from motor_driver import forward, right


# Module Level Instances / Constants
# =============================================================================
ROOT_PATH       = '/home/pi/iot-04/'
GRAPH_FILE      = 'graph'
CATEGORIES_FILE = 'categories.txt'
INPUTSIZE_FILE  = 'inputsize.txt'


devices = mvnc.EnumerateDevices()

assert len(devices) != 0, 'Some Myriad device should be connected with the Raspberry Pi!'

device = mvnc.Device(devices[0])
device.OpenDevice()

with open(ROOT_PATH + GRAPH_FILE, mode='rb') as fin:
    graph = device.AllocateGraph(fin.read())

with open(ROOT_PATH + CATEGORIES_FILE, 'r') as fin:
    categories = list(filter(
        lambda x: x != 'classes',
        ( line.split('\n')[0] for line in fin.readlines() )
    ))

with open(ROOT_PATH + INPUTSIZE_FILE, 'r') as fin:
    image_size = int(fin.readline().split('\n')[0])

camera = cv2.VideoCapture(0)


# Original Functions
# =============================================================================
def square_trim(image):
    x, y, z = image.shape
    delta   = abs(x - y)

    if x > y:
        image = image[int(0.5 * delta): x - int(0.5 * delta), 0: y]

    else:
        image = image[0: x, int(0.5 * delta): y - int(0.5 * delta)]

    return cv2.resize(image, (image_size, image_size))


def normalize(image):
    for x in range(3):
        image[:, :, x] = (image[:, :, x] - 128) / 128

    return image


# Application Entry Point
# =============================================================================
while True:
    [ camera.read() for _ in range(4) ]

    _, image = camera.read()

    image = square_trim(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = normalize(image.astype(np.float16))

    graph.LoadTensor(image.astype(np.float16), 'user object')
    output, user_obj = graph.GetResult()

    top_accuracies = output.argsort()[: : -1][: 20]

    if any( ('street sign' in categories[x]) for x in top_accuracies ):
        print('[RIGHT]')
        right()

    else:
        print('[MOVE FORWARD]')
        forward()

    sleep(0.5)
