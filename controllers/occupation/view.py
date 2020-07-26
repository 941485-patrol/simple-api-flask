from flask import (request, url_for, jsonify)
from controllers.occupation.main import bp
from models import Occupation

@bp.route('/view/<int:id>', methods=['GET'])
def view(id):
    job=Occupation.query.filter_by(id=id).first_or_404(description="Job not found")
    jobObj=job.serialize()
    jobObj['home']=url_for('occupations.index')
    jobObj['this']=request.path
    return jsonify(jobObj), 200