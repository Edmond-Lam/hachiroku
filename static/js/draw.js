var canvas, ctx;
var pmouseX, pmouseY;
var mouseDown;
var strokeWeight = 10;
var slider;

window.onload = function() {
    canvas = document.getElementById("doodle");
    ctx = canvas.getContext("2d");
    pmouseX = -1;
    pmouseY = -1;
    slider=document.getElementById("width");
    canvas.onmousemove = function(e) {
	strokeWeight = slider.value;
	if (pmouseX > 0 && pmouseY > 0 && mouseDown) {
	    ctx.beginPath();
	    ctx.arc(pmouseX, pmouseY, strokeWeight/8, 0, 2 * Math.PI, false);
	    ctx.moveTo(pmouseX, pmouseY);
	    ctx.lineTo(e.offsetX, e.offsetY);
	    ctx.lineWidth = strokeWeight;
	    ctx.stroke();
	}
	    pmouseX = e.offsetX;
	    pmouseY = e.offsetY;
    }
    canvas.onmousedown = function(e) { mouseDown = true; }
    canvas.onmouseup = function(e) {
	mouseDown = false;
	pmouseX = -1;
	pmouseY = -1;
    }
}
