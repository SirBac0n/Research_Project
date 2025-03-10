import time
from backtrack import backtrack
from MTA_Solver import read_mtas
from domain_helper import get_domains
from problem_instances import generate_problem_instances
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def main():
    result = ""
    result = input("Do you want to create new runtime record ('yes'/'no) ").strip().lower() 
    while result not in ['yes','no']:
        result = input("That was not a valid entry! Do you want to create new runtime record ('yes'/'no) ").strip().lower()    
    if result == 'yes':
        df = pd.DataFrame(columns=["Algorithm", "Number of MTAs", "Runtime", "Result"])
        # Always make 10 students
        num_students = 10
        # Start with 1 MTA and go to 20 MTAs
        for num_mtas in range(1,16):
            print(f"{num_mtas} MTAs")
            num_runs = 50
            backtrack_time: float = 0.0
            backtrack_successes: int = 0
            remembering_no_goods_time: float = 0.0
            remembering_no_goods_successes: int = 0
            for i in range(num_runs):
                generate_problem_instances(num_students,num_mtas)

                # Make sure the Excel spreadsheets have time to update
                #time.sleep(.1)

                # Load MTAs and domains
                mtas = read_mtas()
                domains = get_domains(mtas)
                # Solve and time just using backtracking
                start_time = time.time()
                result = backtrack(mtas,domains,remember_no_goods=False)
                end_time = time.time()
                # Increment if success and add to time
                backtrack_time += (end_time - start_time)
                backtrack_successes += 1 if result else 0

                df.loc[len(df)] = ["Backtracking", num_mtas, (end_time - start_time)*1000, 1 if result else 0]

                # Load MTAs and domains
                mtas = read_mtas()
                domains = get_domains(mtas)
                # Solve and time using remembering no-goods
                start_time = time.time()
                result = backtrack(mtas,domains,remember_no_goods=True)
                end_time = time.time()
                # Increment if success and add to time
                remembering_no_goods_time += (end_time - start_time)
                remembering_no_goods_successes += 1 if result else 0

                df.loc[len(df)] = ["Remembering No Goods", num_mtas, (end_time - start_time)*1000, 1 if result else 0]

                if backtrack_successes != remembering_no_goods_successes:
                    raise ValueError("Successes should be the same!")
        
            # Get the average time
            backtrack_time = backtrack_time / num_runs
            remembering_no_goods_time = remembering_no_goods_time / num_runs

            print(f"\tBacktracking: {backtrack_successes} / {num_runs} succeeded with average time of {backtrack_time*1000} milliseconds")
            print(f"\tRemembering No-Goods: {remembering_no_goods_successes} / {num_runs} succeeded with average time of {remembering_no_goods_time*1000} milliseconds")

        df.to_csv("DATA/runtime_record.csv")
    

    # Read in data and create dataframes
    try:
        df = pd.read_csv("DATA/runtime_record.csv")
    except Exception:
        print("File DATA/runtime_record.csv does not exist. Please create a new runtime record.")
        return
    b = df.loc[df["Algorithm"] == "Backtracking"]
    n = df.loc[df["Algorithm"] == "Remembering No Goods"]
    b_avgs = b.groupby("Number of MTAs")["Runtime"].mean()
    n_avgs = n.groupby("Number of MTAs")["Runtime"].mean()
    b_percent = b.groupby("Number of MTAs")['Result'].mean()
    n_percent = n.groupby("Number of MTAs")['Result'].mean()

    # Create runtime plot for backtracking
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    b.plot(kind="scatter", x="Number of MTAs", y="Runtime", ax=ax1, ylabel="Runtime (milliseconds)")
    b_avgs.plot(kind="line", x="Number of MTAs", y="Runtime", ax=ax1)
    ax1.set_title("Backtracking Runtimes")

    # Create runtime plot for remembering no-goods
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    n.plot(kind="scatter", x="Number of MTAs", y="Runtime", ax=ax2, ylabel="Runtime (milliseconds)", color="orange")
    n_avgs.plot(kind="line", x="Number of MTAs", y="Runtime", ax=ax2, color="orange")
    ax2.set_title("Remembering No-Goods Runtimes")

    # Create runtime comparison chart
    b_avgs.name = "Backtracking Runtimes"
    n_avgs.name = "Remembering No-Goods Runtimes"
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    b_avgs.plot(kind="line", x="Number of MTAs", y="Runtime", ax=ax3, ylabel="Runtime (milliseconds)", legend=True)
    n_avgs.plot(kind="line", x="Number of MTAs", y="Runtime", ax=ax3, legend=True, color="orange")
    ax3.set_title("Runtime Comparison")

    # Create backtracking success rate chart
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    b_percent.plot(kind="line", x="Number of MTAs", y="Result", ax=ax4)
    ax4.set_title("Backtracking Success Rate")

    # Create remembering no-goods success rate chart
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    n_percent.plot(kind="line", x="Number of MTAs", y="Result", ax=ax5, color="orange")
    ax5.set_title("Remembering No-Goods Success Rate")
    
    # Display charts
    plt.show()

if __name__ == '__main__':
    main()

