from settings import *
from random import randint
from copy import copy

from boid import Boid

boids: list[Boid] = []

def make_boids():
    for _ in range(100):
        boids.append(Boid(Vector2(randint(0, WIDTH), randint(0, HEIGHT)), randint(0, 359)))

if __name__ == '__main__' :
    init_window(WIDTH, HEIGHT, 'boids simulation demo')
    set_target_fps(60)

    make_boids()

    while not window_should_close():
        boids_copy = copy(boids)
        [boid.update(boids_copy) for boid in boids]

        begin_drawing()

        clear_background(RAYWHITE)
        [boid.render() for boid in boids]
        draw_text(f'FPS: {get_fps()}', 0, 0, 20, GREEN)

        end_drawing()

    close_window()
