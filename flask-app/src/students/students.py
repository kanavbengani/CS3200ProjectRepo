from flask import Blueprint, request, jsonify, make_response, current_app
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


@students.route('/courses/<course_id>/sections', methods=['GET'])
def get_sections_by_course_id(course_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT Se.Section_ID as 'Section',
       IF(Se.InPerson='1',"Yes","No") AS 'InPerson?',
       P.FName as 'Professor First Name',
       P.LName as 'Professor Last Name',
       C.Difficulty as 'Difficulty'
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


@students.route('/courses/<course_id>/reviews', methods=['GET'])
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


@students.route('/courses/<course_id>/<section_id>/reviews', methods=['GET'])
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

# Get textbooks for a specific course.
@students.route('/courses/<course_id>/textbooks', methods=['GET'])
def get_textbooks_by_course_id(course_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT T.Title as 'Title',
       T.Author as 'Author',
       T.ISBN as 'ISBN',
       T.Course_ID as 'Course ID',
       T.Section_ID as 'Section ID'
FROM Course C
            JOIN Department D using (Department_ID)
            JOIN School Sc using (School_ID)
            JOIN Section Se using (Course_ID)
            JOIN Professor P using (Prof_ID)
            JOIN Textbook T using (Section_ID)
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

# POST Requests
@students.route('/courses/<courseID>/<sectionID>/<studentID>/reviews', methods=['POST'])
def add_review(courseID, sectionID, studentID):
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    review_content = req_data['review_content']
    review_rating = req_data['review_rating']

    insert_stmt = 'INSERT INTO Review (Student_ID, Course_ID, Section_ID, Review_Content, Rating) VALUES ("'
    insert_stmt += {studentID} + '", "' + {courseID} + '", "' + \
        {sectionID} + '", "' + review_content + '", "' + review_rating + ')'

    current_app.logger.info(insert_stmt)

    # execute the query
    cursor = db.get_db().cursor()
    cursor.execut(insert_stmt)
    db.get_db().commit()
    return "Success"
