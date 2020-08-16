import random

def train_q_learning(actions,
                     SOLVED_STATE,
                     learning_rate,
                     discount_factor,
                     base_exploration_rate,
                     num_episodes=1e4,
                     reward_dict={"win":1, "loss":-1, "draw":0, "move":-0.05}):
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
        # play episode
        state_hist = play_episode(start_state,
                                  actions,
                                  SOLVED_STATE,
                                  Q_table,
                                  exploration_rate,
                                  max_moves=500,
                                  discount_factor=discount_factor,
                                  learning_rate=learning_rate,
                                  reward_dict=reward_dict,
                                  N_table=N_table)
        exploration_rate *= base_exploration_rate
        games.append(state_hist)

    # print("final exploration rate:", exploration_rate)
    
    return Q_table, N_table, games


def play_episode(start_state,
                 actions,
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
    state_history = [start_state]
    n_moves = 0
    while n_moves <= max_moves:
        state_tuple = tuple(state)
        state_history.append(state_tuple)

        if len(state_history) > 1:
            # we know the state that resulted from the last action
            update_q_table(state_history,
                           action_history,
                           actions,
                           SOLVED_STATE,
                           Q_table,
                           n_moves=n,
                           discount_factor=discount_factor,
                           learning_rate=learning_rate,
                           reward_dict=reward_dict,
                           max_moves=max_moves,
                           N_table=N_table)

        action = choose_Q_action(state_tuple,
                                 actions,
                                 Q_table,
                                 exploration_rate=exploration_rate)
        action_history.append(action)
        perform_action(state_tuple, action)

        n_moves += 1
    return state_history


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
                  max_moves=max_moves):
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