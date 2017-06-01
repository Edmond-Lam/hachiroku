var winner = -1;

window.onload = function() {
    var judgables = document.getElementsByClassName('judgable');
    for (var i = 0; i < judgables.length; i++) {
	judgables[i].onclick = function(e) {
	    winner = Array.prototype.indexOf.call(judgables, this);//judgables.indexOf(this);
	    console.log(winner);
	    document.getElementById("winner").value = winner;
	    for ( var j = 0; j < judgables.length; j++) {
		judgables[j].style.border = "0px";
	    }
	    this.style.border = "3px solid green";
	}
    }
}
