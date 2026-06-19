import pygame
import numpy as np 
from cell import Cell, update, reset
from save_and_load import save, load

def main():
	pygame.init()
	screen_size = 3840 # Make sure it is divisible by 4 :)
	grid_size = 120 # Make sure the screen-grid size ratio is constant :)

	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((screen_size/3,screen_size/5))
	pygame.display.set_caption("Conway's Game of Life")
	running = True
	updating = True

	# Speed of Simulation
	speed = 10 
	count = 0 

	# Moving around the Grid
	shift_x = 0
	shift_y = 0

	grid = []
	for i in range(1, grid_size+1):
		cell_list = []
		for j in range(1, grid_size+1):
			cell_list.append(Cell(i, j, 0, grid_size, screen_size))
		grid.append(cell_list)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					updating = not updating

				if event.key == pygame.K_DOWN:
					speed += 1
				if event.key == pygame.K_UP:
					speed -= 1
					if(speed < 1):
						speed = 1

				if event.key == pygame.K_BACKSPACE:
					for cell_list in grid:
						for cell in cell_list:
							cell.state = 0

				if event.key == pygame.K_w:
					shift_y -= 50
				if event.key == pygame.K_a:
					shift_x -= 50
				if event.key == pygame.K_s:
					shift_y += 50
				if event.key == pygame.K_d:
					shift_x += 50

				# Saving
				if event.key == pygame.K_RETURN:
					save(grid)

				# Loading: Primitive
				if not updating:
					if event.key == pygame.K_0:
						grid = load(0, grid)
					if event.key == pygame.K_1:
						grid = load(1, grid)
					if event.key == pygame.K_2:
						grid = load(2, grid)
					if event.key == pygame.K_3:
						grid = load(3, grid)
					if event.key == pygame.K_4:
						grid = load(4, grid)
					if event.key == pygame.K_5:
						grid = load(5, grid)
					if event.key == pygame.K_6:
						grid = load(6, grid)
					if event.key == pygame.K_7:
						grid = load(7, grid)
					if event.key == pygame.K_8:
						grid = load(8, grid)
					if event.key == pygame.K_9:
						grid = load(9, grid)
									
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				x = int((x+screen_size/4+shift_x)/(screen_size/grid_size))*screen_size/grid_size
				y = int((y+screen_size/4+shift_y)/(screen_size/grid_size))*screen_size/grid_size

				for cell_list in grid:
					for cell in cell_list:
						if cell.rect[0] == x and cell.rect[1] == y:
							cell.state = not cell.state

		screen.fill((255,255,255))
		clock.tick(60)

		if updating and count%speed==0:
			update(grid)
			reset(grid)

		for cell_list in grid:
				for cell in cell_list:
					cell.display(screen, updating, shift_x, shift_y)
		count += 1
		pygame.display.update()

	pygame.quit()

main()