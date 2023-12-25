from ..Controller.genericController import GenericController
from ..Modal.utilities import getColumns, getPrimary
from flask import Blueprint

tableName = "constructorStandings"
id = getPrimary(tableName=tableName)[0][0]

constructorStandingsBP = Blueprint(tableName, __name__, url_prefix=f'/{tableName}')
allColumns = getColumns(tableName, id)

constructorStandings = GenericController(tableName, allColumns, id, "genericTemplate.html")
constructorStandings.render(constructorStandingsBP)