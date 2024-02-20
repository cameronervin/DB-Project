class SQLQueries:
    ### Imports
    def create_departments():
        return f"""
            create table Departments (
            dept_name varchar(255) UNIQUE,
            dept_code varchar(4) UNIQUE,
            primary key (dept_code)
            );
        """
    def create_faculty():
        return f"""
            create table Faculty (
            id int auto_increment,
            name varchar(255),
            email varchar(255),
            fac_rank varchar(255),
            dept_code varchar(255),

            primary key (id),
            foreign key (dept_code) references Departments(dept_code)
            );
        """
    def create_programs():
        return f"""
            create table Programs (
            name VARCHAR(255), 
            dept_code varchar(4),
            head_id int,
            primary key (name,dept_code),
            foreign key (dept_code) references Departments(dept_code),
            foreign key (head_id) references Faculty(id)
            );
        """
    
    def create_courses():
        return f"""
            create table Courses (
            id varchar(4),
            dept_id varchar(4),
            title varchar(255),
            description varchar(255),

            primary key (id,dept_id),
            foreign key (dept_id) references Departments(dept_code) 
            );
        """
    
    def create_objectives():
        return f"""
            create table Objectives (
            id int auto_increment,
            description varchar(255),

            primary key (id)
            );
        """
    
    def create_subobjectives():
        return f"""
            create table SubObjectives (
            objective_id int,
            sub_id int,
            description varchar(255),
            

            primary key (sub_id,objective_id),
            foreign key (objective_id) references Objectives(id)

            );
        """
    
    def create_objective_assignments():
        return f"""
            create table ObjectiveAssignments (
            obj_id int,
            sub_obj_id int,
            section_id varchar(3),
            course_id varchar(4),
            dept_id varchar(4),
            evaluation varchar(255),
            semester varchar(255),
            year YEAR,
            num_passed int,
            num_failed int,
            primary key (obj_id,course_id,sub_obj_id,section_id,dept_id,semester,year),

            foreign key (obj_id,sub_obj_id) references SubObjectives(objective_id,sub_id),
            foreign key (section_id,course_id,dept_id) references Sections(id,course_id,dept_id)
            );
        """
    def create_sections():
        return f"""
            create table Sections (
            id varchar(3),
            course_id varchar(4),
            dept_id varchar(4),
            num_students int,
            semester varchar(255),
            teacher_id int,
            year YEAR,

            primary key (id,course_id,dept_id,semester,year),
            foreign key (course_id,dept_id) references Courses(id,dept_id),
            foreign key (teacher_id) references Faculty(id)
            );
        """
    def create_course_assignments():
        return f"""
            create table CourseAssignments (
            course_dept varchar(4),
            course_id varchar(4),
            dept_id varchar(4),
            program_name varchar(4),

            primary key (course_id,dept_id,program_name,course_dept),
            foreign key (course_id,course_dept) references Courses(id,dept_id),
            foreign key (program_name,dept_id) references Programs(name,dept_code)
            );
        """
    def delete_departments():
        return "drop table if exists Departments;"
    def delete_faculty():
        return "drop table if exists Faculty;"
    def delete_programs():
        return "drop table if exists Programs;"
    def delete_courses():
        return "drop table if exists Courses;"
    def delete_objectives():
        return "drop table if exists Objectives;"
    def delete_subobjectives():
        return "drop table if exists SubObjectives;"
    def delete_objective_assignments():
        return "drop table if exists ObjectiveAssignments;"
    def delete_sections():
        return "drop table if exists Sections;"
    def delete_course_assignments():
        return "drop table if exists CourseAssignments"
    
    @staticmethod
    def get_all_departments():
        return "select * from departments;"
    
    @staticmethod
    def get_all_faculty():
        return "select * from faculty;"
    
    @staticmethod
    def get_all_programs():
        return "select * from programs;"
    @staticmethod
    def get_all_courses():
        return "select * from courses;"
    
    @staticmethod
    def get_all_objectives():
        return "select * from objectives;"
    
    @staticmethod
    def get_all_subobjectives():
        return "select * from subobjectives"
    
    @staticmethod
    def get_all_objective_assignments():
        return "select * from ObjectiveAssignments;"
    
    @staticmethod
    def get_all_sections():
        return "select * from sections"
    
    @staticmethod
    def get_all_course_assignments():
        return "select * from courseassignments;"
    
    @staticmethod
    def insert_department(dept_name,dept_code):
        return f"""
            insert into Departments (dept_name,dept_code)
            values
            ("{dept_name}","{dept_code}");
        """
    @staticmethod
    def insert_faculty(name,email,fac_rank,dept_code):
        return f"""
            insert into faculty(name,email,fac_rank,dept_code)
            values
            ("{name}","{email}","{fac_rank}","{dept_code}");
        """
    @staticmethod
    def insert_program(name,dept_code,head_id):
        return f"""
            insert into Programs(name,dept_code,head_id)
            values
            ("{name}","{dept_code}",{head_id})
        """
    @staticmethod
    def insert_course(id,dept_id,title,description):
        return f"""
            insert into Courses(id,dept_id,title,description)
            values
            ("{id}","{dept_id}","{title}","{description}");
        """
    @staticmethod
    def insert_objective(description):
        return f"""
            insert into objectives(description)
            values
            ("{description}");
        """
    @staticmethod
    def insert_subobjective(obj_id,sub_id,desc):
        return f"""
        insert into SubObjectives(objective_id,sub_id,description)
        values
        ({obj_id},{sub_id},"{desc}");
        """
    @staticmethod
    def insert_objective_assignment(obj_id,sub_obj_id,section_id,course_id,dept_id,evaluation,semester,year,num_passed,num_failed):
        return f"""
            insert into ObjectiveAssignments(obj_id,sub_obj_id,section_id,course_id,dept_id,evaluation,num_passed,num_failed,semester,year)
            values
            ({obj_id},{sub_obj_id},"{section_id}","{course_id}","{dept_id}","{evaluation}",{num_passed},{num_failed}, "{semester}", "{year}");
        """
    @staticmethod
    def insert_section(id,course_id,dept_id,num_students,semester,teacher_id,year):
        return f"""
            insert into Sections(id,course_id,dept_id,num_students,semester,teacher_id,year)
            values
            ("{id}","{course_id}","{dept_id}",{num_students},"{semester}",{teacher_id},"{year}");
        """
    @staticmethod
    def insert_course_assignment(course_id,dept_id,program_name,course_dept):
        return f"""
            insert into CourseAssignments(course_id,dept_id,program_name,course_dept)
            values
            ("{course_id}","{dept_id}","{program_name}","{course_dept}");
        """
    

