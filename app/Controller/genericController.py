from flask import request, render_template, redirect, url_for
from ..Model.utilities import genericDataPrinter, db
from ..Model.utilities import getColumns
from ..Model.utilities import parseForms, deleteElementsFromTable, updateElements, insertElementToTable
from flask import Blueprint

class GenericController():
    def __init__(self, tableName, columns, id, template):
        self.tableName = tableName
        self.columns = columns
        self.id = id
        self.allColumns = getColumns(tableName=self.tableName, id=self.id)
        self.template = template

    def render(self, blueprint):
        @blueprint.route("/", methods=['GET', 'POST'])
        def wrapped():
            showList = self.columns
            orderBy = self.columns[0]
            search = ""
            limitter = "10"

            if request.method == 'POST':
                showList, orderBy, search, deletedElementIdList, deletedElementTableName, deletedElementId, updateElementList, insertedElementList, limitter = parseForms(request.form.items())
                if len(showList) == 0:
                    showList = self.columns
                if orderBy == "":
                    orderBy = self.columns[0]

                if len(updateElementList) != 0:
                    updateElements(tableName=self.tableName, updateElementList=updateElementList, id=self.id)

                if len(deletedElementIdList) != 0:
                    deleteElementsFromTable(tableId=deletedElementId, idList=deletedElementIdList, tableName=deletedElementTableName)

                if len(insertedElementList) != 0:
                    insertElementToTable(tableName=self.tableName, insertedElementList=insertedElementList)

                context = genericDataPrinter(tableName=self.tableName, columnDisplay=showList, orderBy=orderBy, id=self.id, search=search, limitter=limitter)
                selectedColumns = showList
            else:
                context = genericDataPrinter(tableName=self.tableName, columnDisplay=self.columns, orderBy=orderBy, id=self.id, search=search, limitter=limitter)
                selectedColumns = self.columns

            data = {'selectedShowColumns': selectedColumns, 'context': context, 'orderBy': orderBy, 'tableName': self.tableName, "allColumns": self.allColumns, "lastSearched": search, 'id':self.id, 'limitter': limitter}
            return render_template(self.template, context=data)
        
        @blueprint.route("/", methods=['GET', 'POST'])
        def updatePage():
            if request.method == 'POST':
                updateData = request.form
                
                id_value = updateData.get('id')

                query = f"UPDATE {self.tableName} SET "
                for column, value in updateData.items():
                    if column != 'id':
                        query += f"{column} = '{value}', "

                query = query.rstrip(', ')
                query += f" WHERE {self.id} = '{id_value}';"

                db.executeNonQuery(query)

                return redirect(url_for('wrapped'))

            else:
                data = db.executeQuery(f"SELECT * FROM {self.tableName} WHERE {self.id} = {self.id}")
                return render_template("update.html", context=data)
            