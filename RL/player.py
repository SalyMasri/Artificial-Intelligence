#!/usr/bin/env python3
import random
import numpy as np

from agent import Fish
from communicator import Communicator
from shared import SettingLoader


class FishesModelling:
    def init_fishes(self, n):
        fishes = {}
        for i in range(n):
            fishes["fish" + str(i)] = Fish()
        self.fishes = fishes


class PlayerController(SettingLoader, Communicator):
    def __init__(self):
        SettingLoader.__init__(self)
        Communicator.__init__(self)
        self.space_subdivisions = 10
        self.actions = None
        self.action_list = None
        self.states = None
        self.init_state = None
        self.ind2state = None
        self.state2ind = None
        self.alpha = 0
        self.gamma = 0
        self.episode_max = 300

    def init_states(self):
        ind2state = {}
        state2ind = {}
        count = 0
        for row in range(self.space_subdivisions):
            for col in range(self.space_subdivisions):
                ind2state[(col, row)] = count
                state2ind[count] = [col, row]
                count += 1
        self.ind2state = ind2state
        self.state2ind = state2ind

    def init_actions(self):
        self.actions = {
            "left": (-1, 0),
            "right": (1, 0),
            "down": (0, -1),
            "up": (0, 1)
        }
        self.action_list = list(self.actions.keys())

    def allowed_movements(self):
        self.allowed_moves = {}
        for s in self.ind2state.keys():
            self.allowed_moves[self.ind2state[s]] = []
            if s[0] < self.space_subdivisions - 1:
                self.allowed_moves[self.ind2state[s]] += [1]
            if s[0] > 0:
                self.allowed_moves[self.ind2state[s]] += [0]
            if s[1] < self.space_subdivisions - 1:
                self.allowed_moves[self.ind2state[s]] += [3]
            if s[1] > 0:
                self.allowed_moves[self.ind2state[s]] += [2]

    def player_loop(self):
        pass


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


def epsilon_greedy(Q,
                   state,
                   all_actions,
                   current_total_steps=0,
                   epsilon_initial=1,
                   epsilon_final=0.2,
                   anneal_timesteps=10000,
                   eps_type="constant"):

    if eps_type == 'constant':
        epsilon = epsilon_final
        # ADD YOUR CODE SNIPPET BETWEEN EX 4.1
        # Implemenmt the epsilon-greedy algorithm for a constant epsilon value
        # Use epsilon and all input arguments of epsilon_greedy you see fit
        # It is recommended you use the np.random module
        action = None
        # ADD YOUR CODE SNIPPET BETWEEN EX 4.1

    elif eps_type == 'linear':
        # ADD YOUR CODE SNIPPET BETWEENEX  4.2
        # Implemenmt the epsilon-greedy algorithm for a linear epsilon value
        # Use epsilon and all input arguments of epsilon_greedy you see fit
        # use the ScheduleLinear class
        # It is recommended you use the np.random module
        action = None
        # ADD YOUR CODE SNIPPET BETWEENEX  4.2

    else:
        raise "Epsilon greedy type unknown"

    return action


class PlayerControllerRL(PlayerController, FishesModelling):
    def __init__(self):
        super().__init__()

    def player_loop(self):
        # send message to game that you are ready
        self.init_actions()
        self.init_states()
        self.alpha = self.settings.alpha
        self.gamma = self.settings.gamma
        self.epsilon_initial = self.settings.epsilon_initial
        self.epsilon_final = self.settings.epsilon_final
        self.annealing_timesteps = self.settings.annealing_timesteps
        self.threshold = self.settings.threshold
        self.episode_max = self.settings.episode_max

        q = self.q_learning()

        # compute policy
        policy = self.get_policy(q)

        # send policy
        msg = {"policy": policy, "exploration": False}
        self.sender(msg)

        msg = self.receiver()
        print("Q-learning returning")
        return

    def q_learning(self):
        ns = len(self.state2ind.keys())
        na = len(self.actions.keys())
        discount = self.gamma
        lr = self.alpha
        # initialization
        self.allowed_movements()
        # ADD YOUR CODE SNIPPET BETWEEN EX. 2.1
        # Initialize a numpy array with ns state rows and na state columns with float values from 0.0 to 1.0.
        Q = None
        # ADD YOUR CODE SNIPPET BETWEEN EX. 2.1

        for s in range(ns):
            list_pos = self.allowed_moves[s]
            for i in range(4):
                if i not in list_pos:
                    Q[s, i] = np.nan

        Q_old = Q.copy()

        diff = np.infty
        end_episode = False

        init_pos_tuple = self.settings.init_pos_diver
        init_pos = self.ind2state[(init_pos_tuple[0], init_pos_tuple[1])]
        episode = 0

        R_total = 0
        current_total_steps = 0
        steps = 0

        # ADD YOUR CODE SNIPPET BETWEEN EX. 2.3
        # Change the while loop to incorporate a threshold limit, to stop training when the mean difference
        # in the Q table is lower than the threshold
        while episode <= self.episode_max:
            # ADD YOUR CODE SNIPPET BETWEENEX. 2.3

            s_current = init_pos
            R_total = 0
            steps = 0
            while not end_episode:
                # selection of action
                list_pos = self.allowed_moves[s_current]

                # ADD YOUR CODE SNIPPET BETWEEN EX 2.1 and 2.2
                # Chose an action from all possible actions
                action = None
                # ADD YOUR CODE SNIPPET BETWEEN EX 2.1 and 2.2

                # ADD YOUR CODE SNIPPET BETWEEN EX 5
                # Use the epsilon greedy algorithm to retrieve an action
                # ADD YOUR CODE SNIPPET BETWEEN EX 5

                # compute reward
                action_str = self.action_list[action]
                msg = {"action": action_str, "exploration": True}
                self.sender(msg)

                # wait response from game
                msg = self.receiver()
                R = msg["reward"]
                R_total += R
                s_next_tuple = msg["state"]
                end_episode = msg["end_episode"]
                s_next = self.ind2state[s_next_tuple]

                # ADD YOUR CODE SNIPPET BETWEEN EX. 2.2
                # Implement the Bellman Update equation to update Q
                # ADD YOUR CODE SNIPPET BETWEEN EX. 2.2

                s_current = s_next
                current_total_steps += 1
                steps += 1

            # ADD YOUR CODE SNIPPET BETWEEN EX. 2.3
            # Compute the absolute value of the mean between the Q and Q-old
            diff = 100
            # ADD YOUR CODE SNIPPET BETWEEN EX. 2.3
            Q_old[:] = Q
            print(
                "Episode: {}, Steps {}, Diff: {:6e}, Total Reward: {}, Total Steps {}"
                .format(episode, steps, diff, R_total, current_total_steps))
            episode += 1
            end_episode = False

        return Q

    def get_policy(self, Q):
        max_actions = np.nanargmax(Q, axis=1)
        policy = {}
        list_actions = list(self.actions.keys())
        for n in self.state2ind.keys():
            state_tuple = self.state2ind[n]
            policy[(state_tuple[0],
                    state_tuple[1])] = list_actions[max_actions[n]]
        return policy


class PlayerControllerRandom(PlayerController):
    def __init__(self):
        super().__init__()

    def player_loop(self):
        """
        Main loop for the random agent.
        """
        # Initialize states, actions, and allowed movements
        self.init_actions()
        self.init_states()
        self.allowed_movements()

        # Execute the random agent logic
        action_counts = self.random_agent()

        # Compute and send the policy
        policy = self.get_policy(action_counts)
        self.sender({"policy": policy, "exploration": False})

        # Await confirmation
        self.receiver()
        print("Random Agent completed.")

    def random_agent(self):
        """
        Implements a random agent to interact with the environment.
        """
        num_states = len(self.state2ind.keys())
        num_actions = len(self.actions.keys())

        # Precompute allowed actions for states
        allowed_moves_array = {
            state: np.array(actions)
            for state, actions in self.allowed_moves.items()
        }

        # Initialize action counts
        action_counts = np.zeros((num_states, num_actions), dtype=int)

        # Retrieve initial position
        init_state = self.ind2state[tuple(self.settings.init_pos_diver)]

        for episode in range(self.episode_max):
            current_state = init_state
            steps = 0

            while steps < self.settings.episode_len:
                # Randomly sample an action
                actions = allowed_moves_array[current_state]
                chosen_action = np.random.choice(actions)
                action_counts[current_state, chosen_action] += 1

                # Send the action to the environment
                action_str = self.action_list[chosen_action]
                self.sender({"action": action_str, "exploration": True})

                # Receive feedback
                msg = self.receiver()
                if msg["end_episode"]:
                    break

                # Update the current state
                current_state = self.ind2state[tuple(msg["state"])]
                steps += 1

        return action_counts

    def get_policy(self, action_counts):
        """
        Computes the policy based on the most frequently selected actions.
        """
        policy = {}
        for state_index, actions in enumerate(action_counts):
            best_action_index = np.argmax(actions)
            best_action = self.action_list[best_action_index]
            state_tuple = self.state2ind[state_index]
            policy[tuple(state_tuple)] = best_action
        return policy




class ScheduleLinear(object):
    def __init__(self, schedule_timesteps, final_p, initial_p=1.0):
        self.schedule_timesteps = schedule_timesteps
        self.final_p = final_p
        self.initial_p = initial_p

    def value(self, t):
        # ADD YOUR CODE SNIPPET BETWEEN EX 4.2
        # Return the annealed linear value
        return self.initial_p
        # ADD YOUR CODE SNIPPET BETWEEN EX 4.2
