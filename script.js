// Canvas and context setup
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Scale canvas
ctx.scale(1, 1);

// Shape class
class Point {
  constructor(x, y, name) {
    this.x = x;
    this.y = y;
    this.name = name;
  }

  move(dx, dy) {
    this.x += dx;
    this.y += dy;
  }

  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = "black";
    ctx.fill();
    ctx.font = '30px Arial';
    ctx.fillStyle = "black";
    ctx.fillText(this.name, this.x + 0.05, this.y);
  }
}

// Constraint class
class Constraint {
  constructor(point1, point2, length) {
    this.point1 = point1;
    this.point2 = point2;
    this.length = length;
  }

  check() {
    const dx = this.point1.x - this.point2.x;
    const dy = this.point1.y - this.point2.y;
    return Math.hypot(dx, dy) === this.length;
  }

  // 制約が満たされない場合に、その制約が満たされるように point2 の位置を修正する
  correct() {
    //point1 と point2 の間の x 座標と y 座標の差（つまり、ベクトルの成分）を計算
    const dx = this.point1.x - this.point2.x;
    const dy = this.point1.y - this.point2.y;

    //point1 と point2 の間の現在の距離を計算
    const currentLength = Math.hypot(dx, dy);

    //設定された目標の長さ（制約で指定された距離）と現在の長さ（実際の距離）との差を計算
    const diff = this.length - currentLength;
    
    // Use a simple gradient descent approach to correct the position
    // 単純な勾配降下法を用いた調整のための因子。調整の「強さ」を制御する。
    // 値が大きければ大きいほど、一度の調整で point2 が大きく動きます。
    const correctionFactor = 0.000000001;
    
    // Calculate correction for x and y separately
    // X軸方向とY軸方向の補正量をそれぞれ計算。
    // 調整量は、点間のベクトル（dx および dy）に補正因子と差の比を掛けたもの。
    // この比は、誤差が大きいほど、または目標の距離が短いほど大きくなり、その結果、調整の大きさが増加する
    const correctionX = dx * correctionFactor * diff / currentLength;
    const correctionY = dy * correctionFactor * diff / currentLength;
    
    // point2 の位置を修正するため
    this.point2.move(correctionX, correctionY);    
  }
}

// Create points
const a = new Point(200, 100, "a");
const b = new Point(200, 300, "b");
const c = new Point(500, 400, "c");
const d = new Point(500, 100, "d");

// Create constraints
const initialLengths = [
  Math.hypot(a.x - b.x, a.y - b.y), // Initial length of line segment ab
  Math.hypot(c.x - d.x, c.y - d.y), // Initial length of line segment cd
  Math.hypot(b.x - c.x, b.y - c.y), // Initial length of line segment bc
];
const constraints = [
  new Constraint(a, b, initialLengths[0]), // Constraint for line segment ab
  new Constraint(c, d, initialLengths[1]), // Constraint for line segment cd
  new Constraint(b, c, initialLengths[2]), // Constraint for line segment bc
];

// Draw initial state
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  [a, b, c, d].forEach(point => point.draw());
  ctx.beginPath();
  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);
  ctx.lineTo(c.x, c.y);
  ctx.lineTo(d.x, d.y);
  ctx.closePath();
  ctx.stroke();
}

// Draw initial state and log initial lengths
draw();
console.log("Initial lengths: ", initialLengths);


// Simulate drag event
function onDrag(dx, dy) {
  // Move point C
  c.move(dx, dy);

  // Correct position until constraints are satisfied
  let count = 0;
  while (!constraints.every(constraint => constraint.check()) && count < 1000) {
    constraints.forEach(constraint => constraint.correct());
    count++;
  }

  // Redraw and log final lengths
  draw();
  const finalLengths = constraints.map(constraint => Math.hypot(constraint.point1.x - constraint.point2.x, constraint.point1.y - constraint.point2.y));
  console.log("Final lengths: ", finalLengths);

  // Log the position of each point
  console.log(`a: (${a.x}, ${a.y})`);
  console.log(`b: (${b.x}, ${b.y})`);
  console.log(`c: (${c.x}, ${c.y})`);
  console.log(`d: (${d.x}, ${d.y})`);

}

// For example
onDrag(50, 0);
