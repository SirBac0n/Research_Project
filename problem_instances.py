import random
from faker import Faker
from random import randrange
import pandas as pd

# Create initialized global list variables
mta_types: list[str] = ['Preaching','Apologetics','Music','Puppetry','Bible Teaching','Inspirational Writing','Drama','Gospel Art','Sign Language','Worship Leading']
days_of_the_week: list[str] = ['Monday','Tuesday','Wednesday','Thursday','Friday']

def generate_students(n: int) -> list[str]:
    fake: Faker = Faker()
    names: list[str] = []
    # Generate n names
    for _ in range(n):
        # Make sure name does not contain ','
        name: str = ','
        while ',' in name:
            name = fake.name()
        names.append(name)
    return names

def generate_time_tuple(min_time: str, max_time: str, min_hours_dif: int = 1) -> tuple[str, str]:
    """Get a tuple of random time strings between two times. Does not work if HH equals '00'

    min_time and max_time are both of the format HH:MM (e.g. '14:25')

    return a tuple of two string for a times between the two values
    """
    max_time_hour, max_time_minute = max_time.split(':')
    # Get the first time, which has a max end time of min_hours_dif less tahn max time's hour
    first_time: str = random_time_range(min_time, f'{int(max_time_hour)-min_hours_dif}:{max_time_minute}')
    # Get the second time, which starts at first_time
    second_time = random_time_range(first_time,max_time)
    # Convert times to preferred format and then return them as a tuple
    return (time_format(first_time),time_format(second_time))
    
def time_format(time: str) -> str:
    """Convert a time string to a default format"""
    hour, minute = time.split(':')
    h = int(hour)
    m = int(minute)
    am: bool = True if h < 12 else False
    h = h if am or h == 12 else h % 12

    return f"{h:02d}:{m:02d}:00 {'AM' if am else 'PM'}"

def random_time_range(start_time_input: str, end_time_input: str):
    """Get a random time between two times. Adapted from https://codereview.stackexchange.com/questions/274169/get-random-time-between-two-time-inputs
    
    start_time_input and end_time_input are both of the format HH:MM (e.g. '14:25')

    return a new string for a time between the two values
    """
    start_hour, start_minute = start_time_input.split(':')
    end_hour, end_minute = end_time_input.split(':')

    # Get maximum end time for randrange
    if end_hour == '23' and end_minute != '00':
        max_hour = 23 + 1
    else:
        max_hour = end_hour #CHANGED TO end_hour

    if start_minute > end_minute:
        minutes = randrange(int(end_minute), int(start_minute))
    elif start_minute < end_minute:
        minutes = randrange(int(start_minute), int(end_minute))

    hours = ''
    if start_hour == end_hour:
        hours = start_hour
    elif start_hour != end_hour:
        hours = randrange(int(start_hour), int(max_hour))

    if str(hours) == str(end_hour):
        minutes = randrange(int(start_minute)//5, int(end_minute)//5) * 5
    else:
        minutes = randrange(0, 12) * 5

    h = int(hours)
    m = int(minutes)

    return f"{h:02d}:{m:02d}"

def generate_mta_availabilities(min_time: str = '09:00', max_time: str = '17:00', file_path: str | None = 'DATA/mta_type_availability.xlsx') -> pd.DataFrame:
    # Initialize the dataframe
    df = pd.DataFrame(columns=['Type','Availability Day','Availability Start Time','Availability End Time'])
    # Loop through all the MTA types
    for mta_type in mta_types:
        first_entry: bool = True
        # Loop through all the randomly chosen days
        available_days: list[str] = random.sample(days_of_the_week,randrange(1,len(days_of_the_week)))
        for day in available_days:
            # Generate the df entry for this day
            df.loc[len(df)] = [mta_type if first_entry else '',day,*generate_time_tuple(min_time, max_time)]
            first_entry = False

    # Save the file if file_path is given
    if file_path is not None:
        df.to_excel(file_path,index=False,sheet_name='mta_type_availability')    

    return df

def generate_student_unavailabilities(students: list[str], min_time: str = '09:00', max_time: str = '17:00',file_path: str | None = 'DATA/student_unavailability.xlsx') -> pd.DataFrame:
    # Initialize the dataframe
    df = pd.DataFrame(columns=['Student Name','Availability Day','Availability Start Time','Availability End Time'])
    # Loop through all the students
    for student in students:
        first_entry: bool = True
        # Loop through all the randomly chosen days
        available_days: list[str] = random.sample(days_of_the_week,randrange(1,len(days_of_the_week)))
        for day in available_days:
            # Generate the df entry for this day
            df.loc[len(df)] = [student if first_entry else '',day,*generate_time_tuple(min_time,max_time)]
            first_entry = False

    # Save the file if file_path is given
    if file_path is not None:
        df.to_excel(file_path,index=False,sheet_name='student_unavailability')    
    
    return df

def generate_mtas(students: list[str], n: int, max_stuends_per_mta: int = 5, mta_lengths: list[int] = [30,45], file_path: str | None = 'DATA/mtas.xlsx') -> pd.DataFrame: 
    # Initialize the dataframe
    df = pd.DataFrame(columns=['Type','Students','Length (minutes)','Name'])
    # Generate n different MTA's
    for i in range(n):
        # Choose students for the mta
        mta_students: list[str] = random.sample(students,randrange(1,max_stuends_per_mta+1))
        # Choose a random MTA type
        mta_type: str = mta_types[randrange(0,len(mta_types))]
        # Chose a random MTA length
        mta_length = mta_lengths[randrange(0,len(mta_lengths))]
        # Add new values to df
        df.loc[len(df)] = [mta_type,', '.join(mta_students),mta_length,f'MTA {i+1}']

    # Save the file if file_path is given
    if file_path is not None:
        df.to_excel(file_path,index=False,sheet_name='mtas')    

    return df

if __name__ == '__main__':
    print(generate_mtas(generate_students(5),11))
    #generate_student_unavailabilities(generate_students(8))