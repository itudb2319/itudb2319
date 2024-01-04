from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "results"
id = getPrimary(tableName=tableName)[0][0]

resultsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

results = GenericController(tableName, allColumns, id, "genericTemplate.html")
results.render(resultsBP)