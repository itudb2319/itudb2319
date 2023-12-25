from ..Controller.genericController import GenericController
from ..Modal.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "constructorResults"
id = getPrimary(tableName=tableName)[0][0]

constructorResultsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

constructorResults = GenericController(tableName, allColumns, id, "genericTemplate.html")
constructorResults.render(constructorResultsBP)