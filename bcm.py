# Author: Richard Hohensinner

# imports:
import os
import numpy as np
import matplotlib.pylab as pylab
from matplotlib import pyplot as plt
import random

# global variables (inputs)
num_agents = 100
num_iterations = 10000
d = 0.2
mu = 0.5

t2_ds = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]

iteration_steps = [0, 5, 10, 25, 50, 75, 90, 100, 500, 1000]

num_clusters_list = []


def main():
    print("Task 1:")
    task1(num_agents, num_iterations, d, mu)
    #task1_ad(num_agents, num_iterations, d, mu, 1000)
    print("Task 2:")
    task2(num_agents, num_iterations, t2_ds, mu)

    print("Finished")
    exit(0)


def task1(N, I, d, mu):
    try:
        os.stat("results_task1")
    except:
        os.mkdir("results_task1")

    agents = set_up_model(N=N)
    #print("Before: ", agents)

    t1_handle_model(agents, I, d, mu, True)
    #print("After: ", agents)

    pass


def task1_ad(N, I, d, mu, times):
    try:
        os.stat("results_task1")
    except:
        os.mkdir("results_task1")

    cl_list = []
    for time in range(times):

        agents = set_up_model(N=N)
        cl_list.append(t1_handle_model(agents, I, d, mu, False))

    print("Rounds: " + str(len(cl_list)))
    res = []
    for i in cl_list:
        if i not in res:
            res.append(i)

    res_dict = {}
    cls = "Num of Clusters: "
    for c in res:
        cls += str(c) + " "
        res_dict[c] = cl_list.count(c)

    print(cls)
    for key in res_dict:
        print(str(key) + ": " + str((res_dict[key] / len(cl_list)) * 100) + " %")

    pass


def task2(N, I, ds, mu):
    try:
        os.stat("results_task2")
    except:
        os.mkdir("results_task2")

    for d in ds:
        agents = set_up_model(N=N)
        #print("Before: ", agents)

        t2_handle_model(agents, I, d, mu)
        #print("After: ", agents)

    print(num_clusters_list)
    plot_evolution(num_clusters_list, t2_ds, "results_task2")
    pass


def set_up_model(N):
    agent_list = np.random.uniform(0.0, 1.0, N).tolist()

    return agent_list


def t1_handle_model(agents, I, d, mu, plot):

    old_agents = []
    for it in range(I):
        old_agents = agents
        execute_iteration(agents, d, mu)

        if it in iteration_steps and plot:
            plot_iteration(it, agents, "results_task1")

    res = []
    for i in agents:
        if i not in res:
            res.append(i)
    if plot:
        print("Number of Clusters: " + str(len(res)))

    return len(res)


def t2_handle_model(agents, I, d, mu):
    for it in range(I):
        execute_iteration(agents, d, mu)

    agents.sort()

    rounded_agents = []
    for a in agents:
        rounded_agents.append(round(a, 2))

    res = []
    for i in rounded_agents:
        if i not in res:
            res.append(i)
    num_clusters_list.append(int(len(res)))


def execute_iteration(agents, d, mu):
    # generate randomness
    random.shuffle(agents)

    it = 0
    while it < (len(agents) / 2):

        a = agents[it]
        b = agents[it + 1]

        if abs(a - b) < d:
            agents[it] = a + mu * (b - a)
            agents[it + 1] = b + mu * (a - b)
        it += 2


def plot_iteration(it, agents, path):
    fig = pylab.figure(it)
    agents.sort()
    plt.bar(range(len(agents)), agents)
    plt.title("Iteration step: " + str(it))
    fig.savefig(path + "/" + str(it) + ".png")
    fig.show()


def plot_evolution(clusters, ds, path):
    fig = pylab.figure(999)
    plt.scatter(ds, clusters)
    plt.ylabel("#Clusters (c)")
    plt.xlabel("Threshold (d)")
    plt.title("Threshold (0.1 - 0.6)")
    fig.savefig(path + "/" + str("change_ds") + ".png")
    fig.show()



if __name__ == "__main__":
    main()