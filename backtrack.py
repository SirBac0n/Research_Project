import copy
from MTA_Helper import MTA, Time_Block, MTA_Type, Student
from domain_helper import get_domains
from datetime import timedelta


no_goods: set[tuple[int, tuple[MTA_Type, ...], tuple[Student, ...]]] = set()

def backtrack(mtas: list[MTA], domains: list[Time_Block], next_var: int = 0, buffer: int = 5, 
              remember_no_goods: bool = False) -> list[Time_Block] | None:
    """
    Runs basic backtracking search on the given MTA problem

    mtas: the list of MTAs

    domains: the list of domains for each MTA

    next_var: the index of the next variable to assign

    buffer: the amount of time a student needs between scheduled MTAs

    return: a list representing the time slot assignment for each MTA
    """
    # base case, all variables have been assigned
    if next_var == len(mtas):
        return domains
    
    curr_mta_types: set[MTA_Type] | tuple | None = None
    curr_students: set[Student] | tuple | None = None
    # If remembering no-goods...
    if remember_no_goods:
        # Create a set containing the current state of all the MTA Types
        curr_mta_types = {MTA_Type(mta.type.name,copy.deepcopy(mta.type.times)) for mta in mtas}
        # Create a set containing the current state of all the students
        curr_students = set()
        for mta in mtas:
            for student in mta.students:
                curr_students.add(copy.deepcopy(student))
        # Convert the sets to hashable tuples
        curr_mta_types = tuple(curr_mta_types)
        curr_students = tuple(curr_students)
        # If we have seen the above sets before, there is no solution here
        if (next_var,curr_mta_types,curr_students) in no_goods:
            return None

    for value in domains[next_var]: #type: ignore
        consistent = True
        # check if the value is in the available time slots for that MTA type
        for time in mtas[next_var].type.times:
            if (
                value.day == time.day
                and value.start_time >= time.start_time
                and value.end_time <= time.end_time
            ):
                # check if any of the students are unavailable during the current value
                for student in mtas[next_var].students:
                    for unavailable in student.unavailable_times:
                        if value.day == unavailable.day and (
                            (
                                value.start_time >= unavailable.start_time
                                and value.start_time < unavailable.end_time
                            )
                            or (
                                value.end_time >= unavailable.start_time
                                and value.end_time < unavailable.end_time
                            )
                        ):
                            consistent = False
                            break
                    if not consistent:
                        break
                if not consistent:
                    break
                new_mtas = mtas.copy()
                new_times = new_mtas[next_var].type.times.copy()
                new_time = new_times[new_times.index(time)]
                # update the available times for the type of MTA after assigning
                if value.start_time == time.start_time:
                    new_time.start_time = value.end_time
                if value.end_time == time.end_time:
                    new_time.end_time = value.start_time
                if (
                    value.start_time > time.start_time
                    and value.end_time < time.end_time
                ):
                    new_times.insert(
                        new_times.index(new_time),
                        Time_Block(value.end_time, new_time.end_time, value.day),
                    )
                    new_time.end_time = value.start_time
                # update the unavailable times for each student in the MTA after assigning
                for student in new_mtas[next_var].students:
                    student.unavailable_times.append(
                        Time_Block(
                            value.start_time - timedelta(minutes=buffer),
                            value.end_time + timedelta(minutes=buffer),
                            value.day,
                        )
                    )
                # copy previous assignments
                new_domains = domains.copy()[:next_var]
                # assign value
                new_domains.append(value) #type: ignore
                # generate new domains after assignment
                new_domains.extend(get_domains(new_mtas, next_var + 1)) #type: ignore
                result = backtrack(new_mtas, new_domains, next_var + 1, buffer)
                if result:
                    return result
        if not consistent:
            continue

    # If remembering no-goods and curr_mta_types and curr_students are initialized (which they should be at this point)...
    if remember_no_goods and curr_mta_types and curr_students:
        # Add a no-good instance to our set of no-goods
        no_goods.add((next_var,curr_mta_types,curr_students))

    return None
