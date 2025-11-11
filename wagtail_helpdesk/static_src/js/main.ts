import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
import Konva from "konva";
import { co2categories } from "./co2categories.js";

window.Stimulus = Application.start();
const context = require.context("./controllers", true, /\.js$/);
Stimulus.load(definitionsFromContext(context));

let currentCategories = [];
currentCategories.push(co2categories.find((cat) => cat.name == "kg CO2"));
currentCategories.push(...co2categories.filter((cat) => cat.name !== "kg CO2"));

const select = document.getElementById("co2categories");
const button = document.getElementById("co2button");

for (const category of co2categories) {
  select.options[select.options.length] = new Option(
    category.name,
    category.name
  );
}

button.addEventListener("click", (value) => {
  if (
    currentCategories.length < 9 &&
    currentCategories.some(cat => cat.name === select.value) === false
  ) {
    for (const category of co2categories) {
      if (category.name == select.value) {
        currentCategories.push(category);

        redraw();
      }
    }
  }
});

// Konva
// first we need to create a stage
const stage = new Konva.Stage({
  container: "konva", // id of container <div>
  width: 800,
  height: 600,
});

// then create layer
const layer = new Konva.Layer();

//functions
function redraw() {
  stage.removeChildren();
  layer.destroyChildren();
  drawCategories(currentCategories);
  stage.add(layer);
}

function createCircle(x, y, radius, fill, stroke, name) {
  let circle = new Konva.Circle({
    x: x,
    y: y,
    radius: radius,
    fill: fill,
    stroke: stroke,
  });

  circle.on("mousedown", () => {
    currentCategories = currentCategories.filter((cat) => cat.name !== name);
    redraw();
  });

  return circle;
}

function createText(x, y, width, text, fontSize, fontFamily, fill) {
  return new Konva.Text({
    x: x - width / 2,
    y: y,
    text: text,
    fontSize: fontSize,
    fontFamily: fontFamily,
    fill: fill,
    width: width,
    align: "center",
    listening: false,
  });
}

function createImage(x, y, width, height, source, name) {
  const imgObj = new Image();
  imgObj.src = source;

  let img = new Konva.Image({
    x: x - width / 2,
    y: y - height / 2,
    image: imgObj,
    width: width,
    height: height,
    listening: false,
  });

  img.on("mousedown", () => {
    currentCategories = currentCategories.filter((cat) => cat.name !== name);
    redraw();
  });

  return img;
}

function drawCategories(currentCategories) {
  layer.add(
  createText(
    stage.width() / 2,
    0,
    stage.width(),
    "1 " + currentCategories[0].name + " geeft evenveel CO2-uitstoot als:",
    30,
    "Arial",
    "black"
    )
  );

  let circleRadius = stage.width() * 0.09;

  for (let i = 0; i < currentCategories.length; i++) {
    let posX;
    let posY;

    if (i == 0) {
      posX = stage.width() * 0.5;
      posY = stage.height() * 0.5;
    } else {
      let degrees = (360 * i) / (currentCategories.length - 1);
      let rad = (degrees / 360) * 2 * Math.PI;
      posX =
        Math.sin(rad) * 0.5 * (stage.width() * 0.5 + circleRadius) +
        stage.width() * 0.5;
      posY =
        Math.cos(rad) * (stage.height() * 0.9 * 0.5 - circleRadius) +
        stage.height() * 0.5;
    }

    layer.add(
      createCircle(
        posX,
        posY,
        circleRadius,
        "white",
        "black",
        currentCategories[i].name
      )
    );

    layer.add(
      createText(
        posX,
        posY - stage.height() / 9,
        circleRadius * 1.4,
        Math.round(
          (currentCategories[0].conversion_to_kg_CO2 /
            currentCategories[i].conversion_to_kg_CO2) *
            1000
        ) / 1000,
        14,
        "Calibri",
        "red"
      )
    );

    layer.add(
      createText(
        posX,
        posY - stage.height() / 11,
        circleRadius * 1.4,
        currentCategories[i].name,
        14,
        "Calibri",
        "black"
      )
    );

    layer.add(
      createImage(
        posX,
        posY + 0.04 * stage.height(),
        circleRadius,
        circleRadius,
        currentCategories[i].image_url,
        currentCategories[i].name
      )
    );
  }
}

// create our shapes and add the shapes to the layer

drawCategories(currentCategories);

// add the layer to the stage
stage.add(layer);
