import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
import Konva from "konva";

window.Stimulus = Application.start();
const context = require.context("./controllers", true, /\.js$/);
Stimulus.load(definitionsFromContext(context));

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
  [0.69, 0.28],
  [0.8, 0.5],
  [0.69, 0.72],
  [0.5, 0.8],
  [0.31, 0.72],
  [0.2, 0.5],
  [0.31, 0.28],
];
let circleRadius = stage.width() * 0.09;
let amounts = [1, 2, 3, 4, 5, 6, 7, 8, 9];
const co2values = [
  ["cheeseburger", 3],
  ["broodje kroket", 1.34],
  ["broodje gezond", 1.29],
  ["boterham kaas", 0.57],
  ["vegaburger", 0.4],
  ["test1", 20],
  ["test2", 10],
  ["test3", 1.6],
  ["test4", 0.1]
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

function createText(x, y, text, fontSize, fontFamily, fill) {
  return new Konva.Text({
    x: x - stage.width() / 2,
    y: y,
    text: text,
    fontSize: fontSize,
    fontFamily: fontFamily,
    fill: fill,
    width: stage.width(),
    align: "center"
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

layer.add(
  createText(
    stage.width() / 2,
    0,
    "1 Cheeseburger geeft evenveel CO2-uitstoot als:",
    30,
    "Arial",
    "black"
  )
);

for (let [i, position] of circlePositions.entries()) {
  // add the shapes to the layer
  layer.add(
    createCircle(
      stage.width() * position[0],
      stage.height() * position[1],
      circleRadius
    )
  );

  layer.add(
    createText(
      stage.width() * position[0],
      stage.height() * position[1] - stage.height() / 12,
      co2values[i][0],
      16,
      "Calibri",
      "green"
    )
  );

  layer.add(
    createText(
      stage.width() * position[0],
      stage.height() * position[1] + stage.height() / 14,
      Math.round((co2values[0][1]  / co2values[i][1]) * 100) / 100,
      14,
      "Calibri",
      "black"
    )
  );

  let amountCeil = Math.ceil(co2values[0][1] / co2values[i][1]);
  let lastAmount = ( co2values[0][1] / co2values[i][1]) % 1;
  if (lastAmount == 0) {
    lastAmount = 1
  } 

  console.log(lastAmount);

  for (let j = 0; j < amountCeil; j++) {
    if(j == amountCeil - 1) {
      const imageObj = new Image();
      imageObj.src = "https://www.gardengourmet.nl/sites/default/files/styles/768_width/public/2024-08/vegan-burger.png?itok=pXKWu9wB";
      imageObj.onload = () => {
        const halfWidth = imageObj.width * lastAmount;

        const konvaImage = new Konva.Image({
          x: position[0] * stage.width() -
            0.5 * circleRadius +
            j * (circleRadius / amountCeil),
          y: position[1] * stage.height() - (0.5 * circleRadius) / amountCeil,
          image: imageObj,
          // crop defines what part of the image is visible
          crop: {
            x: 0,
            y: 0,
            width: halfWidth,
            height: imageObj.height,
          },
          width: (circleRadius / amountCeil) * lastAmount,
          height: circleRadius / amountCeil
        });

        layer.add(konvaImage);
      };
    }

    else {
      layer.add(
        createImage(
          position[0] * stage.width() -
            0.5 * circleRadius +
            j * (circleRadius / amountCeil),
          position[1] * stage.height() - (0.5 * circleRadius) / amountCeil,
          circleRadius / amountCeil,
          circleRadius / amountCeil,
          "https://www.gardengourmet.nl/sites/default/files/styles/768_width/public/2024-08/vegan-burger.png?itok=pXKWu9wB"
        )
      );
    }
  }
} 

// add the layer to the stage
stage.add(layer);
