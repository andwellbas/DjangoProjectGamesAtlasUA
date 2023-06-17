$(document).ready(function() {
  // get all stars elements
  var stars = $(".rating-star");

  // add an event handler for each star
  stars.on("click", function() {
    var rating = $(this).data("rating");

    // fill all the stars up to and including the compressed star
    stars.removeClass("filled");
    $(this).addClass("filled");

    // update the value of the evaluation field
    $("#id_rating").val(rating);

    // send the form automatically
    $(".user-rating-form").submit();
  });

  // highlight the stars to the current value of the assessment
  var currentRating = parseInt('{{ game.average_rating|default_if_none:"0" }}');
  for (var i = 1; i <= currentRating; i++) {
    stars.eq(i - 1).addClass("filled");
  }
});
