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

greedy_player2 = create_greedy_player("test", r)
g.add_player(greedy_player2)


# create an RL environment with with game
env = NetworkEnv(g)

total_reward = 0
for i in range(20):
	s, r, d, i = env.step(0)
	total_reward += r
print(total_reward)
env.render()


