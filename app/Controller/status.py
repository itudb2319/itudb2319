from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "status"
id = getPrimary(tableName=tableName)[0][0]

statusBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

status = GenericController(tableName, allColumns, id, "genericTemplate.html")
status.render(statusBP)