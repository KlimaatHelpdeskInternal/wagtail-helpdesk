import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
import Konva from "konva";
import { co2categories } from "./co2categories.js";

window.Stimulus = Application.start();
const context = require.context("./controllers", true, /\.js$/);
Stimulus.load(definitionsFromContext(context));

console.log("carboncalculator.ts toegevoegd");

let currentCategories = [];
currentCategories.push(co2categories.find((cat) => cat.name == "kg CO2"));
currentCategories.push(...co2categories.filter((cat) => cat.name !== "kg CO2"));

// Debounce function to limit how often window resize handler triggers
function debounce(func, wait) {
    let timeout;
    return function() {
        clearTimeout(timeout);
        timeout = setTimeout(func, wait);
    };
}

// Reload the page 500ms after the user stops resizing window
window.addEventListener('resize', debounce(() => {
    location.reload();
}, 500));

/*
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
*/

// Konva
// first we need to create a stage
const stage = new Konva.Stage({
  container: "cc__konva", // id of container <div>
});

stage.width(stage.container().offsetWidth);
stage.height(stage.container().offsetHeight * 0.95);

// then create layer
const layer = new Konva.Layer();
      
//functions
function redraw() {
  layer.destroyChildren();
  drawCategories(currentCategories);
}

function createCircle(x, y, radius, fill, stroke, strokeWidth) {
  let circle = new Konva.Circle({
    x: x,
    y: y,
    radius: radius,
    fill: fill,
    stroke: stroke,
    strokeWidth: strokeWidth,
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
    fontStyle: "500",
  });
}

function createImage(x, y, width, height, source) {
  const imgObj = new Image();
  imgObj.src = source;

  let img = new Konva.Image({
    x: x - width / 2,
    y: y - height / 2,
    image: imgObj,
    width: width,
    height: height,
  });

  return img;
}

function drawCategories(currentCategories) {
  let circleRadius = Math.min(stage.height() * 0.13, stage.width() * 0.13);
  let categoryZero;

  for (let i = 0; i < currentCategories.length; i++) {
    let posX;
    let posY;
    let isClicked = false;

    if (i == 0) {
      posX = stage.width() * 0.5;
      posY = stage.height() * 0.5;
    } else {
      let degrees = (360 * i) / (currentCategories.length - 1);
      let rad = (degrees / 360) * 2 * Math.PI;
      posX =
        Math.sin(rad) * (stage.width() * 0.5 - circleRadius - Math.max(0, 0.4 * (stage.width() - stage.height())) - 3) +
        stage.width() * 0.5;
      posY =
        Math.cos(rad) * (stage.height() * 0.5 - circleRadius - Math.max(0, 0.4 * (stage.height() - stage.width())) - 3) +
        stage.height() * 0.5;
    }

    const category = new Konva.Group({
      x: posX,
      y: posY,
      name: currentCategories[i].name
    });

    const circle = createCircle(
      0,
      0,
      circleRadius,
      "white",
      "black",
      2
    );
    
    const numText = createText(
      0,
      -circleRadius * 0.8,
      circleRadius * 0.8,
      Math.round(
        (currentCategories[0].conversion_to_kg_CO2 /
          currentCategories[i].conversion_to_kg_CO2) *
          1000
      ) / 1000,
      14,
      "Geomanist Webfont",
      "red"
    );

    const img = createImage(
      0,
      0,
      circleRadius * 0.9,
      circleRadius * 0.9,
      currentCategories[i].image_url
    );

    const swapIcon = createImage(
      0,
      circleRadius * 0.7,
      circleRadius * 0.35,
      circleRadius * 0.35,
      "https://cdn-icons-png.flaticon.com/128/7133/7133490.png"
    )

    category.add(circle);
    category.add(numText);
    category.add(img);
    
    category.on('mousedown touchend', () => {
      if (document.getElementById("cc__categorytitle") != null) {
        document.getElementById("cc__categorytitle").innerHTML = "Aantal " + currentCategories[i].name;
      }
      if (document.getElementById("cc__categoryexplanation") != null) {
        document.getElementById("cc__categoryexplanation").innerHTML = currentCategories[i].description;
      }
    });

    if (category.x() === stage.width() / 2 && category.y() === stage.height() / 2) {
      categoryZero = category;
    }
    else {
      category.add(swapIcon);
      swapIcon.on('mousedown touchend', () => {
        if (isClicked == false) {
          isClicked = true;
      
          const index = currentCategories.map(cat => cat.name).indexOf(category.name());
          const cat = currentCategories[index];

          const speedAdjustForScreenSize = Math.pow(stage.width() / 1000, 2);
          const xSpeed = (stage.width() / 2 - category.x()) / stage.height() * 0.2;
          const ySpeed = (stage.height() / 2 - category.y()) / stage.height() * 0.2;
          
          const anim = new Konva.Animation(function(frame) {
            category.zIndex(2);
            categoryZero.zIndex(1);

            categoryZero.x(
              categoryZero.x() + -xSpeed * frame.time
            );
            categoryZero.y(
              categoryZero.y() + -ySpeed * frame.time
            );

            category.x(
              category.x() + xSpeed * frame.time
            );
            category.y(
              category.y() + ySpeed * frame.time
            );

            if (stage.width() / 2 * 0.9 <= category.x() && category.x() <= stage.width() / 2 * 1.1 &&
          stage.height() / 2 * 0.9 <= category.y() && category.y() <= stage.height() / 2 * 1.1) {
              anim.stop();

              currentCategories[index] = currentCategories[0];
              currentCategories[0] = cat;  

              redraw();

              isClicked = false;
            }

          }, layer);

          anim.start();
        }
      });
    }

    layer.add(category);
  }
}

// create our shapes and add the shapes to the layer
drawCategories(currentCategories);

// add the layer to the stage
stage.add(layer);
