from flask import render_template, request, \
    redirect, url_for, Response, jsonify, current_app, Blueprint
from flask_login import login_required, current_user

from sageiaticreator import models
from sageiaticreator.extensions import db
from sageiaticreator.query import user as quser
from sageiaticreator.query import organisation as siorganisation
from sageiaticreator.query import activity as siactivity
from sageiaticreator.query import files as sifiles
from sageiaticreator.query import transactions as sitransactions
from sageiaticreator.query import generate as sigenerate

import json, os
from lxml import etree as et


app = Blueprint('generate', __name__,
    url_prefix='/', static_folder='../static')


@app.route("/<organisation_slug>/activity.xml")
def get_activity_file(organisation_slug):
    DATA_STORAGE_DIR = current_app.config['DATA_STORAGE_DIR']
    file_obj = sifiles.get_file_by_type(organisation_slug, "1")
    full_file_path = os.path.join(DATA_STORAGE_DIR,
                                  file_obj.file_name)
    xmlfile = open(full_file_path, 'r')
    return Response(xmlfile.read(),
                    mimetype="text/xml")

@app.route("/<organisation_slug>/organisation.xml")
def get_organisation_file(organisation_slug):
    DATA_STORAGE_DIR = current_app.config['DATA_STORAGE_DIR']
    file_obj = sifiles.get_file_by_type(organisation_slug, "2")
    full_file_path = os.path.join(DATA_STORAGE_DIR,
                                  file_obj.file_name)
    xmlfile = open(full_file_path, 'r')
    return Response(xmlfile.read(),
                    mimetype="text/xml")

@app.route("/<organisation_slug>/files/<file_id>.xml")
def get_file(organisation_slug, file_id):
    DATA_STORAGE_DIR = current_app.config['DATA_STORAGE_DIR']
    file_obj = sifiles.get_file(file_id)
    full_file_path = os.path.join(DATA_STORAGE_DIR,
                                  file_obj.file_name)
    xmlfile = open(full_file_path, 'r')
    return Response(xmlfile.read(),
                    mimetype="text/xml")

@app.route("/<organisation_slug>/transactions_preview/",
    methods=["POST", "GET"])
def transactions_preview(organisation_slug):
    if request.method != "POST":
        flash("Error: no transactions data found.", "danger")
        return redirect(url_for('organisations.organisation_dashboard',
            organisation_slug = organisation_slug))
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

    file = request.files['transactions-file']
    transactions = sitransactions.parse_transactions(
        organisation_slug,
        file)

    return render_template("transactions_preview.html",
                organisation = organisation,
                organisation_budgets = organisation_budgets,
                activities = activities,
                aggregated_accounts = aggregated_accounts,
                excluded_strings = excluded_strings,
                transactions = transactions,
                jsondata = str(json.dumps(transactions)),
                loggedinuser=current_user
                          )

@app.route("/<organisation_slug>/transactions_preview/generate_iati_data/",
    methods=["POST", "GET"])
def generate_iati_data(organisation_slug):
    DATA_STORAGE_DIR = current_app.config['DATA_STORAGE_DIR']
    if request.method == "POST":
        jsondata = json.loads(request.form['jsondata'])

        activity_xml = sigenerate.generate_iati_activity_data(
                            jsondata,
                            organisation_slug
                        )
        # Make a new OrgConvertedFile
        file_type = sifiles.get_file_type_by_name("Activity").code
        newfile_obj = sifiles.create_file(file_type, organisation_slug)

        full_new_file_path = os.path.join(DATA_STORAGE_DIR,
                                          newfile_obj.file_name)
        activity_xml.write(full_new_file_path,
                           encoding="UTF-8",
                           pretty_print = True,
                           xml_declaration=True)

        flash("Successfully generated new activity file! You can find it at the top of 'Converted files', below.", "success")
        return redirect(url_for('organisations.organisation_dashboard',
                                organisation_slug = organisation_slug))

    return jsonify({"error": "No transactions data found"})

@app.route("/<organisation_slug>/generate_org_file/",
           methods=["POST", "GET"])
def orgfile_generate(organisation_slug):
    DATA_STORAGE_DIR = current_app.config['DATA_STORAGE_DIR']
    org_xml = sigenerate.generate_iati_organisation_data(
        organisation_slug
    )
    # Make a new OrgConvertedFile
    file_type = sifiles.get_file_type_by_name("Organisation").code
    newfile_obj = sifiles.create_file(file_type, organisation_slug)

    full_new_file_path = os.path.join(DATA_STORAGE_DIR,
                                      newfile_obj.file_name)

    org_xml.write(full_new_file_path,
                  encoding="UTF-8",
                  pretty_print = True,
                  xml_declaration=True)

    flash("Successfully generated new organisation file! You can find it at the top of 'Converted files', below.", "success")
    return redirect(url_for('organisations.organisation_dashboard',
                            organisation_slug = organisation_slug))
