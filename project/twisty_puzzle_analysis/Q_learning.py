import random
from twisty_puzzle_model import scramble, perform_action
from math import ceil
from copy import deepcopy

def train_q_learning(actions,
                     SOLVED_STATE,
                     learning_rate,
                     discount_factor,
                     base_exploration_rate,
                     max_moves=100,
                     num_episodes=1e4,
                     reward_dict={"solved":5, "timeout":-1, "move":-0.01}):
    """
    play Tic Tac Toe [num_episodes] times to learn using Q-Learning with the given learning rate and discount_factor.
    inputs:
        learning_rate - (float) in range [0,1] - alpha
        discount_factor - (float) in range [0,1] - gamma
        base_exploration_rate - (float) - the starting exploration rate
        num_episodes - (int) - number of episodes for training
        reward_dict - (dict) - a dictionary specifying the rewards for winning, losing and draw
            -> must have keys "win", "loss", "draw"
    returns:
        (dict) - the Q-table after training with the given parameters
    """
    Q_table = dict()    # assign values to every visited state-action pair
    N_table = dict()    # counting how often each state-action pair was visited
    action_dict = dict()    # save the possible actions for each state

    games = []
    scramble_hist = []
    exploration_rate = base_exploration_rate
    for n in range(num_episodes):
        max_scramble_moves = ceil((1+n)/500)
        start_state = deepcopy(SOLVED_STATE)
        scramble_hist.append(scramble(start_state, actions, max_moves=max_scramble_moves))
        # play episode
        state_hist, action_hist = play_episode(start_state,
                                  actions,
                                  SOLVED_STATE,
                                  Q_table,
                                  exploration_rate,
                                  max_moves=max_moves,
                                  discount_factor=discount_factor,
                                  learning_rate=learning_rate,
                                  reward_dict=reward_dict,
                                  N_table=N_table)
        exploration_rate -= base_exploration_rate/(2*num_episodes)
        games.append((scramble_hist[-1], state_hist, action_hist))

    print("final exploration rate:", exploration_rate)

    return Q_table, N_table, games


def play_episode(start_state,
                 actions_dict,
                 SOLVED_STATE,
                 Q_table,
                 exploration_rate,
                 max_moves=500,
                 discount_factor=0.95,
                 learning_rate=0.1,
                 reward_dict={"solved":5, "timeout":-1, "move":-0.01},
                 N_table=dict()):
    """
    self-play an entire episode
    inputs:
    -------
        start_state - (list) - any scrambled state of the puzzle
        Q_table - (dict) - 
        actions - (dict) - list of all possible actions (values) and their names (keys)
        exploration_rate - (float) - 
        max_moves - (int) - maximum number of moves the AI has to solve the puzzle
        discount_factor - (float) - 
        learning_rate - (float) - 
        reward_dict - (dict) - dict containing rewards for certain events must have keys:
            - "solved" - reward for solving the puzzle
            - "timeout" - reward/penalty for not solving the puzzle within max_steps
            - "move" - reward/penalty for each move
        N_table - (dict) - a dictionary where we count how often each state was visited
    returns:
    --------
        (list) - scramble history
        (list) - state history
        (list) - action history
    
    action_dict is changed in-place
    """ 
    state = start_state
    sign = 1
    action_history = []
    state_history = [tuple(start_state)]
    n_moves = 0
    while n_moves <= max_moves:
        state_tuple = tuple(state)
        state_history.append(state_tuple)
        
        action = choose_Q_action(state_tuple,
                                 actions_dict,
                                 Q_table,
                                 exploration_rate=exploration_rate)
        action_history.append(action)

        if len(state_history) > 1:
            # we know the state that resulted from the last action
            update_q_table(state_history,
                           action_history,
                           actions_dict,
                           SOLVED_STATE,
                           Q_table,
                           n_moves=n_moves,
                           discount_factor=discount_factor,
                           learning_rate=learning_rate,
                           reward_dict=reward_dict,
                           max_moves=max_moves,
                           N_table=N_table)

        if puzzle_solved(state, SOLVED_STATE, n_moves, max_moves=max_moves) == "solved":
            break

        perform_action(state, actions_dict[action])
        n_moves += 1
        # print(n_moves, max_moves)
    # if puzzle_solved(state, SOLVED_STATE, n_moves, max_moves=max_moves) == "solved":
    #     print("won", n_moves)
    # else:
    #     print("lost", n_moves)
    return state_history, action_history


def update_q_table(state_history,
                   action_history,
                   actions,
                   SOLVED_STATE,
                   Q_table,
                   n_moves=0,
                   discount_factor=0.95,
                   learning_rate=0.1,
                   reward_dict={"solved":5, "timeout":-1, "move":-0.01},
                   max_moves=500,
                   N_table=dict()):
    """
    update the last state in the Q-table
    returns:
        None
    """
    prev_state = state_history[-2] # S = state
    prev_action = action_history[-1] # A = action
    state = state_history[-1] # S' = next state after action A

    reward = get_reward(list(state),
                        SOLVED_STATE,
                        n_moves,
                        reward_dict=reward_dict,
                        max_moves=max_moves) # R = Reward
    next_rewards = [] # Q(S', a') for all actions a'
    for action in actions:
        try:
            next_rewards.append(Q_table[(state, action)])
        except KeyError:
            Q_table[(state, action)] = 0
            N_table[(state, action)] = 0
            next_rewards.append(0)
    # initialize q-value as 0
    if not (prev_state, prev_action) in Q_table.keys():
        print("second Q-table initialization") #debug
        Q_table[(prev_state, prev_action)] = 0
        N_table[(prev_state, prev_action)] = 0
    # actually update the q-value of the considered move
    # Q(S,A) += alpha*(R + gamma * max(S', a') - Q(S,A))
    Q_table[(prev_state, prev_action)] += learning_rate*(reward + discount_factor * max(next_rewards, default=0) - Q_table[(prev_state, prev_action)])
    N_table[(prev_state, prev_action)] += 1


def get_reward(state,
               SOLVED_STATE,
               n_moves,
               reward_dict={"solved":5, "timeout":-1, "move":-0.01},
               max_moves=500):
    """
    return the reward for the given state and possible actions
    inputs:
    -------
        state - (tuple) or (list) - the state as a tuple or list
        reward_dict - (dict) - dict with specific rewards must have keys:
            - "solved" - reward for solving the puzzle
            - "timeout" - reward/penalty for not solving the puzzle within max_steps
            - "move" - reward/penalty for each move
    """
    puzzle_state = puzzle_solved(state,
                                 SOLVED_STATE,
                                 n_moves,
                                 max_moves=max_moves)
    if puzzle_state == "solved": #draw
        # print("won")
        reward = reward_dict["solved"]
    elif puzzle_state == "timeout":
        print("timeout")
        reward = reward_dict["timeout"]
    else:
        reward = reward_dict["move"]
    return reward


def puzzle_solved(state,
                  SOLVED_STATE,
                  n_moves,
                  max_moves=500):
    """
    determine the current puzzle state:
    returns:
    --------
        (str) - 'solved' if the puzzle is solved according to SOLVED_STATE
                'timeout' if n_moves > max_moves
    """
    if state == SOLVED_STATE:
        return "solved"
    elif n_moves > max_moves:
        return "timeout"


def choose_Q_action(state, actions, Q_table, exploration_rate=0):
    """
    choose an action based on the possible actions, the current Q-table and the current exploration rate
    inputs:
    -------
        state - (tuple) or (list) - the state as a tuple or list
        actions (tuple) or (list) - all possible actions in the given state
        Q_table - (dict) - dictionary storing all known Q-values
        exploration_rate - (float) in [0,1] - probability of choosing exploration rather than exploitation
    """
    r = random.random()
    if r > exploration_rate:
        # exploit knowledge
        action_values = []
        for action_key in actions.keys():
            try:
                action_values.append(Q_table[(state,action_key)])
            except KeyError:
                action_values.append(0)
        max_value = max(action_values)
        best_actions = []
        for action_key, value in zip(actions, action_values):
            if value == max_value:
                best_actions.append(action_key)
        # return random action with maximum expected reward
        return random.choice(best_actions)
    # explore environment through random move
    return random.choice(list(actions.keys()))


# if __name__ == "__main__":
#     """
#     example: floppy cube
#     """
#     actions = {"f" : [[20, 18], [4, 7], [16, 2], [27, 23], [17, 3]],
#                "r" : [[2, 9], [7, 0], [18, 26], [1, 8], [23, 21]],
#                "b" : [[26, 24], [21, 29], [9, 6], [0, 12], [11, 10]],
#                "l" : [[16, 6], [12, 4], [15, 5], [27, 29], [20, 24]]}
#     solved_state = [0,0,0,0,0,0,0,1,1,1,0,1,1,0,1,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5]
#     reward_dict={"solved":5,
#                  "timeout":-1,
#                  "move":-0.01}

#     Q_table, N_table, games = train_q_learning(actions,
#                                                solved_state,
#                                                learning_rate=0.1,
#                                                discount_factor=0.99,
#                                                base_exploration_rate=0.9999,
#                                                num_episodes=10_000,
#                                                reward_dict=reward_dict)
#     def export_Q_table(Q_table, filename="Q_table.txt"):
#         """
#         write the given Q-table into a file
#         """
#         with open(filename, "w") as file:
#             file.write("Q_table = {\n")
#             for key, value in Q_table.items():
#                 file.write(str(key) + ":" + str(value) + ",\n")
#             file.write("}")

#     export_Q_table(Q_table, filename="floppy_q_table.txt")
#     # colors: 0=white 1=yellow 2=green 3=red 4=blue 5=orange