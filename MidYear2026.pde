import pygame

pygame.init()

width = 1510
height = 915
screen = pygame.display.set_mode((width, height))

bg = pygame.image.load("images/background_image.png")
title = pygame.image.load("images/kitchen_text.png")

bg = pygame.transform.scale(bg, (width, height))

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  screen.blit(bg, (0,0))
  
  titleX = width
