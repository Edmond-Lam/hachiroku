var canvas, ctx;
var pmouseX, pmouseY;
var mouseDown;
var strokeWeight = 10;
var timer, counter;
var curColor, drawPreview;
var drawbtn, erasebtn, slider;
var savedImage;
var imgString;

var stoImage = function() {

    imgString = canvas.toDataURL("image/jpeg");
    canvas.parentNode.removeChild(canvas);
    drawPreview.parentNode.removeChild(drawPreview);
    var drawtools = document.getElementsByClassName("drawtool");
    console.log(drawtools);
    for (var i = 0; i < drawtools.length; i++) {
	console.log(drawtools[i]);
	drawtools[i].parentNode.removeChild(drawtools[i]);
    }
    savedImage.src = imgString;
    document.getElementById("upload").value = imgString;
    var submitbtn = document.createElement("input");
    submitbtn.type = "submit";
    submitbtn.value = "Upload Picture";
    document.getElementById("datForm").appendChild(submitbtn);
};

var countDown = function(e) {
    if (timer.innerHTML == "0") {
	timer.innerHTML = "Times Up!!";
	window.clearInterval(counter);
    } else {
	timer.innerHTML = parseInt(timer.innerHTML) - 1;
    }
}

var draw = function(e) {
    drawPreview.style.left = e.clientX - slider.value/2;
    drawPreview.style.top = e.clientY - slider.value/2;
    
    if (pmouseX > 0 && pmouseY > 0 && mouseDown) {
	if (drawbtn.checked) {
	    ctx.fillStyle = curColor;
	    ctx.strokeStyle = curColor;
	    drawPreview.style.borderColor = curColor;
	} else {
	    if (canvas.style.backgroundColor == "") {
		ctx.fillStyle = "#FFFFFF";
		ctx.strokeStyle = "#FFFFFF";
		drawPreview.style.borderColor = "#FFFFFF";
	    } else {
		ctx.fillStyle = canvas.style.backgroundColor;
		ctx.strokeStyle = canvas.style.backgroundColor;
		drawPreview.style.borderColor = canvas.style.backgroundColor;
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

window.onload = function() {
    canvas = document.getElementById("doodle");
    ctx = canvas.getContext("2d");
    ctx.fillStyle = "#FFFFFF";
    ctx.rect(0,0,canvas.width, canvas.height);
    ctx.fill();
    pmouseX = -1;
    pmouseY = -1;
    curColor = "#000000"
    slider=document.getElementById("width");
    clear = document.getElementById("cls");
    drawbtn = document.getElementById("draw");
    erasebtn = document.getElementById("erase");
    drawPreview = document.getElementById("drawcircle");
    timer = document.getElementById("timeleft");
    savedImage = document.getElementById("saved-img");
    window.setTimeout(stoImage, parseInt(timer.innerHTML)*1000);
    counter = window.setInterval(countDown, 1000);    
    clear.onclick = function(e) {
	ctx.fillStyle = "#FFFFFF";
	ctx.rect(0,0,canvas.width, canvas.height);
	ctx.fill();
    };
    
    for (var i = 0; i < document.getElementsByClassName("block").length; i++) {
	document.getElementsByClassName("block")[i].addEventListener("click", function(e) {
	    curColor = this.style.backgroundColor;
	    drawPreview.style.borderColor = curColor;
	});
    }
    
    slider.onchange = function(e) {
	strokeWeight = slider.value;
	drawPreview.style.height = slider.value;
	drawPreview.style.width = slider.value;
	drawPreview.style.borderWidth = slider.value/20;
	document.getElementById("stroke-width").innerHTML = "Scroll to change brush size: " + slider.value;
    };

    canvas.onwheel = function(e) {
	slider.value -= (e.deltaY / Math.abs(e.deltaY));
	strokeWeight = slider.value;
	drawPreview.style.height = slider.value;
	drawPreview.style.width = slider.value;
	drawPreview.style.borderWidth = slider.value/12;
	document.getElementById("stroke-width").innerHTML = "Scroll to change brush size: " + slider.value;
    };
    
    canvas.onmouseleave = function(e) {
	mouseDown = false;
	pmouseX = -1;
	pmouseY = -1;
    }
    
    canvas.onmousemove = function(e) {
	draw(e);
    };
    
    canvas.onmousedown = function(e) {
	mouseDown = true;
	draw(e);
    };
    
    canvas.onmouseup = function(e) {
	mouseDown = false;
	pmouseX = -1;
	pmouseY = -1;
    };
}
