import { draw_slices } from "./utils.js";

const state = {
    //setting up the constants, takes an array to sort and shuffle
    //sets up min and max radius of slices (could potentially be made into slider?)
    //sets up i and j variables for iterate display
    array: [],
    minRadius: 100,
    maxRadius: 300,
    i: 0,
    j: 1,
};


function bubbleSort(array, i) {
    // swap out of order values -- bubble sort
    if (array[i] > array[i + 1]) {
        const temp = array[i];
        array[i] = array[i + 1];
        array[i + 1] = temp;
    };
};

function insertionSort(array, i) {
    key = array[i];
    j = i - 1;

    while (j >= 0 && array[j] > key) {
        array[j + 1] = array[j];
        j = j - 1;
    }
    array[j + 1] = key;
};
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

function mergeSort(arr, n) {

    // For current size of subarrays to
    // be merged curr_size varies from
    // 1 to n/2
    var curr_size;

    // For picking starting index of left subarray to be merged
    var left_start;

    // Merge subarrays in bottom up manner. First merge subarrays
    // of size 1 to create sorted subarrays of size 2, then merge
    // subarrays of size 2 to create sorted subarrays of size 4, and so on.
    for (curr_size = 1; curr_size <= n - 1; curr_size = 2 * curr_size) {

        // Pick starting point of different
        // subarrays of current size
        for (left_start = 0; left_start < n - 1; left_start += 2 * curr_size) {
            // Find ending point of left
            // subarray. mid+1 is starting
            // point of right
            var mid = Math.min(left_start + curr_size - 1, n - 1);

            var right_end = Math.min(left_start + 2 * curr_size - 1, n - 1);

            // Merge Subarrays arr[left_start...mid]
            // & arr[mid+1...right_end]
            merge(arr, left_start, mid, right_end);
        }
    }
}

/*
 * Function to merge the two haves arr[l..m] and arr[m+1..r] of array arr
 */
function merge(arr, l, m, r) {
    var i, j, k;
    var n1 = m - l + 1;
    var n2 = r - m;

    /* create temp arrays */
    var L = Array(n1).fill(0);
    var R = Array(n2).fill(0);

    /*
     * Copy data to temp arrays L and R
     */
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    /*
     * Merge the temp arrays back into arr[l..r]
     */
    i = 0;
    j = 0;
    k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    /*
     * Copy the remaining elements of L, if there are any
     */
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    /*
     * Copy the remaining elements of R, if there are any
     */
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}


function setup() {
    createCanvas(1000, 600);
    colorMode(HSL);
    noStroke();

    //determines initial state of triangles, and how many (could be a slider?)
    state.array = _.shuffle(_.range(40));
};



function draw() {
    //initialize drawing slices
    background(0, 0, 0);

    //put drawslices in separate files and each sort in different files and call all files at different times
    draw_slices(state.array, state.minRadius, state.maxRadius);

    //where to call sorting algorithm (should be slider).
    //bubbleSort(state.array, state.j);

    //insertionSort(state.array, state.j);

    //state.j += 1;
    //if (state.j === state.array.length-1){
    //noLoop();
    //};
    // selectionSort(state.array, state.j, state.i);
    // //iteratively keeps track of array and therefore image, iteratively displays
    // if (state.j === state.array.length) {
    //     state.i += 1;
    //     state.j = state.i + 1;
    // } else {
    //     state.j += 1;
    // }
    // if (state.i === state.array.length - 1) {
    //     noLoop();
    // };

    //iteratively keeps track of array and therefore image, iteratively displays
    //if (state.j === state.array.length - state.i - 1) {
    //state.i += 1;
    //state.j = 0;
    //} else {
    //state.j += 1;
    //}
    //if (state.i === state.array.length - 1){
    //noLoop();
    //};
};

window.setup = setup;
window.draw = draw;
