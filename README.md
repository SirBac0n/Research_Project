# Running the program

## Record runtimes
To record the runtimes of both algorithms, run the record_runtimes.py file. Alternatively, you can display the results of a previous runtime record if a file named runtime_record.csv exists in the DATA folder. 

## Run test instance

### Create problem instance
To create a problem instance edit the excel files named mta_type_availability.xlsx, mtas.xlsx, and student_unavailability.xlsx. Alternitavely, the user can run the problem_instances.py file which will prompt the user to enter the desired number of students and MTAs and will randomly create a number of students and MTAs based on user input. 

### Run the test
To run a simple test instance run the backtrack.py file. The backtrack.py file will prompt the user to specify whether they want to run backtracking search or remembering no goods and the desired buffer time between MTAs. The program will then take the input and run the desired algorithm and print the result.