// Point クラスを定義します。
// xとy座標を持つ点を表現します。
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}

// Line クラスを定義します。
// 2つのPointオブジェクトによって定義される線を表現します。
class Line {
  constructor(point1, point2) {
    this.point1 = point1;
    this.point2 = point2;
  }

  // ラインの長さを計算します（ユークリッド距離）。
  get length() {
    const dx = this.point1.x - this.point2.x;
    const dy = this.point1.y - this.point2.y;
    return Math.sqrt(dx * dx + dy * dy);
  }
}

// 初期点を定義します。
const a = new Point(200, 100);
const d = new Point(500, 100);
let b = new Point(200, 300);
let c = new Point(500, 400);

console.log(`元の点cの座標: (${c.x}, ${c.y})`);

// 初期のラインの長さを計算します。
const l1 = new Line(a, b).length;
const l2 = new Line(b, c).length;
const l3 = new Line(c, d).length;

// 移動したい距離を定義します。
const dx =50;
const dy =00;

// 目的関数を定義します（現在の位置から所望の移動後の位置までの二乗距離）。
const objective = (x, y) => {
  const dxActual = x - (c.x + dx);
  const dyActual = y - (c.y + dy);
  return dxActual * dxActual + dyActual * dyActual;
};

// 制約関数を定義します（各ラインの初期長さと現在の長さとの差）。
const constraints = [
  (x, y) => Math.pow((new Line(a, new Point(x, y)).length - l1), 2),
  (x, y) => Math.pow((new Line(new Point(x, y), c).length - l2), 2),
  (x, y) => Math.pow((new Line(c, d).length - l3), 2),
];

// 制約付き最適化問題を解く関数を定義します。
function solveConstrainedOptimization(objective, constraints, initialGuess) {
  // 収束判定の閾値と最大反復回数を定義します。
  const TOL = 0.00001;
  const MAX_ITER = 1000000;  

  // ペナルティ関数を定義します（制約関数の総和）。
  const penalty = (x, y) => {
    let penaltySum = 0;
    for (let constraint of constraints) {
      const value = constraint(x, y);
      if (value > 0) {
        penaltySum += value;
      }
    }
    return penaltySum;
  };

  // コスト関数を定義します（目的関数 + ペナルティ関数）。
  const cost = (x, y) => objective(x, y) + penalty(x, y);

  // 初期推測値を設定します。
  let [x, y] = initialGuess;
  let costPrev = cost(x, y);

  // 最急降下法を用いて最適解を探索します。
  for (let i = 0; i < MAX_ITER; i++) {
    // コスト関数の勾配を計算します（中心差分法）。
    const dx = (cost(x + TOL, y) - cost(x - TOL, y)) / (2 * TOL);
    const dy = (cost(x, y + TOL) - cost(x, y - TOL)) / (2 * TOL);

    // 勾配に基づいて現在の推測値を更新します。
    x -= TOL * dx;
    y -= TOL * dy;

    // コスト関数の現在の値を計算します。
    const costCurr = cost(x, y);

    // コスト関数の値が収束したらループを終了します。
    if (Math.abs(costCurr - costPrev) < TOL) {
      break;
    }

    // コスト関数の前の値を更新します。
    costPrev = costCurr;
  }

  // 最適解を返します。
  return [x, y];
}

// Canvas要素を取得し、2D描画コンテキストを取得します。
let canvas = document.getElementById("myCanvas");
let ctx = canvas.getContext("2d");

// 点を描画する関数を定義します。
function drawPoint(ctx, point, color = 'black') {
  ctx.beginPath();
  ctx.arc(point.x, point.y, 5, 0, 2 * Math.PI, false);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.lineWidth = 2;
  ctx.strokeStyle = color;
  ctx.stroke();
}

// ラインを描画する関数を定義します。
function drawLine(ctx, line, color = 'black') {
  ctx.beginPath();
  ctx.moveTo(line.point1.x, line.point1.y);
  ctx.lineTo(line.point2.x, line.point2.y);
  ctx.lineWidth = 2;
  ctx.strokeStyle = color;
  ctx.stroke();
}

// 初期点を描画します。
drawPoint(ctx, a);
drawPoint(ctx, b);
drawPoint(ctx, c, 'blue');
drawPoint(ctx, d);

// 初期ラインを描画します。
drawLine(ctx, new Line(a, b));
drawLine(ctx, new Line(b, c), 'blue');
drawLine(ctx, new Line(c, d));
drawLine(ctx, new Line(a, d));

// 制約付き最適化問題を解きます。
let [xOpt, yOpt] = solveConstrainedOptimization(objective, constraints, [c.x, c.y]);

// 点Cの座標を更新します。
c.x = xOpt;
c.y = yOpt;

// 更新後の点Cを描画します。
drawPoint(ctx, c, 'red');

// 更新後のラインを描画します。
drawLine(ctx, new Line(a, b));
drawLine(ctx, new Line(b, c), 'red');
drawLine(ctx, new Line(c, d));

console.log(`新しい点cの座標: (${c.x}, ${c.y})`);