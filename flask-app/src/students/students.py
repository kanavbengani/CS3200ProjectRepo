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
    cursor.execute(f"""SELECT T.Name as 'Title',
       concat(T.AuthorFName, ' ', T.AuthorLName) as 'Author',
       ISBN as 'ISBN',
       Course_ID as 'Course ID'
FROM Course C
            JOIN CourseTextbook USING (Course_ID)
            JOIN Textbook T USING (ISBN)
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

# Returns all schools in the CourseHub database


@students.route('/schools', methods=['GET'])
def get_schools():
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT S.School_ID as 'School ID',
       S.School_Name as 'School Name',
       S.City as 'City',
         S.State as 'State',
         S.Zipcode as 'Zipcode'
FROM School S;""")
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


@students.route('/schools/<school_id>', methods=['GET'])
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

# Returns all courses offered by a specific school


@students.route('/schools/<school_id>/courses', methods=['GET'])
def get_courses_by_school_id(school_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT C.Course_ID as 'Course ID',
       C.Course_Name as 'Course Name',
       CASE
              WHEN C.Difficulty = 1 THEN 'Easy'
              WHEN C.Difficulty = 2 THEN 'Moderately Easy'
                WHEN C.Difficulty = 3 THEN 'Moderate'
                WHEN C.Difficulty = 4 THEN 'Moderately Hard'
                WHEN C.Difficulty = 5 THEN 'Hard'
                ELSE 'Unknown'
            END AS 'Difficulty',
       C.Department_ID as 'Department ID'
FROM Course C
JOIN Department D using (Department_ID)
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

# Returns all professors employed by a school


@students.route('/schools/<school_id>/professors', methods=['GET'])
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

# Returns all courses offered by a specific department


@students.route('/departments/<department_id>/courses', methods=['GET'])
def get_courses_by_department_id(department_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
       C.Course_Name as 'Course Name',
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
WHERE D.Department_ID = {department_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns all previous enrollments for a specific student


@students.route('/students/<student_id>/enrollments', methods=['GET'])
def get_enrollments_by_student_id(student_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
       C.Course_Name as 'Course Name',
       S.Section_ID as 'Section ID',
       O.Price as 'Price',
       concat(O.EnrolledSemester, ' ', O.EnrolledYear) as 'Enrolled In'
FROM Section S
JOIN Course C using (Course_ID)
JOIN EnrollmentOrderDetail O using (Section_ID)
JOIN EnrollmentOrder E using (EnrollmentOrder_ID)
WHERE E.Student_ID = {student_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns enrollments in an enrollment order


@students.route('/enrollmentdetails/<enrollmentorder_id>', methods=['GET'])
def get_enrollments_by_enrollmentorder_id(enrollmentorder_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
        E.Order_Date as 'Order Date',
       C.Course_Name as 'Course Name',
       S.Section_ID as 'Section ID',
       O.Price as 'Price',
       concat(O.EnrolledSemester, ' ', O.EnrolledYear) as 'Enrolled In'
FROM Section S
JOIN Course C using (Course_ID)
JOIN EnrollmentOrderDetail O using (Section_ID)
JOIN EnrollmentOrder E using (EnrollmentOrder_ID)
WHERE E.EnrollmentOrder_ID = {enrollmentorder_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns a list of reviews by the given student


@students.route('/students/<student_id>/reviews', methods=['GET'])
def get_reviews_by_student_id(student_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
       C.Course_Name as 'Course Name',
       S.Section_ID as 'Section ID',
       R.Review_Content as 'Review Content',
       R.Rating as 'Rating'
FROM Review R
JOIN Section S using (Section_ID)
JOIN Course C on R.Course_ID = C.Course_ID
WHERE R.Student_ID = {student_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns information of a given student


@students.route('/students/<student_id>', methods=['GET'])
def get_student_by_id(student_id):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
       S.Student_ID as 'Student ID',
       concat(S.FName, ' ', S.LName) as 'Student Name',
       S.Email as 'Student Email',
       S.Phone as 'Student Phone',
       S.SSN as 'Student Address'
FROM Student S
WHERE S.Student_ID = {student_id};""")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Returns information on a textbook given the ISBN


@students.route('/textbooks/<isbn>', methods=['GET'])
def get_textbook_by_isbn(isbn):
    cursor = db.get_db().cursor()
    cursor.execute(f"""SELECT
       T.ISBN as 'ISBN',
       T.Name as 'Title',
       T.Edition as 'Edition',
       concat(T.AuthorFName, ' ', T.AuthorLName) as 'Author',
       T.Price as 'Price'
FROM Textbook T
WHERE T.ISBN = {isbn};""")
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
@students.route('/professors/<professor_id>', methods=['GET'])
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
