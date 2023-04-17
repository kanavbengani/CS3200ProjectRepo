from flask import Blueprint, request, jsonify, make_response
import json
from src import db


students = Blueprint('students', __name__)


@students.route('/courses', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Department_Name, School_Name,\
        P.FName as \'Professor First Name\', P.LName as \'Professor Last Name\', Difficulty FROM Course \
            JOIN Department using (Department_ID),\
                JOIN School using (School_ID),\
                JOIN Section using (Section_ID),\
                JOIN Professor P using (Prof_ID);')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
