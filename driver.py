import pandas as pd
import numpy as np
import pprint 
from datetime import date
from dbinterface import Interface
from demo_data_generator import DataGen
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

"""
REQUIRED PACKAGES (can be installed with pip IE. `pip install <package_name>`):
    pymysql
    pandas
    numpy
    python-dotenv
    tkinter
"""

def convert_df_to_text(df:pd.DataFrame):
    # width = max([len(c) for c in df.columns])

    vals = ""
    # for index, row in df.iterrows():
    #     _width = max([len(row[c]) for c in df.columns if isinstance(row[c],str)])
    #     if _width > width:
    #         width = _width
    widths = []

    for c in df.columns:
        widths.append(max([len(row[c]) for _,row in df.iterrows() if isinstance(row[c],str)] + [len(c)]))
    for index, row in df.iterrows():
        _vals = [f'{row[c]:<{widths[i]}}' for i,c in enumerate(df.columns)]
        vals += '\n'
        vals += '|'.join(_vals)
    
    _str = [f"{c.upper(): ^{widths[i]}s}" for i,c in enumerate(df.columns)]
    _str = '|'.join(_str)

    _str += '\n'
    for i in range(len(df.columns)):
        _str += '-' * widths[i]
    _str += '-' * len(df.columns)
    _str += vals
    
    return _str

def insert_break_to_txt(txt:str):
    _txt = '\n\n'
    _txt += '=' * ((max([len(v) for v in txt.split('\n')])) + 1)
    _txt += '\n\n'
    return _txt

def clear_and_set_text(txt_area:scrolledtext.ScrolledText,new_text:str):
    txt_area.configure(state='normal')
    txt_area.delete('1.0',tk.END)
    txt_area.insert(tk.INSERT,new_text)
    txt_area.configure(state='disabled')

def clear_all_widgets(wid):
    for v in  wid.winfo_children():
        v.destroy()

FONT = 'TkFixedFont' 

# wigits
class ProgramRunner: #TODO Move wigits to global variable
    def __init__(self):
        self.interface = Interface()
    def run(self):
        self.interface.reset_tables()
        DataGen.populate_all()
        # print(self.interface.get_all_courses())

    def handle_add_department_press(self):
        print('Add Department Button was Pressed')
        clear_all_widgets(config_frame)
        dept_name_label = tk.Label(config_frame,text='Department Name:')
        dept_code_label = tk.Label(config_frame,text='Department Code:')

        dept_name_var = tk.StringVar()
        dept_code_var = tk.StringVar()

        dept_name_entry = tk.Entry(config_frame,textvariable=dept_name_var,font=FONT)
        dept_code_entry = tk.Entry(config_frame,textvariable=dept_code_var,width=4,font=FONT)

        def handle_submit():
            depts = self.interface.get_all_departments()
            if not dept_name_var.get():
                clear_and_set_text(result_text,"Please input a Department Name")

            elif not dept_code_var.get():
                clear_and_set_text(result_text,"Please input a Department Code")

            elif len(dept_code_var.get()) > 4:
                clear_and_set_text(result_text,"Department codes must be 4 or fewer characters")

            elif dept_name_var.get().lower() in [d.lower() for d in depts['dept_name']]:
                clear_and_set_text(result_text,f"{dept_name_var.get()} department name already exists, please enter a unique name")

            elif dept_code_var.get().lower() in [d.lower() for d in depts['dept_code']]:
                clear_and_set_text(result_text,f"{dept_code_var.get()} department code already exists, please enter a unique name")

            else:
                self.interface.insert_department(dept_name_var.get(),dept_code_var.get().upper())
                clear_and_set_text(result_text,f"Added new department with\n\tname: {dept_name_var.get()}\n\tcode: {dept_code_var.get().upper()}")
                

        submit = tk.Button(config_frame,text='Submit',command=handle_submit)
        wigits = [dept_name_label,dept_name_entry,dept_code_label,dept_code_entry,submit]

        for i,w in enumerate(wigits):
            w.grid(row=0,column=i)


        # clear_and_set_text(result_text,'Add department button was pressed')

    def handle_add_faculty_press(self): 
        print('Add Faculty Button was Pressed')
        clear_all_widgets(config_frame)
        # clear_and_set_text(result_text,'Add Faculty Button was Pressed')
        name_var = tk.StringVar()
        email_var = tk.StringVar()
        rank_var = tk.StringVar()
        dept_code_var = tk.StringVar()

        widgets = []
        widgets.append(tk.Label(config_frame,text='Name:'))
        widgets.append(tk.Entry(config_frame,textvariable=name_var,font=FONT))

        widgets.append(tk.Label(config_frame,text='Email:'))
        widgets.append(tk.Entry(config_frame,textvariable=email_var,font=FONT))

        options = [
            'Full',
            'Associate',
            'Assistant',
            'Adjunct'
        ]

        widgets.append(tk.Label(config_frame,text='Rank:'))
        widgets.append(tk.OptionMenu(config_frame,rank_var,*options))
        
        options2 = self.interface.get_all_departments()['dept_code']


        widgets.append(tk.Label(config_frame,text='Department Code:'))
        widgets.append(tk.OptionMenu(config_frame,dept_code_var,*options2))

        


        def handle_submit():
            facs = self.interface.get_all_faculty()
            print({e.lower() for e in facs['email']})
            email_endings = (
                '.com',
                '.net',
                '.edu',
                '.gov',
                '.org'
            )
            if not name_var.get():
                clear_and_set_text(result_text,"Please enter a name")
            elif not email_var.get():
                clear_and_set_text(result_text,"Please enter an email address")
            elif not rank_var.get():
                clear_and_set_text(result_text,"Please select a rank for the faculty member")
            elif not dept_code_var.get():
                clear_and_set_text(result_text,"Please select a department for the professor")
            elif not email_var.get().endswith(email_endings):
                clear_and_set_text(result_text,"Email address extension is invalid. Supported vals are:\n\t" + "\n\t".join(email_endings))
            elif '@' not in email_var.get():
                clear_and_set_text(result_text,'Must have an @ sign in the email address')
            elif email_var.get().lower() in {e.lower() for e in facs['email']}:
                clear_and_set_text(result_text,f"'{email_var.get()}' already exists, must be a unique email address")
            elif ' ' in email_var.get():
                clear_and_set_text(result_text,"Spaces are invalid in an email address, replace with an '_' if needed")
            else:
                self.interface.insert_faculty(name_var.get(),email_var.get(),rank_var.get(),dept_code_var.get())
                clear_and_set_text(result_text,f"Added Faculty with: \n\tName: {name_var.get()}\n\tEmail: {email_var.get()}\n\tRank: {rank_var.get()}\n\tDepartment: {dept_code_var.get()}")
                
        widgets.append(tk.Button(config_frame,text='Submit',command=handle_submit))

        for i,w in enumerate(widgets):
            w.grid(row=0,column=i)

    def handle_add_program_press(self):
        print('Add Program Button was Pressed')
        clear_all_widgets(config_frame)
        # clear_and_set_text(result_text,'Add Program Button was Pressed')
        facs = self.interface.get_all_faculty()

        deg_type_var = tk.StringVar()
        dept_code_var = tk.StringVar()
        dept_head_var = tk.StringVar()

        dept_code_options = self.interface.get_all_departments()['dept_code']
        deg_type_options = [
            'BS',
            'BA',
            'BFA',
            'MS',
            'MBA',
            'MFA',
            'MA',
            'PHD'

        ]

        dept_head_options = []
        dept_head_mapper = {}
        for _,r in facs.iterrows():
            _str = f'{r["name"]} | {r["dept_code"]} | {r["fac_rank"]}'
            dept_head_options.append(_str)
            dept_head_mapper[_str] = r['id']

        wigits = []
        wigits.append(tk.Label(config_frame,text='Degree Type:'))
        wigits.append(tk.OptionMenu(config_frame,deg_type_var,*deg_type_options))
        wigits.append(tk.Label(config_frame,text='Department Code:'))
        wigits.append(tk.OptionMenu(config_frame,dept_code_var,*dept_code_options))
        wigits.append(tk.Label(config_frame,text='Department Head:'))
        wigits.append(tk.OptionMenu(config_frame,dept_head_var,*dept_head_options))

        def handle_submit():
            progs = self.interface.get_all_programs()
            if not deg_type_var.get():
                clear_and_set_text(result_text,"Please select a degree type")
            elif not dept_code_var.get():
                clear_and_set_text(result_text,"Please select a Department for the program")
            elif not dept_head_var.get():
                clear_and_set_text(result_text,"Please select a head of the department")
            elif len(progs[(progs["name"] == deg_type_var.get()) & (progs["dept_code"] == dept_code_var.get())]) != 0:
                clear_and_set_text(result_text,"That program alredy exists")
            else:
                # clear_and_set_text(result_text,"Passed")
                self.interface.insert_program(deg_type_var.get(),dept_code_var.get(),dept_head_mapper[dept_head_var.get()])
                clear_and_set_text(result_text,f"Inserted Program with:\n\tDegree Type: {deg_type_var.get()}\n\tDepartment Code: {dept_code_var.get()}\n\tDepartment Head: {dept_head_var.get()}")
                
        wigits.append(tk.Button(config_frame,text='Submit',command=handle_submit))

        for i,w in enumerate(wigits):
            w.grid(row=0,column=i)
        
        

    def handle_add_course_press(self):
        print('Add Course Button was Pressed')
        clear_all_widgets(config_frame)
        # clear_and_set_text(result_text,'Add Course Button was Pressed')
        code_var = tk.StringVar()
        dept_code_var = tk.StringVar()
        title_var = tk.StringVar()
        # desc_var = tk.StringVar()


        depts = self.interface.get_all_departments()
        dept_code_options = depts['dept_code']


        wigits = []
        wigits.append(tk.Label(config_frame,text='Course Code:'))
        wigits.append(tk.Entry(config_frame,textvariable=code_var,width=4,font=FONT))
        wigits.append(tk.Label(config_frame,text='Department Code:'))
        wigits.append(tk.OptionMenu(config_frame,dept_code_var,*dept_code_options))
        wigits.append(tk.Label(config_frame,text='Course Title:'))
        wigits.append(tk.Entry(config_frame,textvariable=title_var,font=FONT))
        wigits.append(tk.Label(config_frame,text='Course Description:'))
        desc_box = scrolledtext.ScrolledText(config_frame,height=4,width=50)
        wigits.append(desc_box)
        # tk.Text(config_frame,)
        def handle_submit():
            courses = self.interface.get_all_courses()
            desc_text = desc_box.get('1.0',tk.END).strip()
            # print(desc_text,len(desc_text))
            if not code_var.get():
                clear_and_set_text(result_text,"Please enter a 4 digit course code")
            elif not dept_code_var.get():
                clear_and_set_text(result_text,"Please select a department code")
            elif not title_var.get():
                clear_and_set_text(result_text,"Please enter a course title")
            elif  len(desc_text) == 0: 
                clear_and_set_text(result_text,"Please enter a course description up to 255 characters")
            elif len(code_var.get()) != 4 or not code_var.get().isnumeric():
                clear_and_set_text(result_text,"Course code must be a 4 digit code. IE. 5330")
            elif len(desc_text) > 255:
                clear_and_set_text(result_text,f"Nice try Dr. Lin. Course description must be 255 characters or less. Current description is {len(desc_text)}")
            elif len(courses[(courses['id'] == code_var.get()) & (courses['dept_id'] == dept_code_var.get())]) != 0:
                clear_and_set_text(result_text,"That course already exists")
            else:
                # clear_and_set_text(result_text,"Passed")
                self.interface.insert_course(code_var.get(),dept_code_var.get(),title_var.get(),desc_text)
                clear_and_set_text(result_text,f"Inserted course with:\n\tCourse Code: {code_var.get()}\n\tDepartment: {dept_code_var.get()}\n\tTitle: {title_var.get()}\n\tDescription: {desc_text}")
            
        wigits.append(tk.Button(config_frame,text='Submit',command=handle_submit))

        for i,w in enumerate(wigits):
            w.grid(row=0,column=i,sticky='n')


    def handle_add_section_press(self): #TODO: Fix primary key to look at semester and year
        print('Add Section Button was Pressed')
        clear_all_widgets(config_frame)
        # clear_and_set_text(result_text,'Add Section Button was Pressed')
        section_id_var = tk.StringVar()
        course_id_var = tk.StringVar()
        dept_code_var = tk.StringVar()
        num_students_var = tk.StringVar()
        semester_var = tk.StringVar()
        professor_var = tk.StringVar()
        year_var = tk.StringVar()

        curr_dept = None

        depts = self.interface.get_all_departments()
        courses = self.interface.get_all_courses()
        facs = self.interface.get_all_faculty()

        dept_code_options = depts['dept_code']
        adv_options = {'display':False}

        prof_options = []
        prof_mapper = {}
        for _,r in facs.iterrows():
            _str = f'{r["name"]} | {r["email"]}'
            prof_options.append(_str)
            prof_mapper[_str] = r['id']
        
        def handle_submit():
            sections = self.interface.get_all_sections()
            if not section_id_var.get():
                clear_and_set_text(result_text,"Please enter a section number from 000-999")
            elif not course_id_var.get():
                clear_and_set_text(result_text,'Pleaset select a course id')
            elif not dept_code_var.get():
                clear_and_set_text(result_text,'Please select a department code')
            elif not num_students_var.get():
                clear_and_set_text(result_text,'Please enter the number of students in the section')
            elif not semester_var.get():
                clear_and_set_text(result_text,'Please select a semester')
            elif not professor_var.get():
                clear_and_set_text(result_text,'Please select a professor')
            elif not year_var.get():
                clear_and_set_text(result_text,'Please enter a year')
            elif not section_id_var.get().isnumeric() or len(section_id_var.get()) != 3:
                clear_and_set_text(result_text,'Invalid section id, valid ids are between 000-999')
            elif not num_students_var.get().isnumeric() or int(num_students_var.get()) < 0:
                clear_and_set_text(result_text,'Please enter a positive number for the number of students')
            elif not year_var.get().isnumeric() or len(year_var.get()) != 4 or int(year_var.get()) < 0:
                clear_and_set_text(result_text,'Please enter a valid year')
            elif len(sections[(sections['id'] == section_id_var.get()) & (sections['course_id'] == course_id_var.get()) & (sections['dept_id'] == dept_code_var.get()) & (sections['semester'] == semester_var.get()) & (sections['year'] == int(year_var.get()))]) != 0:
                clear_and_set_text(result_text,'That section already exists')
            else:
                # clear_and_set_text(result_text,'valid')
                self.interface.insert_section(
                    section_id_var.get(),
                    course_id_var.get(),
                    dept_code_var.get(),
                    int(num_students_var.get()),
                    semester_var.get(),
                    prof_mapper[professor_var.get()],
                    year_var.get()
                    

                )
                clear_and_set_text(result_text,f"""Inserted section with:
    Section Id: {section_id_var.get()}
    Course ID: {course_id_var.get()}
    Department: {dept_code_var.get()}
    Num Students: {num_students_var.get()}
    Semester: {semester_var.get()}
    Professor: {professor_var.get()}
    Year: {year_var.get()}""")
                
        def handle_dept_selection(sel:str):
            if adv_options['display']:
                for w in adv_wigits:
                    w.destroy()
                section_id_var.set('')
                course_id_var.set('')
            course_id_options = courses[courses['dept_id'] == sel]['id']
            
            if len(course_id_options) == 0:
                clear_and_set_text(result_text,f"No Courses exist yet for {sel}... Taking you to add course page now...")
                self.handle_add_course_press()
                return
            semester_options = [
                'Spring',
                'Summer',
                'Fall'
            ]

            

            adv_wigits.clear()
            adv_wigits.append(tk.Label(config_frame,text='Section Code:'))
            adv_wigits.append(tk.Entry(config_frame,textvariable=section_id_var,width=4,font=FONT))
            adv_wigits.append(tk.Label(config_frame,text='Course Code:'))
            adv_wigits.append(tk.OptionMenu(config_frame,course_id_var,*course_id_options))
            adv_wigits.append(tk.Label(config_frame,text='Number of Students:'))
            adv_wigits.append(tk.Entry(config_frame,textvariable=num_students_var,width=4,font=FONT))
            adv_wigits.append(tk.Label(config_frame,text='Professor:'))
            adv_wigits.append(tk.OptionMenu(config_frame,professor_var,*prof_options))
            adv_wigits.append(tk.Label(config_frame,text='Semester:'))
            adv_wigits.append(tk.OptionMenu(config_frame,semester_var,*semester_options))
            adv_wigits.append(tk.Label(config_frame,text='Year:'))
            adv_wigits.append(tk.Entry(config_frame,textvariable=year_var,width=4,font=FONT))
            adv_wigits.append(tk.Button(config_frame,text='Submit',command=handle_submit))
            adv_options['display']= True
            for i,w in enumerate(adv_wigits):
                w.grid(row=0,column=i + len(basic_wigits))

        adv_wigits = []
        basic_wigits = []
        basic_wigits.append(tk.Label(config_frame,text='Department'))
        basic_wigits.append(tk.OptionMenu(config_frame,dept_code_var,*dept_code_options,command=handle_dept_selection))


        for i,w in enumerate(basic_wigits):
            w.grid(row=0,column=i)


        # tk.OptionMenu(command)

    def handle_add_objective_press(self):
        print('Add Objective Button was Pressed')
        clear_all_widgets(config_frame)
        clear_and_set_text(result_text,'Add Objective Button was Pressed')

        desc_var = tk.StringVar()

        widgets = []
        widgets.append(tk.Label(config_frame,text='Objective Description:'))
        desc_box = scrolledtext.ScrolledText(config_frame,height=4,width=50)
        widgets.append(desc_box)

        def handle_submit():
            objs = self.interface.get_all_objectives()
            sub_objs = self.interface.get_all_subobjectives()
            desc_text = desc_box.get('1.0',tk.END).strip()

            if not len(desc_text) <= 255:
                clear_and_set_text(result_text,"Descriptions must be less than 255 characters")
            elif len(desc_text) == 0:
                clear_and_set_text(result_text,"Please input a description")
            else:
                self.interface.insert_objective(desc_text)
                clear_and_set_text(result_text,f"Added new objective with\n\tdescription: {desc_text}\n\nCreating base Sub-Objective with ID = 0")
                subs = self.interface.get_all_subobjectives()
                # max + 1 so it references the correct id
                if len(subs[subs["objective_id"] == objs['id'].max()+1]) != 0:
                    clear_and_set_text(result_text,"Base sub-objective ID already created")
                else:
                    self.interface.insert_subobjective(objs['id'].max()+1,0,desc_text)

        widgets.append(tk.Button(config_frame,text='Submit',command=handle_submit))
        
        for i,w in enumerate(widgets):
            w.grid(row=0,column=i)


    def handle_add_subobjective_press(self):
        print('Add Sub-Objective Button was Pressed')
        clear_all_widgets(config_frame)
        clear_and_set_text(result_text,'Add Sub-Objective Button was Pressed')
        
        obj_id_var = tk.StringVar()
        desc_var = tk.StringVar()
        objs = self.interface.get_all_objectives()

        obj_mapper = {d:_id for d,_id in zip(objs['description'],objs['id'])}

        widgets = []
        widgets.append(tk.Label(config_frame,text='Objective:'))

        # widgets.append(tk.Entry(config_frame,textvariable=obj_id_var))
        widgets.append(tk.OptionMenu(config_frame,obj_id_var,*obj_mapper.keys()))
        widgets.append(tk.Label(config_frame,text='Sub-Objective Description:'))
        desc_box = scrolledtext.ScrolledText(config_frame,height=4,width=50)
        widgets.append(desc_box)

        def handle_submit():
            
            desc_text = desc_box.get('1.0',tk.END).strip()
            if not obj_id_var.get():
                clear_and_set_text(result_text,"Please select an objective")
            elif len(desc_text) == 0:
                clear_and_set_text(result_text,"Please input sub-objective description")
            elif not len(desc_text) <= 255:
                clear_and_set_text(result_text,"Descriptions must be 255 characters or less")
            else:
                subs = self.interface.get_all_subobjectives()
                
                filtered_subs = subs[subs['objective_id'] == obj_mapper[obj_id_var.get()]]
                sub_obj_id = filtered_subs['sub_id'].max() + 1

                self.interface.insert_subobjective(obj_mapper[obj_id_var.get()],sub_obj_id,desc_text)
                clear_and_set_text(result_text,f"Added Sub-Objective with: \n\tObjective ID: {obj_id_var.get()}\n\tSubobjective ID: {sub_obj_id}\n\tDescription: {desc_text}")
                
        widgets.append(tk.Button(config_frame,text='Submit',command=handle_submit))

        for i,w in enumerate(widgets):
            w.grid(row=0,column=i)                

    def handle_assign_lo_press(self):
        print('Assign Learning Objective button was Pressed')
        clear_all_widgets(config_frame)
        # clear_and_set_text(result_text,'Assign Learning Objective button was Pressed')
        sub_objs = self.interface.get_all_subobjectives()
        sects = self.interface.get_all_sections()
        objs = self.interface.get_all_objectives()
        depts = self.interface.get_all_departments()
        courses = self.interface.get_all_courses()

        obj_var = tk.StringVar()
        sub_obj_var = tk.StringVar()
        sect_var = tk.StringVar()
        course_var = tk.StringVar()
        dept_var = tk.StringVar()
        eval_var = tk.StringVar()
        num_passed_var = tk.StringVar()
        num_failed_var = tk.StringVar()
        semester_var = tk.StringVar()
        year_var = tk.StringVar()


        obj_mapper = {d:_id for d,_id in zip(objs['description'],objs['id'])}
        wigits = []
        wigits_1 = []
        wigits_2 = []
        wigits_3 = []
        inner_wigits =[]

        
        
        def handle_time_selection(sel):
            for w in wigits_1 + wigits_2 + wigits_3:
                w.destroy()
            wigits_1.clear()
            wigits_2.clear()
            wigits_3.clear()

            sect_var.set("")
            if obj_var.get() and dept_var.get() and course_var.get() and semester_var.get() and year_var.get():
                
                filtered_subs = sub_objs[sub_objs['objective_id'] == obj_mapper[obj_var.get()]]
                sub_obj_mapper = {d:_id for d,_id in zip(filtered_subs['description'],filtered_subs['sub_id'])}
                
                wigits_1.append(tk.Label(config_frame,text='Section:'))
                wigits_1.append(tk.OptionMenu(config_frame,sect_var,*sects[(sects['course_id'] == course_var.get()) & (sects['dept_id'] == dept_var.get()) & (sects['year'] == int(year_var.get())) & (sects['semester'] == semester_var.get())]['id']))

                wigits_2.append(tk.Label(config_frame,text='Sub-Objective:'))
                wigits_2.append(tk.OptionMenu(config_frame,sub_obj_var,*sub_obj_mapper.keys()))

                def handle_submit():
                    oas = self.interface.get_all_objective_assignments()
                    num_students_sum = sects[(sects['id'] == sect_var.get()) & (sects['course_id'] == course_var.get()) & (sects['dept_id'] == dept_var.get())]
                    if len(num_students_sum) !=0:
                        num_students_sum = num_students_sum.iloc[0]['num_students']
                    else:
                        num_students_sum = -1
                    if not obj_var.get():
                        clear_and_set_text(result_text,"Please select an objective")
                    elif not sub_obj_var.get():
                        clear_and_set_text(result_text,"Please select a sub objective")
                    elif not sect_var.get():
                        clear_and_set_text(result_text,"Please select a section")
                    elif not course_var.get():
                        clear_and_set_text(result_text,"Please select a course")
                    elif not dept_var.get():
                        clear_and_set_text(result_text,"Please select a department")
                    elif not eval_var.get():
                        clear_and_set_text(result_text,"Please enter an evaluation")
                    elif not num_passed_var.get():
                        clear_and_set_text(result_text,"Please enter the number of students who passed")
                    elif not num_failed_var.get():
                        clear_and_set_text(result_text,"Please enter the number of students who failed the objective")
                    elif not num_passed_var.get().isnumeric():
                        clear_and_set_text(result_text,"Num Passed must be a number")
                    elif not num_failed_var.get().isnumeric():
                        clear_and_set_text(result_text,"Num Failed must be a number")
                    elif '.' in num_passed_var.get() or '-' in num_passed_var.get():
                        clear_and_set_text(result_text,"Num passed must be a positive integer")
                    elif '.' in num_failed_var.get() or '-' in num_passed_var.get():
                        clear_and_set_text(result_text,"Num failed must be a positive integer")
                    elif int(num_failed_var.get()) + int(num_passed_var.get()) != num_students_sum:
                        clear_and_set_text(result_text,f"Num passed and num failed are not possible given the number of students= {num_students_sum}")
                    elif len(eval_var.get()) > 255:
                        clear_and_set_text(result_text,f"Eval must be 255 characters or less, current length is {len(eval_var.get())}")
                    elif len(oas[(oas['obj_id'] == obj_mapper[obj_var.get()]) & (oas['sub_obj_id'] == sub_obj_mapper[sub_obj_var.get()]) & (oas['section_id'] == sect_var.get()) & (oas['course_id'] == course_var.get()) & (oas['dept_id'] == dept_var.get()) & (oas['semester'] == semester_var.get()) & (oas['year'] == int(year_var.get()))]) !=0:
                        clear_and_set_text(result_text,"That objective has already been asigned to that section, please select a unique assignment")
                    else:
                        self.interface.insert_objective_assignment(obj_mapper[obj_var.get()],sub_obj_mapper[sub_obj_var.get()],sect_var.get(),course_var.get(),dept_var.get(),eval_var.get(),semester_var.get(),year_var.get(),int(num_passed_var.get()),int(num_failed_var.get()))
                        clear_and_set_text(result_text,"Inserted Objective assignment")
                    

                wigits_3.append(tk.Label(config_frame,text='Evaluation:'))
                wigits_3.append(tk.Entry(config_frame,textvariable=eval_var,font=FONT,width=50))
                wigits_3.append(tk.Label(config_frame,text='Num Passed:'))
                wigits_3.append(tk.Entry(config_frame,textvariable=num_passed_var,font=FONT,width=4))
                wigits_3.append(tk.Label(config_frame,text='Num Failed:'))
                wigits_3.append(tk.Entry(config_frame,textvariable=num_failed_var,font=FONT,width=4))
                wigits_3.append(tk.Button(config_frame,text='Submit',command=handle_submit))

                for i,w in enumerate(wigits_1):
                    w.grid(row=0,column=len(inner_wigits) + len(wigits) + i)
                for i,w in enumerate(wigits_2):
                    w.grid(row=2,column=i,sticky='ew')
                for i,w in enumerate(wigits_3):
                    w.grid(row=4,column=i,sticky='ew')


        def handle_year_selection(sel):
            _sects = sects[(sects['dept_id'] == dept_var.get()) & (sects['course_id'] == course_var.get()) & (sects['year'] == int(year_var.get()))]

            print(_sects.dtypes)
            inner_wigits.append(tk.Label(config_frame,text="Semester"))
            inner_wigits.append(tk.OptionMenu(config_frame,semester_var,*np.unique(_sects['semester']),command=handle_time_selection))
            for i,w in enumerate(inner_wigits[-2:]):
                w.grid(row=0,column=i + 8)

        def handle_course_selection(sel):
            year_var.set("")
            semester_var.set("")
            _sects = sects[(sects['dept_id'] == dept_var.get()) & (sects['course_id'] == course_var.get())]
            if len(_sects) == 0:
                clear_and_set_text(result_text,"No sections for this course exist. Taking you there to create one now.")
                self.handle_add_section_press()
            else:
                inner_wigits.append(tk.Label(config_frame,text="Year"))
                inner_wigits.append(tk.OptionMenu(config_frame,year_var,*np.unique(_sects['year']),command=handle_year_selection))
                for i,w in enumerate(inner_wigits[-2:]):
                    w.grid(row=0,column=i + 6)

        def handle_obj_dept_selected(sel):
            if obj_var.get() and dept_var.get():
                course_var.set("")
                sect_var.set("")
                year_var.set("")
                semester_var.set("")

                for w in wigits_2 + wigits_3 + wigits_1 + inner_wigits:
                    w.destroy()
                wigits_2.clear()
                wigits_3.clear()
                wigits_1.clear()
                inner_wigits.clear()
                
                inner_wigits.append(tk.Label(config_frame,text='Course:'))
                inner_wigits.append(tk.OptionMenu(config_frame,course_var,*courses[courses['dept_id'] == dept_var.get()]['id'],command=handle_course_selection))
                # inner_wigits.append(tk.Label(config_frame,text='Semester'))

                for i,w in enumerate(inner_wigits):
                    w.grid(row=0,column=i + len(wigits),sticky='ew')

                

        wigits.append(tk.Label(config_frame,text='Objective:'))
        wigits.append(tk.OptionMenu(config_frame,obj_var,*obj_mapper.keys(),command=handle_obj_dept_selected))
        wigits.append(tk.Label(config_frame,text='Department:'))
        wigits.append(tk.OptionMenu(config_frame,dept_var,*depts['dept_code'],command=handle_obj_dept_selected))

        for i,w in enumerate(wigits):
            w.grid(row=0,column=i,sticky='ew')

        

    def handle_assign_course_press(self):
        print('Assign Course button was Pressed')
        clear_all_widgets(config_frame)
        clear_and_set_text(result_text,'Assign Course button was Pressed')

        course_id_var = tk.StringVar()
        dept_id_var = tk.StringVar()
        prog_name_var = tk.StringVar()

        depts = self.interface.get_all_departments()
        courses = self.interface.get_all_courses()
        programs = self.interface.get_all_programs()
        wigits = []
        inner_wigits = []
        course_mapper = {f'{d}{num}':[d,num] for d,num in zip(courses['dept_id'],courses['id'])}

        def handle_submit():
            courses = self.interface.get_all_courses()
            depts = self.interface.get_all_departments()
            progs = self.interface.get_all_programs()
            cas = self.interface.get_all_course_assignments()

            if not course_id_var.get():
                clear_and_set_text(result_text,"Please input a Course ID")
            elif not dept_id_var.get():
                clear_and_set_text(result_text,"Please input a Department ID")
            elif not prog_name_var.get():
                clear_and_set_text(result_text,"Please input a Program Name")
            elif len(dept_id_var.get()) > 4:
                clear_and_set_text(result_text,"Department ID must be 4 characters or less")
            elif len(prog_name_var.get()) > 255:
                clear_and_set_text(result_text,"Program name must be 255 characters or less")
            elif dept_id_var.get().lower() not in [d.lower() for d in depts['dept_code']]:
                clear_and_set_text(result_text,f"{dept_id_var.get()} department ID does not exist, please enter a valid department ID")
            elif prog_name_var.get().lower() not in [p.lower() for p in progs['name']]:
                clear_and_set_text(result_text,f"{prog_name_var.get()} program name does not exist, please enter a valid program name")
            elif len(cas[(cas["course_id"] == course_mapper[course_id_var.get()][1]) & (cas["dept_id"] == dept_id_var.get()) & (cas["program_name"] == prog_name_var.get()) & (course_mapper[course_id_var.get()][0] == cas['course_dept'])]) != 0:
                clear_and_set_text(result_text,"That Course is already assigned")
            else:
                self.interface.insert_course_assignment(course_mapper[course_id_var.get()][1],dept_id_var.get(),prog_name_var.get(),course_mapper[course_id_var.get()][0])
                # self.interface.insert_course_assignment()
                clear_and_set_text(result_text,f"Assigned Course {course_id_var.get()} with: \n\tDepartment ID: {dept_id_var.get()}\n\tProgram Name: {prog_name_var.get()}")

        def handle_dept_selected(sel):
            # for w in inner_wigits:
            #     w.destroy()
            course_id_var.set("")
            prog_name_var.set("")
            inner_wigits.clear()
            inner_wigits.append(tk.Label(config_frame,text='Program:'))
            inner_wigits.append(tk.OptionMenu(config_frame,prog_name_var,*programs[programs['dept_code'] == dept_id_var.get()]['name']))
            inner_wigits.append(tk.Label(config_frame,text='Course:'))
            inner_wigits.append(tk.OptionMenu(config_frame,course_id_var,*course_mapper.keys()))
            inner_wigits.append(tk.Button(config_frame,text='Submit',command=handle_submit))
            for i,w in enumerate(inner_wigits):
                w.grid(row=0,column=len(wigits) + i)

        wigits.append(tk.Label(config_frame,text='Department'))
        wigits.append(tk.OptionMenu(config_frame,dept_id_var,*depts['dept_code'],command=handle_dept_selected))

        for i,w in enumerate(wigits):
            w.grid(row=0,column=i)

        # widgets = []
        # widgets.append(tk.Label(config_frame,text='Course ID:'))
        # widgets.append(tk.Entry(config_frame,textvariable=course_id_var))
        # widgets.append(tk.Label(config_frame,text='Program Name:'))
        # widgets.append(tk.Entry(config_frame,textvariable=prog_name_var))

       
                
        # widgets.append(tk.Button(config_frame,text='Submit',command=handle_submit))

        # for i,w in enumerate(widgets):
        #     w.grid(row=0,column=i)  

    def handle_show_programs_press(self):
        print("Show Programs Button was Pressed")
        clear_all_widgets(config_frame)
        # clear_and_set_text(result_text,convert_df_to_text(self.interface.get_all_courses()))
        dept_label = tk.Label(config_frame,text='Department:')
        dept_label.grid(row=0,column=0)
        dept_txt_var = tk.StringVar()
        options = self.interface.get_all_departments()['dept_name']
        dept_entry = tk.OptionMenu(config_frame,dept_txt_var,*options)
        dept_entry.grid(row=0,column=1,sticky='ew')

        def show_prog_submit():
            if dept_txt_var.get():
                depts = self.interface.get_all_departments()
                facs = self.interface.get_all_faculty()
                joined = depts.merge(facs,left_on='dept_code',right_on='dept_code')
                joined = joined[joined['dept_name'] == dept_txt_var.get()]
                
                progs = self.interface.get_all_programs()
                progs = progs.merge(facs,left_on='head_id',right_on='id',how='left')

                # print(progs.columns)
                progs = progs[['name_x','dept_code_x','name_y','email']]

                progs = progs.rename(columns={
                    'name_x':'Degree',
                    'dept_code_x':'Department',
                    'name_y':'Department Head'
                })

                progs['Department Head'] = progs['Department Head'].fillna('None Assigned')
                # progs = progs[progs['Department'] in joined['dept_code']]
                progs = progs.loc[progs['Department'].isin(joined['dept_code'])]
                # print(joined.columns)
                _txt = convert_df_to_text(joined.drop(['id','dept_code'],axis=1).rename(columns={
                    "dept_name":"Department",
                    'fac_rank':'Faculty Rank'
                }))
                _txt += insert_break_to_txt(_txt)
                _txt += convert_df_to_text(progs)
                
                clear_and_set_text(result_text,_txt)


                clear_all_widgets(config_frame)
            else:
                clear_and_set_text(result_text,"Please select a department")
        dept_submit = tk.Button(config_frame,text='Submit',command=show_prog_submit) #TODO: Assign command to this to submit it
        dept_submit.grid(row=0,column=2)
        # b = tk.Button(config_frame,text='hello world button')
        # b.grid(row=0,column=0)

    def handle_show_courses_press(self):
        print("Show Courses Button was Pressed")
        clear_all_widgets(config_frame)
        clear_and_set_text(result_text, "")

        # Fetching data from the database
        programs = self.interface.get_all_programs()
        programs.sort_values(by='dept_code', inplace=True)
        courses = self.interface.get_all_courses()
        sections = self.interface.get_all_sections()
        objectives = self.interface.get_all_objectives()
        subobjectives = self.interface.get_all_subobjectives()
        objective_assignments = self.interface.get_all_objective_assignments()

        course_assignments = self.interface.get_all_course_assignments()
        # Program dropdown setup
        program_var = tk.StringVar()
        prog_mapper = {f'{n} {d}': {'prog_name': n, 'dept_code': d} for n, d in
                       zip(programs['name'], programs['dept_code'])}

        # Dropdown frame
        dropdown_frame = tk.Frame(config_frame)
        dropdown_frame.pack(fill='x')
        tk.Label(dropdown_frame, text='Program:').pack(side='left')
        program_menu = tk.OptionMenu(dropdown_frame, program_var, *prog_mapper.keys())
        program_menu.pack(side='left')

        # Sort the courses by department id
        courses = courses.sort_values(by='dept_id')

        # Function to update the Treeview with courses from the selected program
        def update_course_treeview(*args):
            style = ttk.Style()
            style.configure("ChildRow.TLabel", background="#ffffff")

            selected_program = program_var.get()
            selected_dept_code = prog_mapper[selected_program]['dept_code']


            # Filter the courses DataFrame for the selected program
            filtered_courses = course_assignments[(course_assignments['dept_id'] == selected_dept_code) & (course_assignments['program_name'] == prog_mapper[selected_program]['prog_name'])]
            filtered_courses = filtered_courses.merge(courses,left_on=['course_dept','course_id'],right_on=['dept_id','id']).rename(columns={'dept_id_x':'dept_id'})
            print(filtered_courses)
            # Clear the current contents of the Treeview
            course_table.delete(*course_table.get_children())

            # Inserting filtered course data into the Treeview
            for course in filtered_courses.itertuples():
                course_id = f'{course.course_dept}{course.course_id}'
                dept_id = course.dept_id
                course_node = course_table.insert('', tk.END, text=course_id,
                                                  values=(course_id, course.title, course.description))

                # Filter sections DataFrame for those related to this course and dept
                course_sections = sections[sections['course_id'] == course_id]
                course_sections = course_sections[course_sections['dept_id'] == dept_id]
                for _, section in course_sections.iterrows():
                    course_table.insert(course_node, tk.END, text=section.id,
                                        values=('\t\t' + section.id, '\t\t' + section.semester, 'Section', section.year),
                                        tags=("child",))
            course_table.tag_configure("child", background="#f0f0f0")

        # Create a frame for the Treeview and scrollbar
        treeview_frame = tk.Frame(config_frame)
        treeview_frame.pack(fill='both', expand=True)

        # Create a treeview to display the courses
        course_table = ttk.Treeview(config_frame)
        course_table['columns'] = ('id', 'title', 'description')
        course_table.column('#0', width=0, stretch=tk.NO)  # Hiding the first empty column
        course_table.heading('#0', text='', anchor=tk.W)
        for col in course_table['columns']:
            course_table.column(col, anchor=tk.CENTER)
            course_table.heading(col, text=col, anchor=tk.CENTER)

        # Adding a scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(treeview_frame, orient='vertical', command=course_table.yview)
        scrollbar.pack(side='right', fill='y')
        course_table.configure(yscrollcommand=scrollbar.set)
        course_table.pack(expand=True, fill='both')  # Pack inside treeview_frame

        # Bind the update function to the program dropdown
        program_var.trace('w', update_course_treeview)

        # Create a frame for displaying section details
        details_frame = tk.Frame(config_frame)
        details_frame.pack(fill='both', expand=True)

        # Function to populate the details frame with objectives and subobjectives
        def populate_details_frame(section_id, course_id, dept_id, semester, year):
            # Clear the current contents of the details frame
            for widget in details_frame.winfo_children():
                widget.destroy()

            # Add new content to the details frame
            details_label_text = f"Objectives and Subobjectives for Course ID {course_id}, Dept ID {dept_id}, Section {section_id}:"
            tk.Label(details_frame, text=details_label_text, anchor='w').pack(
                fill='x')  # Left-aligned and fills the frame horizontally

            # Filter the objective_assignments DataFrame for those related to this section, course, and department
            relevant_objective_assignments = objective_assignments[
                (objective_assignments['section_id'] == section_id) &
                (objective_assignments['course_id'] == course_id) &
                (objective_assignments['dept_id'] == dept_id) &
                (objective_assignments['semester'] == semester) &
                (objective_assignments['year'] == int(year))
                ]

            # Loop to hold the objectives for this section
            for _, obj_assignment in relevant_objective_assignments.iterrows():
                # Get the actual objective from objectives DataFrame
                objective = objectives[objectives['id'] == obj_assignment.obj_id].iloc[0]
                tk.Label(details_frame, text=f"Objective: {objective.description}", anchor='w').pack(
                    fill='x')  # Left-aligned

                # Filter the subobjectives DataFrame for those related to this objective
                relevant_subobjectives = subobjectives[subobjectives['objective_id'] == objective.id]
                for _, subobj in relevant_subobjectives.iterrows():
                    tk.Label(details_frame, text=f"\tSubobjective: {subobj.description}", anchor='w').pack(
                        fill='x')  # Left-aligned with indentation
        def on_section_select(event):
            selected_item = course_table.focus()
            item_values = course_table.item(selected_item, 'values')
            # Check if the selected item is a section by looking at the 'Section' text in values
            if item_values and 'Section' in item_values:
                section_id = item_values[0].strip('\t')
                # Assume that the course_id and dept_id are stored in the parent item of the selected section
                parent_item = course_table.parent(selected_item)
                parent_values = course_table.item(parent_item, 'values')
                course_id = parent_values[0]
                dept_id = parent_values[1]
                semester = item_values[1].strip('\t')
                year = item_values[3]
                print(f"Selected section {section_id} of course {course_id} in department {dept_id} with semester {semester} and year {year}")
                populate_details_frame(section_id, course_id, dept_id, semester, year)

        # Initialize the Treeview with the first selected program
        if prog_mapper:
            program_var.set(next(iter(prog_mapper.keys())))
            update_course_treeview()
        course_table.bind('<<TreeviewSelect>>', on_section_select)

    def handle_show_learning_objectives_press(self):
        print("Show Courses Button was Pressed")
        clear_all_widgets(config_frame)
        clear_and_set_text(result_text, "")

        # Fetching data from the database
        programs = self.interface.get_all_programs()
        programs.sort_values(by='dept_code', inplace=True)
        courses = self.interface.get_all_courses()
        sections = self.interface.get_all_sections()
        objective_assignments = self.interface.get_all_objective_assignments()

        # Program dropdown setup
        self.program_var = tk.StringVar()
        self.prog_mapper = {f'{n} {d}': [n,d] for n, d in zip(programs['name'], programs['dept_code'])}

        # Dropdown frame
        dropdown_frame = tk.Frame(config_frame)
        dropdown_frame.pack(fill='x')
        tk.Label(dropdown_frame, text='Program:').pack(side='left')
        self.program_menu = tk.OptionMenu(dropdown_frame, self.program_var, *self.prog_mapper.keys())
        self.program_menu.pack(side='left')

        # Treeview for displaying objectives
        treeview_frame = tk.Frame(config_frame)
        treeview_frame.pack(fill='both', expand=True)

        self.objectives_treeview = ttk.Treeview(treeview_frame, columns=('id', 'description'))
        self.objectives_treeview.column('#0', width=0, stretch=False)
        self.objectives_treeview.heading('id', text='ID')
        self.objectives_treeview.heading('description', text='Description')
        self.objectives_treeview.pack(fill='both', expand=True)

        # Function to update the Treeview based on selected program
        def update_objectives_treeview(*args):
            selected_dept_code = self.prog_mapper[self.program_var.get()][1]
            print("Selected department code:", selected_dept_code)

            # Clear existing entries in the Treeview
            self.objectives_treeview.delete(*self.objectives_treeview.get_children())
            
            cas = self.interface.get_all_course_assignments()
            cas = cas[cas['dept_id'] == selected_dept_code]

            # Fetch objectives based on selected department code
            #To do this we read the objectiveAssignments table, filter by dept_id, and then display all of the objectives that match an obj_id in the remaining rows.
            objectives_in_dept = objective_assignments[objective_assignments['dept_id'].isin(cas['course_dept'])]
            print(objectives_in_dept)
            objectives_in_dept = objectives_in_dept.merge(self.interface.get_all_course_assignments(),left_on=['course_id','dept_id'],right_on=['course_id','course_dept'])

            objectives_in_dept = objectives_in_dept[objectives_in_dept['program_name'] == self.prog_mapper[self.program_var.get()][0]]
            print(objectives_in_dept)
            objectives = self.interface.get_all_objectives()
            objectives_in_dept = objectives_in_dept.merge(objectives, left_on='obj_id', right_on='id').drop_duplicates(subset=['id','description'])

            print(objectives_in_dept)

            # Add objectives to the treeview
            for obj in objectives_in_dept.itertuples():
                self.objectives_treeview.insert('', 'end', text=obj.id, values=(obj.id, obj.description))

        # Bind the update function to the program dropdown
        self.program_var.trace('w', update_objectives_treeview)

        # Initial population of the Treeview
        if self.prog_mapper:
            first_program = next(iter(self.prog_mapper))
            self.program_var.set(first_program)
            update_objectives_treeview()

    def handle_show_eval_program_press(self):
        print("Show eval from program Button was Pressed")
        clear_all_widgets(config_frame)
        # clear_and_set_text(result_text,"Show eval from program Button was Pressed")
        progs = self.interface.get_all_programs()
        progs = progs.sort_values(by='dept_code')

        semester_var = tk.StringVar()
        program_var = tk.StringVar()
        
        prog_mapper = {f'{n} {d}':{'prog_name':n,'dept_code':d} for n,d in zip(progs['name'],progs['dept_code'])}

        semesters= ['Fall','Spring','Summer']
        wigits = [
            tk.Label(config_frame,text='Semester:'),
            tk.OptionMenu(config_frame,semester_var,*semesters),
            tk.Label(config_frame,text='Program:'),
            tk.OptionMenu(config_frame,program_var,*prog_mapper.keys())

        ]
        
        def handle_submit():
            sects = self.interface.get_all_sections()

            cas = self.interface.get_all_course_assignments()
            cas = cas[(cas['dept_id'] == prog_mapper[program_var.get()]['dept_code']) & (cas['program_name'] == prog_mapper[program_var.get()]['prog_name'])]

            sub_objs = self.interface.get_all_subobjectives()


            oas = self.interface.get_all_objective_assignments()

            oas['pct_passed'] = np.round(oas['num_passed'] / (oas['num_passed'] + oas['num_failed']),2)

            joined = sects.merge(cas,left_on=['course_id','dept_id'],right_on=['course_id','course_dept']).rename(columns={'dept_id_x':'dept_id'})


            joined = joined[joined['semester'] == semester_var.get()]

            joined = joined.merge(oas,left_on=['id','course_id','dept_id','semester','year'],right_on=['section_id','course_id','dept_id','semester','year'],how='left')
            
            
            joined = joined.merge(sub_objs,left_on=['obj_id','sub_obj_id'],right_on=['objective_id','sub_id'],how='left')

            print(joined)
            joined = joined[['id','dept_id','course_id','evaluation','description','pct_passed','year']]
            joined = joined.fillna('N/A').rename(columns={'id':'section','dept_id':'department'})
            txt = convert_df_to_text(joined)
            clear_and_set_text(result_text,txt)
        
        wigits.append(tk.Button(config_frame,text='Submit',command=handle_submit))
        for i,w in enumerate(wigits):
            w.grid(row=0,column=i)
        
        


    def handle_show_eval_dates_press(self):
        
        print("Show Eval from Dates Button was Pressed")
        clear_all_widgets(config_frame)
        year_var = tk.StringVar()
        

        # clear_and_set_text(result_text,"Show Eval from Dates Button was Pressed")
        obj_ass = self.interface.get_all_objective_assignments()
        sections = self.interface.get_all_sections()
        sub_objs = self.interface.get_all_subobjectives()
        
        joined = obj_ass.merge(sections, left_on=['section_id','dept_id','course_id'],right_on=['id','dept_id','course_id'])
        joined = joined.merge(sub_objs,left_on=['obj_id','sub_obj_id'],right_on=['objective_id','sub_id'])

        joined['class'] = joined['dept_id'] +joined['course_id'] + "_" + joined['section_id']
        joined['Percent_Complete'] = np.round(joined['num_passed'] / (joined['num_passed'] + joined['num_failed']),2) * 100
        print(joined.columns)
        joined = joined.rename(columns={'year_x':'year','semester_x':'semester'})
        joined = joined[['class','semester','year','Percent_Complete','evaluation','description']]

        # print(joined[['year','semester']])
        valid_years = np.unique([y if s == 'Fall' or s == 'Summer' else y-1 for s,y in zip(joined['semester'],joined['year'])])

        # print(valid_years)
        valid_years_mapper = {f'{y}-{y+1}':[y,y+1] for y in valid_years}
        
        wigits = []
        wigits.append(tk.Label(config_frame,text='Academic Year:'))
        wigits.append(tk.OptionMenu(config_frame,year_var,*valid_years_mapper.keys()))

        def handle_submit():
           
            
            lower,upper = valid_years_mapper[year_var.get()]

            # print(lower,upper)
            res = joined[((joined['year'] == lower) & (joined['semester'] == 'Summer')) | ((joined['year'] == lower) & (joined['semester'] == 'Fall')) | ((joined['year'] == upper) & (joined['semester'] == 'Spring'))]
            
            txt = convert_df_to_text(res)


            clear_and_set_text(result_text,txt)
            clear_all_widgets(config_frame)
        wigits.append(tk.Button(config_frame,text='Submit',command=handle_submit))
        for i,w in enumerate(wigits):
            w.grid(row=0,column=i)
        
        # print(valid_years)
        
if __name__ == "__main__":
#Sql will make a connection based on information provided in the .env file
    p = ProgramRunner()

    p.run()
    main_window = tk.Tk()
    # button = tk.Button(main_window,text='stop',command=p.run)
    # button.grid(column=0,row=0)
    addition_buttons = [
        tk.Button(main_window,text='Add Department',command=p.handle_add_department_press),
        tk.Button(main_window,text='Add Faculty',command=p.handle_add_faculty_press),
        tk.Button(main_window,text='Add Program',command=p.handle_add_program_press),
        tk.Button(main_window,text='Add Course',command=p.handle_add_course_press),
        tk.Button(main_window,text='Add Section',command=p.handle_add_section_press),
        tk.Button(main_window,text='Add Objective',command=p.handle_add_objective_press),
        tk.Button(main_window,text='Add Sub-Objective',command=p.handle_add_subobjective_press)
    ]
    for i,b in enumerate(addition_buttons):
        b.grid(column=i,row=0,sticky='ew')
    
    assign_buttons = [
        tk.Button(main_window,text='Assign Learning Objective',command=p.handle_assign_lo_press),
        tk.Button(main_window,text='Assign Course',command=p.handle_assign_course_press)
    ]
    for i,b in enumerate(assign_buttons):
        b.grid(row=1,column=i,sticky='ew')
    
    show_buttons = [
        tk.Button(main_window,text='Show Programs',command=p.handle_show_programs_press),
        tk.Button(main_window,text='Show Courses',command=p.handle_show_courses_press),
        tk.Button(main_window,text='Show Eval Results from Program',command=p.handle_show_eval_program_press),
        tk.Button(main_window,text='Show Eval Results from Dates',command=p.handle_show_eval_dates_press),
        tk.Button(main_window,text='Show Learning Objectives',command=p.handle_show_learning_objectives_press),
    ]

    for i,b in enumerate(show_buttons):
        b.grid(row=2,column=i,sticky='ew')

    config_frame = tk.Frame(main_window) # Used for adding wigets to that allow customization of query
    config_frame.grid(row=3,column=0,columnspan=max(len(show_buttons),len(assign_buttons),len(addition_buttons)),rowspan=5,sticky='ew')
    
    result_frame = tk.Frame(main_window) # Used for showing results to user
    result_frame.grid(row=8,column=0,columnspan=max(len(show_buttons),len(assign_buttons),len(addition_buttons)),rowspan=5,sticky='ew')
    
    result_text = scrolledtext.ScrolledText(result_frame,width=200,height=50)
    result_text.insert(tk.INSERT,
                       "Results will appear here")
    result_text.grid(column=0,row=0,sticky='ew',columnspan=max(len(show_buttons),len(assign_buttons),len(addition_buttons)))
    result_text.configure(state='disabled')
    



    main_window.mainloop()
