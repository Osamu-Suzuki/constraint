import numpy as np
from scipy.optimize import minimize

class FixedPointConstraint:
    def __init__(self, index, position):
        self.index = index
        self.position = position

    def __call__(self, x):
        return np.linalg.norm(x[2*self.index:2*self.index+2] - self.position)

class FixedLengthConstraint:
    def __init__(self, index1, index2, length):
        self.index1 = index1
        self.index2 = index2
        self.length = length

    def __call__(self, x):
        return np.linalg.norm(x[2*self.index1:2*self.index1+2] - x[2*self.index2:2*self.index2+2]) - self.length

def target_point_distance(target_point, index):
    def distance(x):
        return np.linalg.norm(x[2*index:2*index+2] - target_point)
    return distance

def move_point(points, target_point_index, target_point, constraints):
    initial_points = np.array(points).flatten()
    target_distance = target_point_distance(target_point, target_point_index)
    res = minimize(target_distance, initial_points, constraints=[{'type': 'eq', 'fun': c} for c in constraints])
    return np.reshape(res.x, (-1, 2))

# Example 1
import matplotlib.pyplot as plt

# Example 1
import matplotlib.pyplot as plt

# Example 1
points = [(200, 100), (200, 300), (500, 400), (500, 100)]
constraints = [FixedPointConstraint(0, points[0]), FixedPointConstraint(3, points[3]),
               FixedLengthConstraint(0, 1, np.linalg.norm(np.array(points[0])-np.array(points[1]))),
               FixedLengthConstraint(1, 2, np.linalg.norm(np.array(points[1])-np.array(points[2]))),
               FixedLengthConstraint(2, 3, np.linalg.norm(np.array(points[2])-np.array(points[3])))]

new_points = move_point(points, 2, (600, 300), constraints)
new_points = new_points.tolist()  # Converting array to list

# Visualize the points before moving
plt.figure(figsize=(6,6))
plt.scatter(*zip(*points), color='r')
plt.plot(*zip(*(points + [points[0]])), color='r', linestyle='--')  # To connect the points

# Visualize the points after moving
plt.scatter(*zip(*new_points), color='b')
plt.plot(*zip(*(new_points + [new_points[0]])), color='b', linestyle='--')  # To connect the points

plt.axis('equal')  # Make scales of x-axis and y-axis equal
plt.show()




# Example 2
points = [(2, 2), (5, 3)]
constraints = [FixedPointConstraint(0, points[0]),
               FixedLengthConstraint(0, 1, np.linalg.norm(np.array(points[0])-np.array(points[1])))]
print(move_point(points, 1, (5, 6), constraints))
