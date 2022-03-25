
var frame_no = 0;
var digit_frame_no = 0;
var delta = 0;
var charwidth = 38; // yep. super hacked to figure this out.
var shift = charwidth/4.0;
var spaces = "                                                                  ";

var disp_pi1m = spaces + pi1m;

var width = 2736;
var height = 1216;
var twopi = 2 * Math.PI;
var radius = 500;
var cx = width/2;
var cy = height/2 - 30;

function prep_canvas() {
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");

    for ( var i=0; i<10; i++ ) {
	ctx.beginPath();
	ctx.arc( cx, cy, radius, i*(twopi/10)+0.05, (i+1)*(twopi/10)-0.05 );

	var rgb = evaluate_cmap( i/10.0, 'gist_rainbow', false);

	ctx.strokeStyle = 'rgba(' + rgb.join(",") + ',0.9)';
	ctx.lineCap = "round";
	ctx.lineWidth = 20;
	ctx.stroke();
    }
}

function draw_arc( d1, d2 ) {
    d1 = parseInt( d1 );
    d2 = parseInt( d2 );

    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");

    var d1theta = twopi * (d1/10) + 0.05 + frame_no/20000.0;
    var d2theta = twopi * (d2/10) + 0.05 + frame_no/20000.0;

    var sx = cx + (radius-10) * Math.cos( d1theta );
    var sy = cy + (radius-10) * Math.sin( d1theta );
    var ex = cx + (radius-10) * Math.cos( d2theta );
    var ey = cy + (radius-10) * Math.sin( d2theta );

    ctx.beginPath();
    ctx.moveTo(sx,sy);
    ctx.quadraticCurveTo(cx,cy,ex,ey);
    var rgb = evaluate_cmap( d1/10.0, 'gist_rainbow', false);
    ctx.strokeStyle = 'rgba(' + rgb.join(",") + ',0.1)';
    ctx.lineCap = "round";
    ctx.lineWidth = 2;
    ctx.stroke();
}

function animate() {
    requestAnimationFrame( animate );

    frame_no++;
    if ( frame_no > 1 ) {
	draw_arc( pi1m[frame_no], pi1m[frame_no+1] );
    }

    var digitelem = document.getElementById( "pidigits" );
    digitelem.style.left = String(digitelem.getBoundingClientRect().left - shift) + 'px';
    delta += shift;
    if ( delta == charwidth ) {
	digitelem.style.left = digitelem.getBoundingClientRect().left + charwidth + 'px';
	delta = 0;
	digit_frame_no++;
	document.getElementById( "pidigits" ).innerHTML = disp_pi1m.substr(digit_frame_no,100)
    }
}
