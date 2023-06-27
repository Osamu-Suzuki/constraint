import numpy as np
from scipy.optimize import minimize

# Pointクラス
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_array(cls, array):
        return cls(array[0], array[1])


# Lineクラス
class Line():
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = self.get_length()

    def get_length(self):
        return np.sqrt((self.point2.x - self.point1.x)**2 + (self.point2.y - self.point1.y)**2)



# Constraintクラス
class Constraint():
    def __init__(self):
        pass

class FixedPointConstraint(Constraint):
    def __init__(self, point, target_point):
        self.point = point
        self.target_point = target_point

    def constraint_func(self, points):
        p = Point.from_array(points[2*self.point:2*(self.point+1)])
        return np.array([p.x - self.target_point.x, p.y - self.target_point.y])

class FixedLengthConstraint(Constraint):
    def __init__(self, line, length):
        self.line = line
        self.length = length

    def constraint_func(self, points):
        p1 = Point.from_array(points[2*self.line.point1:2*(self.line.point1+1)])
        p2 = Point.from_array(points[2*self.line.point2:2*(self.line.point2+1)])
        return np.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2) - self.length


def optimize_point_and_line(points_to_optimize, target_point, fixed_constraints, length_constraints):
    # 初期値
    if not isinstance(points_to_optimize, list):
        points_to_optimize = [points_to_optimize]
    x0 = [point.x for point in points_to_optimize] + [point.y for point in points_to_optimize]

    # 目的関数
    def objective(x):
        return np.sum((x[:len(points_to_optimize)] - target_point.x)**2 + (x[len(points_to_optimize):] - target_point.y)**2)

    # 制約条件
    constraints = [{'type': 'eq', 'fun': constraint.constraint_func} for constraint in fixed_constraints + length_constraints]

    # 最適化計算
    solution = minimize(objective, x0, constraints=constraints)
    
    # 最適化された点
    optimized_points = [Point(solution.x[i], solution.x[i+len(points_to_optimize)]) for i in range(len(points_to_optimize))]

    return optimized_points



# 例1
a = Point(200, 100)
b = Point(200, 300)
c = Point(500, 400)
d = Point(500, 100)

target = Point(600, 300)

ab = Line(a, b)
bc = Line(b, c)
cd = Line(c, d)

fixed_constraints = [FixedPointConstraint(a, a), FixedPointConstraint(d, d)]
length_constraints = [FixedLengthConstraint(ab, ab.length), FixedLengthConstraint(bc, bc.length), FixedLengthConstraint(cd, cd.length)]

optimized_b, optimized_c = optimize_point_and_line([b, c], target, fixed_constraints, length_constraints)

print(f'Optimized b: ({optimized_b.x}, {optimized_b.y})')
print(f'Optimized c: ({optimized_c.x}, {optimized_c.y})')

# 例2
a = Point(2, 2)
b = Point(5, 3)

target = Point(5, 6)

ab = Line(a, b)

fixed_constraints = [FixedPointConstraint(a, a)]
length_constraints = [FixedLengthConstraint(ab, ab.length)]

optimized_b = optimize_point_and_line([b], target, fixed_constraints, length_constraints)

print(f'Optimized b: ({optimized_b.x}, {optimized_b.y})')
input()