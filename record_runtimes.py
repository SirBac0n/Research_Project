import time
from backtrack import backtrack
from MTA_Solver import read_mtas
from domain_helper import get_domains
from problem_instances import generate_problem_instances
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def main():
    """df = pd.DataFrame(columns=["Algorithm", "Num_MTAs", "Runtime", "Result"])
    # Always make 10 students
    num_students = 10
    # Start with 1 MTA and go to 20 MTA's
    for num_mtas in range(1,16):
        print(f"{num_mtas} MTA's")
        num_runs = 15
        backtrack_time: float = 0.0
        backtrack_successes: int = 0
        remembering_no_goods_time: float = 0.0
        remembering_no_goods_successes: int = 0
        for i in range(num_runs):
            generate_problem_instances(num_students,num_mtas)

            # Make sure the Excel spreadsheets have time to update
            #time.sleep(.1)

            # Load MTA's and domains
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

            # Load MTA's and domains
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
"""
    #df.to_csv("temp.xlsx")
    df = pd.read_csv("temp.csv")
    b = df.loc[df["Algorithm"] == "Backtracking"]
    n = df.loc[df["Algorithm"] == "Remembering No Goods"]
    b_avgs = b.groupby("Num_MTAs")["Runtime"].mean()
    n_avgs = n.groupby("Num_MTAs")["Runtime"].mean()
    b_percent = b.groupby("Num_MTAs")['Result'].mean()
    n_percent = n.groupby("Num_MTAs")['Result'].mean()
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    b.plot(kind="scatter", x="Num_MTAs", y="Runtime", ax=ax1)
    b_avgs.plot(kind="line", x="Num_MTAs", y="Runtime", ax=ax1)
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    n.plot(kind="scatter", x="Num_MTAs", y="Runtime", ax=ax2)
    n_avgs.plot(kind="line", x="Num_MTAs", y="Runtime", ax=ax2)
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    b_avgs.plot(kind="line", x="Num_MTAs", y="Runtime", ax=ax3)
    n_avgs.plot(kind="line", x="Num_MTAs", y="Runtime", ax=ax3)
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    b_percent.plot(kind="line", x="Num_MTAs", y="Result", ax=ax4)
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    n_percent.plot(kind="line", x="Num_MTAs", y="Result", ax=ax5)

    plt.show()

if __name__ == '__main__':
    main()

