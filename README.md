Sage to IATI Publisher
======================

Converts transactional information exported from Sage accounting software into IATI-XML format.

License: AGPL v3.0
------------------

Copyright (C) 2015 Mark Brough, Publish What You Fund

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
DISCLAIMER
----------

    This software is not in any way endorsed by or related to Sage.
    
Installation
------------

Set up a virtualenv:

    virtualenv ./pyenv

Activate the virtualenv:

    source ./pyenv/bin/activate

Install the requirements:

    pip install -r requirements.txt

Copy and edit the config.py.tmpl:

    cp config.py.tmpl config.py

You can also copy end edit the setup.py.tmpl to get going quickly (this 
will be replaced with a more sensible setup mechanism in future):

    cp sageiaticreator/setup.py.tmpl setup.py

Run the server:

    python manage.py runserver

Setup:

    http://localhost:5000/setup/