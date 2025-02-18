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


def backtrack(
    mtas: list[MTA], domains: list[Time_Block], next_var: int = 0, buffer: int = 5
):
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
    for value in domains[next_var]:
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
                new_times = new_mtas[next_var].type.times
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
                new_domains.append(value)
                # generate new domains after assignment
                new_domains.extend(get_domains(new_mtas, next_var + 1))
                result = backtrack(new_mtas, new_domains, next_var + 1, buffer)
                if result:
                    return result
        if not consistent:
            continue
    return None
