from sqlconnector import SqlQueryRunner
import pandas as pd
from sql_queries import SQLQueries as sq


class Interface:
    def __init__(self):
        self.runner = SqlQueryRunner()
    def create_all_tables(self):
        self.runner.runChanger(sq.create_departments())
        self.runner.runChanger(sq.create_faculty())
        self.runner.runChanger(sq.create_programs())
        self.runner.runChanger(sq.create_courses())
        self.runner.runChanger(sq.create_objectives())
        self.runner.runChanger(sq.create_subobjectives())
        self.runner.runChanger(sq.create_sections())
        self.runner.runChanger(sq.create_objective_assignments())
        self.runner.runChanger(sq.create_course_assignments())
    def delete_all_tables(self):
        self.runner.runChanger(sq.delete_course_assignments())
        self.runner.runChanger(sq.delete_objective_assignments())
        self.runner.runChanger(sq.delete_sections())
        self.runner.runChanger(sq.delete_subobjectives())
        self.runner.runChanger(sq.delete_objectives())
        self.runner.runChanger(sq.delete_courses())
        self.runner.runChanger(sq.delete_programs())
        self.runner.runChanger(sq.delete_faculty())
        self.runner.runChanger(sq.delete_departments())
    def reset_tables(self):
        self.delete_all_tables()
        self.create_all_tables()

    def get_all_departments(self):
        return self.runner.runSelect(sq.get_all_departments())
    def get_all_faculty(self):
        return self.runner.runSelect(sq.get_all_faculty())
    def get_all_programs(self):
        return self.runner.runSelect(sq.get_all_programs())
    def get_all_courses(self):
        return self.runner.runSelect(sq.get_all_courses())
    def get_all_objectives(self):
        return self.runner.runSelect(sq.get_all_objectives())
    def get_all_subobjectives(self):
        return self.runner.runSelect(sq.get_all_subobjectives())
    def get_all_objective_assignments(self):
        return self.runner.runSelect(sq.get_all_objective_assignments())
    def get_all_sections(self):
        return self.runner.runSelect(sq.get_all_sections())
    def get_all_course_assignments(self):
        return self.runner.runSelect(sq.get_all_course_assignments())
        
    def insert_department(self,dept_name,dept_code):
        self.runner.runChanger(sq.insert_department(dept_name,dept_code))
    def insert_faculty(self,name,email,fac_rank,dept_code):
        self.runner.runChanger(sq.insert_faculty(name,email,fac_rank,dept_code))
    def insert_program(self,name,dept_code,head_id):
        self.runner.runChanger(sq.insert_program(name,dept_code,head_id))
    def insert_course(self,id,dept_id,title,description):
        self.runner.runChanger(sq.insert_course(id,dept_id,title,description))
    def insert_objective(self,description):
        self.runner.runChanger(sq.insert_objective(description))
    def insert_subobjective(self,obj_id,sub_id,desc):
        self.runner.runChanger(sq.insert_subobjective(obj_id,sub_id,desc))
    def insert_objective_assignment(self,obj_id,sub_obj_id,section_id,course_id,dept_id,evaluation,semester,year,num_passed,num_failed):
        self.runner.runChanger(sq.insert_objective_assignment(obj_id,sub_obj_id,section_id,course_id,dept_id,evaluation,semester,year,num_passed,num_failed))
    def insert_section(self,id,course_id,dept_id,num_students,semester,teacher_id,year):
        self.runner.runChanger(sq.insert_section(id,course_id,dept_id,num_students,semester,teacher_id,year))
    def insert_course_assignment(self,course_id,dept_id,program_name,course_dept):
        self.runner.runChanger(sq.insert_course_assignment(course_id,dept_id,program_name,course_dept))
    
    
    