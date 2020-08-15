import random

def train_q_learning(learning_rate, discount_factor, base_exploration_rate, num_episodes=1e4, reward_dict={"win":1, "loss":-1, "draw":0, "move":-0.05}):
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
    exploration_rate = base_exploration_rate
    for n in range(num_episodes):
        # play episode
        state_hist = play_episode(Q_table, action_dict, exploration_rate, discount_factor, learning_rate, reward_dict, N_table)
        exploration_rate *= base_exploration_rate
        games.append(state_hist)

    # print("final exploration rate:", exploration_rate)
    
    return Q_table, N_table, games


def play_episode(Q_table, action_dict, exploration_rate, discount_factor=0.95, learning_rate=0.1, reward_dict={"win":1, "loss":-1, "draw":0, "move":-0.05}, N_table=dict()):
    """
    self-play an entire episode
    returns:
        (list) - state history
        (list) - action history
    
    action_dict is changed in-place
    """ 
    state = [0 for _ in range(9)]
    sign = 1
    action_history = []
    state_history = []
    while True:
        state_tuple = tuple(state)
        state_history.append(state_tuple)
        # get possible actions
        try:
            actions = action_dict[state_tuple]
        except KeyError:
            actions = get_actions(state)
            action_dict[state_tuple] = actions

        if len(state_history) > 2: 
            # we know the state that resulted from the last action
            update_q_table(Q_table, state_history, action_history, actions, discount_factor, learning_rate, reward_dict, N_table)

        if len(actions) == 0:
            break # game has ended

        action = choose_Q_action(state_tuple, actions, Q_table, exploration_rate=exploration_rate)
        action_history.append(action)
        perform_action(state_tuple, action)

    last_state = state_history[-2]
    last_action = action_history[-1]
    if not (last_state, last_action) in Q_table.keys():
        Q_table[(last_state, last_action)] = 0
        N_table[(last_state, last_action)] = 0
    # print("before", Q_table[(last_state, last_action)])
    Q_table[(last_state, last_action)] += learning_rate*(reward_dict["win"] - Q_table[(last_state, last_action)])
    N_table[(last_state, last_action)] += 1
    
    return state_history


def update_q_table(Q_table, state_history, action_history, actions, discount_factor, learning_rate, reward_dict, N_table):
    """
    update the second to last state in the Q-table
    returns:
        None
    """
    prev_state = state_history[-3] # S = state
    prev_action = action_history[-2] # A = action
    state = state_history[-1] # S' = next state after action A

    reward = get_reward(list(state), actions, reward_dict) # R = Reward
    next_rewards = [] # Q(S', a') for all actions a'
    for action in actions:
        try:
            next_rewards.append(Q_table[(state, action)])
        except KeyError:
            Q_table[(state, action)] = 0
            N_table[(state, action)] = 0
            next_rewards.append(0)

    if not (prev_state, prev_action) in Q_table.keys():
        Q_table[(prev_state, prev_action)] = 0
        N_table[(prev_state, prev_action)] = 0
    if ((1,2,0,0,1,2,0,0,0),8) in Q_table.keys():
        test_value = str(Q_table[((1,2,0,0,1,2,0,0,0),8)])
    # Q(S,A) += alpha*(R + gamma * max(S', a') - Q(S,A))
    Q_table[(prev_state, prev_action)] += learning_rate*(reward + discount_factor * max(next_rewards, default=0) - Q_table[(prev_state, prev_action)])
    N_table[(prev_state, prev_action)] += 1
    if ((1,2,0,0,1,2,0,0,0),8) in Q_table.keys():
        if test_value != str(Q_table[((1,2,0,0,1,2,0,0,0),8)]):
            print("old value:", test_value)
            print("reward was", reward)
            print("new value:", Q_table[((1,2,0,0,1,2,0,0,0),8)])


def get_reward(state, actions, reward_dict, max_steps=500):
    """
    return the reward for the given state and possible actions
    inputs:
    -------
        state - ()
        action - 
        reward_dict - (dict) - dict with specific rewards must have keys:
            - "solved"
    """
    puzzle_state = puzzle_solved(state, max_steps=max_steps)
    if puzzle_state == "solved": #draw
        reward = reward_dict["solved"]
    elif puzzle_state == "timeout":
        reward = reward_dict["timeout"]
    else:
        reward = reward_dict["move"]
    return reward


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
        # print("exploit", r, exploration_rate)
        # exploit knowledge
        action_values = []
        for action in actions:
            try:
                action_values.append(Q_table[(state,action)])
            except KeyError:
                action_values.append(0)
        max_value = max(action_values)
        best_actions = []
        for action, value in zip(actions, action_values):
            if value == max_value:
                best_actions.append(action)
        # return random action with maximum expected reward
        return random.choice(best_actions)
    # explore environment through random move
    return random.choice(actions)


def perform_action(state, action):
    """
    perform the given action on the given state in-place
    for twisty puzzles this means applying the permutations of a move

    inputs:
        state - (list) of ints - list representing the state
        action - (list) of lists of ints - list representing an action, here as a list of cycles
            cycles are lists of list indices of the state list.
    """
    for cycle in action:
        j = cycle[0]
        for i in cycle:
            state[i], state[j] = state[j], state[i]

    return state