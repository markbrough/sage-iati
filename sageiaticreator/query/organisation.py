from sageiaticreator.extensions import db
from sageiaticreator import models
import normality
import datetime, time

def isostring_date(value):
    # Returns a date object from a string of format YYYY-MM-DD
    return datetime.datetime.strptime(value, "%Y-%m-%d")

def create_org(data):
    #FIXME check this org doesn't already exist?
    org = models.Organisation()

    for attr, val in data.items():
        setattr(org, attr, val)
    org.organisation_slug = normality.slugify(data['organisation_name'])
    db.session.add(org)
    db.session.commit()
    return org

def get_org(organisation_slug):
    org = models.Organisation.query.filter_by(
        organisation_slug = organisation_slug
    ).first_or_404()
    return org

def list_orgs():
    orgs = models.Organisation.query.all()
    return orgs

def create_org_budget(data):
    tb = models.OrgBudget()
    tb.start_date = isostring_date(data['start_date'])
    tb.end_date = isostring_date(data['end_date'])
    tb.value = data['value']
    tb.organisation_slug= data['organisation_slug']
    db.session.add(tb)
    db.session.commit()

def list_org_budgets(organisation_slug):
    tb = models.OrgBudget.query.filter_by(
        organisation_slug = organisation_slug
    ).all()
    return tb


def list_org_expenditure(organisation_slug):
    tb = models.OrgExpenditure.query.filter_by(
        organisation_slug=organisation_slug
    ).all()
    return tb


def update_attr(data):
    organisation = models.Organisation.query.filter_by(
        organisation_slug = data['organisation_slug']
    ).first()
    setattr(organisation, data['attr'], data['value'])
    db.session.add(organisation)
    db.session.commit()
    return True


def update_budget(data):
    ob = models.OrgBudget.query.filter_by(
        id = data['id']
    ).first()
    if data['attr'].endswith('date'):
        data['value'] = isostring_date(data['value'])
    setattr(ob, data['attr'], data['value'])
    db.session.add(ob)
    db.session.commit()
    return True


def new_budget(organisation_slug):
    nb = models.OrgBudget()
    nb.start_date = datetime.datetime.utcnow()
    nb.end_date = datetime.datetime.utcnow()
    nb.value = 0
    nb.status = 1
    nb.organisation_slug = organisation_slug
    db.session.add(nb)
    db.session.commit()
    return nb.as_dict()


def delete_budget(budget_id):
    bo = models.OrgBudget.query.filter_by(
        id = budget_id
    ).first()
    if bo:
        db.session.delete(bo)
        db.session.commit()
        return True
    return False


def new_budgetline(budget_id):
    nbl = models.OrgBudgetLine()
    nbl.budget_id = budget_id
    nbl.ref = 'Reference'
    nbl.description = 'Description'
    nbl.value = 0
    db.session.add(nbl)
    db.session.commit()
    return nbl.as_dict()


def update_budgetline(data):
    obl = models.OrgBudgetLine.query.filter_by(
        id=data['id']
    ).first()
    setattr(obl, data['attr'], data['value'])
    db.session.add(obl)
    db.session.commit()
    return True


def delete_budgetline(budgetline_id):
    bl = models.OrgBudgetLine.query.filter_by(
        id=budgetline_id
    ).first()
    if bl:
        db.session.delete(bl)
        db.session.commit()
        return True
    return False


def update_expenditure(data):
    ob = models.OrgExpenditure.query.filter_by(
        id=data['id']
    ).first()
    if data['attr'].endswith('date'):
        data['value'] = isostring_date(data['value'])
    setattr(ob, data['attr'], data['value'])
    db.session.add(ob)
    db.session.commit()
    return True


def new_expenditure(organisation_slug):
    nb = models.OrgExpenditure()
    nb.start_date = datetime.datetime.utcnow()
    nb.end_date = datetime.datetime.utcnow()
    nb.value = 0
    nb.organisation_slug = organisation_slug
    db.session.add(nb)
    db.session.commit()
    return nb.as_dict()


def delete_expenditure(expenditure_id):
    bo = models.OrgExpenditure.query.filter_by(
        id=expenditure_id
    ).first()
    if bo:
        db.session.delete(bo)
        db.session.commit()
        return True
    return False


def new_expenditureline(expenditure_id):
    nel = models.OrgExpenditureLine()
    nel.expenditure_id = expenditure_id
    nel.ref = 'Reference'
    nel.description = 'Description'
    nel.value = 0
    db.session.add(nel)
    db.session.commit()
    return nel.as_dict()


def update_expenditureline(data):
    oel = models.OrgExpenditureLine.query.filter_by(
        id=data['id']
    ).first()
    setattr(oel, data['attr'], data['value'])
    db.session.add(oel)
    db.session.commit()
    return True


def delete_expenditureline(expenditureline_id):
    el = models.OrgExpenditureLine.query.filter_by(
        id=expenditureline_id
    ).first()
    if el:
        db.session.delete(el)
        db.session.commit()
        return True
    return False


def list_org_docs(organisation_slug):
    td = models.OrgDoc.query.filter_by(
        organisation_slug = organisation_slug
    ).all()
    return td

def new_doc(organisation_slug):
    nd = models.OrgDoc()
    nd.title = ""
    nd.url = ""
    nd.category = ""
    nd.date = None
    nd.format = ""
    nd.organisation_slug = organisation_slug
    db.session.add(nd)
    db.session.commit()
    return nd

def delete_doc(doc_id):
    dd = models.OrgDoc.query.filter_by(
        id = doc_id
    ).first()
    if dd:
        db.session.delete(dd)
        db.session.commit()
        return True
    return False

def update_doc(data):
    ud = models.OrgDoc.query.filter_by(
        id = data['id']
    ).first()
    if data['attr'] == 'date':
        if data['value'] == '':
            data['value'] = None
        else:
            data['value'] = isostring_date(data['value'])
    setattr(ud, data['attr'], data['value'])
    db.session.add(ud)
    db.session.commit()
    return True

def create_excluded_string(excluded_string_data):
    es = models.OrgExcludedStrings()
    es.organisation_slug = excluded_string_data['organisation_slug']
    es.excluded_string = excluded_string_data['excluded_string']
    db.session.add(es)
    db.session.commit()
    return es

def list_excluded_strings(organisation_slug):
    es = models.OrgExcludedStrings.query.filter_by(
        organisation_slug = organisation_slug
    ).all()
    return es

def delete_excluded_string(excluded_string_id):
    es = models.OrgExcludedStrings.query.filter_by(
        id = excluded_string_id
    ).first()
    db.session.delete(es)
    db.session.commit()
    return True

def create_aggregated_account(aggregated_account_data):
    ac = models.OrgAggregatedAccounts()
    ac.organisation_slug = aggregated_account_data['organisation_slug']
    ac.account_number = aggregated_account_data['account_number']
    ac.account_description = aggregated_account_data['account_description']
    db.session.add(ac)
    db.session.commit()
    return ac

def list_aggregated_accounts(organisation_slug):
    ac = models.OrgAggregatedAccounts.query.filter_by(
        organisation_slug = organisation_slug
    ).all()
    return ac

def delete_aggregated_account(account_id):
    ac = models.OrgAggregatedAccounts.query.filter_by(
        id = account_id
    ).first()
    db.session.delete(ac)
    db.session.commit()
    return True

def list_funders(organisation_slug):
    funders = models.OrgFunder.query.filter_by(
        organisation_slug = organisation_slug
    ).all()
    return funders

def create_funder(data):
    nf = models.OrgFunder()
    for k, v in data.items():
        setattr(nf, k, v)
    db.session.add(nf)
    db.session.commit()
    return nf

def delete_funder(funder_id):
    df = models.OrgFunder.query.filter_by(
        id = funder_id
    ).first()
    db.session.delete(df)
    db.session.commit()
    return True
