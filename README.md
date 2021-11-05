# Travelling Salesman Problem

In this repository I'm having a go at solving the [Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) (TSP) using a variety of methods, including reinforcement learning. This is an NP-hard problem with N! possible solutions, meaning that a brute-force approach is not scalable.

The idea is simple: generate a collection of points on a 2D plane, call the first point "home" which is where you will always need to start and finish, then find the shortest path between all points. It might be helpful to think of the 2D plane as a map and the points as destinations that need to be visited. Assuming that you are walking to and from each destination, you need to find the shortest route.

Useful references:
* [TSP solved with SA and GA](https://www.youtube.com/watch?v=0rPZSyTgo-w&ab_channel=PaulFred)
* [TSP with Monte Carlo Tree Search](https://www.youtube.com/watch?v=ECpuWvv--GU&ab_channel=JO)
* [PyConcorde](https://github.com/jvkersch/pyconcorde)
