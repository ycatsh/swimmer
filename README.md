# Visualizing Swimming
Trains and visualizes agents to learn how to swim via a genetic algorithm.

## Genetic Algorithm
Each generated agent has 7 traits (genomes) which is randomly decided. The script defines a range for a bunch of traits that define an agent's ability to swim.  
  
The agent's speed is then calculated based on their traits and added to a list of all the corresponding speeds of the population. The population is mutated and crossed to allow diversity and learning between the generated agents to simulate the [survival of the fittest](https://en.wikipedia.org/wiki/Survival_of_the_fittest)    
  
When the generation is compeleted, the solution to the speed equation is found. It results in an optimal solution to the range of traits specified. 

## How it works
The algorithm trains an agent to learn how to swim based on the following parameters:  

```py
weight_range = (40, 100) # kilograms
height_range = (1.5, 2) # meters
arm_length_range = (0.5, 1) # meters
leg_length_range = (0.75, 1.25) # meters 
body_shape_range = (0, 1) # 0 = unfit to swim, 1 = lean and straight (fit)
strokes_range = (0.1, 2) #0 = very slow, 2 = fast
breathing_range = (1, 5) # once every 1, 2, 3, 4, or 5 strokes
head_diameter_radius = (0.1, 0.15) # head radius, greater is bad
```

The swimming speed is calculated by an equation:  

$$\begin{align*} \text{buoyancy} &= \rho \times{V_{agent}}\times{SG} \\
&= \rho \times{\frac{m}{\rho_{agent}}}\times{SG} \\
\text{speed} &= \frac{h+2\{(l_{arm}+l_{leg})(n_{strokes})\}\times{B_{shape}}\times{\frac{b_{range}}{5}}\times1-d_{head}}{m} \quad \text{if buoyancy} > \text{weight}, \\
&= 0 \quad \text{otherwise} \end{align*}$$

This translates (in code) to:
```py
    buoyancy = water_density * (human[0]/average_human_density) * specific_gravity
    if buoyancy > human[0]:
        swimming_speed = ((human[1]+ (2*(human[2]+human[3])*human[7]))*human[4]*(human[5]/5))*(1-human[6])/human[0]
    else:
        swimming_speed = 0
```

Additionally, mutation and crossovers facilitates diversity and enables the agents to progressively learn.

## Target
Speed: 1 m/s  
Distance: 1000 m   
Time: 1000 s

## Visualization  
Only the maximum speeds are visualized for every 350 (population size) generations to make the visualization much faster and easier to watch.

https://user-images.githubusercontent.com/91330011/232504679-68e76ec4-e16b-448b-93e2-72cceeaf9ee3.mp4