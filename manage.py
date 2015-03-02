#!/usr/bin/env python

#  Tool to publish IATI data from Sage
#
#  Copyright (C) 2015 Mark Brough, Publish What You Fund
#
#  This programme is free software; you may redistribute and/or modify
#  it under the terms of the GNU Affero General Public License v3.0

from flask.ext.script import Manager
import sageiaticreator

def run():
    manager = Manager(sageiaticreator.app)
    manager.run()

if __name__ == "__main__":
    run()
