from flask import Flask, render_template, flash, request, Markup, \
    session, redirect, url_for, escape, Response, abort, send_file, jsonify
from flask.ext.login import login_required, current_user
                            
from sageiaticreator import app, db, models
from sageiaticreator.query import user as quser
from sageiaticreator.query import organisation as siorganisation
from sageiaticreator.query import activity as siactivity
from sageiaticreator.query import files as sifiles

import json

@app.route("/<organisation_slug>/<activity_id>/edit/")
def activity_edit(organisation_slug, activity_id):
    organisation = siorganisation.get_org(organisation_slug)
    activity = siactivity.get_activity(activity_id)
    return render_template("activity_edit.html",
                organisation = organisation,
                activity = activity,
                loggedinuser=current_user,
                          )
                          
@app.route("/<organisation_slug>/<activity_id>/edit/update_result/", methods=['POST'])
def activity_edit_result_attr(organisation_slug, activity_id):
    data = {
        'attr': request.form['attr'],
        'value': request.form['value'],
        'id': request.form['id']
    }
    update_status = siactivity.update_result_attr(data)
    if update_status == True:
        return "success"
    return "error"

@app.route("/<organisation_slug>/<activity_id>/edit/update_indicator/", methods=['POST'])
def activity_edit_indicator_attr(organisation_slug, activity_id):
    data = {
        'attr': request.form['attr'],
        'value': request.form['value'],
        'id': request.form['id']
    }
    update_status = siactivity.update_indicator_attr(data)
    if update_status == True:
        return "success"
    return "error"

@app.route("/<organisation_slug>/<activity_id>/edit/update_period/", methods=['POST'])
def activity_edit_period_attr(organisation_slug, activity_id):
    data = {
        'attr': request.form['attr'],
        'value': request.form['value'],
        'id': request.form['id']
    }
    update_status = siactivity.update_indicator_period_attr(data)
    if update_status == True:
        return "success"
    return "error"

@app.route("/<organisation_slug>/<activity_id>/edit/delete_result_data/", methods=['POST'])
def activity_delete_result_data(organisation_slug, activity_id):
    data = {
        'id': request.form['id'],
        'result_type': request.form['result_type']
    }
    delete_status = siactivity.delete_result_data(data)
    if delete_status == True:
        return "success"
    return "error"

@app.route("/<organisation_slug>/<activity_id>/edit/add_result_data/", methods=['POST'])
def activity_add_results_data(organisation_slug, activity_id):
    data = request.form
    add_status = siactivity.add_result_data(activity_id, data)
    if add_status:
        status_dict = add_status.as_dict()
        for k, v in status_dict.items():
            if k.endswith("year"):
                status_dict[k] = str(v)[0:4]
            if k.startswith("period"):
                status_dict[k] = str(v)[0:10]
        return jsonify(status_dict)
    return "error"

@app.route("/<organisation_slug>/<activity_id>/edit/update_activity/", methods=['POST'])
def activity_edit_attr(organisation_slug, activity_id):
    data = {
        'attr': request.form['attr'],
        'value': request.form['value'],
        'organisation_slug': organisation_slug,
        'id': activity_id,
    }
    update_status = siactivity.update_attr(data)
    if update_status == True:
        return "success"
    return "error"