
""" Authors: Seth Harmon
    Course:  COMP 445
    Date:    10 March 2025
    Description: file solve the MTA problem
    Run with: ./MTA_Solver.py
"""

import sys
import pandas as pd
from datetime import datetime
from backtrack import backtrack
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
    # Read in MTAs and domains
    mtas = read_mtas()
    domains = get_domains(mtas)
    # Ask user for the algorithm to ues
    algorithm = input("Enter 'b' for backtracking search or 'n' for remembering no goods: ").lower()
    while algorithm != "b" and algorithm != "n":
        algorithm = input("Invalid input, please enter 'b' or 'n': ")
    # Get the buffer period for between MTAs
    buffer = -1
    while True:
        # Keep looping till we get a valid integer that is greater than or equal to 0
        try:
            buffer = int(input("Enter the buffer period for minutes between MTAs (will be converted to divisible by five): "))
            if buffer >= 0: break
        except:
            pass
        print("Invalid input, please enter a non-negative integer. ",end='')
    # Make sure it is divisible by five
    remainder = buffer % 5
    buffer = buffer + (5-remainder) if remainder > 2 else buffer - remainder
    # Get whether the user wants a verbose run or not
    verbosity = -1
    try:
        verbosity: int = int(input("What level of verbosity would you like (0/1/2)? "))
    except:
        while verbosity not in [0, 1, 2]:
            try:
                verbosity = int(input("Invalid input, what level of verbosity would you like (0/1/2)? "))
            except:
                pass
    # Run search
    result = backtrack(mtas, domains, buffer=buffer, remember_no_goods=(algorithm == 'n'), verbosity=verbosity)
    # Print results
    if result:
        print("\nResult found:")
        for i in range(len(result)):
            print(f"{mtas[i].type.name} = {result[i]}")
    else:
        print("\nNo result found")

if __name__ == "__main__":
    main()
