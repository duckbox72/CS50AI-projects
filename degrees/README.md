# Degrees

This project is a implementation of CS50 Artificial Intelligence with Python Porject 0a - Degrees

It uses the Breadh-First Search alghorith approach to find the shortest path beween two given actors, considering his neighboors, and all th neighboors of those recusively until target is reached through the shortest path.


 **shortest_path(source, target)** function located in [**degrees.py**](degrees.py) is responsible for the actual search. It makes a call the QueueFrontier() function in [**utils.py**](utils.py) in order do remove nodes from the frontier in a first-in, first-out (queue) behaviour finding for sure the shortest path, if there is a possible one.


Implemented by Luis Felipe Klaus 