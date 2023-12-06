from flask import request, render_template, Blueprint, flash
from ..Modal.database import db
from werkzeug.utils import secure_filename
from os.path import join

adminBP = Blueprint('admin', __name__, url_prefix='/admin')

@adminBP.route('/bulkCUD', methods=['GET','POST'])
def cudWithCSVFile():
    if request.method == 'GET':
        return render_template('adminCUD.html')
    else:
        if 'file' not in request.files:
            return 'No file part in the request.'
        file = request.files['file']
        
        if file.filename == '':
            flash('No file submitted.')
        
        if file:
            filename = secure_filename(file.filename)
            file.save(join("/project/app/uploads", filename))
            if db.generateQuery(filename) == -1:
                flash("The bulk CUD conventions have not been met!\nCheck the convention.")
            else:
                return render_template('adminCUD.html')