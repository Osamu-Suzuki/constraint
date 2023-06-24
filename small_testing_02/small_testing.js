// 座標の定義
const x_a_fixed = 2;
const y_a_fixed = 1;
const x_b_fixed = 2;
const y_b_fixed = 3;
const x_d = 5;
const y_d = 1;
let x_c = 5; // 初期座標
let y_c = 4; // 初期座標

// 目標の線分の長さ
const AB_length = Math.sqrt(Math.pow(x_a_fixed - x_b_fixed, 2) + Math.pow(y_a_fixed - y_b_fixed, 2));
const CD_length = Math.sqrt(Math.pow(x_c - x_d, 2) + Math.pow(y_c - y_d, 2));

// 制約条件の行列形式を定義
const A_fixed = math.matrix([
  [1, 0, 0, 0, 0, 0],  // x_a
  [0, 1, 0, 0, 0, 0],  // y_a
  [0, 0, 1, 0, 0, 0],  // x_b
  [0, 0, 0, 1, 0, 0]   // y_b
]);

const b_fixed = math.matrix([
  [x_a_fixed],
  [y_a_fixed],
  [x_b_fixed],
  [y_b_fixed]
]);

const A_length = math.matrix([
  [(x_a_fixed - x_b_fixed) / AB_length, (y_a_fixed - y_b_fixed) / AB_length, 0, 0, 0, 0],  // x_a, y_a
  [0, 0, (x_a_fixed - x_b_fixed) / AB_length, (y_a_fixed - y_b_fixed) / AB_length, 0, 0],  // x_b, y_b
  [0, 0, 0, 0, (x_c - x_d) / CD_length, (y_c - y_d) / CD_length]                         // x_c, y_c
]);

const b_length = math.matrix([
  [0],
  [0],
  [0]
]);

// 連立方程式を解く
const solution = math.lusolve(math.concat(A_fixed, A_length), math.concat(b_fixed, b_length));
const [x_a, y_a, x_b, y_b, x_c_new, y_c_new] = math.flatten(solution.toArray());

// 点cの位置を更新
x_c = x_c_new;
y_c = y_c_new;

// 結果を表示
console.log(`新しい点cの座標: (${x_c}, ${y_c})`);
