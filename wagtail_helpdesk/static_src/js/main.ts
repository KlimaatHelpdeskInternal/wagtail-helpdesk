import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
import Konva from "konva";

window.Stimulus = Application.start();
const context = require.context("./controllers", true, /\.js$/);
Stimulus.load(definitionsFromContext(context));

let circleCount = 9;
const categories = [
  {
    name: "kg CO2",
    value: 1,
    icon: "https://cdn-icons-png.flaticon.com/512/3492/3492640.png",
  },
  {
    name: "cheeseburgers",
    value: 3,
    icon: "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
  },
  {
    name: "vegaburgers",
    value: 0.4,
    icon: "https://cdn-icons-png.flaticon.com/512/1687/1687009.png",
  },
  {
    name: "uur autorijden",
    value: 7,
    icon: "https://cdn-icons-png.flaticon.com/512/8308/8308414.png",
  },
  {
    name: "uur vliegen",
    value: 400,
    icon: "https://cdn-icons-png.flaticon.com/512/7893/7893979.png",
  },
  {
    name: "keer 10 min. douchen",
    value: 0.6,
    icon: "https://cdn-icons-png.flaticon.com/512/760/760637.png",
  },
  {
    name: "dagen computer gebruiken",
    value: 0.48,
    icon: "https://img.freepik.com/premium-vector/desktop-computer-icon-vector-design-template-simple-clean_1309366-1987.jpg",
  },
  {
    name: "dagen huis verwarmen (gas)",
    value: 5.22,
    icon: "https://cdn-icons-png.flaticon.com/512/9879/9879880.png",
  },
  {
    name: "dagen huis verwarmen (warmtepomp)",
    value: 3.13,
    icon: "https://us.123rf.com/450wm/vectorwin/vectorwin2401/vectorwin240100503/221481784-heat-recovery-system-geothermal-color-icon-vector-illustration.jpg?ver=6",
  },
];
let currentCategories = categories.slice();

const select = document.getElementById("co2categories");
const button = document.getElementById("co2button");

for (const category of categories) {
  select.options[select.options.length] = new Option(category.name, category.name);
}

button.addEventListener("click", (value => {
  if (currentCategories.length < 9 && currentCategories.includes(select.value) === false) {
    console.log(select.value);
    for (const category of categories) {
      if (category.name == select.value) {
        currentCategories.push(category);
        
        redraw()
      }
    }
  }
}));

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
  drawCircles(currentCategories);
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
    currentCategories = currentCategories.filter(cat => cat.name !== name);
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
    listening: false
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
    listening: false,
  });
}

function drawCircles(currentCategories) {
  let circleRadius = stage.width() * 0.09;
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

  for (let i = 0; i < currentCategories.length; i++) {
      layer.add(
      createCircle(
        stage.width() * circlePositions[i][0],
        stage.height() * circlePositions[i][1],
        circleRadius,
        "white",
        "black",
        currentCategories[i].name
      )
    );

    layer.add(
      createText(
        stage.width() * circlePositions[i][0],
        stage.height() * circlePositions[i][1] - stage.height() / 9,
        circleRadius * 1.5,
        Math.round((currentCategories[0].value / currentCategories[i].value) * 1000) / 1000,
        14,
        "Calibri",
        "green"
      )
    );

    layer.add(
      createText(
        stage.width() * circlePositions[i][0],
        stage.height() * circlePositions[i][1] - stage.height() / 11,
        circleRadius * 1.5,
        currentCategories[i].name,
        14,
        "Calibri",
        "green"
      )
    );

    let amountCeil = Math.ceil(
      currentCategories[0].value / currentCategories[i].value
    );
    let lastAmount = (currentCategories[0].value / currentCategories[i].value) % 1;
    if (lastAmount == 0) {
      lastAmount = 1;
    }

    for (let j = 0; j < amountCeil; j++) {
      if (j == amountCeil - 1) {
        const imageObj = new Image();
        imageObj.src = currentCategories[i].icon;
        imageObj.onload = () => {
          const halfWidth = imageObj.width * lastAmount;

          const konvaImage = new Konva.Image({
            x:
              circlePositions[i][0] * stage.width() -
              0.5 * circleRadius +
              j * (circleRadius / amountCeil),
            y:
              circlePositions[i][1] * stage.height() -
              (0.5 * circleRadius) / amountCeil +
              0.035 * stage.height(),
            image: imageObj,
            // crop defines what part of the image is visible
            crop: {
              x: 0,
              y: 0,
              width: halfWidth,
              height: imageObj.height,
            },
            width: (circleRadius / amountCeil) * lastAmount,
            height: circleRadius / amountCeil,
          });

          layer.add(konvaImage);
        };
      } else {
        layer.add(
          createImage(
            circlePositions[i][0] * stage.width() -
              0.5 * circleRadius +
              j * (circleRadius / amountCeil),
            circlePositions[i][1] * stage.height() -
              (0.5 * circleRadius) / amountCeil +
              0.035 * stage.height(),
            circleRadius / amountCeil,
            circleRadius / amountCeil,
            currentCategories[i].icon
          )
        );
      }
    }
  }
}

// create our shapes and add the shapes to the layer
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

drawCircles(currentCategories);

// add the layer to the stage
stage.add(layer);
