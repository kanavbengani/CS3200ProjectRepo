from flask import Blueprint, request, jsonify, make_response
import json
from src import db


professors = Blueprint('professors', __name__)

# Returns all courses.
@professors.route('/courses', methods=['GET'])
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
@professors.route('/courses/<course_id>', methods=['GET'])
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
@professors.route('/courses/<course_id>/<section_id>', methods=['GET'])
def get_courses_by_id_and_section_id(course_id, section_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT C.Course_Name as 'Course Name',
       Se.Section_ID as 'Section',
       Sc.School_Name as 'School Name',
       IF(Se.InPerson='1',"Yes","No") AS 'In Person?',
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
@professors.route('/courses/<course_id>/sections', methods=['GET'])
def get_sections_by_course_id(course_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT Se.Section_ID as 'Section',
       IF(Se.InPerson='1',"Yes","No") AS 'InPerson?',
       P.FName as 'Professor First Name',
       P.LName as 'Professor Last Name',
       CASE
              WHEN C.Difficulty = 1 THEN 'Easy'
              WHEN C.Difficulty = 2 THEN 'Moderately Easy'
                WHEN C.Difficulty = 3 THEN 'Moderate'
                WHEN C.Difficulty = 4 THEN 'Moderately Hard'
                WHEN C.Difficulty = 5 THEN 'Hard'
                ELSE 'Unknown'
            END AS 'Difficulty'
FROM Course C
            JOIN Department D using (Department_ID)
            JOIN School Sc using (School_ID)
            JOIN Section Se using (Course_ID)
            JOIN Professor P using (Prof_ID)
WHERE C.Course_ID = {course_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns all reviews of a specific course.
@professors.route('/courses/<course_id>/reviews', methods=['GET'])
def get_reviews_by_course_id(course_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT R.Rating as 'Rating',
       R.Review_Content as 'Comment',
       R.Review_Date as 'Date',
       R.Course_ID as 'Course ID',
       R.Section_ID as 'Section ID',
       R.Student_ID as 'Student ID'
FROM Course C
            JOIN Department D using (Department_ID)
            JOIN School Sc using (School_ID)
            JOIN Section Se using (Course_ID)
            JOIN Professor P using (Prof_ID)
            JOIN Review R using (Section_ID)
WHERE C.Course_ID = {course_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Returns all reviews of a specific section.
@professors.route('/courses/<course_id>/<section_id>/reviews', methods=['GET'])
def get_reviews_by_course_id_and_section_id(course_id, section_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT R.Rating as 'Rating',
       R.Review_Content as 'Comment',
       R.Review_Date as 'Date',
       R.Course_ID as 'Course ID',
       R.Section_ID as 'Section ID',
       R.Student_ID as 'Student ID'
FROM Course C
            JOIN Department D using (Department_ID)
            JOIN School Sc using (School_ID)
            JOIN Section Se using (Course_ID)
            JOIN Professor P using (Prof_ID)
            JOIN Review R using (Section_ID)
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


# Returns information about a specific school
@professors.route('/schools/<school_id>', methods=['GET'])
def get_school_by_id(school_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT DISTINCT S.School_ID as 'School ID',
       S.School_Name as 'School Name',
       S.City as 'City',
         S.State as 'State',
         S.Zipcode as 'Zipcode',
            D.Department_Name as 'Department Name'
FROM School S
JOIN Department D using (School_ID)
JOIN Course C using (Department_ID)
WHERE S.School_ID = {school_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns all professors employed by a school
@professors.route('/schools/<school_id>/professors', methods=['GET'])
def get_professors_by_school_id(school_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
       concat(P.FName, ' ', P.LName) as 'Professor Name',
       P.Years_Worked as 'Years Employed'
FROM Professor P
JOIN School S using (School_ID)
WHERE S.School_ID = {school_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns all courses taught by a professor


@professors.route('/professors/<professor_id>', methods=['GET'])
def get_courses_by_professor_id(professor_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
       C.Course_ID as 'Course ID',
       C.Course_Name as 'Course Name',
       CASE
              WHEN C.Difficulty = 1 THEN 'Easy'
              WHEN C.Difficulty = 2 THEN 'Moderately Easy'
                WHEN C.Difficulty = 3 THEN 'Moderate'
                WHEN C.Difficulty = 4 THEN 'Moderately Hard'
                WHEN C.Difficulty = 5 THEN 'Hard'
                ELSE 'Unknown'
            END AS 'Difficulty',
        S.Section_ID as 'Section ID'
FROM Course C
JOIN Section S using (Course_ID)
JOIN Professor P using (Prof_ID)
WHERE P.Prof_ID = {professor_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
