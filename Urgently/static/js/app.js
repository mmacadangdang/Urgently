function calculateUrgency(input) {
  // Result div
  var result = d3.select("#result");
  // Result image
  var resultImage = d3.select("#resultImage");
  // Loading image
  var loadingImage = d3.select("#loadingImage");
  loadingImageSource = 'static/img/loading.gif'
    // Show loading icon
    loadingImage.attr("src", loadingImageSource);
  // Input text
  var input = d3.select("#input").property("value");

  // defaults
  var urgencyValue = 'urgent';
  var urgencyImage = '../images/error.png';

  // URL endpoint
  var url = `/calculator/${input}`;

  console.log(`Result variable: ${result}`);
  console.log(`Input text: ${input}`);
  console.log(`Requesting URL: ${url}`);
  var response = d3.json(url, function(response) {
    console.log("Processing the prediction response");
    // Use d3 to clear any existing images from the result div
    console.log(`Response: ${response.URL}`);
    var image = response.URL;
    console.log(`Image: ${image}`);

    // Use d3 to insert the image result into the result div
    loadingImage.attr("src", image);
    //result.html(`<img src="${image}"`);

  });
};
