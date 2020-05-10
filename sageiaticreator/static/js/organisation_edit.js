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
$(document).on("input", "#funding_org_activity_id", function(e) {
  $("#funding_org_activity_id_search").attr('href', `https://d-portal.org/q.html?aid=${e.target.value}`)
})
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
    $("#addIncomingFundsForm #organisationfunder_id").append(' \
      <option value="' + data['id'] + '">' + data['funding_org_name'] + '</option>\
      ')
    $('#addFunderModal').modal('hide');
  }).fail(function(){
    alert("Couldn't add funder!");
  });
});

$("#addIncomingFundsBtn").click(function(e){
  e.preventDefault();
  var organisationfunder_id = $("#addIncomingFundsForm #organisationfunder_id").val();
  var account_number = $("#addIncomingFundsForm #account_number").val();
  var funding_org_activity_id = $("#addIncomingFundsForm #funding_org_activity_id").val();
  data = {
    'organisationfunder_id': organisationfunder_id,
    'account_number': account_number,
    'funding_org_activity_id': funding_org_activity_id
  }
  $.post("add_incoming_funds/", data, function(resultdata) {
    var data = $.parseJSON(resultdata);
    $("#incoming-funds-table tbody").append(' \
      <tr data-incoming-funds-id="' + data['id'] + '"> \
        <td>' + data['organisationfunder_name'] + '</td> \
        <td>' + data['account_number'] + '</td> \
        <td>' + data['funding_org_activity_id'] + '</td> \
        <td> \
          <a href="" class="deleteIncomingFundsBtn"> \
            <span class="glyphicon glyphicon-trash"></span> \
          </a> \
        </td> \
      </tr> \
    ');
    $('#addIncomingFundsModal').modal('hide');
  }).fail(function(){
    alert("Couldn't add incoming funds!");
  });
});

$(document).on("click", ".deleteIncomingFundsBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var incoming_funds_id = $(tr).attr("data-incoming-funds-id");
  var data = {'incoming_funds_id': incoming_funds_id};
  $.post("delete_incoming_funds/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that incoming funds entry!");
  });
});

$(".addOrgBudgetBtn").click(function(e) {
  e.preventDefault;
  $.post("new_org_budget/", function(resultdata) {
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
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="status" \
          value="' + data['status'] + '"> \
        </div></td> \
      <td> \
          <a href="#" title="Delete budget" class="deleteOrgBudgetBtn"><span class="glyphicon glyphicon-trash"></span></a> \
          &nbsp; \
          <a href="#" title="Add budget line" class="addOrgBudgetLineBtn"><span class="glyphicon glyphicon-plus"></span></a> \
        </td> \
    </tr>')
  }).fail(function() {
    alert("Unable to add a new budget!");
  });
});

$(document).on("click", ".addOrgBudgetLineBtn", function(e) {
  e.preventDefault;
  var btn = this;
  var tr = $(btn).closest("tr");
  var budgetId = $(tr).attr("data-budget-id");
  var data = {'budget_id': budgetId};
  $.post("new_org_budgetline/", data, function(resultdata) {
    data = $.parseJSON(resultdata);
    $(tr).after(' \
    <tr data-budgetline-id="' + data['id'] + '"> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="ref" \
          value="' + data['ref'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="description" \
          value="' + data['description'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="value" \
          value="' + data['value'] + '"> \
        </div></td> \
      <td></td> \
      <td> \
          <a href="#" title="Delete budget line" class="deleteOrgBudgetLineBtn"><span class="glyphicon glyphicon-trash"></span></a> \
        </td> \
    </tr>')
  }).fail(function() {
    alert("Unable to add a new budget line!");
  });
  return false;
});

$(document).on("click", ".addOrgExpenditureBtn", function(e) {
  e.preventDefault;
  $.post("new_org_expenditure/", function(resultdata) {
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
          <a href="#" title="Delete expenditure" class="deleteOrgExpenditureBtn"><span class="glyphicon glyphicon-trash"></span></a> \
          &nbsp; \
          <a href="#" title="Add expenditure line" class="addOrgExpenditureLineBtn"><span class="glyphicon glyphicon-plus"></span></a> \
        </td> \
    </tr>')
  }).fail(function() {
    alert("Unable to add a new expenditure!");
  });
  return false;
});

$(".addOrgExpenditureLineBtn").click(function(e) {
  e.preventDefault;
  var btn = this;
  var tr = $(btn).closest("tr");
  var expenditureId = $(tr).attr("data-expenditure-id");
  var data = {'expenditure_id': expenditureId};
  $.post("new_org_expenditureline/", data, function(resultdata) {
    data = $.parseJSON(resultdata);
    $(tr).after(' \
    <tr data-expenditureline-id="' + data['id'] + '"> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="ref" \
          value="' + data['ref'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="description" \
          value="' + data['description'] + '"> \
        </div></td> \
      <td><div class="form-group"> \
          <input type="text" class="form-control" name="value" \
          value="' + data['value'] + '"> \
        </div></td> \
      <td> \
          <a href="#" title="Delete expenditure line" class="deleteOrgExpenditureLineBtn"><span class="glyphicon glyphicon-trash"></span></a> \
        </td> \
    </tr>')
  }).fail(function() {
    alert("Unable to add a new expenditure line!");
  });
});

$(".addOrgDocBtn").click(function(e) {
  e.preventDefault;
  $.post("new_org_doc/", function(resultdata) {
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
    $('#addIncomingFundsForm #organisationfunder_id option[value="'+funder_id+'"]').remove()
  }).fail(function() {
    alert("Unable to delete that funder! If there are incoming funds associated with this funder, you have to delete them first.");
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
    'value': this.value
  }
  var id = $(this).closest("tr").attr("data-budgetline-id");
  var route = 'update_org_budgetline/';
  if (!id) {
    id = $(this).closest("tr").attr("data-budget-id");
    route = 'update_org_budgetline/';
  }
  data['id'] = id
  var input = this;
  resetFormGroup(input);
  $.post(route, data, function(resultdata) {
    successFormGroup(input);
  }).fail(function(){
    errorFormGroup(input);
  });
});
$(document).on("change", "#org-expenditure-form input", function(e) {
  var data = {
    'attr': this.name,
    'value': this.value
  }
  var id = $(this).closest("tr").attr("data-expenditureline-id");
  var route = 'update_org_expenditureline/';
  if (!id) {
    id = $(this).closest("tr").attr("data-expenditure-id");
    route = 'update_org_expenditureline/';
  }
  data['id'] = id
  var input = this;
  resetFormGroup(input);
  $.post(route, data, function(resultdata) {
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
$(document).on("click", ".deleteOrgBudgetLineBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var budgetline_id = $(tr).attr("data-budgetline-id");
  var data = {'budgetline_id': budgetline_id};
  $.post("delete_org_budgetline/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that budget line!");
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
$(document).on("click", ".deleteOrgExpenditureLineBtn", function(e) {
  e.preventDefault();
  var btn = this;
  var tr = $(btn).closest("tr");
  var expenditureline_id = $(tr).attr("data-expenditureline-id");
  var data = {'expenditureline_id': expenditureline_id};
  $.post("delete_org_expenditureline/", data, function(resultdata) {
    $(tr).fadeOut();
  }).fail(function() {
    alert("Unable to delete that expenditure line!");
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
