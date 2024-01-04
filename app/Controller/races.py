from ..Controller.genericController import GenericController
from ..Model.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "races"
id = getPrimary(tableName=tableName)[0][0]

racesBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

races = GenericController(tableName, allColumns, id, "genericTemplate.html")
races.render(racesBP)