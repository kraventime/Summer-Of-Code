import pygame
import numpy as np
from cell import Cell, update, reset

def save(grid):
	saved = False
	save_count = 0
	while not saved:
		try: 
			with open(f"config{save_count}.txt", "x", encoding="utf-8") as f:
				for cell_list in grid:
					for cell in cell_list:
						f.write(str([cell.x, cell.y, cell.state, cell.grid_size, cell.screen_size])+"|")
					f.write("?")
				saved = True
		except FileExistsError:
			save_count += 1

def load(file_number, grid):
	try: 
		with open(f"config{file_number}.txt", "r", encoding="utf-8") as f:
			grid = []
			cell_lists = f.read().replace(" ", "").replace("[","").replace("]","").split("?")
			cell_lists.pop(-1)
			for cell_list in cell_lists:
				cells = cell_list.split("|")
				cells.pop(-1)
				row = []
				for cell in cells:
					cell = cell.split(",")
					if len(cell) == 0:
						continue
					row.append(Cell(int(cell[0]), int(cell[1]), int(cell[2]), int(cell[3]), int(cell[4])))
				grid.append(row)
			return grid
	except FileNotFoundError:
		return grid

		