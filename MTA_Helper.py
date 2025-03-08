from datetime import datetime


class Time_Block:
    """
    Represents a block of time spanning from start_time to end_time on day
    """

    def __init__(self, start_time: datetime, end_time: datetime, day: str):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

    def __str__(self):
        return f"{self.day}: {self.start_time} - {self.end_time}"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Time_Block):
            return False
        return self.start_time == value.start_time and self.end_time == value.end_time and self.day == value.day


class Student:
    """
    Represents a student that stores the name of the student and a list of times the student is unavailable
    """

    def __init__(self, name: str, unavailable_times: list[Time_Block]):
        self.name = name
        self.unavailable_times = unavailable_times

    def __str__(self):
        ret_str = f"{self.name}:\n"
        for time in self.unavailable_times:
            ret_str += f"{time}\n"
        return ret_str
    
    def __eq__(self, value: object) -> bool:
        # Not equal if value is not a Student or if names are different
        if not isinstance(value, Student) or self.name != value.name: # or len(self.unavailable_times) != len(value.unavailable_times)
            return False
        # Return if the lists are equal - should work!
        return self.unavailable_times == value.unavailable_times
        # # Loop through all items in each unavailable times to see if they are all the same
        # for i in range(len(self.unavailable_times)):
        #     # If a pair does not match, return False
        #     if not self.unavailable_times[i] == value.unavailable_times[i]:
        #         return False
        # # If they were all the same return True
        # return True

    def __hash__(self) -> int:
        return hash((self.name,len(self.unavailable_times)))


class MTA_Type:
    """
    Represents a type of MTA that stores the name of the MTA as well as the times the MTA can take place
    """

    def __init__(self, name: str, times: list[Time_Block]):
        self.name = name
        self.times = times

    def __str__(self):
        ret_str = f"{self.name}:\n"
        for time in self.times:
            ret_str += f"{time}\n"
        return ret_str

    def __eq__(self, value: object) -> bool:
        # Not equal if value is not a MTA Type or if names are different
        if not isinstance(value, MTA_Type) or self.name != value.name:
            return False
        # Return if the lists are equal - should work!
        return self.times == value.times
    
    def __hash__(self) -> int:
        return hash(self.name)

class MTA:
    """
    Represents an individual MTA that stores a list of students participating, the type of the MTA,
     
    the available times for this individual MTA, and the length of the MTA
    """

    def __init__(
        self,
        students: list[Student],
        type: MTA_Type,
        times: list[Time_Block],
        length: int,
    ):
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
