import { draw_slices, config } from "./utils.js";

let state;

function bubbleSort(array, i) {
    // swap out of order values -- bubble sort
    if (array[i] > array[i + 1]) {
        const temp = array[i];
        array[i] = array[i + 1];
        array[i + 1] = temp;
    };
};


function s(sketch) {

    function initialize() {
        state = {
            //setting up the constants, takes an array to sort and shuffle
            //sets up min and max radius of slices (could potentially be made into slider?)
            //sets up i and j variables for iterate display
            array: _.shuffle(_.range(config.slice_count)),
            minRadius: config.min_radius,
            maxRadius: config.max_radius,
            i: 0,
            j: 1,
            slc: config.slice_count,
        };
        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);
        sketch.loop();
    }

    sketch.setup = () => {
        let cnv = sketch.createCanvas(config.canvas_size, config.canvas_size);
        cnv.parent("bubble");
        sketch.colorMode(sketch.HSL);
        sketch.noStroke();

        config.initializers.push(initialize);
        initialize();
    };

    sketch.draw = () => {
        sketch.frameRate(config.frameRate);
        if (state.slc !== config.slice_count) {
            initialize();
        };
        //initialize drawing slices
        sketch.background(0, 0, 0);

        //put drawslices in separate files and each sort in different files and call all files at different times
        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);

        //where to call sorting algorithm (should be slider).
        bubbleSort(state.array, state.j);

        //iteratively keeps track of array and therefore image, iteratively displays
        if (state.j === state.array.length - state.i - 1) {
            state.i += 1;
            state.j = 0;
        } else {
            state.j += 1;
        }
        if (state.i === state.array.length - 1) {
            sketch.noLoop();
            config.complete(3, initialize);
        };
    };
};

let myp5 = new p5(s);
