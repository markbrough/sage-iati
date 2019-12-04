$(document).on("click", ".publish-btn", function(e) {
  e.preventDefault();
  var el = $(this);
  var file_id = el.attr("data-file-id");
  var file_type = el.attr("data-file-type");
  data = {
    'file_id': file_id
  }
  $.post("publish_file/", data, function(resultdata) {
    var data = $.parseJSON(resultdata);
    function unpublish(file_type_code) {
      published = $(".ft"+file_type).removeClass("btn-success").addClass("btn-primary").addClass("publish-btn").text("Publish");
    }
    function publish(element) {
      element.removeClass("btn-primary").addClass("btn-success").removeClass("publish-btn").text("Published");
    }
    unpublish(file_type);
    publish(el);
  }).fail(function(){
    alert("Couldn't update the published file!");
  });
});
$("#confirm-delete").on('show.bs.modal', function(e) {
    var target_href = $(e.relatedTarget).data("href");
    console.log(target_href)
    $('#confirm-delete-button').attr("href", target_href);
});