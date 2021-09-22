// Performance optimizations based on
// https://github.com/Tebs-Lab/conways-game-of-life/blob/master/scripts/conways-simulator.js

const PATTERNS = [
  // gliders in different orientations
  ["010", "001", "111"],
  ["010", "100", "111"],
  ["011", "101", "001"],
  ["001", "101", "011"],
  ["100", "101", "110"],
  ["110", "101", "110"],
  ["111", "100", "010"],
  ["111", "001", "010"],
  // R-pentomino
  ["011", "110", "010"],
];

// Size in pixels to make each cell. Not density independent.
const CELL_SIZE = 4;
// This assumes 60FPS, and running at 1x on a 30FPS display might not show some oscillations.
const FRAME_DURATION = 16.6667;
// We have to cap steps per frame or we can get into a feedback loop where each frame takes longer than the last one
const MAX_STEPS_PER_FRAME = 15;
// How many steps we let a cell be continuously alive for before killing it
const DEATH_AGE = 10000;
// How many gliders to randomly populate the map with
const INITIAL_GLIDER_COUNT = 50;

function wrapValue(value, max) {
  if (value < 0) {
    return max + value;
  }

  return value % max;
}

const lerp = (a, b, v) => a + (v * (b - a));

function lerpColors(a, b, v) {
  const aRed = a >> 16;
  const aGreen = (a >> 8) && 0xff;
  const aBlue = a & 0xff;
  const bRed = b >> 16;
  const bGreen = (b >> 8) && 0xff;
  const bBlue = b & 0xff;

  const mixRed = lerp(aRed, bRed, v);
  const mixGreen = lerp(aGreen, bGreen, v);
  const mixBlue = lerp(aBlue, bBlue, v);

  return (mixRed << 16) | (mixGreen << 8) | mixBlue
}


class GameOfLife {
  constructor() {
    this.bindMethods();

    this.reloadGraphics();

    window.addEventListener("resize", () => {
      this.reloadGraphics();
      this.start();
    })

    const client = new FootronMessaging.Messaging();
    client.mount();
    client.addMessageListener(this.messageHandler);
  }

  bindMethods() {
    this.loop = this.loop.bind(this);
    this.messageHandler = this.messageHandler.bind(this);
    this.reloadGraphics = this.reloadGraphics.bind(this);
  }

  reloadGraphics() {
    this.width = Math.ceil(window.innerWidth / CELL_SIZE);
    this.height = Math.ceil(window.innerHeight / CELL_SIZE);
    this.wrapWidth = (value) => wrapValue(value, this.width);
    this.wrapHeight = (value) => wrapValue(value, this.height);
    this.running = false;
    this.stepsPerFrame = 1;

    this.initializeGraphics();
    this.initializeGrid();
  }

  messageHandler(message) {
    // A nice exponential function that gives a nice feeling of control over speed
    this.stepsPerFrame = Math.min(((2.9833 * message) ** 2) + 0.1, 9) * 0.3;
  }

  initializeGraphics() {
    this.app = new PIXI.Application();
    this.app.renderer.view.style.position = "absolute";
    this.app.renderer.view.style.display = "block";
    this.app.renderer.autoResize = true;
    this.app.renderer.resize(window.innerWidth, window.innerHeight);

    document.body.appendChild(this.app.view);

    this.graphics = new PIXI.Graphics();

    this.container = new PIXI.Container();

    const bloomFilterFringe = new PIXI.filters.AdvancedBloomFilter({
      blur: 0.01,
    });
    const bloomFilterInner = new PIXI.filters.AdvancedBloomFilter({
      blur: 5,
      quality: 10,
    });
    const bloomFilterOuter = new PIXI.filters.AdvancedBloomFilter({
      blur: 20,
      quality: 50,
      threshold: 0.4,
    });
    const defocusFilter = new PIXI.filters.BlurFilter(0.3);

    this.graphics.filters = [
      bloomFilterFringe,
      bloomFilterInner,
      bloomFilterOuter,
      defocusFilter,
    ];

    this.container.addChild(this.graphics);
    this.app.stage.addChild(this.container);
  }

  spawnRandomGlider() {
    const x = Math.round(Math.random() * this.width);
    const y = Math.round(Math.random() * this.height);
    const pattern = PATTERNS[Math.floor(Math.random() * PATTERNS.length)];

    Array.from(pattern).forEach((str, v) =>
      Array.from(str).forEach(
        (c, h) =>
          (this.cells[
          this.wrapWidth(x + h) * this.width + this.wrapHeight(y + v)
            ].alive = c === "1")
      )
    );
  }

  initializeGrid() {
    this.cells = new Array(this.width + this.height);

    for (let i = 0; i < this.width; i++) {
      for (let j = 0; j < this.height; j++) {
        this.cells[i * this.width + j] = new Cell(false);
      }
    }

    for (let i = 0; i < this.width; i++) {
      for (let j = 0; j < this.height; j++) {
        this.cells[i * this.width + j].neighbors = this.getCellNeighbors(
          i,
          j,
          this.cells
        );
      }
    }

    for (let k = 0; k < INITIAL_GLIDER_COUNT; k++) {
      this.spawnRandomGlider();
    }
  }

  start() {
    if (this.running) {
      return;
    }

    this.lastFrameTime = -1;
    // Hack to make extremely slow rates work
    this.deltaSinceStep = 0;
    this.running = true;
    requestAnimationFrame(this.loop);
  }

  // noinspection JSUnusedGlobalSymbols
  stop() {
    if (!this.running) {
      return;
    }

    this.running = false;
  }

  getCellNeighbors(i, j, inCells) {
    const neighbors = [
      [-1, -1],
      [0, -1],
      [1, -1],
      [-1, 0],
      [1, 0],
      [-1, 1],
      [0, 1],
      [1, 1],
    ];
    return neighbors.map(
      ([a, b]) =>
        inCells[this.wrapWidth(i + a) * this.width + this.wrapHeight(j + b)]
    );
  }

  stepCells() {
    if (Math.random() < 0.01) {
      this.spawnRandomGlider();
    }
    this.cells.forEach((c) => c.prepareUpdate());
    this.cells.forEach((c) => c.update());
  }

  loop(time) {
    let delta = 0;

    if (this.lastFrameTime !== -1) {
      // Limit delta to half a frame of catch up
      delta = Math.floor(time - this.lastFrameTime, FRAME_DURATION * 1.5);
    }

    this.lastFrameTime = time;

    let steps = Math.min(
      Math.floor(((delta + this.deltaSinceStep) / FRAME_DURATION) * this.stepsPerFrame),
      MAX_STEPS_PER_FRAME
    );

    if (steps > 1 && this.deltaSinceStep === 0) {
      // @vinhowe: this forces steps to be odd so we can see even/odd oscillations at any speed
      // _assuming_ we're not making up lost time for a missed step
      steps += 1 - (steps % 2);
    }
    if (steps === 0) {
      this.deltaSinceStep += delta;
    }
    if (steps > 0) {
      this.deltaSinceStep = 0;
    }

    this.graphics.clear();
    this.graphics.beginFill(0x00112c);
    this.graphics.drawRect(0, 0, window.innerWidth, window.innerHeight);
    for (let i = 0; i < steps; i++) {
      this.stepCells();
    }
    for (let i = 0; i < this.width; i++) {
      for (let j = 0; j < this.height; j++) {
        const cell = this.cells[i * this.width + j]
        if (!cell.alive) {
          continue;
        }
        // TODO: Optimize this so we order cells by age and step colors to reduce beginFill calls
        this.graphics.beginFill(lerpColors(0xffffff, 0x000088, cell.age / DEATH_AGE));
        this.graphics.drawRect(
          i * CELL_SIZE,
          j * CELL_SIZE,
          CELL_SIZE,
          CELL_SIZE
        );
      }
    }

    if (this.running) {
      requestAnimationFrame(this.loop);
    }
  }
}

// This model is simplified from
// https://github.com/Tebs-Lab/conways-game-of-life/blob/82ffbd038c24b466b38d41b444890491307f39fe/scripts/conways-simulator.js#L390-L485
class Cell {
  constructor(alive) {
    this.alive = alive;
    this.neighbors = [];
    this.nextState = null;
    this.age = 0;
  }

  prepareUpdate() {
    const neighborsAlive = this.neighbors.filter((n) => n.alive);

    if (this.age >= DEATH_AGE) {
      this.nextState = false;
      // Kill immediate neighbors to get rid of floaters. This is probably fine for our very chaotic simulations now,
      // but it could probably mess up more complicated patterns.
      neighborsAlive.forEach((neighbor) => {
        neighbor.age = this.age;
      });
      return;
    }

    const neighborsAliveCount = neighborsAlive.length;

    if (this.alive && (neighborsAliveCount < 2 || neighborsAliveCount > 3)) {
      this.nextState = false;
      return;
    }

    if (!this.alive && neighborsAliveCount === 3) {
      this.nextState = true;
      return;
    }

    // Default, state doesn't change
    this.nextState = this.alive;
  }

  update() {
    this.alive = this.nextState;
    this.nextState = null;

    if (this.alive) {
      this.age++;
    } else {
      this.age = 0;
    }
  }
}

function start() {
  const life = new GameOfLife();
  life.start();
}

window.addEventListener("load", start);
