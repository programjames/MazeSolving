# Path Finding Algorithms
This uses two algorithms to solve mazes. The common A* algorithm, and a backwards breadth first search algorithm that I will refer to as C* from now on (C* for Camacho). The C* algorithm is more useful for moving around large groups (such as in Battlecode), as it is only ever run once. However, it is less accurate as a path may be blocked by another person, in which case it tries the next best directions to move in.

I have included several visuals within the code that rely on pygame and numpy to run (as well as the standard libraries random and time), however the functions a_star and c_star do not utilize any external packages.

To install pygame and numpy, the following commands can often be run on the terminal:
```
pip install pygame
pip install numpy
```
If this doesn't work, then try using the methods found on [pygame's website](https://www.pygame.org/wiki/GettingStarted) and [scipy's website](https://scipy.org/install.html) to install them.
