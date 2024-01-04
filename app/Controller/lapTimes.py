from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "laptimes"
id = getPrimary(tableName=tableName)[0][0]

laptimesBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

laptimes = GenericController(tableName, allColumns, id, "genericTemplate.html")
laptimes.render(laptimesBP)