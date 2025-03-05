import pygame
import cv2
import numpy as np
import sys

camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

mode = [int(camera.get(3)/2), int(camera.get(4)/2)]
screen = pygame.display.set_mode(mode)

while True:

    ret, frame = camera.read()

    screen.fill([0, 0, 0])
    frame = cv2.resize(frame, mode)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)

pygame.quit()
cv2.destroyAllWindows()