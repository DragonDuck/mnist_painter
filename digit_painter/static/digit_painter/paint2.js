function init(){
    // Grab canvas object
    canvas = document.getElementById("paint");
    ctx = canvas.getContext("2d");
    ctx.lineWidth = 1;
    ctx.strokeStyle = "#000000";

    // Set up data array that will be passed to the backend
    var arrX = 28;
    var arrY = 28;
    var grid = new Array(arrX);
    for(var i = 0; i < arrY; i++) {
        grid[i] = new Array(arrY);
        grid[i].fill(0);
    }

    // Paint canvas grid
    var gridX = 20;
    var gridY = 20;
    canvas.width = gridX * arrX;
    canvas.height = gridY * arrY;
    for(var ii = 1; ii < arrX; ii++){
        curX = ii * gridX;
        startY = 0;
        endY = canvas.height;
        ctx.beginPath();
        ctx.moveTo(curX, startY);
        ctx.lineTo(curX, endY);
        ctx.stroke();
        ctx.closePath();
    }
    for(var ii = 1; ii < arrY; ii++){
        curY = ii * gridY;
        startX = 0;
        endX = canvas.width;
        ctx.beginPath();
        ctx.moveTo(startX, curY);
        ctx.lineTo(endX, curY);
        ctx.stroke();
        ctx.closePath();
    }

    // Add listeners to keep track of which grid element is being painted
    var hold = false;
    canvas.addEventListener("mousedown", function (e){
        hold = true;
    });
    canvas.addEventListener("mouseup", function (e){
        hold = false;
    });
}