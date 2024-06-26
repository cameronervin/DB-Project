# CS7330Program
## Installation and Running
1. Install anaconda or miniconda (tutorials are available online as how to do this on different systems)
2. Install mysql and optionally a gui for looking at the database (we reccomend MySQLWorkbench)
3. Create a user and a database through the terminal or MySqlWorkbench
4. Create a `.env` file with the following attributes:
    - `HOST='<HostIp (Typically == localhost)>'`
    - `DBUSERNAME='<Username for a user with permissions to add remove and update table>'`
    - `PASSWORD='<Password for the username above>'`
    - `DB_NAME='<Name of a preexisting database on the sql server for the program to overwrite>'`
5. Move the `.env` file into the project repository
6. Create a conda environment for installation of packages (not necessary to use conda but is a good idea for package management)
7. Install the following required packages via `pip install <package_name>`:
    - `tkinter`
    - `pymysql`
    - `python-dotenv`
    - `pandas`
    - `numpy`
8. Run the file called `driver.py` and the GUI should appear
9. The different buttons that appear signify the different operations that can be made to the data. 
10. Once a button is pressed, there will be additional buttons and text fields to enter additional information
11. Once the additional information has been entered, the submit button on the right will make the desired changes to the database (if inputs are valid)
## Implementation Manual
### `sql_queries.py`
- Contains a class called `SqlQueries`
- This class stores all of our sql queries as python functions that return the sql statement as a string
- IE. `get_all_faculty()` will return "Select * from faculty;" as a string
- This implementation was chosen because it allows us to make changes to the sql queries without having to refactor the entire code base
### `sqlconnector.py`
- Contains a class called `SqlQueryRunner`
- `SqlQueryRunner` has 2 functions: 
    - `runChanger(sq_statement)`:
        - This function will run a statement that changes the database. Such as Insert, Create Table, Update, Delete...
    - `runSelect(sq_statement)`:
        - This function will run a statement that does not change the database. Such as a Select statement
    - `get_conn()`:
        - This function is not meant to be called outside of the class and it just connects to the sql database for queries to be run
### `db_interface.py`
- Contains a class called `Interface`
- `Interface` is designed to obfsucate the need to know whether or not to call `runChanger` vs `runSelect`
- `Interface` Has functions that are equivalent to all of the sql statements
- For example: `Interface.add_faculty()` will accept all of the information needed to add a faculty member and call the correct sql statement to the correct `SqlQueryRunner` funciton
- It also allows us to add additional logic to certain statements without the user needing to do so in the front end
- For example, in the `Interface.add_objective`, we can also make the database create a default subobjective and the user does not have to tell the database to  do so
### `test_data_generator.py`
- This file contains a class called `DataGen`
- `DataGen` has several functions that are used for populating the database with some initial data
- `DataGen.populate_all()` is the method that is most used as it will populate the entire database with valid data
- There are also methods to populate just a single table for testing, but those are not meant to be called by the user
### `driver.py`
- This file contains a class called `ProgramRunner` and several helper functions
- The main method in the file is designed to spin up the GUI for this program and assign the buttons to the various methods in `ProgramRunner`
- The methods within `ProgramRunner` are designed to handle a specific button press. IE. `handle_add_faculty()` is designed to prompt the user with the additional information that they will need to enter to add a faculty member and actually add it to the database
- Each method in `ProgramRunner` will create more GUI elements for the user to interract with using `Tkinter`
- Each method is also responsible for checking for the validity of what the user enters before uploading it to the database
- This means that the `handle_add_faculty()` method is responsible for getting the user input, making sure that it is valid information (like the email contains an @ sign for example) and then uploading that information into the database
## Database Schema
![alt text](db_schema.png "Schema")
### Sections Table
- Contains the following attributes:
    - `id Varchar(3)`: Represents the section id (IE. 001 or 007)
    - `course_id varchar(4)`: Represents the course the section belongs to (IE. 7330)
    - `dept_id VARCHAR(4)`: Represents the department that the course belongs to (IE. CS, ARHS etc.)
    - `num_students INT`: Represents the number of students in the course
    - `semester: VARCHAR(255)` Represents the semester that the section was offered (IE. Spring/Fall/Summer)
    - `teacher_id INT`: Represents the teacher ID denoting which faculty member is teaching the course
    - `year: YEAR`: Represents the year in which the course was offered
    - `primary key (id,course_id,dept_id,semester,year)`: Primary key is a combination of these attributes as it uniquely identifies the section
    - `foreign key (course_id,dept_id) references Courses(id,dept_id)`: Ensures that the course that the section belongs to exists in the courses table
    - `foreign key (teacher_id) references Faculty(id)`: Ensures that the faculty member assigned to teach the course exists in the faculty table
### ObjectiveAssignments Table
- __NOTE:__ We chose to associate objectives/subobjectives with sections as the sections have the years and semesters. This allows the user to have different objectives throughout the years without changing the requirements that previous course sections fufilled. Meaning that if a student took CS7330 in the Spring of 2020 and it fufilled requirements 1,2,3, if the university decided to change the contents of the course in the Summer of 2023 which results in the requirements 2,3,4,5 being fufilled, this schema allows the university to distinguish between the the two sections without overwriting the first set of requirements.
- Contains the following attributes:
    - `obj_id INT`: Signifies the ID of the objective to associate with a section
    - `sub_obj_id INT`: Signifies the SubObjective ID that is to be associated with the section
    - `section_id VARCHAR(3)`: Signifies the section for the assignment (IE. 001, 002 etc.)
    - `course_id VARCHAR(4)`: Signifies the course that the section belongs to (IE. 7330)
    - `dept_id VARCHAR(4)`: Signifies the department that the course belongs to (IE. CS, ARHS etc.)
    - `evaluation VARCHAR(255)`: How the section evaluates the objective (Typically something like "Exam", "Programming Assignment")
    - `num_passed INT`: Describes the number of students who fulfilled the requirement (IE. Number of students who passed the exam)
    - `num_failed INT`: Describes the number of students who failed to fulfill the evaluation (IE. Number of students who failed the exam)
    - `primary key (obj_id,course_id,sub_obj_id,section_id,dept_id)`: Ensures that a section can only have the same objective assigned to it one time and not many times
    - `foreign key (obj_id,sub_obj_id) references SubObjectives(objective_id,sub_id)`: Ensures that the objective to be assigned exists in the SubObjectives Table
    - `foreign key (section_id,course_id,dept_id) references Sections(id,course_id,dept_id)`: Ensures that the section that the objective is being assigned to exists in the Sections Table

### SubObjectives Table
- Contains the following attributes:
    - `objective_id INT`: The objective that this subObjective belongs to
    - `sub_id INT`: The unique identifier for the subObjective within the parent Objective
    - `description VARCHAR(255)`: What the subObjective is (IE. "Understand how context switching works")
    - `primary key (sub_id,objective_id)`: Ensures that the same subobjective cannot exist for the same parent objective but allows the same subObjective to exist for different parent Objectives
    - `foreign key (objective_id) references Objectives(id)`: Ensures that the parent objective that the subObjective belongs to exists in the Objectives Table
### Courses Table
- Contains the following attributes:
    - `id VARCHAR(4)`: ID of the course (IE. 7330, 5330 etc.)
    - `dept_id VARCHAR(4)`: Department code for the course (IE. CS, ARHS etc.)
    - `title VARCHAR(255)`: Title of the course as a string (IE. "Mobile Apps"),
    - `description VARCHAR(255)`: Description of the course as a string (IE. "Swift and Objective C programming course designed to teach students how to develop IOS applications")
    - `primary key (id,dept_id)`: Ensures that a course id can only exist one time for the department 
    - `foreign key (dept_id) references Departments(dept_code)`: Ensures that the department that the course belongs to exists in the Departments Table
### Departments Table
- Contains the following attributes:
    - `dept_name VARCHAR(255) UNIQUE`: Name of the department (IE. Computer Science)
    - `dept_code VARCHAR(4) UNIQUE`: Department code (IE. CS, ARHS, etc.)
    - `primary key (dept_code)`: Allows for the database to do faster lookups based on department code because it is set as the primary key
### Faculty Table
- Contains the following attributes:
    - `id INT auto_increment`: Id of the faculty member (set to auto increment because the user should not care about the faculty id)
    - `name VARCHAR(255)`: Name of the faculty member
    - `email VARCHAR(255)`: Email for the faculty (Note, the python interface will ensure that there are no duplicate emails in the database)
    - `fac_rank VARCHAR(255)`: Faculty rank (python interface forces to be one of: ["Full", "Adjunct","Associate","Assistant"])
    - `dept_code VARCHAR(255)`: Department that the faculty member belongs to (IE. CS, ARHS etc.)
    - `primary key (id)`: Ensures that the faculty ID uniquely identifies the faculty member (allows for the same name to exist)
    - `foreign key (dept_code) references Departments(dept_code)`: Ensures that the department that the faculty member belongs to exists in the database
### Objectives Table
- Contains the following attributes:
    - `id INT auto_increment`: ID for the attribute (autoincrementing because the user does not care what the id is, only that the objective is inserted)
    - `description varchar(255)`: Description of what the objective is (IE. "Understand basic programming skills and techniques")
    - `primary key (id)`: Ensures that the ID is the unique identifier for the attributes in the table
### Programs Table
- Contains the following attributes:
    - `name VARCHAR(255)`: Degree type of the program (python interface restricts the input to one of: ["MS","BS","BA","MA","BFA","MBA","PHD","MFA"])
    - `dept_code VARCHAR(4)`: Department code of the program (IE. CS, ARHS)
    - `head_id INT`: Faculty ID for the head of the department
    - ``primary key (name,dept_code)`: Ensures that the only a single degree type can exist for each department (IE. no duplicate MS in CS)
    - `foreign key (dept_code) references Departments(dept_code)`: Ensures that the department for the program exists in the Department Table
    - `foreign key (head_id) references Faculty(id)`: Ensures that the head of the department exists in the Faculty Table
### CourseAssignments Table
- Contains the following attributes:
    - `course_id VARCHAR(4)`: ID for the course to assign to a program (IE. 7330)
    - `dept_id varchar(4)`: Department code for the course to be assigned to a program (IE. CS, ARHS)
    - `program_name varchar(4)`: Degree type (IE. MS, BA, etc.) 
    - `primary key (course_id,dept_id,program_name)`: ensures that each course can be assigned to the same program at most 1 time
    - `foreign key (course_id,dept_id) references Courses(id,dept_id)`: Ensures that the course we are assigning to a program exists in the programs Table
    - `foreign key (program_name) references Programs(name)`: Ensures that the program that we want to assign a course to exists in the programs table
