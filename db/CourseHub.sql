-- This file is to bootstrap a database for the CS3200 project. 

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
create database if not exists CourseHub;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
-- TODO: If you changed the name of the database above, you need 
-- to change it here too.
grant all privileges on CourseHub.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too. 
use CourseHub;

-- Student
CREATE TABLE IF NOT EXISTS Student
(
    Student_ID int PRIMARY KEY,
    FName      varchar(25) NOT NULL,
    LName      varchar(25) NOT NULL,
    Email      varchar(50),
    Phone      varchar(20),
    SSN        varchar(20)
);

-- Enrollment_Order
CREATE TABLE IF NOT EXISTS EnrollmentOrder
(
    EnrollmentOrder_ID int PRIMARY KEY,
    Student_ID         int      NOT NULL,
    Order_Date         datetime NOT NULL DEFAULT current_timestamp,
    CONSTRAINT FK_1 FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- School
CREATE TABLE IF NOT EXISTS School
(
    School_ID   int PRIMARY KEY,
    School_Name varchar(100) NOT NULL,
    City        varchar(50)  NOT NULL,
    State       varchar(50)  NOT NULL,
    Zipcode     varchar(10)  NOT NULL
);

-- Academic Officer
CREATE TABLE IF NOT EXISTS AcademicOfficer
(
    Officer_ID   int PRIMARY KEY,
    FName        varchar(25) NOT NULL,
    LName        varchar(25) NOT NULL,
    School_ID    int         NOT NULL,
    Years_Worked int,
    CONSTRAINT FK_2 FOREIGN KEY (School_ID)
        REFERENCES School (School_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Department
CREATE TABLE IF NOT EXISTS Department
(
    Department_ID   int PRIMARY KEY,
    Department_Name varchar(50) NOT NULL,
    School_ID       int         NOT NULL,
    CONSTRAINT FK_3 FOREIGN KEY (School_ID)
        REFERENCES School (School_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Course
CREATE TABLE IF NOT EXISTS Course
(
    Course_ID     int PRIMARY KEY,
    Course_Name   varchar(50) NOT NULL,
    Difficulty    int,
    Department_ID int         NOT NULL,
    CONSTRAINT FK_5 FOREIGN KEY (Department_ID)
        REFERENCES Department (Department_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Professor
CREATE TABLE IF NOT EXISTS Professor
(
    Prof_ID      int PRIMARY KEY,
    FName        varchar(25) NOT NULL,
    LName        varchar(25) NOT NULL,
    School_ID    int         NOT NULL,
    Years_Worked int,
    CONSTRAINT FK_4 FOREIGN KEY (School_ID)
        REFERENCES School (School_ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Section
CREATE TABLE IF NOT EXISTS Section
(
    Course_ID  int,
    Section_ID int,
    InPerson   boolean     NOT NULL,
    City       varchar(50),
    State      varchar(50),
    Zipcode    varchar(10),
    Capacity   int         NOT NULL,
    Prof_ID    int         NOT NULL,
    Price float(5, 2) NOT NULL,
    PRIMARY KEY (Course_ID, Section_ID),
    CONSTRAINT FK_6 FOREIGN KEY (Course_ID)
        REFERENCES Course (Course_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT FK_7 FOREIGN KEY (Prof_ID)
        REFERENCES Professor (Prof_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Textbook
CREATE TABLE IF NOT EXISTS Textbook
(
    ISBN        varchar(20) PRIMARY KEY,
    Name        varchar(500) NOT NULL,
    Price       float(5, 2),
    AuthorFName varchar(25),
    AuthorLName varchar(25),
    Edition     varchar(25)
);

-- Review
CREATE TABLE IF NOT EXISTS Review
(
    Student_ID     int,
    Course_ID      int,
    Section_ID     int,
    Review_Date    datetime NOT NULL DEFAULT current_timestamp,
    Review_Content varchar(500),
    Rating         int      NOT NULL,
    PRIMARY KEY (Student_ID, Course_ID, Section_ID),
    CONSTRAINT FK_8 FOREIGN KEY (Student_ID)
        REFERENCES Student (Student_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT FK_9 FOREIGN KEY (Course_ID, Section_ID)
        REFERENCES Section (Course_ID, Section_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- EnrollmentOrderDetail
CREATE TABLE IF NOT EXISTS EnrollmentOrderDetail
(
    EnrollmentOrder_ID int,
    Course_ID          int,
    Section_ID         int,
    Price              float(5, 2) NOT NULL,
    EnrolledSemester varchar(10) NOT NULL,
    EnrolledYear year NOT NULL,
    PRIMARY KEY (EnrollmentOrder_ID, Course_ID, Section_ID),
    CONSTRAINT FK_10 FOREIGN KEY (EnrollmentOrder_ID)
        REFERENCES EnrollmentOrder (EnrollmentOrder_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT FK_11 FOREIGN KEY (Course_ID, Section_ID)
        REFERENCES Section (Course_ID, Section_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- CourseTextbook
CREATE TABLE IF NOT EXISTS CourseTextbook
(
    ISBN      varchar(20),
    Course_ID int,
    PRIMARY KEY (ISBN, COURSE_ID),
    CONSTRAINT FK_12 FOREIGN KEY (ISBN)
        REFERENCES Textbook (ISBN)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT FK_13 FOREIGN KEY (Course_ID)
        REFERENCES Course (Course_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);