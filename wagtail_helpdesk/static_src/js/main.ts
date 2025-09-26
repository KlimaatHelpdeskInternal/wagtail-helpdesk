import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
import Konva from "konva";

console.log("test");

window.Stimulus = Application.start();
const context = require.context("./controllers", true, /\.js$/);
Stimulus.load(definitionsFromContext(context));

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const img = new Image();
img.src =
  "https://www.gardengourmet.nl/sites/default/files/styles/768_width/public/2024-08/vegan-burger.png?itok=pXKWu9wB";

canvas.width = 800;
canvas.height = 600;

let canvasCirclePositions = [
  [0.5, 0.5],
  [0.5, 0.2],
  [0.71, 0.29],
  [0.8, 0.5],
  [0.71, 0.71],
  [0.5, 0.8],
  [0.29, 0.71],
  [0.2, 0.5],
  [0.29, 0.29],
];

let circleRadius = 0.1 * canvas.height;

let amounts = [1, 2, 3, 4, 5, 6, 7, 8, 9];

ctx.font = "20px Arial";
ctx.fillText("Carbon Calculator", canvas.width / 20, canvas.height / 20);

ctx.beginPath();
for (let [i, position] of canvasCirclePositions.entries()) {
  ctx.moveTo(
    position[0] * canvas.width + circleRadius,
    position[1] * canvas.height
  );
  ctx.arc(
    position[0] * canvas.width,
    position[1] * canvas.height,
    circleRadius,
    0,
    2 * Math.PI
  );

  for (let j = 0; j < amounts[i]; j++)
    img.addEventListener("load", () => {
      ctx.drawImage(
        img,
        position[0] * canvas.width -
          0.5 * circleRadius +
          j * (circleRadius / amounts[i]),
        position[1] * canvas.height - (0.5 * circleRadius) / amounts[i],
        circleRadius / amounts[i],
        circleRadius / amounts[i]
      );
    });
}
ctx.stroke();

// first we need to create a stage
const stage = new Konva.Stage({
  container: "konva", // id of container <div>
  width: 800,
  height: 600,
});

// then create layer
const layer = new Konva.Layer();

// create our shapes
let circlePositions = [
  [0.5, 0.5],
  [0.5, 0.2],
  [0.71, 0.29],
  [0.8, 0.5],
  [0.71, 0.71],
  [0.5, 0.8],
  [0.29, 0.71],
  [0.2, 0.5],
  [0.29, 0.29],
];

function createCircle(x, y, radius) {
  return new Konva.Circle({
    x: x,
    y: y,
    radius: radius,
    fill: "white",
    stroke: "black",
  });
}

function createImage(x, y, width, height, source) {
  const imgObj = new Image();
  imgObj.src = source;

  return new Konva.Image({
    x: x,
    y: y,
    image: imgObj,
    width: width,
    height: height,
  });
}

for (let [i, position] of circlePositions.entries()) {
  // add the shapes to the layer
  layer.add(
    createCircle(
      stage.width() * position[0],
      stage.height() * position[1],
      stage.width() * 0.08
    )
  );

  for (let j = 0; j < amounts[i]; j++) {
    layer.add(
      createImage(
        position[0] * stage.width() -
          0.5 * circleRadius +
          j * (circleRadius / amounts[i]),
        position[1] * stage.height() - (0.5 * circleRadius) / amounts[i],
        circleRadius / amounts[i],
        circleRadius / amounts[i],
        "https://www.gardengourmet.nl/sites/default/files/styles/768_width/public/2024-08/vegan-burger.png?itok=pXKWu9wB"
      )
    );
  }
}

// add the layer to the stage
stage.add(layer);
