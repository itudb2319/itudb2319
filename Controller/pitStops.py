from ..Controller.genericController import GenericController
from ..Modal.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "pitStops"
id = getPrimary(tableName=tableName)[0][0]

pitStopsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

pitStops = GenericController(tableName, allColumns, id, "genericTemplate.html")
pitStops.render(pitStopsBP)