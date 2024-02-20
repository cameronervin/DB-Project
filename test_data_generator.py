from sqlconnector import SqlQueryRunner
from sql_queries import SQLQueries as sq

runner = SqlQueryRunner(suppress_output=True)

class DataGen:
    @staticmethod
    def populate_departments():
        vals = [("Computer Science","CS"),
            ("Math","MATH"),
            ("Finance","FIN"),
            ("Art History","ARHS")]
        for v in vals:
            runner.runChanger(sq.insert_department(*v))

    @staticmethod
    def populate_faculty():
        vals = [("Dr. Lin","dlin@smu.edu","Full","CS"),
            ("Dr. Alford","galford@smu.edu","Full","CS"),
            ("Dr. Doe","jdoe@smu.edu","Adjunct","MATH"),
            ("Dr. Doe","jdoe23@smu.edu","Full","MATH"),
            ("Dr. Larson","elarson@smu.edu","Full","FIN"),
            ("Dr. Larson","elarson23@smu.edu","Adjunct","ARHS")]
        for v in vals:
            runner.runChanger(sq.insert_faculty(*v))

    @staticmethod
    def populate_programs():
        vals = [("MS","CS",1),
            ("BS","CS",2),
            ("BA","CS",2),
            ("PHD","MATH",4),
            ("BS","FIN",5),
            ("BA","ARHS",6)]
        for v in vals:
            runner.runChanger(sq.insert_program(*v))


    @staticmethod
    def populate_courses():
        vals = [("7330","CS","File Org & Database Management","Learn how to use a databse and sql and other useful things"),
            ("5330","CS","File Org & Database Management","Learn how to use a databse and sql and other useful things"),
            ("2341","CS","Data Structures","Learn how to use a cry and work through a mental breakdown"),
            ("1300","MATH","Calculus","Integrals and other fun things"),
            ("1300","FIN","Financial Accounting","Learn how to color inside the lines idk im not a finance major"),
            ("2340","ARHS","From Cavemen to Gladiators","Learn how to be a roman general and command the front lines")
        ]
        for v in vals:
            runner.runChanger(sq.insert_course(*v))
        

    @staticmethod
    def populate_objectives():
        vals = [
            "Presentation Skills",
            "Programming Skills",
            "Writing Good"
        ]
        for v in vals:
            runner.runChanger(sq.insert_objective(v))

    @staticmethod
    def populate_subobjectives():
        vals = [
            (1,1,"Students should be comfortable getting in front of the class to present"),
            (1,2,"Students should be able to create a slide deck with meaningful information"),
            (2,1,"Students should be able to code"),
            (2,2,"Students can write c++ code"),
            (2,3,"Students can write sql code"),
            (3,1,"Students can write essays")
        ]
        for v in vals:
            runner.runChanger(sq.insert_subobjective(*v))
        

    @staticmethod
    def populate_objective_assignments():
        #obj_id,sub_obj_id,section_id,course_id,dept_id,evaluation
        vals = [
            (1,1,"001","7330","CS","Group Presentation",23,20),
            (1,1,"001","5330","CS","Research Paper Presentation",130,4),
            (1,2,"001","7330","CS","Group Presentation",40,3),
            (2,1,"011","2341","CS","Programming Assignment",50,20),
            (1,2,"011","2340","ARHS","Presentation over Gladiators or something",250,50),
            (3,1,"011","2340","ARHS","In Class Essay 10 pages",270,30),
            (1,2,"011","1300","MATH","Make a slide deck of favorite math equations",3,1),
            (3,1,"011","1300","MATH","Essay about why math is great",2,2),
            (3,1,"011","1300","FIN","Essay about colors or something",10,9),
            (1,2,"011","1300","FIN","Presentation about your favorite color",14,5),
            (2,2,"001","2341","CS","C++ Programming assignment. Build a data structure",50,6)
        ]
        for v in vals:
            runner.runChanger(sq.insert_objective_assignment(*v))

    @staticmethod
    def populate_sections():
        vals = [
            ("001","7330","CS",43,"Fall",1,"2022"),
            ("002","7330","CS",15,"Spring",1,"2020"),
            ("001","5330","CS",134,"Fall",1,"2021"),
            ("002","5330","CS",6,"Spring",1,"2023"),
            ("001","2341","CS",56,"Spring",2,"2021"),
            ("011","2341","CS",70,"Spring",2,"2022"),
            ("011","1300","MATH",4,"Summer",4,"2023"),
            ("011","1300","FIN",19,"Summer",5,"2021"),
            ("011","2340","ARHS",300,"Summer",6,"2023")
        ]
        
        for v in vals:
            runner.runChanger(sq.insert_section(*v))
        
    @staticmethod
    def populate_course_assignments():
        vals = [
            ("1300","FIN","BS"),
            ("7330","CS","MS"),
            ("5330","CS","BS"),
            ("5330","CS","BA"),
            ("2341","CS","BS"),
            ("2341","CS","BA"),
            ("1300","MATH","PHD"),
            ("2340","ARHS","BA")
        ]
    
        for v in vals:
            runner.runChanger(sq.insert_course_assignment(*v))

    @staticmethod
    def populate_all():
        DataGen.populate_departments()
        DataGen.populate_faculty()
        DataGen.populate_programs()
        DataGen.populate_courses()
        DataGen.populate_objectives()
        DataGen.populate_subobjectives()
        DataGen.populate_sections()
        DataGen.populate_objective_assignments()
        DataGen.populate_course_assignments()

if __name__ == "__main__":
    # DataGen.populate_all()
    DataGen.populate_all()