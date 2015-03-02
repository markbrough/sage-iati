from sageiaticreator import db, models
import organisation as siorganisation
import normality
import datetime, time

def isostring_date(value):
    # Returns a date object from a string of format YYYY-MM-DD
    return datetime.datetime.strptime(value, "%Y-%m-%d")

def create_file(file_type, organisation_slug):
    organisation = siorganisation.get_org(organisation_slug)
    file_generated_datetime = datetime.datetime.utcnow()

    orgfile = models.OrgConvertedFile()
    orgfile.organisation_slug = organisation_slug
    orgfile.file_type_code = file_type
    orgfile.file_generated_date = file_generated_datetime
    orgfile.file_name = "%s-%s-%s.xml" % (organisation.organisation_ref,
                                          file_type,
                                          str(file_generated_datetime))
    db.session.add(orgfile)
    db.session.commit()
    return orgfile
    
def get_file(id):
    orgfile = models.OrgConvertedFile.query.filter_by(
        id = id
    ).first_or_404()
    return orgfile
    
def create_file_type(code, name):
    file_type = models.FileType()
    file_type.code = code
    file_type.name = name
    db.session.add(file_type)
    db.session.commit()
    return file_type
        
def get_file_type_by_name(name):
    filetype = models.FileType.query.filter_by(
        name = name
    ).first_or_404()
    return filetype
    
def list_files(organisation_slug):
    orgfiles = models.OrgConvertedFile.query.filter_by(
        organisation_slug = organisation_slug
            ).all()
    return orgfiles