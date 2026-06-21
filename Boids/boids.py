import pygame
import numpy as np

class Boid(pygame.sprite.Sprite):
    def __init__(self, i, x, y, vx, vy, vrange):
       pygame.sprite.Sprite.__init__(self)
       self.tag = i
       self.image = pygame.image.load("boyeed.png").convert_alpha()
       self.image = pygame.transform.scale(self.image, (self.image.get_width()*0.01, self.image.get_height()*0.01))
       self.pos = pygame.Vector2(x,y)
       self.vel = pygame.Vector2(vx, vy)
       self.acc = pygame.Vector2(0, 0)
       self.vrange = vrange
       self.rect = self.image.get_rect(center=(self.pos.x,self.pos.y))

    def update(self, delta_time):
    	# Update parameters
    	self.pos += self.vel * delta_time
    	self.vel += self.acc * delta_time

    	# Bounce off walls
    	if(self.pos.x > 640 or self.pos.x < 0):
    		self.pos.x = min(640, max(0, self.pos.x))
    		self.vel.x = -self.vel.x
    	if(self.pos.y > 640 or self.pos.y < 0):
    		self.pos.y = min(640, max(0, self.pos.y))
    		self.vel.y = -self.vel.y

    	# Update actual position
    	self.rect.x = self.pos.x 
    	self.rect.y = self.pos.y

    	self.acc = pygame.Vector2(0,0) 	

    # Check the given range for boids
    def check_range(self, boids_list, range_scan):
    	boids_in_range = []
    	for boid in boids_list:
    		if boid.tag == self.tag:
    			continue

    		if((boid.pos-self.pos).length() <= range_scan):
    			boids_in_range.append(boid)

    	return boids_in_range

    # Aligment: Match the velocities
    def alignment(self, align_c, boids_list):
    	boids_in_range = self.check_range(boids_list, self.vrange)
    	if(len(boids_in_range) > 0):
	    	flock_vel = pygame.Vector2(0, 0)
	    	for boid in boids_in_range:
	    		flock_vel += boid.vel 

	    	flock_vel = flock_vel/len(boids_in_range)
	    	self.acc += align_c * (flock_vel - self.vel)

	# Cohesion: Try to attract flock
    def cohesion(self, cohes_c, boids_list):
        boids_in_range = self.check_range(boids_list, self.vrange)
        if(len(boids_in_range) > 0):
	        flock_pos = pygame.Vector2(0, 0)
	        for boid in boids_in_range:
	    	    flock_pos += boid.pos

	        flock_pos = flock_pos/len(boids_in_range)
	        self.acc += cohes_c * (flock_pos - self.pos)


	# Separation: Try to repel crowd
    def separation(self, sep_c, boids_list):
	    boids_in_range = self.check_range(boids_list, self.vrange/4)
	    if(len(boids_in_range) > 0):
	        repelling_force = pygame.Vector2(0, 0)
	        for boid in boids_in_range:
	            repelling_force += (self.pos - boid.pos)/((self.pos-boid.pos).length()**2)

	        self.acc += sep_c * repelling_force

    def viscosity(self, visc_c):
	    self.acc += visc_c * (-self.vel)


def main():
	pygame.init()
	screen = pygame.display.set_mode((640,640))

	clock = pygame.time.Clock()
	running = True
	delta_time = 0.1

	# Make some Boids
	boids = []
	for i in range(25):
		vx = np.random.default_rng().random()*200
		vy = np.sqrt((200**2) - (vx**2))
		boid = Boid(i, (i%5)*128, np.floor(i/5)*128, ((-1)**i)*vx, ((-1)**i)*vy, 128)
		boids.append(boid)

	while running:
		screen.fill((255,255,255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# Update each boid
		for boid in boids:
			boid.alignment(10000, boids)
			boid.cohesion(10000, boids)
			boid.separation(10000, boids)
			boid.viscosity(0)
			boid.update(delta_time)
			screen.blit(boid.image, boid.rect)

		delta_time = max(0.001, min(0.1, clock.tick(60)/1000))
		pygame.display.flip()

	pygame.quit()


main()