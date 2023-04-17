from flask import Blueprint, request, jsonify, make_response
import json
from src import db


students = Blueprint('students', __name__)

# Returns all courses.


@students.route('/courses', methods=['GET'])
def get_courses():
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT C.Course_Name as 'Course',
       D.Department_Name as 'Department',
       Sc.School_Name as 'School',
       C.Difficulty as 'Difficulty'
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

# Returns information for a specific course.


@students.route('/courses/<course_id>', methods=['GET'])
def get_courses_by_id(course_id):
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT DISTINCT C.Course_Name as 'Course',
       D.Department_Name as 'Department',
       Sc.School_Name as 'School',
       C.Difficulty as 'Difficulty'
FROM Course C
            JOIN Department D using (Department_ID)
            JOIN School Sc using (School_ID)
            JOIN Section Se using (Course_ID)
            JOIN Professor P using (Prof_ID)
WHERE C.Course_ID = %s;""", course_id)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns information for a specific section of a course.


@students.route('/courses/<course_id>/<section_id>', methods=['GET'])
def get_courses_by_id_and_section_id(course_id, section_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT C.Course_Name as 'Course Name',
       Se.Section_ID as 'Section',
       Sc.School_Name as 'School Name',
       Se.InPerson as 'In person?',
       P.FName as 'Professor First Name',
       P.LName as 'Professor Last Name',
       C.Difficulty as 'Difficulty'
FROM Course C
            JOIN Department D using (Department_ID)
            JOIN School Sc using (School_ID)
            JOIN Section Se using (Course_ID)
            JOIN Professor P using (Prof_ID)
WHERE C.Course_ID = {course_id} AND Se.Section_ID = {section_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns all sections of a specific course.
