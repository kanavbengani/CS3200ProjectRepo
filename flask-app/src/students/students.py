from flask import Blueprint, request, jsonify, make_response
import json
from src import db


students = Blueprint('students', __name__)


@students.route('/courses', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT C.Course_Name,
       D.Department_Name,
       Sc.School_Name,
       P.FName as 'Professor First Name',
       P.LName as 'Professor Last Name',
       C.Difficulty
FROM Course C
         JOIN Department D using (Department_ID)
         JOIN School Sc using (School_ID)
         JOIN Section Se using (Course_ID)
         JOIN Professor P using (Prof_ID);""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@students.route('/desccourses', methods=['GET'])
def desc_courses():
    cursor = db.get_db().cursor()
    cursor.execute('desc Course;')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
