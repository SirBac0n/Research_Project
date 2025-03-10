
""" Authors: Seth Harmon
    Course:  COMP 445
    Date:    10 March 2025
    Description: file with code to help get domains
"""

from datetime import timedelta
from MTA_Helper import MTA, Time_Block

def get_domains(mtas: list[MTA], idx: int = 0) -> list[list[Time_Block]]:
    """
    Creates the domains for the mtas starting from idx until reaching the end of the list of mtas

    mtas: the list of MTAs

    idx: the index to start from to generate domains

    return: a list representing the domains of the MTAs
    """
    domains = []
    for i in range(idx, len(mtas)):
        mta = mtas[i]
        domain = []
        to_add = {}
        for time in mta.times:
            removed = False
            # check if students unavailability overlaps with MTA's available times
            for student in mta.students:
                for unavailable in student.unavailable_times:
                    if time.day != unavailable.day:
                        continue
                    # if a student is unavailable for the entire duration of the MTA time slot, remove the MTA time slot
                    if (
                        unavailable.start_time <= time.start_time
                        and unavailable.end_time >= time.end_time
                    ):
                        mta.times.remove(time)
                        removed = True
                        break
                    # if a student's unavailability lies within the MTA's availability, split the MTA's availability to account for the student
                    if (
                        unavailable.start_time > time.start_time
                        and unavailable.end_time < time.end_time
                    ):
                        time.end_time = unavailable.start_time
                        to_add[mta.times.index(time)] = Time_Block(
                            unavailable.end_time, time.end_time, time.day
                        )
                    # if a student's unavailabiltiy lies at the beginning of the MTA's availability, adjust the MTA's availabilty accordingly
                    if (
                        unavailable.start_time == time.start_time
                        and unavailable.end_time < time.end_time
                    ):
                        time.start_time = unavailable.end_time
                    # if a student's unavailabiltiy lies at the end of the MTA's availability, adjust the MTA's availabilty accordingly
                    if (
                        unavailable.start_time > time.start_time
                        and unavailable.end_time == time.end_time
                    ):
                        time.end_time = unavailable.start_time
                if removed:
                    break
            if removed:
                continue
        for key, value in to_add.items():
            mta.times.insert(key, value)
        # create available times for the MTA in 5 minute increments
        for time in mta.times:
            curr_time = time.start_time
            # while there is enough time for the MTA to finish
            while curr_time <= time.end_time - timedelta(minutes=mta.length):
                domain.append(
                    Time_Block(
                        curr_time, curr_time + timedelta(minutes=mta.length), time.day
                    )
                )
                curr_time += timedelta(minutes=5)
        domains.append(domain)
    return domains