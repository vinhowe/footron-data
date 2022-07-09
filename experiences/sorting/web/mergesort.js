import { config, draw_slices } from "./utils.js";

let state;

const FULLY_SORTED = 0;
const NEXT_SUBGROUP_SIZE = 1;
const STEP_MERGE = 2;
const NEXT_SUBGROUP = 3;

function merge(arr, left, right) {
    // console.log("in merge:", { arr, left, right })
    // let arr = []
    // Break out of loop if any one of the array gets empty
    //while (left.length && right.length) {
    // Pick the smaller among the smallest element of left and right sub arrays
    if (!(left.length && right.length)) {
        return [[...arr, ...left, ...right], [], []]
    }
    else {
        if (left[0] < right[0]) {
            arr.push(left.shift())
        } else {
            arr.push(right.shift())
        }
    }

    //}
    // Concatenating the leftover elements
    // (in case we didn't go through the entire left or right array)
    return [arr, left, right]
};

function selectiveMerge(array, i, sgs) {
    const copy = [...array]
    //check that there is another subgroup to sort in current pass
    if (array.length - i < sgs + 1) {
        // console.log("Not another subgroup")
        // console.log(array.length, i, sgs)
        return [NEXT_SUBGROUP_SIZE, copy]
    };
    const start = copy.slice(0, i);
    if (!state.left.length && !state.right.length) {
        // console.log("setting boys")
        state.left = copy.slice(i, i + sgs);
        const subgroupEnd = i + 2 * sgs < array.length ? i + 2 * sgs : array.length;
        // console.log(subgroupEnd);
        state.right = copy.slice(i + sgs, subgroupEnd);
        // console.log({ copy, left: state.left, right: state.right[0], rightStart: i + sgs, rightEnd: subgroupEnd })
    }

    const [merged, left, right] = merge(state.merged, state.left, state.right);
    if (merged.length === copy.length) {
        return [FULLY_SORTED, merged]
    }
    state.merged = merged;
    state.left = left;
    state.right = right;
    const status = (left.length + right.length) ? STEP_MERGE : NEXT_SUBGROUP


    const endIndex = (i + 2 * sgs) - copy.length;
    const end = endIndex >= 0 ? [] : copy.slice(endIndex)
    const concat = [...start, ...merged, ...left, ...right, ...end]

    if (status === NEXT_SUBGROUP) {
        state.merged = [];
    }

    return [status, concat];
};

function s(sketch) {

    function initialize() {
        state = {
            //setting up the constants, takes an array to sort and shuffle
            //sets up min and max radius of slices (could potentially be made into slider?)
            //sets up i and j variables for iterate display
            array: _.shuffle(_.range(config.slice_count)),
            states: [],
            minRadius: config.min_radius,
            maxRadius: config.max_radius,
            subgroupSize: 1,
            i: 0,
            slc: config.slice_count,
            merged: [],
            left: [],
            right: [],
        };
        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);
        sketch.loop();
    }

    sketch.setup = () => {
        let cnv = sketch.createCanvas(config.canvas_size, config.canvas_size);
        cnv.parent("merge");
        sketch.colorMode(sketch.HSL);
        sketch.noStroke();

        config.initializers.push(initialize);
        initialize();
    };


    sketch.draw = () => {
        // initialize drawing slices
        sketch.background(0, 0, 0);
        sketch.frameRate(config.frameRate - 10);

        if (state.slc !== config.slice_count) {
            initialize()
        };

        const [result, next] = selectiveMerge(state.array, state.i, state.subgroupSize);

        state.array = [...next]



        //put drawslices in separate files and each sort in different files and call all files at different times
        draw_slices(sketch, state.array, state.minRadius, state.maxRadius);

        switch (result) {
            case FULLY_SORTED:
                // console.log("DONE!")
                sketch.noLoop();
                config.complete(0, initialize);
                break
            case NEXT_SUBGROUP_SIZE:
                state.i = 0;
                state.subgroupSize *= 2;
                break;
            case NEXT_SUBGROUP:
                state.i += 2 * state.subgroupSize;
                break;
            case STEP_MERGE:
                break;
        }


    };
};

let myp5 = new p5(s);