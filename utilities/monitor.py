import numpy as np
import matplotlib.pyplot as plt
import csv
import time
#from .helper import get_constant_string
# from constants import *             # Capital lettered variables are constants from the constants.py file

import os


def calculate_moving_avarage(scores, num_agent=1, scores_window=100):
    single_agent_returns = np.transpose(np.array(scores))
    moving_avarages = [np.convolve(single_agent_returns[i], np.ones(scores_window)/scores_window, mode='valid') for i in range(num_agent)]

    return moving_avarages


def calculate_max(scores):
    new_scores = scores.copy()

    for i, episode_score in enumerate(new_scores):
        new_scores[i] = np.delete(episode_score, np.argmin(episode_score))

    print(new_scores[-5:])
    return new_scores


def render_figure(scores, agents, name="", scores_window=0, path="", goal=0, save=False, display= True):
    if len(path) < 1:
        path = 'experiments/saved/'



    # fig, (ax, tb) = plt.subplots(nrows=1, ncols=2)
    fig = plt.figure()

    ax = fig.add_subplot(1, 3, (1, 2))
    tb = fig.add_subplot(1, 3, 3)

    # --- Plot labels --- #
    parameter_string, for_filename = agents[0].get_title()


    ax.set_title(parameter_string[1])
    ax.set_ylabel('Score')
    ax.set_xlabel('Episode #')

    fig.text(0.975, 0.1, parameter_string[0], size=7, color='gray', 
        horizontalalignment='right',
        verticalalignment='top')

    # --- Plot table --- #
    tb.axis('tight')
    tb.axis("off")
    rows = ['# of agents', 'stochasticity', 'grid size', 'agent fixed', 'goal fixed']
    columns = ['Exp1']
    cell_text = [['3'], ['0.7'], ['5 x 5'], ['True'], ['False']]
    he_table = tb.table(cellText=cell_text,
                      rowLabels=rows,
                      colLabels=columns, 
                      loc='center right')


    # --- Plot scores --- #
    if len(agents)>1: # multiple agents
        accumulated_by_agent = np.transpose(np.array(scores))
        for i_agent in range(len(agents)):
            ax.plot(np.arange(1, len(accumulated_by_agent[i_agent])+1), accumulated_by_agent[i_agent])
    else: ax.plot(np.arange(1, len(scores)+1), scores)

    # --- Plot moving avarages --- #
    if scores_window > 0:
        moving_avarages = []
        if len(agents)>1: moving_avarages = calculate_moving_avarage(scores, len(agents), scores_window=scores_window)
        else: moving_avarages = calculate_moving_avarage([scores], len(agents), scores_window=scores_window)
        best_of_two = calculate_moving_avarage(calculate_max(scores), 1, scores_window=scores_window)

        for i_agent in range(len(moving_avarages)):
            ax.plot(np.arange(len(moving_avarages[i_agent]) + scores_window)[scores_window:], moving_avarages[i_agent], 'g-')
        
        ax.plot(np.arange(len(best_of_two[0]) + scores_window)[scores_window:], best_of_two[0], 'k-')
    if goal > 0.: ax.axhline(y=goal, color='c', linestyle='--')

    fig.tight_layout()

    # --- Save and Display --- #
    if save: fig.savefig("{}{}_figure_{}.jpg".format(path, time.strftime("%Y-%m-%d_%H%M%S"), name), bbox_inches='tight')
    if display: fig.show()




def save_scores(scores, agents, name="",  path=""):
    if len(path) < 1:
        path = 'experiments/saved/'

    if not os.path.exists(path):
        print("Directory doesn't exist, going to create one first")
        os.makedirs(path)

    _, for_filename = agents[0].get_title()

    with open("{}{}_scores_{}.csv".format(path, time.strftime("%Y-%m-%d_%H%M%S"), name), 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(scores)

    print("Scores saved!")


def read_scores(network_name=''.format(time.strftime("%Y-%m-%d_%H%M")), path=''):
    if len(path) < 1:
        path = 'experiments/saved/'

    if os.path.exists(path):

        # _, for_filename  = get_constant_string()

        with open("{}{}.csv".format(path, network_name), newline='') as f:
            reader = csv.reader(f)
            read_score_history = list(reader)[0]

        parsed = [float(i) for i in read_score_history]

        return parsed

def save_states(states, name="", path=""):
    if len(path) < 1:
        path = 'experiments/saved/'

    with open("{}{}_states_{}.csv".format(path, time.strftime("%Y-%m-%d_%H%M%S"), name), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(states)