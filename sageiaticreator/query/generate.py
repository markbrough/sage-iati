from sageiaticreator import app, db, models
import organisation as siorganisation
import activity as siactivity
import xlrd
import normality
import datetime, time
import re
from lxml import etree as et
from sageiaticreator.lib.codelist_helpers import codelists

DATA_STORAGE_DIR = app.config['DATA_STORAGE_DIR']

def isostring_date(value):
    # Returns a date object from a string of format YYYY-MM-DD
    return datetime.datetime.strptime(value, "%Y-%m-%d")
    
def date_isostring(value):
    # Returns a string of format YYYY-MM-DD from a date object
    return value.isoformat()
    
def current_datetime():
    return datetime.datetime.now().replace(
            microsecond=0).isoformat()
    
def actual_or_planned(value):
    date = isostring_date(value)
    current_datetime = datetime.datetime.now()
    if date > current_datetime:
        return "actual"
    return "planned"

def el_with_narrative(element_name, narrative):
    el = et.Element(element_name)
    el_nar = et.Element("narrative")
    el.append(el_nar)
    el_nar.text = narrative
    return el

def el_with_text(element_name, text):
    el = et.Element(element_name)
    el.text = text
    return el

# Generate activity date: actual if in past, otherwise planned
def el_date(start_end, iso_date):
    adt = codelists("ActivityDateType")
    
    actual_planned = actual_or_planned(iso_date)
    date_type = adt[start_end][actual_or_planned(iso_date)]
    
    el = et.Element('activity-date')
    el.set("type", date_type)
    el.set("iso-date", iso_date)
    return el
    
def el_org(role, o_name, o_ref, o_type):
    if role == "reporting":
        el = et.Element("reporting-org")
    else:
        r = codelists("OrganisationRole")
        el = et.Element("participating-org")
        el.set("role", r[role])
    el.set("ref", o_ref)
    el.set("type", o_type)
    el_nar = et.Element("narrative")
    el.append(el_nar)
    el_nar.text = o_name
    return el
    
def el_iati_identifier(activity, o_ref):
    el = et.Element("iati-identifier")
    a_code = activity['code']
    el.text = "%s-%s" % (o_ref, a_code)
    return el

def el_with_code(element_name, code, vocabulary=None):
    el = et.Element(element_name)
    el.set("code", code)
    if vocabulary:
        el.set("vocabulary", vocabulary)
    return el
    
def el_with_attrib(element_name, attrib, attrib_value):
    el = et.Element(element_name)
    el.set(attrib, attrib_value)
    return el
    
def el_contact_info(organisation):
    ec = et.Element("contact-info")
    ec.append(el_with_narrative("organisation",
              organisation.organisation_name))
    ec.append(el_with_narrative("person-name",
              organisation.organisation_contact_name))
    ec.append(el_with_text("telephone",
              organisation.organisation_contact_phone))
    ec.append(el_with_text("email",
              organisation.organisation_contact_email))
    ec.append(el_with_text("website",
              organisation.organisation_contact_website))
    ec.append(el_with_narrative("mailing-address",
              organisation.organisation_contact_address))
    return ec
    
def build_transaction(transaction_data):
    transaction_id = str(transaction_data["transaction_id"])
    transaction_date = transaction_data["date"]
    transaction_value = transaction_data["value"]
    transaction_description = transaction_data["description"]
    sector_code = transaction_data["sector_code"]
    sector_name = transaction_data["sector_name"]
    
    trt = transaction_data['transaction_type']
    if trt == "Debit": trtval = "E"
    if trt == "Credit": trtval = "IF"
    tt = codelists("TransactionType")
    transaction_type = tt[trtval]
    
    t = et.Element("transaction")
    t.set("ref", transaction_id)
    
    t.append(el_with_code("transaction-type", transaction_type))
    
    tdate = et.Element("transaction-date")
    t.append(tdate)
    tdate.set("iso-date", transaction_date)
    
    tvalue = et.Element("value")
    t.append(tvalue)
    tvalue.text = unicode(transaction_value)
    tvalue.set("value-date", transaction_date)
    
    t.append(el_with_narrative("description", transaction_description))
    
    t_sector = el_with_narrative("sector", sector_name)
    t_sector.set("code", sector_code)
    t_sector.set("vocabulary", "99")
    t.append(t_sector)

    return t
    
def build_account(ia, account):
    transactions = []
    if 'aggregation' in account:
        transactions = [build_transaction(aggregated_value)
            for d, aggregated_value in
            account['aggregated_values'].items()]
            
    else:
        transactions = [build_transaction(disaggregated_value)
            for disaggregated_value in
            account['disaggregated_values']]
    
    for transaction in transactions:
        ia.append(transaction)
            
    return ia

def build_accounts(ia, accounts):
    for account in accounts:
        build_account(ia, account)
    return ia
    
def build_period(el_i, period):
    p = period.as_dict()
    el_p = et.Element("period")
    el_i.append(el_p)
    el_p_s = et.Element("period-start")
    el_p.append(el_p_s)
    el_p_s.set("iso-date", date_isostring(p['period_start']))
    el_p_s = et.Element("period-end")
    el_p.append(el_p_s)
    el_p_s.set("iso-date", date_isostring(p['period_end']))
    
    el_target=el_with_attrib("target", "value", p['target_value'])
    el_p.append(el_target)
    if p.get('target_comment'):
        el_target.append(el_with_narrative("comment", p['target_comment']))
    
    el_actual=el_with_attrib("actual", "value", p['actual_value'])
    el_p.append(el_actual)
    if p.get('actual_comment'): 
        el_actual.append(el_with_narrative("comment", p['actual_comment']))
    return el_p
    
def build_indicator(el_result, indicator):
    i = indicator.as_dict()
    el_i = el_with_attrib("indicator", "measure", "1")
    el_result.append(el_i)
    if i.get('indicator_title'):
        el_i.append(el_with_narrative("title", i['indicator_title']))
    if i.get('indicator_description'):
        el_i.append(el_with_narrative("description",
                    i['indicator_description']))

    if i.get('baseline_year') and i.get('baseline_value'):
        el_i_b = et.Element("baseline")
        el_i.append(el_i_b)
        el_i_b.set("year", str(i['baseline_year'])[0:4])
        el_i_b.set("value", str(i['baseline_value']))
    if i.get('baseline_comment'):
        el_i_b.append(el_with_narrative("comment", i['baseline_comment']))
    
    for period in indicator.periods:
        build_period(el_i, period)
    return el_i
    
def build_result(ia, result):
    r = result.as_dict()
    el_result = el_with_attrib("result", "type", r['result_type'])
    ia.append(el_result)
    el_result.append(el_with_narrative("title", r['result_title']))
    if r.get('result_description'):
        el_result.append(el_with_narrative("description",
                         r['result_description']))
    for indicator in result.indicators:
        build_indicator(el_result, indicator)
    return ia
    
def build_results(ia, results):
    for result in results:
        build_result(ia, result)
    return ia

def build_activity(doc, activity, organisation):
    db_activity = siactivity.get_activity(activity['id'])
    
    ia = et.Element("iati-activity")
    doc.append(ia)

    ia.set("last-updated-datetime", current_datetime())
    #FIXME: put default currency in organisation settings
    ia.set("default-currency", organisation.organisation_default_currency)
    
    o_name = organisation.organisation_name
    o_ref = organisation.organisation_ref
    o_type = organisation.organisation_type
    
    # IATI Identifier
    ia.append(el_iati_identifier(activity, o_ref))
    
    # Reporting org
    ia.append(el_org("reporting", o_name, o_ref, o_type))
    
    # Title, Description
    ia.append(el_with_narrative("title", activity['title']))
    ia.append(el_with_narrative("description", activity['description']))
    
    # Participating orgs
    for funder in organisation.funders:
        ia.append(el_org("Funding", funder.funding_org_name, 
                                    funder.funding_org_ref, 
                                    funder.funding_org_type))
    ia.append(el_org("Implementing", o_name, o_ref, o_type))
    ia.append(el_org("Extending", o_name, o_ref, o_type))
    
    ia.append(el_with_code("activity-status", activity['activity_status']))
    
    # Activity dates
    ia.append(el_date("start", activity['start_date']))
    ia.append(el_date("end", activity['end_date']))
    
    # Contact info
    ia.append(el_contact_info(organisation))
    
    # Geography
    if activity['recipient_country']:
        ia.append(el_with_code("recipient-country", 
                  activity['recipient_country_code']))
    if activity['recipient_region']:
        ia.append(el_with_code("recipient-region",
                  activity['recipient_region_code']))
    #FIXME: Add location
    
    # Classifications
    ia.append(el_with_code("sector", activity['sector'], "1"))
    ia.append(el_with_code("default-flow-type", activity['flow_type']))
    ia.append(el_with_code("default-aid-type", activity['aid_type']))
    
    # Transactions
    ia = build_accounts(ia, activity['accounts'].values())
    
    #FIXME: Add documents
    #FIXME: Add conditions
    
    ia = build_results(ia, db_activity.results)
    
    return doc

# Process prepared transactions jsondata
def generate_iati_activity_data(jsondata, organisation_slug):
    doc = et.Element('iati-activities')
    doc.set("version", "2.01")
    doc.set("generated-datetime", current_datetime())
    
    organisation = siorganisation.get_org(organisation_slug)
    
    for activity_id, activity in jsondata['activities'].items():
        doc = build_activity(doc, activity, organisation)
    
    doc = et.ElementTree(doc)
    return doc
    
def el_with_isodate(element_name, iso_date):
    el = et.Element(element_name)
    el.set("iso-date", date_isostring(iso_date))
    return el

def el_total_budget(budget):
    el_b = et.Element("total-budget")
    el_b.append(el_with_isodate("period-start", budget.start_date))
    el_b.append(el_with_isodate("period-end", budget.end_date))
    el_val = el_with_text("value", str(budget.value))
    el_val.set("value-date", date_isostring(budget.start_date))
    el_b.append(el_val)    
    return el_b
    
def el_org_doc(document):
    el_d = et.Element("document-link")
    el_d.set("url", document.url)
    el_d.set("format", document.format)
    el_d.append(el_with_narrative("title", document.title))
    el_d.append(el_with_attrib("category", "code", document.category))
    return el_d
    
def build_organisation(doc, organisation):
    o_name = organisation.organisation_name
    o_ref = organisation.organisation_ref
    o_type = organisation.organisation_type
    o_currency = organisation.organisation_default_currency
    
    org = el_with_attrib("iati-organisation", "last-updated-datetime",
                         current_datetime())
    doc.append(org)
    org.set("default-currency", o_currency)
    org.append(el_with_text("organisation-identifier",
                            o_ref))
    org.append(el_with_narrative("name", o_name))

    # Reporting org
    org.append(el_org("reporting", o_name, o_ref, o_type))
    
    # Total budgets
    for budget in organisation.budgets:
        org.append(el_total_budget(budget))
        
    # Documents
    for document in organisation.documents:
        org.append(el_org_doc(document))
    return doc
    
# ORGANISATION FILE
def generate_iati_organisation_data(organisation_slug):
    organisation = siorganisation.get_org(organisation_slug)
    doc = et.Element('iati-organisations')
    doc.set("version", "2.01")
    doc.set("generated-datetime", current_datetime())
    doc = build_organisation(doc, organisation)
    doc = et.ElementTree(doc)
    return doc
