import pygame
import numpy as np

class Cell(pygame.sprite.Sprite):
	def __init__(self, x, y, state, grid_size, screen_size):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.state = state
		self.screen_size = screen_size
		self.grid_size = grid_size
		self.neighbours = 0
		self.rect = pygame.Rect((x-1)*screen_size/grid_size, (y-1)*screen_size/grid_size, screen_size/grid_size, screen_size/grid_size)

	def display(self, screen, updating, shift_x, shift_y):
		self.rect[0] -= (self.screen_size/4 + shift_x)
		self.rect[1] -= (self.screen_size/4 + shift_y)
		if self.state == 1:
			pygame.draw.rect(screen, (0,0,0), self.rect)
		else:
			if updating == True:
				pygame.draw.rect(screen, (0,0,0), self.rect, int((self.screen_size/self.grid_size)/32))
			else:
				pygame.draw.rect(screen, (255,0,0), self.rect, int((self.screen_size/self.grid_size)/32))
		self.rect[0] += (self.screen_size/4 + shift_x)
		self.rect[1] += (self.screen_size/4 + shift_y)

def update(grid):
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			for m in [i-1,i,i+1]:
				for n in [j-1,j,j+1]:
					if m < 0 or m >= grid[i][j].grid_size or n < 0 or n >= grid[i][j].grid_size:
						continue
					elif m == i and n == j:
						continue
					elif grid[i][j].state == 1:
						grid[m][n].neighbours += 1

	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j].neighbours < 2:
				grid[i][j].state = 0
			elif grid[i][j].neighbours == 3:
				grid[i][j].state = 1
			elif grid[i][j].neighbours == 4:
				grid[i][j].state = 0
			else:
				pass

def reset(grid):
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			grid[i][j].neighbours = 0