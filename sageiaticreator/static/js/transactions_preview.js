$("#btn-reveal-aggregated-details").click(function(e){
  e.preventDefault();
  if ($(this).attr("data-toggle") == "show") {
    $(this).attr("data-toggle", "hide");
    $(this).html('<span class="glyphicon glyphicon-eye-close"></span> Hide details of aggregated transactions');
    $(".aggregated-details").show();
  } else {
    $(this).attr("data-toggle", "show");
    $(this).html('<span class="glyphicon glyphicon-eye-open"></span> Show details of aggregated transactions');
    $(".aggregated-details").hide();
  }
});