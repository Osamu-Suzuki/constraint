import numpy as np
from scipy.spatial import distance
from scipy.optimize import minimize

#######################################################

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.initial_length = self.length()

    def length(self):
        return np.sqrt((self.point1.x - self.point2.x)**2 + (self.point1.y - self.point2.y)**2)


#######################################################



class FixedPointConstraint:
    def __init__(self, point):
        self.point = point


class FixedLengthConstraint:
    def __init__(self, line):
        self.line = line


#######################################################


def optimize(move_point, target_point, fixed_constraints, length_constraints):
    def objective_function(x):
        # The function to minimize is the distance to target_point
        return distance.euclidean([x[0], x[1]], [target_point.x, target_point.y])

    constraints = []

    # Add constraints for fixed points (points other than move_point)
    for constraint in fixed_constraints:
        def fixed_point_constraint(x, point=constraint.point):
            if move_point == point:
                return np.array([x[0] - point.x, x[1] - point.y])
            else:
                return np.array([0, 0])
        constraints.append(fixed_point_constraint)

    # Add constraints for fixed line lengths
    for constraint in length_constraints:
        def fixed_length_constraint(x, line=constraint.line):
            if move_point in [line.point1, line.point2]:
                if line.point1 == move_point:
                    other_point = line.point2
                else:
                    other_point = line.point1
                return line.initial_length - np.sqrt((x[0] - other_point.x)**2 + (x[1] - other_point.y)**2)
            else:
                return 0
        constraints.append(fixed_length_constraint)

    constraints = [{'type': 'eq', 'fun': constraint} for constraint in constraints]

    # Perform the optimization
    result = minimize(objective_function, [move_point.x, move_point.y], constraints=constraints)
    print(result)
    
    # Update the coordinates of move_point and return it
    move_point.x = result.x[0]
    move_point.y = result.x[1]
    return move_point


#######################################################


# 例1
a = Point(200, 100)
b = Point(200, 300)
c = Point(500, 400)
d = Point(500, 100)

target_point = Point(600, 300)

ab = Line(a, b)
bc = Line(b, c)
cd = Line(c, d)

fixed_constraints = [FixedPointConstraint(a), FixedPointConstraint(d)]
length_constraints = [FixedLengthConstraint(ab), FixedLengthConstraint(bc), FixedLengthConstraint(cd)]

optimized_c = optimize(c, target_point, fixed_constraints, length_constraints)

print(f'Optimized c: ({optimized_c.x}, {optimized_c.y})')


# 例2
a = Point(2, 2)
b = Point(5, 3)

target_point = Point(5, 6)

ab = Line(a, b)

fixed_constraints = [FixedPointConstraint(a)]
length_constraints = [FixedLengthConstraint(ab)]

optimized_b = optimize(b, target_point, fixed_constraints, length_constraints)

print(f'Optimized b: ({optimized_b.x}, {optimized_b.y})')
