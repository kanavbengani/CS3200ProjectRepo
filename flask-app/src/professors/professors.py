from flask import Blueprint, request, jsonify, make_response
import json
from src import db


professors = Blueprint('professors', __name__)

# Get all courses from the db
@professors.route('/courses', methods=['GET'])
def get_courses():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Department_Name, School_Name,
        P.FName as \'Professor First Name\', 
        P.LName as \'Professor Last Name\', Difficulty 
        FROM Course JOIN Department using (Department_ID)
        JOIN School using (School_ID) 
        JOIN Section using (Section_ID)
        JOIN Professor P using (Prof_ID);
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Gets details about a course
@professors.route('/courses/{courseID}', methods=['GET'])
def get_CourseDetails():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Course_Name, Difficulty, Department_Name
        FROM Course JOIN Department using (Department_ID);
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Gets all reviews of a particular Course
@professors.route('/courses/{courseID}/reviews', methods=['GET'])
def get_CourseReviews():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Course_Name, S.FName, S.LName, Section_ID, Rating, Review_Content, Review_Date
        FROM Review JOIN Course using (Course_ID) JOIN Student using (Student_ID)
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Gets all reviews of a particular section of a Course
@professors.route('/courses/{courseID}/{sectionID}/reviews', methods=['GET'])
def get_CourseReviewsForSection():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Course_Name, S.FName, S.LName, Section_ID, Rating, Review_Content, Review_Date
        FROM Review JOIN Section using (Course_ID) JOIN Course using (Course_ID) JOIN Student using (Student_ID)
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Gets all sections of a particular course
@professors.route('/courses/{courseID}/sections', methods=['GET'])
def get_Sections():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Section_ID as \'Section\'
        FROM Section JOIN Course using (Course_ID)
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Gets details about a section of a course
@professors.route('/courses/{courseID}/{sectionID}', methods=['GET'])
def get_SectionDetails():
    cursor = db.get_db().cursor()
    query = '''
        SELECT P.FName as \'Professor First Name\', P.LName as \'Professor Last Name\', 
        City, State, Zip, Capacity, Price
        FROM Section JOIN Professor using (Prof_ID);
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all schools participating in CourseHub
@professors.route('/schools', methods=['GET'])
def get_SchoolInfo():
    cursor = db.get_db().cursor()
    query = '''
        SELECT School_Name, School_ID
        FROM School
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all info on a School
@professors.route('/schools/{schoolID}', methods=['GET'])
def get_SchoolInfoById():
    cursor = db.get_db().cursor()
    query = '''
        SELECT P.FName as \'Professor First Name\',
                P.LName as \'Professor Last Name\' 
        FROM School JOIN Professor using (Prof_ID);
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# Get a list of all professors in a school
@professors.route('/schools/{schoolID}/professors', methods=['GET'])
def get_ProfsInSchool():
    cursor = db.get_db().cursor()
    query = '''
        SELECT P.FName as \'Professor First Name\', 
               P.LName as \'Professor Last Name\'
               FROM School JOIN Professor using (Prof_ID)
               ORDER BY P.LName, P.FName;
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get a list of all info about a textbook
@professors.route('/textbooks/{ISBN}', methods=['GET'])
def get_TextbookInfo():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Name, Price, AuthorFName, AuthorLName, Edition, ISBN
        FROM Textbook
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get a list of all classes taught by a professor
@professors.route('/professors/{professorID}', methods=['GET'])
def get_classesTaughtByProf():
    cursor = db.get_db().cursor()
    query = '''
        SELECT Course_Name
        FROM Course JOIN Section using (Course_ID) 
        JOIN Professor using (Prof_ID);
    '''
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
