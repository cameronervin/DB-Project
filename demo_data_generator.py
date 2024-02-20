from sqlconnector import SqlQueryRunner
from sql_queries import SQLQueries as sq
from dbinterface import Interface
runner = SqlQueryRunner(suppress_output=True)

class DataGen:
    @staticmethod
    def populate_departments():
        vals = [("Computer Science","COMP"),
            ("Basket Weaving","BSKW"),
            # ("Finance","FIN"),
            # ("Art History","ARHS")
            ]
        for v in vals:
            runner.runChanger(sq.insert_department(*v))

    @staticmethod
    def populate_faculty():
        # vals = [("Dr. Lin","dlin@smu.edu","Full","CS"),
        #     ("Dr. Alford","galford@smu.edu","Full","CS"),
        #     ("Dr. Doe","jdoe@smu.edu","Adjunct","MATH"),
        #     ("Dr. Doe","jdoe23@smu.edu","Full","MATH"),
        #     ("Dr. Larson","elarson@smu.edu","Full","FIN"),
        #     ("Dr. Larson","elarson23@smu.edu","Adjunct","ARHS")]
        # for v in vals:
        #     runner.runChanger(sq.insert_faculty(*v))
        cs_faculty = [
            ("Dr. Smith", "smith@smu.edu", "Full", "COMP"),
            ("Dr. Johnson", "johnson@smu.edu", "Associate", "COMP"),
            ("Dr. Alford", "galford@smu.edu", "Full", "COMP"),
            ("Dr. Kyle", "kyle@smu.edu", "Adjunct", "COMP"),
            ("Dr. Jenna", "jdenna@smu.edu", "Full", "COMP"),
            ("Dr. Larson", "elarson@smu.edu", "Full", "COMP"),
            ("Dr. Larson", "elarson23@smu.edu", "Adjunct", "COMP"),
            ("Dr. Coyle", "fcoyle5@smu.edu", "Full", "COMP"),
            ("Dr. Elizabeth", "eliz9@smu.edu", "Adjunct", "COMP"),
            ("Dr. Carly", "jcarly23@smu.edu", "Full", "COMP"),
            ("Dr. Jane", "jane2@smu.edu", "Adjunct", "COMP"),
            ("Dr. Hahsler", "hahsler@smu.edu", "Full", "COMP"),
        ]

        # Define Basket Weaving faculty data
        bskw_faculty = [
            ("Prof. Chandler", "chandlerb@smu.edu", "Full", "BSKW"),
            ("Prof. Rachel", "rachel@smu.edu", "Associate", "BSKW"),
            ("Prof. Monica", "monicab@smu.edu", "Full", "BSKW"),
            ("Prof. Ross", "ross12@smu.edu", "Adjunct", "BSKW"),
            ("Prof. Phoebe", "phobebb@smu.edu", "Full", "BSKW"),
            ("Prof. Joe", "joey@smu.edu", "Adjunct", "BSKW"),
        ]
        # Insert each faculty member into the database
        for faculty_member in cs_faculty + bskw_faculty:
            runner.runChanger(sq.insert_faculty(*faculty_member))

    @staticmethod
    def populate_programs():
        vals = [("BS","COMP",1),
            # ("BS","CS",2),
            # ("BA","CS",2),
            # ("PHD","MATH",4),
            # ("BS","FIN",5),
            ("BA","BSKW",14)]
        for v in vals:
            runner.runChanger(sq.insert_program(*v))


    @staticmethod
    def populate_courses():
        vals = [
            ("1000","COMP","CS1","Introduction to programming in Java"),
            ("1100","COMP","CS2","Programming concepts in C++"),
            ("1200","COMP","CS3","Object oriented and functional programming basics"),
            ("2000","COMP","Data Structures","Building basic data structures & optimization of them"),
            ("3000","COMP","Algorithims","Creation and optimization of advanced concepts in algorithm design/implementation"),

            ("1000","BSKW","Basics of Basket Weaving","Introduction to the process of creating a basket"),
            ("1010","BSKW","Baskets of the World","Discuss the coolest looking baskets ever woven"),
            ("2020","BSKW","History of Basket Weaving","History of the amazing process of weaving baskets"),
            ("3000","BSKW","Newtonian Physics as applied to basket weaving","Gettin real fancy with this one Dr. Lin... Application of physics to basket weaving"),
            
            ]
        for v in vals:
            runner.runChanger(sq.insert_course(*v))
        

    @staticmethod
    def populate_objectives():
        vals = [
            "Presentation Skills",
            "Programming Skills",
            "Writing Skills"
        ]
        for v in vals:
            runner.runChanger(sq.insert_objective(v))

    @staticmethod
    def populate_subobjectives():
        vals = [
            (1,0,"Presentation Skills"),
            (1,1,"Students should be comfortable getting in front of the class to present"),
            (1,2,"Students should be able to create a slide deck with meaningful information"),
            
            (2,0,"Programming Skills"),
            (2,1,"Students should be able to code"),
            (2,2,"Students can write c++ code"),
            (2,3,"Students can write java code"),
            
            (3,0,"Writing Skills"),
            (3,1,"Students can write essays"),
            (3,2,"Students can write Research Papers"),
        ]
        for v in vals:
            runner.runChanger(sq.insert_subobjective(*v))
        

    @staticmethod
    def populate_objective_assignments():
        #obj_id,sub_obj_id,section_id,course_id,dept_id,evaluation,num_passed,num_failed
        vals = [
            (1,1,"001","1000","BSKW","Group Presentation","Fall","2023",25,10),
            (1,1,"001","1000","BSKW","Group Presentation","Spring","2023",20,4),
            (1,1,"001","1000","BSKW","Group Presentation","Summer","2023",15,15),
            
            (1,1,"001","1010","BSKW","Group Presentation","Fall","2023",40,20),
            (1,1,"001","1010","BSKW","Group Presentation","Spring","2023",40,40),
            (1,1,"001","1010","BSKW","Group Presentation","Summer","2023",15,10),

            (1,1,"001","2020","BSKW","Group Presentation","Spring","2023",40,20),

            (1,1,"001","3000","BSKW","Group Presentation","Fall","2023",50,25),

            #COMP

            (1,1,"001","1000","COMP","Group Presentation","Fall","2023",10,15),
            (1,1,"001","1000","COMP","Group Presentation","Spring","2023",20,15),
            (1,2,"001","1000","COMP","Powerpoint Submission","Spring","2023",20,15),
            (2,1,"001","1000","COMP","Programming Assignment","Spring","2023",20,15),
            
            (2,1,"001","1100","COMP","Programming Assignment","Fall","2023",30,30),
            (2,1,"001","1100","COMP","Programming Assignment","Spring","2023",40,20),

            (2,1,"001","1200","COMP","Programming Assignment","Fall","2023",40,5),
            (2,1,"001","1200","COMP","Programming Assignment","Spring","2023",55,5),

            (2,1,"001","2000","COMP","Programming Assignment","Fall","2023",30,5),
            (2,1,"001","2000","COMP","Programming Assignment","Spring","2023",25,5),

            (2,1,"001","3000","COMP","Programming Assignment","Fall","2023",20,4),
            (2,1,"001","3000","COMP","Programming Assignment","Spring","2023",10,6),

            (1,1,"002","1000","COMP","Group Presentation","Fall","2023",10,10),
            (1,1,"002","1000","COMP","Group Presentation","Spring","2023",15,15),
            (1,2,"002","1000","COMP","Powerpoint Submission","Spring","2023",20,10),
            (2,1,"002","1000","COMP","Programming Assignment","Spring","2023",25,5),

            (2,1,"002","1100","COMP","Programming Assignment","Fall","2023",50,25),
            (2,1,"002","1100","COMP","Programming Assignment","Spring","2023",40,15),

            (2,1,"002","1200","COMP","Programming Assignment","Fall","2023",39,1),
            (2,1,"002","1200","COMP","Programming Assignment","Spring","2023",47,3),


        ]
        for v in vals:
            runner.runChanger(sq.insert_objective_assignment(*v))

    @staticmethod
    def populate_sections():
        vals = [
            #COMP
            ("001","1000","COMP",25,"Fall",1,"2023"),
            ("002","1000","COMP",20,"Fall",1,"2023"),
            
            ("001","1000","COMP",35,"Spring",1,"2023"),
            ("002","1000","COMP",30,"Spring",1,"2023"),

            ("001","1100","COMP",60,"Spring",3,"2023"),
            ("002","1100","COMP",55,"Spring",3,"2023"),

            ("001","1100","COMP",60,"Fall",3,"2023"),
            ("002","1100","COMP",75,"Fall",3,"2023"),

            ("001","1200","COMP",45,"Fall",6,"2023"),
            ("002","1200","COMP",40,"Fall",6,"2023"),

            ("001","1200","COMP",60,"Spring",6,"2023"),
            ("002","1200","COMP",50,"Spring",6,"2023"),

            ("001","2000","COMP",30,"Spring",12,"2023"),
            ("001","2000","COMP",35,"Fall",12,"2023"),

            ("001","3000","COMP",16,"Spring",1,"2023"),
            ("001","3000","COMP",24,"Fall",1,"2023"),

            #BSKW
            ("001","1000","BSKW",24,"Spring",13,"2023"),
            ("001","1000","BSKW",30,"Summer",13,"2023"),
            ("001","1000","BSKW",35,"Fall",13,"2023"),
            
            ("001","1010","BSKW",80,"Spring",18,"2023"),
            ("001","1010","BSKW",25,"Summer",18,"2023"),
            ("001","1010","BSKW",60,"Fall",18,"2023"),
            
            ("001","2020","BSKW",60,"Spring",17,"2023"),
            ("001","3000","BSKW",75,"Fall",17,"2023"),
            

            
        ]
        
        for v in vals:
            runner.runChanger(sq.insert_section(*v))
        
    @staticmethod
    def populate_course_assignments():
        vals = [
            ("1000","COMP","BS","COMP"),
            ("1100","COMP","BS","COMP"),
            ("1200","COMP","BS","COMP"),
            ("2000","COMP","BS","COMP"),
            ("3000","COMP","BS","COMP"),
            
            ("1000","BSKW","BA","BSKW"),
            ("1010","BSKW","BA","BSKW"),
            ("2020","BSKW","BA","BSKW"),
            ("3000","BSKW","BA","BSKW"),
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
    inf = Interface()
    inf.reset_tables()
    DataGen.populate_departments()
    DataGen.populate_faculty()
    DataGen.populate_programs()
    DataGen.populate_courses()
    DataGen.populate_objectives()
    DataGen.populate_subobjectives()
    DataGen.populate_sections()
    DataGen.populate_objective_assignments()
    DataGen.populate_course_assignments()

    