
var TOTAL_IN = 0;
var TOTAL_POINTS = 0;
var TOTAL_OUT = 0;

//BGCOLOR = '#444444';
BGCOLOR = '#445566';

var scene, scgroup, pgroup, renderer, camera;

function initialize_three_scene() {

    _bgColor = new THREE.Color( BGCOLOR );

    //
    // -------------------------------------------------------
    //

    renderer = new THREE.WebGLRenderer( { antialias: true, alpha: true } );

    renderer.setClearColor( _bgColor );
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.shadowMap.enabled = true;

    renderer.setSize( 2736, 1216 );
    document.body.appendChild( renderer.domElement );

    //
    // -------------------------------------------------------
    //

    scene = new THREE.Scene();
    scene.background = _bgColor;
    scene.fog = new THREE.FogExp2( _bgColor, 0.02 );

    camera = new THREE.PerspectiveCamera( 50, 2736.0 / 1216.0, 0.1, 1000 );
    camera.position.z = 4;

    const lights = [];
    lights[ 0 ] = new THREE.PointLight( 0xffffff, 1, 0 );
    lights[ 1 ] = new THREE.PointLight( 0xffffff, 1, 0 );
    lights[ 2 ] = new THREE.PointLight( 0xffffff, 1, 0 );
    lights[ 0 ].position.set( 0, 200, 0 );
    lights[ 1 ].position.set( 100, 200, 100 );
    lights[ 2 ].position.set( - 100, - 200, - 100 );
    scene.add( lights[ 0 ] );
    scene.add( lights[ 1 ] );
    scene.add( lights[ 2 ] );

    pgroup = new THREE.Group();
    scene.add( pgroup );

    scgroup = create_spherecube()
    scene.add( create_floor() );
    scene.add( scgroup );

    scgroup.position.x -= 1.1;
    pgroup.position.x -= 1.1;

    return scene, scgroup, pgroup
}

//
// -------------------------------------------------------
//

function create_spherecube() {
    const group = new THREE.Group();    
    const cgeometry = new THREE.BoxGeometry(2,2,2);
    const cmaterial = new THREE.MeshPhongMaterial( { emissive: 0x072534, side: THREE.DoubleSide, flatShading: true } );
    const cline = new THREE.Mesh( cgeometry, cmaterial );
    cline.material.color = new THREE.Color(0.7,0.7,1);
    //cline.material.depthTest = false;
    cline.material.opacity = 0.25;
    cline.material.transparent = true;
    cline.material.depthWrite = false;
    group.add( cline );

    const sgeometry = new THREE.SphereGeometry( 1.0, 32, 32, 0, Math.PI );
    //const smaterial = new THREE.MeshBasicMaterial( { color: 0xffff00 } );
    const smaterial = new THREE.MeshPhongMaterial( { color: 0x156289, emissive: 0x072534, side: THREE.DoubleSide } ); // , flatShading: true
    const sphere = new THREE.Mesh( sgeometry, smaterial );
    group.add( sphere );

    /*
    const geometry = new THREE.SphereGeometry( 1.005, 32, 32 );
    const wireframe = new THREE.WireframeGeometry( geometry );
    const line = new THREE.LineSegments( wireframe );
    line.material.color = new THREE.Color(0.7,0.7,1);
    //line.material.depthTest = false;
    line.material.side = THREE.DoubleSide;
    line.material.opacity = 0.03;
    line.material.transparent = true;
    line.material.depthWrite = false;
    group.add( line );
    */

    return group;
}

function add_points( cnt, add_to_scene ) {
    if (!add_to_scene) {
	return simple_add_points( cnt );
    } else {
	return complex_add_points( cnt );
    }
}

function simple_add_points( cnt ) {
    var n = 2;
    var n2 = n / 2; // particles spread in the cube

    var in_cnt = 0;
    var out_cnt = 0;
    
    for (var i = 0; i < cnt; i++) {
	var x = Math.random() * n - n2;
	var y = Math.random() * n - n2;
	var z = Math.random() * n - n2;
	var in_or_out = Math.sqrt( x*x + y*y + z*z ) < 1.0;
	if ( in_or_out ) {
	    in_cnt++;
	} else {
	    out_cnt++;
	}
    }
    return [ None, in_cnt, out_cnt ];
}

function complex_add_points( cnt ) {
    var geometry = new THREE.BufferGeometry();
    var positions = [];
    var colors = [];
    var color = new THREE.Color();

    var n = 2;
    var n2 = n / 2; // particles spread in the cube

    var in_cnt = 0;
    var out_cnt = 0;

    for (var i = 0; i < cnt; i++) {
	var x = Math.random() * n - n2;
	var y = Math.random() * n - n2;
	var z = Math.random() * n - n2;
	var in_or_out = Math.sqrt( x*x + y*y + z*z ) < 1.0;
	if ( in_or_out ) {
	    in_cnt++;
	} else {
	    out_cnt++;
	}

   	if ( in_or_out ) {
	    color.setRGB(1.0, 0.0, 0.0);	    
	} else {
	    color.setRGB(0.0, 1.0, 0.0);
	}
	positions.push(x, y, z);	
	colors.push(color.r, color.g, color.b);
    }

    geometry.setAttribute(
	'position',
	new THREE.Float32BufferAttribute(positions, 3)
    );
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geometry.computeBoundingSphere();

    var material = new THREE.PointsMaterial({
	size: 1.0/250.0,
	vertexColors: THREE.VertexColors
    });

    let p = new THREE.Points(geometry, material);
    
    pgroup.add(p);
    
    return [ p, in_cnt, out_cnt ];
}

function create_floor() {
    var geometry = new THREE.PlaneGeometry( 4000, 4000, 10, 10 );
    var planeMaterial = new THREE.MeshStandardMaterial( {
        roughness: 0.7,
        metalness: 1.0,
        color: 0x333333,
        emissive: 0x000000
    });
    var floor = new THREE.Mesh( geometry, planeMaterial );

    floor.rotation.x = -1.57;
    floor.receiveShadow = true;
    floor.position.y = -10;

    return floor;
}

var frame_no = 0;
function animate() {
    requestAnimationFrame( animate );

    frame_no ++;
    
    scgroup.rotation.y += 0.004;
    pgroup.rotation.y += 0.004;

    //var [p, in_cnt, out_cnt] = add_points( 1000, frame_no % 2 == 0 );
    var [p, in_cnt, out_cnt] = add_points( 500, true );

    TOTAL_IN += in_cnt;
    TOTAL_OUT += out_cnt;
    TOTAL_POINTS = TOTAL_IN + TOTAL_OUT;
    var pihat = 6.0 * ( TOTAL_IN / TOTAL_POINTS );
    
    document.getElementById( "in_cnt" ).innerHTML = TOTAL_IN;
    document.getElementById( "overall_cnt" ).innerHTML = TOTAL_POINTS;
    document.getElementById( "pihat" ).innerHTML = pihat.toFixed(7);

    if ( TOTAL_POINTS > 5000000 ) {
	reset_scene();
    }
    
    renderer.render( scene, camera );
}

function reset_scene() {
    TOTAL_IN = 0;
    TOTAL_POINTS = 0;
    TOTAL_OUT = 0;
    pgroup.clear();
}

