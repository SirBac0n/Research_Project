import pandas as pd

class Time_Block:
    def __init__(self, start_time, end_time, day):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

class Student:
    def __init__(self, unavailable_times: list[Time_Block]):
        self.unavailable_times = unavailable_times

class MTA:
    def __init__(self, students: list[Student], type, times: list[Time_Block], length):
        self.students = students
        self.type = type
        self.times = times
        self.length = length

def main():
    mtas_df = pd.read_excel("DATA/mtas.xlsx")
    mta_type_df = pd.read_excel("DATA/mta_type_availability.xlsx")
    student_df = pd.read_excel("DATA/student_unavailability.xlsx")
    mta_list = []
    mtas = mtas_df.iterrows()
    #print(mtas_df)
    print(student_df)
    students = {}
    for row in student_df.iterrows():
        data = row[1]
        student = data["Student Name"]
        print(student == "NaN")
        if student != "nan":
            curr_student = student
        try:
            students[curr_student].append(Time_Block(data["Unavailability Start Time"], data["Unavailability End Time"], data["Unavailability Day"]))
        except:
            students[curr_student] = [Time_Block(data["Unavailability Start Time"], data["Unavailability End Time"], data["Unavailability Day"])]
    print(students)
    for row in mtas_df.iterrows():
        mta_type = row[1]["Type"]
         

if __name__=="__main__":
    main()