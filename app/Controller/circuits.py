from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "circuits"
id = getPrimary(tableName=tableName)[0][0]

circuitsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

circuits = GenericController(tableName, allColumns, id, "genericTemplate.html")
circuits.render(circuitsBP)