from datetime import datetime

import pandas as pd

from backtrack import backtrack
from remembering_no_goods import remembering_no_goods
from domain_helper import get_domains
from MTA_Helper import MTA, MTA_Type, Student, Time_Block


def read_mtas() -> list[MTA]:
    """
    Creates a list of MTAs from a group of excel files

    return: a list of MTAs
    """
    mtas_df = pd.read_excel("DATA/mtas.xlsx")
    mta_type_df = pd.read_excel("DATA/mta_type_availability.xlsx")
    student_df = pd.read_excel("DATA/student_unavailability.xlsx")
    # create a list of students
    student_times: dict[str, list[Time_Block]] = {}
    for row in student_df.iterrows():
        data = row[1]
        student = data["Student Name"]
        curr_student = ''
        if isinstance(student, str):
            curr_student = student
        try:
            student_times[curr_student].append(
                Time_Block(
                    datetime.combine(
                        datetime.today(), data["Unavailability Start Time"].time()
                    ),
                    datetime.combine(datetime.today(), data["Unavailability End Time"].time()),
                    data["Unavailability Day"],
                )
            )
        except:
            student_times[curr_student] = [
                Time_Block(
                    datetime.combine(
                        datetime.today(), data["Unavailability Start Time"].time()
                    ),
                    datetime.combine(datetime.today(), data["Unavailability End Time"].time()),
                    data["Unavailability Day"],
                )
            ]
    students: dict[str, Student] = {}
    for key in student_times.keys():
        students[key] = Student(key, student_times[key])
    # create a list of available times for MTAs
    mta_times: dict[str, list[Time_Block]] = {}
    for row in mta_type_df.iterrows():
        data = row[1]
        mta_type = data["Type"]
        curr_type = ''
        if isinstance(mta_type, str):
            curr_type = mta_type
        try:
            mta_times[curr_type].append( 
                Time_Block(
                    datetime.combine(datetime.today(), data["Availability Start Time"].time()),
                    datetime.combine(datetime.today(), data["Availability End Time"].time()),
                    data["Availability Day"],
                ) 
            ) 
        except:
            mta_times[curr_type] = [
                Time_Block(
                    datetime.combine(datetime.today(), data["Availability Start Time"].time()),
                    datetime.combine(datetime.today(), data["Availability End Time"].time()),
                    data["Availability Day"],
                )
            ]
    mta_types: dict[str, MTA_Type] = {}
    for key, value in mta_times.items():
        mta_types[key] = MTA_Type(key, value)
    # create a list of MTAs
    mtas: list[MTA] = []
    for row in mtas_df.iterrows():
        data = row[1]
        students_str = data["Students"].split(", ")
        student_list = []
        for student in students_str:
            student_list.append(students[student])
        mta_type = data["Type"]
        mtas.append(
            MTA(
                student_list,
                mta_types[mta_type],
                mta_types[mta_type].times,
                data["Length (minutes)"],
            )
        )
    return mtas

def main():
    """
    Solves MTA problems using two different algorithms and runs tests
    """
    mtas = read_mtas()
    domains = get_domains(mtas)
    result = backtrack(mtas, domains,remember_no_goods=True)
    if result is None:
        print("No result found")
        return
    print("Result found!")
    for item in result: 
        print(item)

if __name__ == "__main__":
    main()
