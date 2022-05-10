import { draw_slices, config } from "./utils.js";
let state;

function insertionSort(array, i, j) {
    let key = array[i];


    if (j >= 0 && array[j] > array[i]) {
        array[j + 1] = array[j];
    }
    else {
        return false;
    }

    array[j] = key;
    return true;
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
            i: 1,
            j: 0,
            k: 1,
            slc: config.slice_count,
        };

        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);
        sketch.loop();
    }

    sketch.setup = () => {
        let cnv = sketch.createCanvas(config.canvas_size, config.canvas_size);
        cnv.parent("insertion");
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

        // console.log(state.array)
        const searching = insertionSort(state.array, state.i, state.j);
        if (searching) {
            state.i--;
            state.j--;
        }
        else {
            state.k++
            state.i = state.k;
            state.j = state.i - 1;
        }


        //put drawslices in separate files and each sort in different files and call all files at different times
        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);

        if (state.k === state.array.length) {
            sketch.noLoop();
            config.complete(1, initialize);
        };
    };
};

let myp5 = new p5(s);
