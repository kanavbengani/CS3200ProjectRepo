from flask import Blueprint, request, jsonify, make_response, current_app
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


@professors.route('/courses/<course_id>/<section_id>', methods=['GET', 'PUT'])
def get_courses_by_id_and_section_id(course_id, section_id):
    if request.method == 'GET':
        cursor = db.get_db().cursor()
        cursor.execute(f"""SELECT C.Course_Name as 'Course Name',
       Se.Section_ID as 'Section',
       Sc.School_Name as 'School Name',
       IF(Se.InPerson='1',"Yes","No") AS 'In Person?',
       P.FName as 'Professor First Name',
       P.LName as 'Professor Last Name',
       Se.Price as 'Price',
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
    elif request.method == 'PUT':
        cursor = db.get_db().cursor()
        cursor.execute(f"""UPDATE Section
            SET InPerson = {request.json['InPerson']},
            City = '{request.json['City']}',
            State = '{request.json['State']}',
            Zipcode = {request.json['Zipcode']},
            Capacity = {request.json['Capacity']},
            Price = {request.json['Price']}
            WHERE Section_ID = {section_id};""")
        db.get_db().commit()
        return make_response(jsonify({'message': 'Section updated successfully.'}), 200)


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
            END AS 'Difficulty',
        Se.Price as 'Price',
        Se.Capacity as 'Capacity'
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
    cursor.execute(f"""SELECT 
       round(avg(R.Rating),1) as 'Average Rating of All Sections (out of 5)',
       C.Course_Name as 'Course Name'
       FROM Course C
            JOIN Section Se using (Course_ID)
            JOIN Review R using (Section_ID)
       WHERE C.Course_ID = {course_id}
       GROUP BY C.Course_Name;""")
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
    cursor.execute(f"""SELECT R.Rating as 'Rating out of 5',
       R.Review_Content as 'Comment',
       R.Review_Date as 'Date',
       C.Course_Name as 'Course Name',
       R.Section_ID as 'Section Number',
       concat(P.FName, ' ', P.LName) as 'Professor Name',
       concat(St.FName, ' ', St.LName) as 'Student Name'
FROM Course C
            JOIN Department D using (Department_ID)
            JOIN School Sc using (School_ID)
            JOIN Section Se using (Course_ID)
            JOIN Professor P using (Prof_ID)
            JOIN Review R using (Section_ID)
            JOIN Student St using (Student_ID)
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
                        S.Zipcode as 'Zipcode'
                    FROM School S WHERE S.School_ID = {school_id};""")
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

# Returns information about a professor or updates information by professor id


@professors.route('/professors/<professor_id>', methods=['GET', 'PUT', 'DELETE'])
def professor_id(professor_id):
    if request.method == 'GET':
        cursor = db.get_db().cursor()
        cursor.execute(f"""SELECT
        FName as 'First Name',
        LName as 'Last Name',
        Years_Worked as 'Years worked',
        S.School_Name as 'Teaches at'
        FROM Professor P
        JOIN School S using (School_ID)
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
    elif request.method == 'PUT':
        current_app.logger.info('Processing form data')
        req_data = request.get_json()
        current_app.logger.info(req_data)

        fname = req_data['fname']
        lname = req_data['lname']
        years_worked = req_data['years_worked']

        update_stmt = f"UPDATE Professor SET FName = '{fname}', LName = '{lname}', Years_Worked = '{years_worked}' WHERE Prof_ID = {professor_id}"

        current_app.logger.info(update_stmt)

        # execute the query
        cursor = db.get_db().cursor()
        cursor.execute(update_stmt)
        db.get_db().commit()
        return "Success"
    elif request.method == 'DELETE':
        delete_stmt = f"DELETE FROM Professor WHERE Prof_ID = {professor_id};"

        cursor = db.get_db().cursor()
        cursor.execute(delete_stmt)
        db.get_db().commit()
        return "Success"

# returns all courses taught by a professor


@professors.route('/professors/<professor_id>/courses', methods=['GET'])
def courses_taught_by_prof(professor_id):
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
        S.Section_ID as 'Section ID',
        Sc.School_Name as 'School'
    FROM Course C
    JOIN Section S using (Course_ID)
    JOIN Professor P using (Prof_ID)
    JOIN School Sc using (School_ID)
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

# Adds a textbook by a professor for a course


@professors.route('/courses/<courseID>/textbooks', methods=['POST'])
def add_textbook(courseID):
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    isbn = req_data['isbn']
    name = req_data['name']
    price = req_data['price']
    authorfname = req_data['authorfname']
    authorlname = req_data['authorlname']
    edition = req_data['edition']

    insert_stmt = f"""INSERT INTO Textbook
            (ISBN, 
            Name, 
            Price, 
            AuthorFName, 
            AuthorLName, 
            Edition)
    SELECT '{isbn}',
           '{name}',
           {price},
           '{authorfname}',
           '{authorlname}',
           '{edition}'
    WHERE NOT EXISTS
        (SELECT 1
         FROM Textbook
         WHERE ISBN = '{isbn}');"""

    # execute the query
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()

    insert_stmt = f"""INSERT INTO CourseTextbook
            (ISBN, 
            Course_ID)
    SELECT '{isbn}',
           {courseID}
    WHERE NOT EXISTS
        (SELECT 1
         FROM CourseTextbook
         WHERE ISBN = '{isbn}' AND Course_ID = {courseID});"""

    # execute the query
    cursor = db.get_db().cursor()
    cursor.execute(insert_stmt)
    db.get_db().commit()
    return "Success"

# Updates the price of a textbook


@professors.route('/textbooks/<isbn>', methods=['PUT'])
def update_textbook(isbn):
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    price = req_data['price']

    update_stmt = f"""UPDATE Textbook
    SET Price = {price}
    WHERE ISBN = {isbn};"""

    # execute the query
    cursor = db.get_db().cursor()
    cursor.execute(update_stmt)
    db.get_db().commit()
    return "Success"
