import pandas as pd
from datetime import datetime, timedelta

class Time_Block:
    def __init__(self, start_time: datetime, end_time: datetime, day):
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
    
class MTA_Type:
    def __init__(self, name, times):
        self.name = name
        self.times = times

    def __str__(self):
        ret_str = f"{self.name}:\n"
        for time in self.times:
            ret_str += f"{time}\n"
        return ret_str

class MTA:
    def __init__(self, students: list[Student], type: MTA_Type, times: list[Time_Block], length):
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
    
def read_mtas():
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
            student_times[curr_student].append(Time_Block(datetime.combine(datetime.today(), data["Unavailability Start Time"]), datetime.combine(datetime.today(), data["Unavailability End Time"]), data["Unavailability Day"]))
        except:
            student_times[curr_student] = [Time_Block(datetime.combine(datetime.today(), data["Unavailability Start Time"]), datetime.combine(datetime.today(), data["Unavailability End Time"]), data["Unavailability Day"])]
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
            mta_times[curr_type].append(Time_Block(datetime.combine(datetime.today(), data["Availability Start Time"]), datetime.combine(datetime.today(), data["Availability End Time"]), data["Availability Day"]))
        except:
            mta_times[curr_type] = [Time_Block(datetime.combine(datetime.today(), data["Availability Start Time"]), datetime.combine(datetime.today(), data["Availability End Time"]), data["Availability Day"])]
    mta_types = {}
    for key, value in mta_times.items():
        mta_types[key] = MTA_Type(key, value)
    mtas = []
    for row in mtas_df.iterrows():
        data = row[1]
        students_str = data["Students"].split(", ")
        student_list = []
        for student in students_str:
            student_list.append(students[student])
        mta_type = data["Type"]
        mtas.append(MTA(student_list, mta_types[mta_type], mta_types[mta_type].times, data["Length (minutes)"]))
    return mtas

def get_domains(mtas: list[MTA]):
    domains = []
    for mta in mtas:
        domain = []
        to_add = {}
        for time in mta.times:
            for student in mta.students:
                for unavailable in student.unavailable_times:
                    if time.day != unavailable.day:
                        continue
                    if unavailable.start_time <= time.start_time and unavailable.end_time >= time.end_time:
                        mta.times.remove(time)
                        removed = True
                        break
                    if unavailable.start_time > time.start_time and unavailable.end_time < time.end_time:
                        time.end_time = unavailable.start_time
                        to_add[mta.times.index(time)] = Time_Block(unavailable.end_time, time.end_time, time.day)
                    if unavailable.start_time == time.start_time and unavailable.end_time < time.end_time:
                        time.start_time = unavailable.end_time
                    if unavailable.start_time > time.start_time and unavailable.end_time == time.end_time:
                        time.end_time = unavailable.start_time
                if removed:
                    break
            if removed:
                continue
        for key, value in to_add.items():
            mta.times.insert(key, value)
        for time in mta.times:
            curr_time = time.start_time
            while curr_time <= time.end_time - timedelta(minutes=mta.length):
                domain.append(curr_time)
                curr_time += timedelta(minutes=5)
        domains.append(domain)
    return domains

def backtrack(mtas, domains, next_var):
    if next_var == len(mtas):
        return domains
    for value in domains[next_var]:
        pass

def main():
    mtas = read_mtas()
    print(mtas[0])
    domains = get_domains(mtas)
    for item in domains[0]:
        print(item)
    
    

if __name__=="__main__":
    main()