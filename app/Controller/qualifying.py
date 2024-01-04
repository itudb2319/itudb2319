from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "qualifying"
id = getPrimary(tableName=tableName)[0][0]

qualifyingBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

qualifying = GenericController(tableName, allColumns, id, "genericTemplate.html")
qualifying.render(qualifyingBP)