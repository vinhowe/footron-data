
var color_step = 0.0;

var frame_no = 3;
var width = 2736;
var height = 1216;

var deltas = [ -4, -3, -2, -1, 0, 0, 1, 2, 3, 4 ];
var curdelt = 1;

var digits_per_frame = 1000;
var TOTAL = 1000000;

var cx = 2300;
var cy = 1100;

var SS = 0.25;

function draw_line( dx, dy, colorind ) {

    if ( colorind > 1.0) {
	colorind = 1.0;
    }

//    console.log( cx, cy, dx, dy, colorind );
    
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");

    ctx.beginPath();
    ctx.moveTo(cx,cy);
    cx += dx*SS;
    cy += dy*SS;
    ctx.lineTo(cx,cy);

    cx = (0.999999)*cx + 0.000001*(width/2.0);
    cy = (0.999999)*cy + 0.000001*(height/2.0);    
    
    var rgb = evaluate_cmap( colorind, 'twilight', false);
    ctx.strokeStyle = 'rgba(' + rgb.join(",") + ',0.3)';
    ctx.lineCap = "round";
    ctx.lineWidth = 3;
    ctx.stroke();
}

function animate() {
    requestAnimationFrame( animate );


    for ( var i=0; i<digits_per_frame; i++ ) {

	color_step += 1.0/TOTAL;
	if ( color_step >= 1.0 ) {
	    color_step = 0.0;
	}
	
	var dx = parseInt( pi1m[frame_no] );
	var dy = parseInt( pi1m[frame_no+curdelt] );
	
	frame_no = frame_no + 1 + curdelt;
	
	draw_line( deltas[dx], deltas[dy], color_step );
	
	if ( frame_no >= TOTAL-10000 ) {	
	    frame_no = 3;
	    curdelt += 1;
	}
    }
}
