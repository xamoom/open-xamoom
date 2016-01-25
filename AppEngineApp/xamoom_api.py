#!/usr/bin/env python

"""
open xamoom cloud backend
Copyright (C) 2015  xamoom GmbH

This file is part of open xamoom

open xamoom is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

xamoom-wordpress is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with open xamoom.  If not, see <http://www.gnu.org/licenses/>.
"""

""" This module initializes the Google Cloud Endpoints API server with all API classes.
This module and the API server instance (APPLICATION) is referenced in app.yaml.
This file is part of open-xamoom.  """

import endpoints
from xamoom_enduser_api import XamoomEndUserApi
from xamoom_integration_api import XamoomIntegrationApi

__author__ = "xamoom GmbH, Bruno Hautzenberger"

__version__ = "19.2.1.6"
__maintainer__ = "Bruno Hautzenberger"
__email__ = "bruno@xamoom.com"
__status__ = "Production"


# The API server instance
APPLICATION = endpoints.api_server([XamoomIntegrationApi, XamoomEndUserApi])