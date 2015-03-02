from sageiaticreator import db, models
from query import organisation, activity, files
from query import user as quser

def setup():
    db.create_all()
    org_data = {
        "organisation_name": "Publish What You Fund",
        "organisation_ref": "GB-COH-07676886",
        "organisation_type": "21",
        "organisation_default_currency": "GBP",
        "organisation_contact_name": "Linda Grimsey",
        "organisation_contact_email": "info@publishwhatyoufund.org",
        "organisation_contact_address": "Southbank House, Black Prince Road, London SE1 7SJ. United Kingdom",
        "organisation_contact_phone": "+44 20 3176 2512",
        "organisation_contact_website": "http://www.publishwhatyoufund.org",
    }
    org = organisation.create_org(org_data)
    
    budget_data = {
        "start_date": '2014-01-10',
        "end_date": '2015-09-30',
        "value": 12345.00,
        "organisation_slug": org.organisation_slug,
    }
    organisation.create_org_budget(budget_data)
    
    excluded_strings = ["NAMES", "OF", "YOUR", "EMPLOYEES"
        ]
    
    for e in excluded_strings:
        excluded_string_data = {
            "organisation_slug": org.organisation_slug,
            "excluded_string": e,
        }
        organisation.create_excluded_string(excluded_string_data)
    
    aggregated_accounts = [
        {'account_number': '61000', 
         'account_description': 'Aggregated salaries'}, 
        {'account_number': '61100', 
         'account_description': 'Aggregated national insurance'},]
    
    for account in aggregated_accounts:
        account['organisation_slug'] = org.organisation_slug
        organisation.create_aggregated_account(account)
    
    activity_data = [{
        "code": "1",
        "title": "Advocacy and communications",
        "description": """Workstream 1 covers our advocacy and communications activities designed to change the policy environment and build a broader movement and partnerships around aid transparency.  Publish What You Fund's main targets are the International Aid Transparency Initiative (IATI), World Bank, the U.S. Government and the European Union institutions - with a secondary focus on other leading donor nations (including EU Member States) and a recipient country outreach programme.  IATI plays two roles in our advocacy and communications work - both a target of our advocacy activities but also the central vehicle for delivering aid transparency.  Our activities therefore include ensuring that IATI's evolution continues to deliver on existing donor commitments and particularly the needs of recipient countries, including the satisfactory finalisation of the "budget identifier".""",
        "organisation_slug": org.organisation_slug,
        "start_date": "2011-10-01",
        "end_date": "2017-09-30",
        "sector": "15163",
        "flow_type": "30",
        "aid_type": "C01",
        "activity_status": "2",
        "recipient_region": 1,
        "recipient_region_code": "998",
    },
    {
        "code": "2",
        "title": "Research and monitoring",
        "description": """Workstream 2 encompasses our monitoring and research activities, which are key inputs and tools for our advocacy and communication work. The primary activity of this workstream is the sustained monitoring of donor performance on aid transparency.  Following the publication of Publish What You Fund's 2010 Aid Transparency Assessment and the work with European CSO platforms on the AidWatch Report , an Aid Transparency Index has been developed, piloting a new methodology and primary data collection approach.  Going forward the aim is to undertake an annual round of data collection using the Aid Transparency Tracker and an open online data collection platform developed with Global Integrity, launched in late September 2011.  Using the annual data collected, Publish What You Fund will produce an index and ranking of donor transparency to be published in an annual aid transparency report.  The 2012 Index and report to be published in October 2012 will cover 72 aid agencies including all the major OECD bilaterals, multilaterals, IATI signatories, emerging providers of south-south cooperation and climate finance funds.""",
        "organisation_slug": org.organisation_slug,
        "start_date": "2011-10-01",
        "end_date": "2017-09-30",
        "sector": "15163",
        "flow_type": "30",
        "aid_type": "C01",
        "activity_status": "2",
        "recipient_region": 1,
        "recipient_region_code": "998",
    },
    {
        "code": "3",
        "title": "Operations and governance",
        "description": """Workstream 3 provides Publish What You Fund the organisational support and capacity to deliver an effective, flexible, transparent and well-managed campaign.  These internal activities concentrate on the provision of effective funding and staffing and governance, so as to ensure we both deliver on our overall objectives and that we reflect our principles in our own actions.  Publish What You Fund became an independent not-for-profit company on 1st October 2011.  We will also be scaling up our fundraising strategy to secure essential resources from foundations, private individuals and organisational partners.""",
        "organisation_slug": org.organisation_slug,
        "start_date": "2011-10-01",
        "end_date": "2017-09-30",
        "sector": "15163",
        "flow_type": "30",
        "aid_type": "C01",
        "activity_status": "2",
        "recipient_region": 1,
        "recipient_region_code": "998",
    },
    ]
    for ad in activity_data:
        activity.create_activity(ad)
    results = [
        {"result_title": "Increased IATI implementation",
         "result_description": "",
         "result_type": "outcome",
         "indicators": [
             {
             "indicator_title": "Number of IATI signatories",
             "indicator_desription": "",
             "baseline_value": "",
             "baseline_year": "2011",
             "baseline_comment": "",
             "periods": [
                 {
                     "period_start": "2011-01-01",
                     "period_end": "2016-09-30",
                     "target_value": "30",
                     "target_comment": "",
                     "actual_value": "37",
                     "actual_comment": "",
                 }
             ]
             },
             {
             "indicator_title": "Number of IATI implementation plans published by signatories",
             "indicator_desription": "",
             "baseline_value": "",
             "baseline_year": "2011",
             "baseline_comment": "",
             "periods": [
                 {
                     "period_start": "2011-01-01",
                     "period_end": "2016-09-30",
                     "target_value": "37",
                     "target_comment": "",
                     "actual_value": "35",
                     "actual_comment": "",
                 }
             ]
             }
     ]
     }
    ]
    activity.add_results_data(results, 1, "publish-what-you-fund")
    
    file_types = [{'code': '1', 'name': 'Activity'},
                  {'code': '2', 'name': 'Organisation'}]
    for ft in file_types:
        files.create_file_type(ft['code'], ft['name'])
        
    userdata = {
        'username': 'mark',
        'password': '12345',
        'name': 'Mark',
        'email_address': 'mark.brough@publishwhatyoufund.org',
        'organisation_slug': 'PWYF',
    }
    newu = quser.addUser(userdata)
    userpermissiondata = {
        'user_id': newu.id,
        'permission_name': 'view',
        'organisation_slug': org.organisation_slug,
    }
    userpermission = quser.addUserPermission(userpermissiondata)