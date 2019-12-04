from flask import render_template, request, jsonify, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

from sageiaticreator import models
from sageiaticreator.extensions import db
from sageiaticreator.query import user as quser
from sageiaticreator.query import organisation as siorganisation
from sageiaticreator.query import activity as siactivity
from sageiaticreator.query import files as sifiles

import json
import datetime

app = Blueprint('activities', __name__,
    url_prefix='/', static_folder='../static')


@app.route("/<organisation_slug>/new_activity/")
@login_required
def activity_new(organisation_slug):
    today = datetime.datetime.utcnow().date().isoformat()
    activity_data = {'start_date': today, 'end_date': today,
         'organisation_slug': organisation_slug}
    blank_fields = ['code', 'title', 'description']
    [activity_data.update({field: ''}) for field in blank_fields]

    previous_activity = models.Activity.query.order_by(
        models.Activity.id.desc()).first()
    if previous_activity:
        inherit_fields = ['recipient_country',
            'recipient_country_code', 'recipient_region',
            'recipient_region_code', 'sector',
            'flow_type', 'aid_type', 'activity_status']
        [activity_data.update({field: getattr(
            previous_activity, field)}) for field in inherit_fields]

    activity = siactivity.create_activity(activity_data
        )
    return redirect(url_for('activities.activity_edit',
        organisation_slug=organisation_slug,
        activity_id=activity.id))


@app.route("/<organisation_slug>/<activity_id>/delete/")
@login_required
def activity_delete(organisation_slug, activity_id):
    result = siactivity.delete_activity(activity_id)
    if result:
        flash("Successfully deleted that activity.", "success")
    else:
        flash("There was an error, and that activity could not be deleted.", "danger")
    return redirect(url_for("organisations.organisation_dashboard",
        organisation_slug=organisation_slug))
    return "Delete activity"


@app.route("/<organisation_slug>/<activity_id>/edit/")
@login_required
def activity_edit(organisation_slug, activity_id):
    organisation = siorganisation.get_org(organisation_slug)
    activity = siactivity.get_activity(activity_id)
    return render_template("activity_edit.html",
                organisation = organisation,
                activity = activity,
                loggedinuser=current_user,
                          )

@app.route("/<organisation_slug>/<activity_id>/edit/update_result/", methods=['POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
