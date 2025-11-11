export const co2categories=null;
function LoadCarbonCategories()
{
  alert('In loadCarboncategories');
  const rawtext = carbonemissioncategoriesvar;
  co2categories = ReadCO2CategoriesFromJSONFormat(rawtext);
}
function ReadCategoryNamesFromConfig(co2categories) {
  var categorynames = [];

  for (var i = 0; i < co2categories.length; i++) {
      categorynames.push(co2categories[i].fields["name"]);
  }
  return categorynames;
}
function ReadCO2CategoriesFromJSONFormat( rawdata) {
  var co2categories = [];
  var parseddata = "";
  try {
    var parseddata = JSON.parse(rawdata);
  } 
  catch (error) {
    console.error("JSON parse error:", error);
  
  }
  //console.log("retrieved parseddata json data size" + Object.keys(parseddata).length);
  for (var i = 0; i < Object.keys(parseddata).length; i++) {
      console.log("json data i: " + JSON.stringify(parseddata[i].fields));
      co2categories.push(parseddata[i].fields);
  }
  return co2categories;
}
function ReadCarbonCalculatorConfig(json_data) {

  console.log("read data: " + json_data);
  co2categories = json_data;
  return co2categories;

}
