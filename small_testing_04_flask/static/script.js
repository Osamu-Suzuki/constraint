let data = {
    a: {x: 200, y: 100},
    b: {x: 200, y: 300},
    c: {x: 500, y: 400},
    d: {x: 500, y: 100},
    displacement: [100, -20]
}

fetch('/optimize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(r_data => {
    // 最適化後の新しい座標を取得
    let newCoordinates = r_data;

    // 新しい座標をcanvasに描画
    let canvas = document.getElementById('myCanvas');
    let ctx = canvas.getContext('2d');

    console.log(data);

    // 初期座標描画
    ctx.beginPath();
    ctx.moveTo(data.a.x, data.a.y);
    ctx.lineTo(data.b.x, data.b.y);
    ctx.lineTo(data.c.x, data.c.y);
    ctx.lineTo(data.d.x, data.d.y);
    ctx.lineTo(data.a.x, data.a.y);
    ctx.stroke();

    // 最終座標描画
    ctx.beginPath();
    ctx.moveTo(data.a.x, data.a.y);
    ctx.lineTo(newCoordinates.b.x, newCoordinates.b.y);
    ctx.lineTo(newCoordinates.c.x, newCoordinates.c.y);
    ctx.lineTo(data.d.x, data.d.y);
    ctx.lineTo(data.a.x, data.a.y);
    ctx.stroke();
})
.catch((error) => {
    console.error('Error:', error);
});
