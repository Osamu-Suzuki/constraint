// 図形と拘束条件のクラスを定義
class Shape {
    constructor() {
        // 図形の座標、大きさなどの情報を保持
    }
    // 図形を描画するメソッド
    draw() { /* ... */ }
}

class Constraint {
    constructor(shape1, shape2, condition) {
        this.shape1 = shape1;
        this.shape2 = shape2;
        this.condition = condition;
    }
    // 拘束条件が満たされているかチェックするメソッド
    check() {
        return this.condition(this.shape1, this.shape2);
    }
}

// 図形と拘束条件のリストを作成
let shapes = [/* ... */];
let constraints = [/* ... */];

// ユーザーが図形をドラッグしたときのイベントハンドラ
function onDrag(shape, dx, dy) {
    // 図形を一時的に移動
    shape.move(dx, dy);
    // 拘束条件が全て満たされるように図形を調整
    while (!constraints.every(c => c.check())) {
        // 数値計算ライブラリを使って、拘束条件を満たすような位置や大きさを求める
    }
    // 図形を描画
    shapes.forEach(s => s.draw());
}