import time
from backtrack import backtrack
from MTA_Solver import read_mtas
from domain_helper import get_domains
from problem_instances import generate_problem_instances


def main():
    # Always make 10 students
    num_students = 10
    # Start with 1 MTA and go to 20 MTA's
    for num_mtas in range(1,21):
        print(f"{num_mtas} MTA's")
        num_runs = 5
        backtrack_time: float = 0.0
        backtrack_successes: int = 0
        remembering_no_goods_time: float = 0.0
        remembering_no_goods_successes: int = 0
        for _ in range(num_runs):
            generate_problem_instances(num_students,num_mtas)
            mtas = read_mtas()
            domains = get_domains(mtas)
            # Make sure the Excel spreadsheets have time to update
            time.sleep(.5)

            # Solve and time just using backtracking
            start_time = time.time()
            result = backtrack(mtas,domains,remember_no_goods=False)
            end_time = time.time()
            # Increment if success and add to time
            backtrack_time += (end_time - start_time)
            backtrack_successes += 1 if result else 0

            # Solve and time using remembering no-goods
            start_time = time.time()
            result = backtrack(mtas,domains,remember_no_goods=True)
            end_time = time.time()
            # Increment if success and add to time
            remembering_no_goods_time += (end_time - start_time)
            remembering_no_goods_successes += 1 if result else 0

        # Get the average time
        backtrack_time = backtrack_time / num_runs
        remembering_no_goods_time = remembering_no_goods_time / num_runs

        print(f"\tBacktracking: {backtrack_successes} / {num_runs} succeeded with average time of {backtrack_time*1000} milliseconds")
        print(f"\tRemembering No-Goods: {remembering_no_goods_successes} / {num_runs} succeeded with average time of {remembering_no_goods_time*1000} milliseconds")

if __name__ == '__main__':
    main()

