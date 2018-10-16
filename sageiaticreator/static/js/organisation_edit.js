function resetFormGroup(input) {
  $(input).parent().removeClass("has-success has-error has-feedback");
  $(input).parent().find(".form-control-feedback").remove();
  $(input).parent().find(".form-control-status").remove();
}
function successFormGroup(input) {
  $(input).parent().addClass("has-success has-feedback");
  $(input).after('<span class="glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span> \
  <span class="sr-only form-control-status">(success)</span>');
}
function errorFormGroup(input) {
  $(input).parent().addClass("has-error has-feedback");
  $(input).after('<span class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span> \
  <span class="sr-only form-control-status">(error)</span>');
}
$("#addAggregateAccountBtn").click(function(e) {
  e.preventDefault();
  var account_number = $("#addAggregateAccountForm #account_number").val();
  var account_description = $("#addAggregateAccountForm #account_description").val();
  data = {
    'account_number': account_number,
    'account_description': account_description
  }
  $.post("add_aggregate_account/", data, function(resultdata) {
    var data = $.parseJSON(resultdata);
    $("#aggregated-accounts-table tbody").append(' \
      <tr data-aggregated-account-id="' + data['id'] + '"> \
        <td>' + data['account_number'] + '</td> \
        <td>' + data['account_description'] + '</td> \
        <td> \
          <a href="" class="deleteAggregatedAccountBtn"> \
            <span class="glyphicon glyphicon-trash"></span> \
          </a> \
        </td> \
      </tr> \
    ');
    $('#aggregateAccountModal').modal('hide');
  }).fail(function(){
    alert("Couldn't add aggregate account!");
  });
});
$("#addExcludedStringBtn").click(function(e){
  e.preventDefault();
  var excluded_string = $("#addExcludedStringForm #excluded_string").val();
  data = {
    'excluded_string': excluded_string
  }
  $.post("add_excluded_string/", data, function(resultdata) {
    var data = $.parseJSON(resultdata);
    $("#excluded-strings-table tbody").append(' \
      <tr data-excluded-string-id="' + data['id'] + '"> \
        <td>' + data['excluded_string'] + '</td> \
        <td> \
          <a href="" class="deleteExcludedStringBtn"> \
            <span class="glyphicon glyphicon-trash"></span> \
          </a> \
        </td> \
      </tr> \
    ');
    $('#excludedStringModal').modal('hide');
  }).fail(function(){
    alert("Couldn't add string!");
  });
});

$("#addFunderBtn").click(function(e){
  e.preventDefault();
  var funding_org_name = $("#addFunderForm #funding_org_name").val();
  var funding_org_ref = $("#addFunderForm #funding_org_ref").val();
  var funding_org_type = $("#addFunderForm #funding_org_type").val();
  data = {
    'funding_org_name': funding_org_name,
    'funding_org_ref': funding_org_ref,
    'funding_org_type': funding_org_type
  }
  $.post("add_funding_org/", data, function(resultdata) {
    var data = $.parseJSON(resultdata);
    $("#funding-orgs-table tbody").append(' \
      <tr data-funder-id="' + data['id'] + '"> \
        <td>' + data['funding_org_name'] + '</td> \
        <td>' + data['funding_org_ref'] + '</td> \
        <td>' + data['funding_org_type'] + '</td> \
        <td> \
          <a href="" class="deleteFunderBtn"> \
            <span class="glyphicon glyphicon-trash"></span> \
          </a> \
        </td> \
      </tr> \
    ');
    $('#addFunderModal').modal('hide');
  }).fail(function(){
    alert("Couldn't add funder!");
  });
});

$(".addOrgBudgetBtn").click(function(e) {
  e.preventDefault;
  var data = {'data': 'data'};
  $.post("new_org_budget/", data, function(resultdata) {
    data = $.parseJSON(resultdata);
    $("#org-budget-form tbody").append(' \
    <tr data-budget-id="' + data['id'] + '"> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="start_date" \
          value="' + data['start_date'] + '"> \
        </div> \
      </td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="end_date" \
          value="' + data['end_date'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="value" \
          value="' + data['value'] + '"> \
        </div></td> \
      <td> \
          <a href="" class="deleteOrgBudgetBtn"> \
            <span class="glyphicon glyphicon-trash"></span> \
          </a> \
        </td> \
    </tr>')
  }).fail(function() {
    alert("Unable to add a new budget!");
  });
});

$(".addOrgExpenditureBtn").click(function(e) {
  e.preventDefault;
  var data = {'data': 'data'};
  $.post("new_org_expenditure/", data, function(resultdata) {
    data = $.parseJSON(resultdata);
    $("#org-expenditure-form tbody").append(' \
    <tr data-expenditure-id="' + data['id'] + '"> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="start_date" \
          value="' + data['start_date'] + '"> \
        </div> \
      </td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="end_date" \
          value="' + data['end_date'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="value" \
          value="' + data['value'] + '"> \
        </div></td> \
      <td> \
          <a href="" class="deleteOrgExpenditureBtn"> \
            <span class="glyphicon glyphicon-trash"></span> \
          </a> \
        </td> \
    </tr>')
  }).fail(function() {
    alert("Unable to add a new expenditure!");
  });
});

$(".addOrgDocBtn").click(function(e) {
  e.preventDefault;
  var data = {'data': 'data'};
  $.post("new_org_doc/", data, function(resultdata) {
    data = $.parseJSON(resultdata);
    $("#org-doc-form tbody").append(' \
    <tr data-doc-id="' + data['id'] + '"> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="title" \
          value="' + data['title'] + '"> \
        </div> \
      </td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="url" \
          value="' + data['url'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="format" \
          value="' + data['format'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="date" \
          value=""> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="category" \
          value="' + data['category'] + '"> \
        </div></td> \
      <td> \
          <a href="" class="deleteOrgDocBtn"> \
            <span class="glyphicon glyphicon-trash"></span> \
          </a> \
        </td> \
    </tr>')
  }).fail(function() {
    alert("Unable to add a new budget!");
  }); 
});

$(document).on("click", ".deleteFunderBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var funder_id = $(tr).attr("data-funder-id");
  var data = {'funder_id': funder_id};
  $.post("delete_funder/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that funder!");
  });
});
$(document).on("focus", "#org-data-form input", function(e) {
  resetFormGroup(this);
});
$(document).on("change", "#org-data-form input", function(e) {
  var data = {
    'attr': this.name,
    'value': this.value,
  }
  var input = this;
  resetFormGroup(input);
  $.post("update_org_attr/", data, function(resultdata) {
    successFormGroup(input);
  }).fail(function(){
    errorFormGroup(input);
  });  
});
$(document).on("focus", "#org-budget-form input, #org-doc.form input, #org-expenditure-form input", function(e) {
  resetFormGroup(this);
});
$(document).on("change", "#org-budget-form input", function(e) {
  var data = {
    'attr': this.name,
    'value': this.value,
    'id': $(this).closest("tr").attr("data-budget-id"),
  }
  var input = this;
  resetFormGroup(input);
  $.post("update_org_budget/", data, function(resultdata) {
    successFormGroup(input);
  }).fail(function(){
    errorFormGroup(input);
  });
});
$(document).on("change", "#org-expenditure-form input", function(e) {
  var data = {
    'attr': this.name,
    'value': this.value,
    'id': $(this).closest("tr").attr("data-expenditure-id"),
  }
  var input = this;
  resetFormGroup(input);
  $.post("update_org_expenditure/", data, function(resultdata) {
    successFormGroup(input);
  }).fail(function(){
    errorFormGroup(input);
  });
});
$(document).on("click", ".deleteOrgBudgetBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var budget_id = $(tr).attr("data-budget-id");
  var data = {'budget_id': budget_id};
  $.post("delete_org_budget/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that budget!");
  });
});
$(document).on("click", ".deleteOrgExpenditureBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var expenditure_id = $(tr).attr("data-expenditure-id");
  var data = {'expenditure_id': expenditure_id};
  $.post("delete_org_expenditure/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that expenditure!");
  });
});
$(document).on("change", "#org-doc-form input", function(e) {
  var data = {
    'attr': this.name,
    'value': this.value,
    'id': $(this).closest("tr").attr("data-doc-id"),
  }
  var input = this;
  resetFormGroup(input);
  $.post("update_org_doc/", data, function(resultdata) {
    successFormGroup(input);
  }).fail(function(){
    errorFormGroup(input);
  }); 
});
$(document).on("click", ".deleteOrgDocBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var doc_id = $(tr).attr("data-doc-id");
  var data = {'doc_id': doc_id};
  $.post("delete_org_doc/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that document!");
  });
});
$(document).on("click", ".deleteExcludedStringBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var excluded_string_id = $(tr).attr("data-excluded-string-id");
  var data = {'excluded_string_id': excluded_string_id};
  $.post("delete_excluded_string/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that string!");
  });
});
$(document).on("click", ".deleteAggregatedAccountBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var aggregated_account_id = $(tr).attr("data-aggregated-account-id");
  var data = {'aggregated_account_id': aggregated_account_id};
  $.post("delete_aggregated_account/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that aggregated account!");
  });
});