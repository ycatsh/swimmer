import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import random 
import pygame
from pygame.locals import *

pygame.init()

window_size = 1500,600
window = pygame.display.set_mode((window_size), pygame.SCALED)
pygame.display.set_caption("Swimming Genetic Algorithm Visualization")

font = pygame.font.Font("assets/fonts/C&C Red Alert [INET].ttf", 25)

target_distance = 1000 # meters
target_speed = 1 # m/s

water_density = 1000 # kg/m^3
specific_gravity = 1 # 1t/m^3
average_human_density = 1000 # kg/m^3

weight_range = (40, 100) # kilograms
height_range = (1.5, 2) # meters
arm_length_range = (0.5, 1) # meters
leg_length_range = (0.75, 1.25) # meters 
body_shape_range = (0, 1) # 0 = unfit to swim, 1 = lean and straight (fit)
strokes_range = (0.1, 2) #0 = very slow, 2 = fast
breathing_range = (1, 5) # once every 1, 2, 3, 4, or 5 strokes
head_diameter_radius = (0.1, 0.15) # head radius, greater is bad

traits_range = [(40, 100), (1.5, 2), (0.5, 1), (0.75, 1.25), (0, 1), (0.1, 2), (1, 5), (0.1, 0.15)]

population_size = 350
generations = 50000
mutation_rate = 0.05


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (52, 131, 235)
YELLOW = (240, 218, 58)

def text(text, font, x, y):
    disp_text = font.render(text, True, (255, 255, 255))
    window.blit(disp_text, (x, y))


def draw_stick_figure(color, x, y, pop, dy):
    pygame.draw.circle(window, color, (x, y), 2)

    pygame.draw.line(window, color, (x, y), (x-10, y), 1)

    pygame.draw.line(window, color, (x-2, y), (x+5, y+dy), 1)
    pygame.draw.line(window, color, (x-2, y), (x+5, y+dy), 1)

    pygame.draw.line(window, color, (x-10, y), (x-15, y+dy), 1)
    pygame.draw.line(window, color, (x-10, y), (x-15, y+dy), 1)


def population(population_size):
    population = []
    for _ in range(population_size):
        human = [random.uniform(weight_range[0], weight_range[1]),
            random.uniform(height_range[0], height_range[1]),
            random.uniform(arm_length_range[0], arm_length_range[1]),
            random.uniform(leg_length_range[0], leg_length_range[1]),
            random.uniform(body_shape_range[0], body_shape_range[1]),
            random.uniform(breathing_range[0], breathing_range[1]),
            random.uniform(head_diameter_radius[0], head_diameter_radius[1]),
            random.uniform(strokes_range[0], strokes_range[1])]
        population.append(human)

    return population


def speed(human, water_density, average_human_density, specific_gravity):
    buoyancy = water_density * (human[0]/average_human_density) * specific_gravity
    if buoyancy > human[0]:
        swimming_speed = ((human[1]+ (2*(human[2]+human[3])*human[7]))*human[4]*(human[5]/5))*(1-human[6])/human[0]
    else:
        swimming_speed = 0

    return swimming_speed


def fitness(population, water_density, average_human_density, specific_gravity):
    fitness_scores = []
    for human in population:
        human_speed = speed(human, water_density, average_human_density, specific_gravity)
        score = human_speed
        fitness_scores.append(score)

    return fitness_scores


def selection(fitness_scores):
    sum_scores = sum(fitness_scores)
    parents_prob = [score/sum_scores if score != 0 and sum_scores != 0 else 0 for score in fitness_scores]
    parents = [random.choices(population, weights=parents_prob)[0] for _ in range(4)]
    
    return parents


def crossover(parents, traits_range):
    child = []
    good_traits = [[] for _ in range(len(traits_range))]

    for idx in range(len(traits_range)):
        good_traits[idx] = [parent[idx] for parent in parents]

    child = [random.choice(good_traits[i]) for i in range(len(traits_range))]

    return child


def mutation(human, mutation_rate):
    chance = random.uniform(0, 1)
    for trait in range(len(human)):
        if chance < mutation_rate:
            human[trait] = human[trait]*random.uniform(0.99, 1.01)

    return human


class Human:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y 
        self.speed = speed
        self.drown = 100 #scaled by a factor of 10 because speed is 10x
        self.if_drown = False
        self.time = 0
    
    def draw(self):
        dy = random.choice([-4, 4])
        if self.if_drown:
            dy = 0
    
        if self.speed >= 0.999:
            draw_stick_figure(GREEN, self.x, self.y, population, dy)
        elif self.speed > 0.6:
            draw_stick_figure(BLUE, self.x, self.y, population, dy)
        elif self.speed < 0.3:
            draw_stick_figure(RED, self.x, self.y, population, dy)
        else:
            draw_stick_figure(YELLOW, self.x, self.y, population, dy)

    def move(self):
        self.time += 1
        if self.time < self.drown:
            self.x += (self.speed)*10 #speed 10x to speed up visualization
        else:
            self.if_drown = True
            self.y += 10

    def ypos(self):
        return self.y

    def xpos(self):
        return self.x


population = population(population_size)
visualization = True
drawn_humans = []

for i in range(generations):
    window.fill(BLACK)

    pygame.draw.line(window, (255, 255, 255), (1010, 0), (1010, 600), 1)

    fitness_scores = fitness(population, water_density, average_human_density, specific_gravity)
    max_fitness = max(fitness_scores)
    avg_fitness= sum(fitness_scores)/len(fitness_scores)

    text("red: Low Speed", font, window_size[0]-300, 40)
    text("green: Mid Speed", font, window_size[0]-300, 80)
    text("blue: Good Speed", font, window_size[0]-300, 120)
    text(f"Max Speed: {str(max_fitness)[:5]} m/s", font, window_size[0]-300, 240)
    text(f"Lowest Time: {str(1000/(max_fitness+0.001))[:6]} s", font, window_size[0]-300, 280) #adding 0.001 to avoid divion by 0
    text("Target time: 1000 s", font, window_size[0]-300, 320)
    text("Line: 1000 m", font, window_size[0]-300, 480)
    text("green: Fittest Agents", font, window_size[0]-300, 520)

    for draw_human in drawn_humans:
        draw_human.draw()
        draw_human.move()

        if draw_human.ypos() < -10:
            drawn_humans.remove(draw_human)
        
        if draw_human.xpos() >= 1010:
            text("(fittest agent)", font, 1050, draw_human.ypos())
            break

    drawn_humans.append(Human(10, random.randint(10, window_size[1]-10), max_fitness)) 
    
    new_population = []
    while len(new_population) < population_size:
        parents = selection(fitness_scores)
        child = crossover(parents, traits_range)
        child = mutation(child, mutation_rate) #might not change 
        new_population.append(child) 

    population = new_population
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()