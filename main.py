import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import random 
import pygame

pygame.init()

window_size = 1920,600
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
body_shape_range = (0, 1) # 0= unfit to swim, 1= lean and straight (fit)
breathing_range = (1, 5) # once every 1, 2, 3, 4, or 5 strokes
head_diameter_radius = (0.1, 0.15) # head radius, greater is bad

traits_range = [(40, 100), (1.5, 2), (0.5, 1), (0.75, 1.25), (0, 1), (1, 5), (0.1, 0.15)]

population_window_size = 350
generations = 50000
mutation_rate = 0.05


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def text(text, font, x, y):
    disp_text = font.render(text, True, (255, 255, 255))
    window.blit(disp_text, (x, y))


def population(population_window_size):
    population = []
    for _ in range(population_window_size):
        human = (random.uniform(weight_range[0], weight_range[1]),
            random.uniform(height_range[0], height_range[1]),
            random.uniform(arm_length_range[0], arm_length_range[1]),
            random.uniform(leg_length_range[0], leg_length_range[1]),
            random.uniform(body_shape_range[0], body_shape_range[1]),
            random.uniform(breathing_range[0], breathing_range[1]),
            random.uniform(head_diameter_radius[0], head_diameter_radius[1]))
        population.append(human)

    return population


def speed(human, water_density, average_human_density, specific_gravity):
    buoyancy = water_density * (human[0]/average_human_density) * specific_gravity
    if buoyancy > human[0]:
        swimming_speed = ((human[1]+ 2*(human[2]+human[3]))*human[4]*(human[5]/5))*(1-human[6])/human[0]
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
    parents = [random.choices(population, weights=parents_prob)[0] for _ in range(2)]
    
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
    def __init__(self, x, y, n):
        self.x = x
        self.y = y 
        self.speed = fitness_scores[n]
    
    def draw(self, n):
        if fitness_scores[n] > 0.5:
            pygame.draw.circle(window, GREEN, (self.x, self.y), 2)

        elif fitness_scores[n] < 0.3:
            pygame.draw.circle(window, RED, (self.x, self.y), 2)
            
        else:
            pygame.draw.circle(window, BLUE, (self.x, self.y), 2)

    def move(self):
        self.x += (self.speed)*10


population = population(population_window_size)
drawn_humans = []
n = 0

for i in range(generations):
    window.fill(BLACK)

    fitness_scores = fitness(population, water_density, average_human_density, specific_gravity)
    max_fitness = max(fitness_scores)
    avg_fitness= sum(fitness_scores)/len(fitness_scores)

    text("red: Low Speed", font, window_size[0]-300, 40)
    text("green: Good Speed", font, window_size[0]-300, 80)
    text("blue: Avg Speed", font, window_size[0]-300, 120)
    text(f"Max Speed: {str(max_fitness)[:5]} m/s", font, window_size[0]-300, 240)
    text(f"Lowest Time: {str(1000/max_fitness)[:6]} s", font, window_size[0]-300, 280)
    text(f"Target time: 1000 s", font, window_size[0]-300, 320)
    

    print(f"Generation {i+1} | Highest Fitness: {str(max_fitness)[:10]} | Average Fitness: {str(avg_fitness)[:10]}")
    n += 1

    drawn_humans.append(Human(10, random.randint(10, window_size[1]-10), n))

    if len(drawn_humans) >= 100:
        drawn_humans = drawn_humans[100:]

    for draw_human in drawn_humans:
        draw_human.draw(n)
        draw_human.move()

    if max_fitness >= 0.999:
        print(f'\nAgent Found: Generation Number: {i+1}\nHighest Fitness: {max_fitness}\nAverage Fitness: {avg_fitness}\nTraits: {population[fitness_scores.index(max_fitness)]}\n\n')
        break

    new_population = []
    while len(new_population) < population_window_size:
        parents = selection(fitness_scores)
        child = crossover(parents, traits_range)
        child = mutation(child, mutation_rate) #might not change 
        new_population.append(child) 

    population = new_population
    n = 0
    pygame.display.flip()
