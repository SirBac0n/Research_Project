import random
from faker import Faker
from random import randrange
import pandas as pd

# Create initialized global list variables
mta_types: list[str] = ['Preaching','Apologetics','Music','Puppetry','Bible Teaching','Inspirational Writing','Drama','Gospel Art','Sign Language','Worship Leading']
days_of_the_week: list[str] = ['Monday','Tuesday','Wednesday','Thursday','Friday']

def generate_students(n: int) -> list[str]:
    fake: Faker = Faker()
    return [fake.name() for _ in range(n)]

def generate_mta_availability_times(min_time: str, max_time: str, min_hours_dif: int = 1) -> tuple[str, str]:
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

    # if start_seconds == end_seconds:
    #     seconds = start_seconds
    # elif start_seconds > end_seconds:
    #     seconds = randrange(int(start_seconds), int(59))
    # elif start_seconds < end_seconds:
    #     seconds = randrange(int(start_seconds), int(end_seconds))

    h = int(hours)
    m = int(minutes)
    #am: bool = True if h < 12 else False
    #h = h if am else h % 12

    return f"{h:02d}:{m:02d}" #:00 {'AM' if am else 'PM'}

def generate_mta_availabilities(min_time: str = '09:00', max_time: str = '17:00',file_path: str | None = 'DATA/mta_type_availability.xlsx') -> pd.DataFrame:
    # Initialize the dataframe
    df = pd.DataFrame(columns=['Type','Availability Day','Availability Start Time','Availability End Time'])
    # Loop through all the MTA types
    for mta_type in mta_types:
        first_entry: bool = True
        # Loop through all the randomly chosen days
        available_days: list[str] = random.sample(days_of_the_week,randrange(1,len(days_of_the_week)))
        for day in available_days:
            # Generate the df entry for this day
            df.loc[len(df)] = [mta_type if first_entry else '',day,*generate_mta_availability_times(min_time, max_time)]
            first_entry = False

    # Save the file if file_path is given
    if file_path is not None:
        df.to_excel(file_path,index=False)    

    return df

if __name__ == '__main__':
    generate_mta_availabilities()