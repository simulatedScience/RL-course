class puzzle_ai():
    def __init__(self, ACTIONS_DICT, SOLVED_STATE, reward_dict, name="twisty_puzzle #0", learning_rate=0.02, discount_factor=0.95, base_exploration_rate=0.7):
        """
        """
        self.name = name
        self.ACTIONS_DICT = ACTIONS_DICT
        self.SOLVED_STATE = SOLVED_STATE

        self.reward_dict = reward_dict
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.base_exploration_rate = base_exploration_rate

        self.Q_table = None
        self.N_table = None

    def train_q_learning(self, reward_dict=None, learning_rate=None, discount_factor=None, base_exploration_rate=None, keep_Q_table=True):
        """
        play Tic Tac Toe [num_episodes] times to learn using Q-Learning with the given learning rate and discount_factor.
        inputs:
            learning_rate - (float) in range [0,1] - alpha
            discount_factor - (float) in range [0,1] - gamma
            base_exploration_rate - (float) - the starting exploration rate
            num_episodes - (int) - number of episodes for training
            reward_dict - (dict) - dict containing rewards for certain events must have keys:
                - "solved" - reward for solving the puzzle
                - "timeout" - reward/penalty for not solving the puzzle within max_steps
                - "move" - reward/penalty for each move
            keep_Q_table - (bool) - whether or not to keep the existing Q-table or retrain the AI from scratch
        returns:
            (list) or tuples - information about the training games:
                tuples include: 
                    scrambles
                    state_history
                    action_history
        """
        if self.Q_table == None:
            self.Q_table = dict()    # assign values to every visited state-action pair
        if self.N_table == None:
            self.N_table = dict()    # counting how often each state-action pair was visited

        games = []
        scramble_hist = []
        exploration_rate = self.base_exploration_rate
        for n in range(num_episodes):
            max_scramble_moves = ceil((1+n)/500)
            start_state = deepcopy(self.SOLVED_STATE)
            scramble_hist.append(scramble(start_state, self.ACTIONS_DICT, max_moves=max_scramble_moves))
            # play episode
            state_hist, action_hist = play_episode(start_state,
                                                   max_moves=max_moves)
            exploration_rate -= self.base_exploration_rate/(2*num_episodes)
            games.append((scramble_hist[-1], state_hist, action_hist))

        print("final exploration rate:", exploration_rate)

        return games


    def play_episode(self,
                    start_state,
                    max_moves=500):
        """
        self-play an entire episode
        inputs:
        -------
            start_state - (list) - any scrambled state of the puzzle
            max_moves - (int) - maximum number of moves the AI has to solve the puzzle
        returns:
        --------
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
                                     Q_table,
                                     exploration_rate=exploration_rate)
            action_history.append(action)

            if len(state_history) > 1:
                # we know the state that resulted from the last action
                update_q_table(state_history,
                               action_history,
                               n_moves=n_moves,
                               max_moves=max_moves)

            if puzzle_solved(state, n_moves, max_moves=max_moves) == "solved":
                break

            perform_action(state, self.ACTIONS_DICT[action])
            n_moves += 1
            # print(n_moves, max_moves)
        # if puzzle_solved(state, self.SOLVED_STATE, n_moves, max_moves=max_moves) == "solved":
        #     print("won", n_moves)
        # else:
        #     print("lost", n_moves)
        return state_history, action_history


    def update_q_table(self,
                       state_history,
                       action_history,
                       n_moves=0,
                       max_moves=500):
        """
        update the last state in the Q-table
        returns:
            None
        """
        prev_state = state_history[-2] # S = state
        prev_action = action_history[-1] # A = action
        state = state_history[-1] # S' = next state after action A

        reward = get_reward(list(state),
                            n_moves,
                            max_moves=max_moves) # R = Reward
        next_rewards = [] # Q(S', a') for all actions a'
        for action in self.ACTIONS_DICT:
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
        Q_table[(prev_state, prev_action)] += self.learning_rate*(reward + self.discount_factor * max(next_rewards, default=0) - Q_table[(prev_state, prev_action)])
        N_table[(prev_state, prev_action)] += 1


    def get_reward(self,
                state,
                n_moves,
                max_moves=500):
        """
        return the reward for the given state and possible actions
        inputs:
        -------
            state - (tuple) or (list) - the state as a tuple or list
            n_moves - (int) - current number of moves performed
            max_moves - (int) - maximum allowed number of moves before timeout
        """
        puzzle_state = puzzle_solved(state,
                                    n_moves,
                                    max_moves=max_moves)
        if puzzle_state == "solved": #draw
            # print("won")
            reward = self.reward_dict["solved"]
        elif puzzle_state == "timeout":
            print("timeout")
            reward = self.reward_dict["timeout"]
        else:
            reward = self.reward_dict["move"]
        return reward


    def puzzle_solved(self,
                      state,
                      n_moves,
                      max_moves=500):
        """
        determine the current puzzle state:
        returns:
        --------
            (str) - 'solved' if the puzzle is solved according to SOLVED_STATE
                    'timeout' if n_moves > max_moves
        """
        if state == self.SOLVED_STATE:
            return "solved"
        elif n_moves > max_moves:
            return "timeout"


    def choose_Q_action(self, state, exploration_rate=0):
        """
        choose an action based on the possible actions, the current Q-table and the current exploration rate
        inputs:
        -------
            state - (tuple) or (list) - the state as a tuple or list
            Q_table - (dict) - dictionary storing all known Q-values
            exploration_rate - (float) in [0,1] - probability of choosing exploration rather than exploitation
        """
        r = random.random()
        if r > exploration_rate:
            # exploit knowledge
            action_values = []
            for action_key in self.ACTIONS_DICT.keys():
                try:
                    action_values.append(Q_table[(state,action_key)])
                except KeyError:
                    action_values.append(0)
            max_value = max(action_values)
            best_actions = []
            for action_key, value in zip(self.ACTIONS_DICT, action_values):
                if value == max_value:
                    best_actions.append(action_key)
            # return random action with maximum expected reward
            return random.choice(best_actions)
        # explore environment through random move
        return random.choice(list(self.ACTIONS_DICT.keys()))
