from settings import *
import numpy as np

class Boid:
    def __init__(self, position: Vector2, rotation: int):
        self.position = position
        self.rotation = rotation
        self.velocity = vector2_rotate(Vector2(1, 0), np.deg2rad(rotation))
        self.max_speed: int = 10
        self.size: int = 10

        self.acceleration: Vector2 = vector2_zero()
        self.max_force = 0.1
    
    def check_edges(self):
        if self.position.x < -self.size:
            self.position.x = WIDTH + self.size
        elif self.position.x > WIDTH + self.size:
            self.position.x = -self.size
        
        if self.position.y < -self.size:
            self.position.y = HEIGHT + self.size
        elif self.position.y > HEIGHT + self.size:
            self.position.y = -self.size

    def alignment(self, boids):
        radius: int = 25
        steering: Vector2 = vector2_zero()
        total: int = 0

        for other in boids:
            if vector2_distance(self.position, other.position) < radius and not vector2_equals(self.position, other.position):
                steering = vector2_add(steering, other.velocity)
                total += 1
        
        if total > 0:
            steering = vector2_scale(steering, 1.0/total)
            steering = vector2_scale(vector2_normalize(steering), self.max_speed) # scale steering length to self.speed
            steering = vector2_subtract(steering, self.velocity)
            steering = vector2_clamp_value(steering, 0, self.max_force) # clamp to max

        return steering
    
    def separation(self, boids):
        radius: int = 24
        steering: Vector2 = vector2_zero()
        total: int = 0

        for other in boids:
            dist = vector2_distance(self.position, other.position)
            if dist < radius and not vector2_equals(self.position, other.position):
                diff = vector2_subtract(self.position, other.position)
                diff = vector2_scale(diff, 1.0/(dist * dist))
                steering = vector2_add(steering, diff)
                total += 1
        
        if total > 0:
            steering = vector2_scale(steering, 1.0/total)
            steering = vector2_scale(vector2_normalize(steering), self.max_speed) # scale steering length to self.speed
            steering = vector2_subtract(steering, self.velocity)
            steering = vector2_clamp_value(steering, 0, self.max_force) # clamp to max

        return steering

    def cohesion(self, boids):
        radius: int = 100
        steering: Vector2 = vector2_zero()
        total: int = 0

        for other in boids:
            if vector2_distance(self.position, other.position) < radius and not vector2_equals(self.position, other.position):
                steering = vector2_add(steering, other.position)
                total += 1
        
        if total > 0:
            steering = vector2_scale(steering, 1.0/total)
            steering = vector2_subtract(steering, self.position)
            steering = vector2_scale(vector2_normalize(steering), self.max_speed) # scale steering length to self.speed
            steering = vector2_subtract(steering, self.velocity)
            steering = vector2_clamp_value(steering, 0, self.max_force) # clamp to max

        return steering
    
    def flock(self, boids):
        alignment = self.alignment(boids)
        separation = self.separation(boids)
        cohesion = self.cohesion(boids)

        self.acceleration = vector2_add(self.acceleration, alignment)
        self.acceleration = vector2_add(self.acceleration, separation)
        self.acceleration = vector2_add(self.acceleration, cohesion)

    def update(self, boids):
        self.check_edges()

        self.flock(boids)

        self.position = vector2_add(self.position, self.velocity)
        self.velocity = vector2_add(self.velocity, self.acceleration)
        self.velocity = vector2_clamp_value(self.velocity, 0, self.max_speed)
        self.acceleration = vector2_zero()

        self.rotation = np.rad2deg(vector2_angle(Vector2(1, 0), self.velocity))

    def render(self):
        draw_poly_lines(self.position, 3, self.size, self.rotation, BLACK)
