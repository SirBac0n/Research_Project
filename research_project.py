import pandas as pd

class Time_Block:
    def __init__(self, start_time, end_time, day):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

    def __str__(self):
        return f"{self.day}: {self.start_time} - {self.end_time}"

class Student:
    def __init__(self, name: str, unavailable_times: list[Time_Block]):
        self.name = name
        self.unavailable_times = unavailable_times

    def __str__(self):
        ret_str = f"{self.name}:\n"
        for time in self.unavailable_times:
            ret_str += f"{time}\n"
        return ret_str

class MTA:
    def __init__(self, students: list[Student], type, times: list[Time_Block], length):
        self.students = students
        self.type = type
        self.times = times
        self.length = length

    def __str__(self):
        ret_str = f"{self.type}:\n"
        for student in self.students:
            ret_str += f"{student}\n"
        ret_str += f"Length: {self.length}\n"
        for time in self.times:
            ret_str += f"{time}\n"
        return ret_str

def main():
    mtas_df = pd.read_excel("DATA/mtas.xlsx")
    mta_type_df = pd.read_excel("DATA/mta_type_availability.xlsx")
    student_df = pd.read_excel("DATA/student_unavailability.xlsx")
    student_times = {}
    for row in student_df.iterrows():
        data = row[1]
        student = data["Student Name"]
        if isinstance(student, str):
            curr_student = student
        try:
            student_times[curr_student].append(Time_Block(data["Unavailability Start Time"], data["Unavailability End Time"], data["Unavailability Day"]))
        except:
            student_times[curr_student] = [Time_Block(data["Unavailability Start Time"], data["Unavailability End Time"], data["Unavailability Day"])]
    students = {}
    for key in student_times.keys():
        students[key] = (Student(key, student_times[key]))
    mta_times = {}
    for row in mta_type_df.iterrows():
        data = row[1]
        mta_type = data["Type"]
        if isinstance(mta_type, str):
            curr_type = mta_type
        try:
            mta_times[curr_type].append(Time_Block(data["Availability Start Time"], data["Availability End Time"], data["Availability Day"]))
        except:
            mta_times[curr_type] = [Time_Block(data["Availability Start Time"], data["Availability End Time"], data["Availability Day"])]
    mtas = []
    for row in mtas_df.iterrows():
        data = row[1]
        students_str = data["Students"].split(", ")
        student_list = []
        for student in students_str:
            student_list.append(students[student])
        mta_type = data["Type"]
        mtas.append(MTA(student_list, mta_type, mta_times[mta_type], data["Length (minutes)"]))
    print(mtas[1])




if __name__=="__main__":
    main()