var svg;
var rid;
var moving = true;
var circles = 0;
var circtimer;

var linedot = function() {
    drawCircle(Math.floor(Math.random()*(window.innerWidth-180))+90, Math.floor(Math.random() * (window.innerHeight-180))+90, Math.floor(Math.random()*35)+10);
    circles++;
    if (circles > 50) {
	window.clearInterval(circtimer);
    }
};

var drawCircle = function(x, y, r, vx, vy) {
    var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", x );
    if (x <= r ) { x += r; }
    if (x >= parseInt(svg.getAttribute("width"))-r) { x -= r; }
    if (y <= r ) { y += r; }
    if (y >= parseInt(svg.getAttribute("height"))-r) { y -= r; }
    circle.setAttribute("cy", y);
    if (vx == undefined) {
	circle.setAttribute("vx", getRandomPlusOrMinus());
    } else {
	circle.setAttribute("vx", vx);
    }
    if (vy == undefined) {
	circle.setAttribute("vy", getRandomPlusOrMinus());
    } else {
	circle.setAttribute("vy", vy);
    }
    var grow = function() {
	circle.setAttribute("r", parseInt(circle.getAttribute("r"))+2);
    }
    var interval = window.setInterval(function() {
	if (parseInt(circle.getAttribute("r")) > r*2-1) {
	    window.clearInterval(interval);
	} else {
	    grow()
	}
    }, .05);
    circle.setAttribute("r", 1);//r*2);
    circle.setAttribute("fill", "hsl(" + rid % 360 + ", 90%, 60%)");
    //circle.setAttribute("fill", color);
    svg.appendChild(circle);
    console.log("Circle at ( " + x + ", " + y + " )");
    return circle;
};

var getRandomPlusOrMinus = function() {
    if (Math.random() > 0.5) {
	return 1;
    }
    return -1;
}
    
var draw = function() {
    if (moving) {
	for (i=0; i < svg.childNodes.length; i++) {
	    var thisone = svg.childNodes[i];
	    thisone.setAttribute("cx", parseInt(thisone.getAttribute("cx"))+parseInt(thisone.getAttribute("vx")));
	    thisone.setAttribute("cy", parseInt(thisone.getAttribute("cy"))+parseInt(thisone.getAttribute("vy")));
	    if (parseInt(thisone.getAttribute("cx")) + parseInt(thisone.getAttribute("r")) > parseInt(svg.getAttribute("width")) || parseInt(thisone.getAttribute("cx")) - parseInt(thisone.getAttribute("r")) < 0) {
		thisone.setAttribute("vx", - parseInt(thisone.getAttribute("vx")));
	    }
	    if (parseInt(thisone.getAttribute("cy")) + parseInt(thisone.getAttribute("r")) > parseInt(svg.getAttribute("height")) || parseInt(thisone.getAttribute("cy")) - parseInt(thisone.getAttribute("r")) < 0) {
		thisone.setAttribute("vy",- parseInt(thisone.getAttribute("vy")));
	    }
	    /*if (parseInt(thisone.getAttribute("cx")) == Math.floor(parseInt(svg.getAttribute("width")) / 2)) {
		split(thisone);
	    }*/
	    if (parseInt(thisone.getAttribute("r"))<1) {
		svg.removeChild(thisone);
	    }

	}
    }
    rid = window.requestAnimationFrame(draw);
}

var split = function(bubble) {
    drawCircle(parseInt(bubble.getAttribute("cx")), parseInt(bubble.getAttribute("cy")), Math.floor(parseFloat(bubble.getAttribute("r"))/2), parseInt(bubble.getAttribute("vx")), parseInt(bubble.getAttribute("vy")));
    drawCircle(parseInt(bubble.getAttribute("cx")), parseInt(bubble.getAttribute("cy")), Math.floor(parseFloat(bubble.getAttribute("r"))/2), - parseInt(bubble.getAttribute("vx")), - parseInt(bubble.getAttribute("vy")));
    svg.removeChild(bubble);
}

var move = function() {
    moving = !moving;
}

var clearAll = function() {
    while (svg.firstChild) {
	svg.removeChild(svg.firstChild);
    }
};

var resize = function() {
    svg.setAttribute("width", window.innerWidth);
    svg.setAttribute("height", window.innerHeight);
};

var setup = function() {
    svg = document.getElementById("doodles");
    svg.setAttribute("width", window.innerWidth);
    svg.setAttribute("height", window.innerHeight);
    window.onresize = resize;
    console.log(svg);
    circtimer = window.setInterval(linedot, 500);
    svg.addEventListener("click", linedot);
    draw();
};

window.onload = setup;

