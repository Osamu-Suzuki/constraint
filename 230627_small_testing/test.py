import numpy as np
from scipy.optimize import minimize
from copy import deepcopy

####################################################################################

# 座標を持つPointクラスを定義します。
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
# 2つのPointインスタンスを結ぶLineクラスを定義します。
# Lineインスタンスはその長さも計算します。
class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = self.calculate_length()

    # Lineインスタンスの長さを計算するメソッドです。
    def calculate_length(self):
        return np.sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)


####################################################################################


# FixedPointConstraintクラスは、ある点が固定されていることを表現します。
class FixedPointConstraint:
    def __init__(self, point_id):
        self.point_id = point_id

    # 初期位置からの変位を計算します。制約としてはこの変位が0であるべきです。
    def __call__(self, points_flat):
        points = flat_to_array(points_flat)
        point = points[self.point_id]

        # 現在の点の座標を取得
        current_position = np.array([point.x, point.y])

        # 初期状態の点の座標を取得
        initial_position = np.array([initial_points[self.point_id].x, initial_points[self.point_id].y])

        # 現在の座標と初期座標との差分ベクトルを計算
        diff_vector = current_position - initial_position

        # ベクトルの長さ（ノルム）を計算して返す（つまり、点の初期位置からの移動距離）
        return np.linalg.norm(diff_vector)


## 以下、line_nameではなく、point_idを使うやり方に変更が必要
# FixedLengthConstraintクラスは、ある線の長さが固定されていることを表現します。
class FixedLengthConstraint:
    def __init__(self, line_name):
        self.line_name = line_name
    
    # 線の現在の長さと初期の長さとの差を計算します。制約としてはこの差が0であるべきです。
    def __call__(self, points_flat):
        points = flat_to_dict(points_flat)
        line = lines[self.line_name]

        # 現在の線の長さを計算
        current_length = np.linalg.norm(np.array([line.point1.x, line.point1.y]) - np.array([line.point2.x, line.point2.y]))

        # 初期状態の線の長さを取得
        initial_length = initial_lines[self.line_name].length

        # 現在の長さと初期の長さの差を計算して返す
        length_diff = current_length - initial_length
        return length_diff


####################################################################################


# 目標点までの距離を計算する関数を生成します。これが最小化の対象となります。
def target_point_distance(target_point_name):
    # 生成された関数
    def distance(points_flat):
        points = flat_to_dict(points_flat)
        print(points)

        # 移動させたい点の現在の位置を取得
        moving_point = np.array([points[target_point_name].x, points[target_point_name].y])
        print('moving_point:' + str(moving_point))

        # 移動させたい目標点の位置
        target_point_position = np.array([target_point.x, target_point.y])
        print('target_point_position:' + str(target_point_position) + "\n")

        # 移動させたい点と目標点との差分ベクトルを計算
        diff_vector = moving_point - target_point_position

        # 差分ベクトルのノルム（長さ）を計算して返す。これが2点間の距離になる。
        return np.linalg.norm(diff_vector)

    # 生成した関数を返す
    return distance


####################################################################################



# 目標点への移動を試みる関数です。
def move_point(target_point_name, target_point, constraints):
    # 点の座標を1次元の配列に平坦化します。
    initial_points_flat = np.array([coord for point in points.values() for coord in [point.x, point.y]])

    # 目標点までの距離を計算する関数を取得します。
    target_distance = target_point_distance(target_point_name)

    # 初めに、制約条件を準備します。各制約条件を 'type' と 'fun' の辞書で表現します。
    # ここでは、全ての制約が等式 ('eq') であると仮定しています。
    constraints_for_optimization = []
    for c in constraints:
        constraint_dict = {'type': 'eq', 'fun': c}
        constraints_for_optimization.append(constraint_dict)

    # scipyのminimize関数を呼び出します。目標関数、初期値、制約条件を引数として渡します。
    # minimize関数は、目標関数を最小化するようなパラメータを探索します。
    # この探索は、初期値から始まり、制約条件を満たす範囲で行われます。
    res = minimize(target_distance, initial_points_flat, constraints=constraints_for_optimization)
    print(res)

    # 最適化後の座標を取得し、それを点に適用します。
    updated_points_flat = res.x
    for i, name in enumerate(points):
        points[name].x, points[name].y = updated_points_flat[2*i:2*i+2]

    return points


def flat_to_dict(points_flat):
    return {name: Point(points_flat[i], points_flat[i+1]) for i, name in enumerate(points_names)}


####################################################################################


# 例1
# 初期座標と目標座標を設定します。

a = Point(200, 100)
b = ...

points = [Point(200, 100), Point(200, 300), Point(500, 400), Point(500, 100)]
initial_points = deepcopy(points)  # 初期座標を保持しておきます。

ab = Line(a, b)
bc = Line(b, c)
...

lines = [Line(points[0], points[1]), Line(points[1], points[2]), Line(points[2], points[3])]
initial_lines = deepcopy(lines)  # 初期状態の線を保持する辞書を作成

constraints = [FixedPointConstraint('a'), FixedPointConstraint('d'), FixedLengthConstraint('ab'), FixedLengthConstraint('bc'), FixedLengthConstraint('cd')]
target_point = Point(600, 300)

# 点cを目標点に移動させます。
new_points = move_point('c', target_point, constraints)

# 新しい座標を表示します。
for name, point in new_points.items():
    print(name, point.x, point.y)


# 例2
# 初期座標と目標座標を設定します。
# points_names = ['a', 'b']
# points = {'a': Point(2, 2), 'b': Point(5, 3)}
# initial_points = points.copy()  # 初期座標を保持しておきます。
# lines = {'ab': Line(points['a'], points['b'])}
# constraints = [FixedPointConstraint('a'), FixedLengthConstraint('ab')]
# target_point = Point(5, 6)

# 点bを目標点に移動させます。
# new_points = move_point('b', target_point, constraints)

# 新しい座標を表示します。
# for name, point in new_points.items():
#     print(name, point.x, point.y)
