from ..Controller.genericController import GenericController
from ..Modal.utilities import getColumns, getPrimary
from flask import Blueprint


tableName = "sprintResults"
id = getPrimary(tableName=tableName)[0][0]


sprintResultsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

sprintResults = GenericController(tableName, allColumns, id, "genericTemplate.html")
sprintResults.render(sprintResultsBP)