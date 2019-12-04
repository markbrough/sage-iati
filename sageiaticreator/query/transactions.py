from flask import current_app
from sageiaticreator.extensions import db
from sageiaticreator import models
from sageiaticreator.query import organisation as siorganisation
from sageiaticreator.query import activity as siactivity
import xlrd
import normality
import datetime, time
import re

# Process transactions spreadsheet
# Divide into activities
# Generate IATI-identifier
# Aggregate and exclude

ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

def isostring_date(value):
    # Returns a date object from a string of format YYYY-MM-DD
    return datetime.datetime.strptime(value, "%Y-%m-%d")

def isoformat_date(value, bookdatemode):
    # Returns a date YYYY-MM-DD from a string of format DD/MM/YYYY
    # In an older version of Sage, dates were stored as strings
    # In a newer version, they're stored as Excel dates
    if (type(value) == str):
        return datetime.datetime.strptime(value, "%d/%m/%Y").date().isoformat()
    year, month, day, hour, minute, second = xlrd.xldate_as_tuple(value, bookdatemode)
    return datetime.datetime(year,month,day).date().isoformat()

def date_to_isoformat(date):
    return date.isoformat()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def correct_dept(department, activities):
    dept = unicode(int(department))
    if dept not in activities:
        #FIXME allow activities to specify default; for now just put
        # everything in the highest number activity
        return max(activities.keys())
    return dept

def redact(description, excluded_strings):
    exclusions = '|'.join(excluded_strings)
    redact_re = r'(^| )({})( |$)'.format(exclusions)
    redacted_description = re.sub(redact_re, r'\1*\3', description)
    if redacted_description != description:
        return True, redacted_description
    return False, description

def get_sheet_data(organisation_slug, file):
    # Disaggregated row
    def disaggregated_row(transactional_data, account_number,
                          account_description, sheet, row_number,
                          activities, excluded_strings, book):

        transaction_id = int(sheet.cell_value(row_number, 1))
        date = isoformat_date(sheet.cell_value(row_number, 3), book.datemode)
        description_unredacted = sheet.cell_value(row_number, 8)
        if description_unredacted == "Ledger Year End":
            return None
        redacted, description = redact(description_unredacted,
                                       excluded_strings)
        department = sheet.cell_value(row_number, 10)
        debit = sheet.cell_value(row_number, 14)
        credit = sheet.cell_value(row_number, 16)

        dept = correct_dept(
                department,
                activities
                )
        tr = transactional_data['activities'][dept]['accounts']
        if account_number not in tr:
            tr[account_number] = {'disaggregated_values': [],
                                  'aggregated_values': {}}
        tra = tr[account_number]
        trd = tra['disaggregated_values']

        if credit != "":
            transaction_type = "Credit"
            value = credit
        else:
            transaction_type = "Debit"
            value = debit
        dr = {
            "transaction_id": transaction_id,
            "sector_code": account_number,
            "sector_name": account_description,
            "date": date,
            "description": description,
            "description_unredacted": description_unredacted,
            "redacted": redacted,
            "value": value,
            "transaction_type": transaction_type,
            "department": department,
        }

        trd.append(dr)

        return dr

    # Row to be aggregated
    def aggregated_row(transactional_data, account_number,
                       account_description, sheet, row_number, dr, book):

        dept = correct_dept(
                dr['department'],
                activities
                )

        tr = transactional_data['activities'][dept]['accounts']
        if account_number not in tr:
            tr[account_number] = {'disaggregated_values': [],
                                  'aggregated_values': {}}
        tra = tr[account_number]
        tra['aggregation'] = True
        tra = tra['aggregated_values']

        datem = "%s-28" % dr['date'][0:7]
        if datem not in tra:
            tra[datem] = dr.copy()
            tra[datem]['date'] = datem
            tra[datem]['transaction_id'] = "%s-%s" % (account_number,
                datem)
            tra[datem]['description'] = account_description
        else:
            # If it's an incoming fund, then delete to create cumulative
            # value; else it's an expenditure, so just add
            if dr['transaction_type'] == "IF":
                tra[datem]['value'] -= dr['value']
            else:
                tra[datem]['value'] += dr['value']

        return transactional_data

    book = xlrd.open_workbook(filename=None,
        file_contents = file.stream.read())
    sheet = book.sheet_by_name("Nominal Activity")
    num_rows = sheet.nrows

    date_exported = sheet.cell_value(0, 2)
    #FIXME does the date exported value need to be used?

    account_number = None

    aggregated_accounts = siorganisation.list_aggregated_accounts(
        organisation_slug
    )
    aggregated_account_numbers = dict(
        map(lambda x: (x.account_number, x.account_description),
                            aggregated_accounts)
    )

    excluded_strings = siorganisation.list_excluded_strings(
        organisation_slug
    )
    excluded_strings = list(
        map(lambda x: x.excluded_string,
                      excluded_strings)
    )

    def fix_dates_accounts(data):
        data['start_date'] = date_to_isoformat(data['start_date'])
        data['end_date'] = date_to_isoformat(data['end_date'])
        data['accounts'] = {}
        return data

    activities = siactivity.list_activities(organisation_slug)
    activities = dict(
        map(lambda x: (x.code, fix_dates_accounts(x.as_dict())),
                       activities)
    )

    transactional_data = {'activities': activities }

    for row_number in range(0, num_rows):
        cv = sheet.cell_value(row_number, 1)
        if cv in ("", "N/C:",):
            an = sheet.cell_value(row_number, 2)
            ad = sheet.cell_value(row_number, 6)
            if an != "" and ad != "":
                account_number = an
                account_description = ad
            continue

        # Ignore header rows and blank rows
        if str(cv).startswith("No") or (cv == ""):
            continue

        # Drop all rows before an account is set
        if not account_number:
            continue

        dr = disaggregated_row(transactional_data, account_number,
                          account_description, sheet, row_number,
                          activities, excluded_strings, book)
        if dr is None:
            continue

        if account_number in aggregated_account_numbers:
            aggregated_row(transactional_data, account_number,
                           aggregated_account_numbers[account_number],
                           sheet, row_number, dr, book)

    for k, v in transactional_data["activities"].items():
        for account, values in transactional_data["activities"][k]["accounts"].items():
            v = transactional_data["activities"][k]["accounts"][account]
            dv = sorted(v["disaggregated_values"], key=lambda x: x["date"])
            transactional_data["activities"][k]["accounts"][account]["disaggregated_values"] = dv

    return transactional_data

def parse_transactions(organisation_slug, file):
    if file and allowed_file(file.filename):
        return get_sheet_data(organisation_slug, file)
