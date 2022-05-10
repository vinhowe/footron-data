import { draw_slices, config } from "./utils.js";
let state;

function swap(arr, xp, yp) {
    var temp = arr[xp];
    arr[xp] = arr[yp];
    arr[yp] = temp;
}
function selectionSort(array, j, i) {
    var min_idx = i;
    if (array[j] < array[min_idx])
        min_idx = j;
    // Swap the found minimum element with the first element
    swap(array, min_idx, i);
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
            j: 0,
            k: 1,
            slc: config.slice_count,
        };
        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);
        sketch.loop();
    }

    sketch.setup = () => {
        let cnv = sketch.createCanvas(config.canvas_size, config.canvas_size);
        cnv.parent("selection");
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
        selectionSort(state.array, state.j, state.i);


        //put drawslices in separate files and each sort in different files and call all files at different times
        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);
        //iteratively keeps track of array and therefore image, iteratively displays
        if (state.j === state.array.length) {
            state.i += 1;
            state.j = state.i + 1;
        } else {
            state.j += 1;
        }
        if (state.i === state.array.length - 1) {
            sketch.noLoop();
            config.complete(2, initialize);
        };
    };
};

let myp5 = new p5(s);