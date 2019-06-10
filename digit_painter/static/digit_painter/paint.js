function init(){
    var canvas = document.getElementById("paint");
    var hidden_field = document.getElementById("img_base64");
    var ctx = canvas.getContext("2d");
    var curX, curY, prevX, prevY;
    var hold = false;
    ctx.lineWidth = 30;
    ctx.strokeStyle = "#000000";
    ctx.lineCap = "round";

    canvas.addEventListener("mousedown", function (e){
        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        hold = true;

        prevX = curX;
        prevY = curY;
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    }, false);

    canvas.addEventListener("mousemove", function (e){
        if(hold){
            prevX = curX;
            prevY = curY;
            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;
            ctx.moveTo(prevX, prevY);
            ctx.lineTo(curX, curY);
            ctx.stroke();
            ctx.closePath();
            hidden_field.value = canvas.toDataURL("image/png")
        }
    }, false);

    canvas.addEventListener("mouseup", function (e){
        hold = false;
    }, false);

    canvas.addEventListener("mouseout", function (e){
        hold = false;
    }, false);
};

/*
// This function is currently defunct as it does not seem to clear the form cache. Submitting after clearing the
// canvas but not drawing anything new still submits the old content to the form.
function clearcanvas(){
    var canvas = document.getElementById("paint");
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}
*/