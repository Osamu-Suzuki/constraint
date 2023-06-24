import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

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

# Points and lines definition
a = Point(200, 100)
b = Point(200, 300)
c = Point(500, 400)
d = Point(500, 100)

ab = Line(a, b)
bc = Line(b, c)
cd = Line(c, d)
da = Line(d, a)

# Constraints lengths
l1 = ab.length
l2 = bc.length
l3 = cd.length

# Displacement
dx, dy = 100, -20

# 点B (z[0],z[1])
# 点C (z[2],z[3])
# 点Bと点Cの座標を変数とし、点Cと指定された平行移動量との距離の二乗を最小化
def objective(z):
    return ((c.x+dx)-z[2]) ** 2 + ((c.y+dy)-z[3]) ** 2

# 点Bと点Cの座標を変数とし、各制約条件（線分の長さ）を満たすかどうかを評価
def constraint1(z):
    return np.sqrt((a.x - z[0]) ** 2 + (a.y - z[1]) ** 2) - ab.length  # abの長さ

def constraint2(z):
    return np.sqrt((z[2] - z[0]) ** 2 + (z[3] - z[1]) ** 2) - bc.length  # bcの長さ

def constraint3(z):
    return np.sqrt((z[2] - d.x) ** 2 + (z[3] - d.y) ** 2) - cd.length  # cdの長さ


# 制約条件を表す辞書のリスト
# 各制約条件は、typeキーに'eq'（等式制約）を持ち、funキーに対応する制約条件関数を持つ
cons = [{'type': 'eq', 'fun': constraint1},
        {'type': 'eq', 'fun': constraint2},
        {'type': 'eq', 'fun': constraint3}]

x0 = np.array([b.x, b.y, c.x, c.y])  # 最適化の初期点

sol = minimize(objective, x0, constraints=cons, method='SLSQP')

print(sol)

# Print initial coordinates
print("Initial coordinates:")
print("a: ", (a.x, a.y))
print("b: ", (b.x, b.y))
print("c: ", (c.x, c.y))
print("d: ", (d.x, d.y))
print("ab length", ab.length)
print("bc length", bc.length)
print("cd length", cd.length)
print("da length", da.length)


# Print final coordinates
new_b = Point(sol.x[0], sol.x[1])
new_c = Point(sol.x[2], sol.x[3])
new_ab = Line(a, new_b)
new_bc = Line(new_b, new_c)
new_cd = Line(new_c, d)

print("\nFinal coordinates:")
print("a: ", (a.x, a.y))
print("b': ", (new_b.x, new_b.y))
print("c': ", (new_c.x, new_c.y))
print("d: ", (d.x, d.y))
print("new_ab length", new_ab.length)
print("new_bc length", new_bc.length)
print("new_cd length", new_cd.length)
print("new_da length", da.length)

# Plot initial and final positions
plt.figure()

# Initial position
plt.plot([a.x, b.x, c.x, d.x, a.x], [a.y, b.y, c.y, d.y, a.y], 'o-')
plt.text(a.x, a.y, 'a')
plt.text(b.x, b.y, 'b')
plt.text(c.x, c.y, 'c')
plt.text(d.x, d.y, 'd')

# Final position
plt.plot([a.x, new_b.x, new_c.x, d.x, a.x], [a.y, new_b.y, new_c.y, d.y, a.y], 'o-')
plt.text(new_b.x, new_b.y, 'b\'', color='red')
plt.text(new_c.x, new_c.y, 'c\'', color='red')

plt.grid(True)
plt.show()
