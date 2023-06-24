import numpy as np
from scipy.optimize import minimize

###########################################

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @property
    def length(self):
        return np.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

###########################################

class Constraint:
    def evaluate(self, points):
        """
        Evaluate the constraint.
        :param points: A dictionary of points.
        :return: The value of the constraint function.
        """
        raise NotImplementedError

class FixedDistanceConstraint(Constraint):
    def __init__(self, point1, point2, distance):
        self.point1 = point1
        self.point2 = point2
        self.distance = distance

    def evaluate(self, points):
        p1 = points[self.point1]
        p2 = points[self.point2]
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5 - self.distance

class FixedPointConstraint(Constraint):
    def __init__(self, point, x, y):
        self.point = point
        self.x = x
        self.y = y

    def evaluate(self, points):
        p = points[self.point]
        return (p.x - self.x) ** 2 + (p.y - self.y) ** 2

class FixedAngleConstraint(Constraint):
    def __init__(self, point1, point2, point3, angle):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.angle = angle

    def evaluate(self, points):
        # Calculate the angle between point1-point2 and point3-point2
        # and return the difference from the desired angle
        # ...
        pass




###########################################

def run_optimization(constraints, initial_points):  #data):

    #a = Point(data['a']['x'], data['a']['y'])
    #b = Point(data['b']['x'], data['b']['y'])
    #c = Point(data['c']['x'], data['c']['y'])
    #d = Point(data['d']['x'], data['d']['y'])
    #dx, dy = data['displacement']
    
    #ab = Line(a, b)
    #bc = Line(b, c)
    #cd = Line(c, d)
    #da = Line(d, a)
    
    
    def objective_function(point_array, target_x, target_y):
        x, y = point_array
        
        # 点と目標点との距離の二乗を計算
        distance_squared = (x - target_x) ** 2 + (y - target_y) ** 2
        
        return distance_squared


    # def objective(z):
    #    return ((c.x+dx)-z[2]) ** 2 + ((c.y+dy)-z[3]) ** 2

    #def constraint1(z):
    #    return np.sqrt((a.x - z[0]) ** 2 + (a.y - z[1]) ** 2) - ab.length

    #def constraint2(z):
    #    return np.sqrt((z[2] - z[0]) ** 2 + (z[3] - z[1]) ** 2) - bc.length

    #def constraint3(z):
    #    return np.sqrt((z[2] - d.x) ** 2 + (z[3] - d.y) ** 2) - cd.length

    cons = [{'type': 'eq', 'fun': constraint1},
            {'type': 'eq', 'fun': constraint2},
            {'type': 'eq', 'fun': constraint3}]

    x0 = np.array([b.x, b.y, c.x, c.y])

    sol = minimize(objective, x0, constraints=cons, method='SLSQP')

    result = {
        'b': {'x': sol.x[0], 'y': sol.x[1]},
        'c': {'x': sol.x[2], 'y': sol.x[3]}
    }

    return result


###########################################

# 初期点の設定
initial_points = {
    'a': Point(0, 0),
    'b': Point(1, 0),
    'c': Point(1, 1)
}

# 拘束条件のリストを作成
constraints = [
    FixedDistanceConstraint('a', 'b', 1),
    FixedPointConstraint('a', 0, 0),
    FixedAngleConstraint('a', 'b', 'c', 90)
]

# 最適化を実行
result = run_optimization(constraints, initial_points)

