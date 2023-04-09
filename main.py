import random 
#import math

target_distance = 1000 # meters
target_speed = 1 # m/s

#specific_gravity = 5 [*]

weight_range = (40, 100) # kilograms
height_range = (1.5, 2) #meters
arm_length_range = (0.5, 1) # meters
#leg_length_range = (0.75, 1.25) # meters [*]
body_shape_range = (0, 1) # 0= unfit to swim, 1= lean and straight (fit)
breathing_range = (1, 5) # once every 1, 2, 3, 4, or 5 strokes
#breathing_direction = (0, 1) #0= one side, 1= both sides [*]

traits_range = [(40, 100), (1.5, 2), (0.5, 1), (0, 1), (1, 5)]


population_size = 200
generations = 20000
mutation_rate = 0.01


def population(population_size):
    population = []
    for _ in range(population_size):
        human = (random.uniform(weight_range[0], weight_range[1]),
            random.uniform(height_range[0], height_range[1]),
            random.uniform(arm_length_range[0], arm_length_range[1]),
            #random.uniform(leg_length_range[0], leg_length_range[1]),
            random.uniform(body_shape_range[0], body_shape_range[1]),
            random.uniform(breathing_range[0], breathing_range[1]))
        population.append(human)

    return population


def speed(human):
    #drag_force = human[4]* (math.pi*(0.07**2))*human[0]*specific_gravity
    #prop_force = (2*(human[2]+human[3])+human[1])*human[0]*specific_gravity
    swimming_speed = ((human[1] + human[2])*human[3]*(human[4]/5))/human[0]

    return swimming_speed


def fitness(population, target_speed):
    fitness_scores = []
    for human in population:
        human_speed = speed(human)
        score = human_speed
        fitness_scores.append(score)

    return fitness_scores


def selection(fitness_scores):
    sum_scores = sum(fitness_scores)
    parents_prob = [score/sum_scores for score in fitness_scores]
    parents = [random.choices(population, weights=parents_prob)[0] for _ in range(10)]
    
    return parents


def crossover(parents):
    child = []
    good_traits = [[] for _ in range(5)]

    for idx in range(5):
        good_traits[idx] = [parent[idx] for parent in parents]

    child = [random.choice(good_traits[i]) for i in range(5)]

    return child


def mutation(human, mutation_rate):
    chance = random.uniform(0, 1)
    for trait in range(len(human)):
        if chance < mutation_rate:
            human[trait] = human[trait]*random.uniform(0.99, 1.01)

    return human


population = population(population_size)

for i in range(generations):
    fitness_scores = fitness(population, target_speed)
    max_fitness = max(fitness_scores)
    avg_fitness= sum(fitness_scores)/len(fitness_scores)
    print(f"Generation {i+1} | Highest Fitness: {max_fitness} | Average Fitness: {avg_fitness}")

    if max_fitness >= 0.999:
        print(f'\n\nAgent Found: Generation Number: {i+1}\nHighest Fitness: {max_fitness}\nAverage Fitness: {avg_fitness}\n\n')
        break

    new_population = []
    while len(new_population) < population_size:
        parents = selection(fitness_scores)
        child = crossover(parents)
        child = mutation(child, mutation_rate, traits_range) #might not change 
        new_population.append(child) 

    population = new_population