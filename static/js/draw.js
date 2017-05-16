var canvas, ctx;
var pmouseX, pmouseY;
var mouseDown;
var strokeWeight = 10;
var slider;
var curColor;

window.onload = function() {
    canvas = document.getElementById("doodle");
    ctx = canvas.getContext("2d");
    pmouseX = -1;
    pmouseY = -1;
    curColor = "#000000"
    slider=document.getElementById("width");
    clear = document.getElementById("cls");
    drawbtn = document.getElementById("draw");
    erasebtn = document.getElementById("erase");
    drawPreview = document.getElementById("drawcircle");
    clear.onclick = function(e) {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
    };
    for (var i = 0; i < document.getElementsByClassName("block").length; i++) {
	document.getElementsByClassName("block")[i].addEventListener("click", function(e) {
	    curColor = this.style.backgroundColor;
	});
    }
    canvas.onmousemove = function(e) {
	strokeWeight = slider.value;
	if (pmouseX > 0 && pmouseY > 0 && mouseDown) {
	    if (drawbtn.checked) {
		console.log(drawbtn.checked);
		ctx.fillStyle = curColor;
		ctx.strokeStyle = curColor;
	    } else {
		if (canvas.style.backgroundColor == "") {
		    ctx.fillStyle = "#FFFFFF";
		    ctx.strokeStyle = "#FFFFFF";
		} else {
		    ctx.fillStyle = canvas.style.backgroundColor;
		    ctx.strokeStyle = canvas.style.backgroundColor;
		}
	    }
	    ctx.beginPath();
	    ctx.arc(pmouseX, pmouseY, strokeWeight/2, 0, 2 * Math.PI, false);
	    ctx.fill();
	    ctx.beginPath();
	    ctx.moveTo(pmouseX, pmouseY);
	    ctx.lineTo(e.offsetX, e.offsetY);
	    ctx.lineWidth = strokeWeight;
	    ctx.stroke();
	}
	    pmouseX = e.offsetX;
	    pmouseY = e.offsetY;
    };
    canvas.onmousedown = function(e) { mouseDown = true; };
    canvas.onmouseup = function(e) {
	mouseDown = false;
	pmouseX = -1;
	pmouseY = -1;
    };
}
