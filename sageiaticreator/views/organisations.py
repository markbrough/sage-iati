from flask import Flask, render_template, flash, request, Markup, \
    session, redirect, url_for, escape, Response, abort, send_file, jsonify
from flask.ext.login import login_required, current_user
                            
from sageiaticreator import app, db, models
from sageiaticreator.query import user as quser
from sageiaticreator.query import organisation as siorganisation
from sageiaticreator.query import activity as siactivity
from sageiaticreator.query import files as sifiles
import json

@app.route("/<organisation_slug>/")
@login_required
def organisation_dashboard(organisation_slug):
    organisation = siorganisation.get_org(organisation_slug)
    organisation_budgets = siorganisation.list_org_budgets(
        organisation_slug
    )
    activities = siactivity.list_activities(
        organisation_slug
    )
    aggregated_accounts = siorganisation.list_aggregated_accounts(
        organisation_slug
    )
    excluded_strings = siorganisation.list_excluded_strings(
        organisation_slug
    )
    converted_files = sifiles.list_files(organisation_slug)
    return render_template("organisation.html",
                organisation = organisation,
                organisation_budgets = organisation_budgets,
                activities = activities,
                aggregated_accounts = aggregated_accounts,
                excluded_strings = excluded_strings,
                converted_files = converted_files,
                loggedinuser=current_user,
                          )

@app.route("/<organisation_slug>/edit/")
def organisation_edit(organisation_slug):
    organisation = siorganisation.get_org(organisation_slug)
    organisation_budgets = siorganisation.list_org_budgets(
        organisation_slug
    )
    organisation_docs = siorganisation.list_org_docs(
        organisation_slug
    )
    excluded_strings = siorganisation.list_excluded_strings(
        organisation_slug
    )
    aggregated_accounts = siorganisation.list_aggregated_accounts(
        organisation_slug
    )
    funders = siorganisation.list_funders(
        organisation_slug
    )
    return render_template("organisation_edit.html",
                organisation = organisation,
                organisation_budgets = organisation_budgets,
                excluded_strings = excluded_strings,
                aggregated_accounts = aggregated_accounts,
                funders = funders,
                organisation_docs = organisation_docs,
                loggedinuser=current_user
                          )

@app.route("/<organisation_slug>/edit/update_org_attr/", methods=['POST'])
def organisation_edit_attr(organisation_slug):
    data = {
        'attr': request.form['attr'],
        'value': request.form['value'],
        'organisation_slug': organisation_slug,
    }
    update_status = siorganisation.update_attr(data)
    if update_status == True:
        return "success"
    return "error"

@app.route("/<organisation_slug>/edit/update_org_budget/", methods=['POST'])
def organisation_edit_budget(organisation_slug):
    data = {
        'attr': request.form['attr'],
        'value': request.form['value'],
        'id': request.form['id'],
        'organisation_slug': organisation_slug,
    }
    update_status = siorganisation.update_budget(data)
    if update_status == True:
        return "success"
    return "error"

@app.route("/<organisation_slug>/edit/new_org_budget/", methods=['POST'])
def organisation_new_budget(organisation_slug):
    new_budget = siorganisation.new_budget(organisation_slug)
    if new_budget:
        return json.dumps(new_budget)
    return "error"

@app.route("/<organisation_slug>/edit/delete_org_budget/", methods=['POST'])
def organisation_delete_budget(organisation_slug):
    budget_id = request.form['budget_id']
    deleted_budget = siorganisation.delete_budget(budget_id)
    if deleted_budget:
        return "success"
    return False

@app.route("/<organisation_slug>/edit/new_org_doc/", methods=['POST'])
def organisation_new_doc(organisation_slug):
    new_doc = siorganisation.new_doc(organisation_slug)
    if new_doc:
        return json.dumps(new_doc.as_dict())
    return "error"

@app.route("/<organisation_slug>/edit/delete_org_doc/", methods=['POST'])
def organisation_delete_doc(organisation_slug):
    doc_id = request.form['doc_id']
    deleted_doc = siorganisation.delete_doc(doc_id)
    if deleted_doc:
        return "success"
    return False

@app.route("/<organisation_slug>/edit/update_org_doc/", methods=['POST'])
def organisation_edit_doc(organisation_slug):
    data = {
        'attr': request.form['attr'],
        'value': request.form['value'],
        'id': request.form['id'],
        'organisation_slug': organisation_slug,
    }
    update_status = siorganisation.update_doc(data)
    if update_status == True:
        return "success"
    return "error"
    
@app.route("/<organisation_slug>/edit/add_funding_org/", methods=['POST'])
def organisation_new_funder(organisation_slug):
    data = {
        "funding_org_name": request.form['funding_org_name'],
        "funding_org_ref": request.form['funding_org_ref'],
        "funding_org_type": request.form['funding_org_type'],
        "organisation_slug": organisation_slug,
    }
    new_funder = siorganisation.create_funder(data)
    if new_funder:
        return json.dumps(new_funder.as_dict())
    return "error"

@app.route("/<organisation_slug>/edit/delete_funder/", methods=['POST'])
def organisation_delete_funder(organisation_slug):
    funder_id = request.form['funder_id']
    deleted_funder = siorganisation.delete_funder(
        funder_id
    )
    if deleted_funder:
        return "success"
    return False

@app.route("/<organisation_slug>/edit/delete_aggregated_account/", methods=['POST'])
def organisation_delete_aggregated_account(organisation_slug):
    aggregated_account_id = request.form['aggregated_account_id']
    deleted_account = siorganisation.delete_aggregated_account(
        aggregated_account_id
    )
    if deleted_account:
        return "success"
    return False

@app.route("/<organisation_slug>/edit/delete_excluded_string/", methods=['POST'])
def organisation_delete_excluded_string(organisation_slug):
    excluded_string_id = request.form['excluded_string_id']
    deleted_string = siorganisation.delete_excluded_string(
        excluded_string_id
    )
    if deleted_string:
        return "success"
    return False

@app.route("/<organisation_slug>/edit/add_excluded_string/", methods=['POST'])
def organisation_add_excluded_string(organisation_slug):
    excluded_string = request.form['excluded_string']
    data = {
        'excluded_string': excluded_string,
        'organisation_slug': organisation_slug,
    }
    excluded_string = siorganisation.create_excluded_string(
        data
    )
    if excluded_string:
        return json.dumps(excluded_string.as_dict())
    return False

@app.route("/<organisation_slug>/edit/add_aggregate_account/", methods=['POST'])
def organisation_add_aggregate_account(organisation_slug):
    account_number = request.form['account_number']
    account_description = request.form['account_description']
    data = {
        'account_number': account_number,
        'account_description': account_description,
        'organisation_slug': organisation_slug,
    }
    aggregate_account = siorganisation.create_aggregated_account(
        data
    )
    if aggregate_account:
        return json.dumps(aggregate_account.as_dict())
    return False