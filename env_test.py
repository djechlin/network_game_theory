from networkenv import NetworkEnv
import game

from utils import create_greedy_player

# create some rules for the game
r = game.Rules()
r.nb_max_step = 20
r.nb_players = 10
# create a game with these rules
g = game.Game(r)
greedy_player = create_greedy_player("test", r)
g.add_player(greedy_player)

# create an RL environment with with game
env = NetworkEnv(g)

for i in range(10):
	env.step(0)
env.render()

