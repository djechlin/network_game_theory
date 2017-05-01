import math
import game
from gym import spaces
import numpy as np
import networkx as nx


def get_actions(game):
    actions = list(itertools.combinations(list(game.players.keys()), 2))
    # add option to take no action
    actions.append(None)
    return actions

def get_action_space(game):
    actions = get_actions(game)
    return len(actions)

def get_input_space(game):
    return game.rules.nb_players**2

def get_game_graph(game):
    return np.float32(nx.adjacency_matrix(game.graph).todense())


def get_reward(centralities, previous_centrality):
    """
    Returns a reward as a function of the centrality
    """
    return centralities[0]

class NetworkEnv(object):
    """The abstract environment class that is used by all agents. This class has the exact
    same API that OpenAI Gym uses so that integrating with it is trivial. In contrast to the
    OpenAI Gym implementation, this class only defines the abstract methods without any actual
    implementation.
    """
    def __init__(self, game):
        game.initialize_graph()
        self.game = game
        self.rules = game.rules
        self.num_players = game.rules.nb_players
        self.reward_range = (-np.inf, np.inf)

        num_actions = get_action_space(game)
        self.action_space = spaces.Discrete(num_actions)

        shape = (self.num_players, self.num_players)
        self.observation_space = spaces.Box(np.zeros(shape), np.ones(shape))

        # Filled in by _reset()
        self.previous_centrality = 0
        self.round = 0
        self.round_limit = self.game.rules.nb_max_step
        self.state = get_game_graph(self.game).flatten()
        self.done = False

    def step(self, action):
        """Run one timestep of the environment's dynamics.
        Accepts an action and returns a tuple (observation, reward, done, info).
        # Arguments
            action (object): An action provided by the environment.
        # Returns
            observation (object): Agent's observation of the current environment.
            reward (float) : Amount of reward returned after previous action.
            done (boolean): Whether the episode has ended, in which case further step() calls will return undefined results.
            info (dict): Contains auxiliary diagnostic information (helpful for debugging, and sometimes learning).
        """
        possible_actions = get_actions(self.game)
        chosen_action = [possible_actions[action]]
        opponent_actions = list(self.game.get_actions())
        chosen_action.extend(opponent_actions)
        self.game.play_round(actions=chose_action)
        state = get_game_graph(self.game).flatten()
        centralities = nx.betweenness_centrality(self.game.graph)
        # collect reward
        reward = get_reward(centralities, self.previous_centrality)
        self.previous_centrality = centralities[0]
        self.round += 1
        # check if done
        done = self.check_game_objective()
        info = {"rl_action": chosen_action[0], "centralities": centralities}

        return state, reward, done, info

    def check_game_objective(self):
        if self.round == self.round_limit:
            return True
        else:
            return False

    def reset(self):
        """
        Resets the state of the environment and returns an initial observation.
        
        # Returns
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """
        # Filled in by _reset()
        self.game.reset()
        self.previous_centrality = 0
        self.round = 0
        self.round_limit = self.game.rules.nb_max_step
        self.state = get_game_graph(self.game).flatten()
        self.done = False
        return state

    def render(self, mode='human', close=False):
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) 
        
        # Arguments
            mode (str): The mode to render with.
            close (bool): Close all open renderings.
        """
        plotter = game.Plotter()
        plotter.plot_state(self.game)

    def close(self):
        """Override in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        pass

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).
        
        # Returns
            Returns the list of seeds used in this env's random number generators
        """
        return [8110]

    def configure(self, *args, **kwargs):
        """Provides runtime configuration to the environment.
        This configuration should consist of data that tells your
        environment how to run (such as an address of a remote server,
        or path to your ImageNet data). It should not affect the
        semantics of the environment.
        """
        pass

    def __del__(self):
        self.close()

    def __str__(self):
        return '<{} instance>'.format(type(self).__name__)
