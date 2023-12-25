from ..Controller.genericController import GenericController
from ..Modal.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "driverStandings"
id = getPrimary(tableName=tableName)[0][0]

driverStandingsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

driverStandings = GenericController(tableName, allColumns, id, "genericTemplate.html")
driverStandings.render(driverStandingsBP)