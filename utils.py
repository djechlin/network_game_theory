import game

strategy_builder = game.StrategyBuilder()

def create_inactive_player(name, rules):
    player = game.Player()
    player.rules = rules
    player.name = name
    player.type = game.EntityType.competitive_player
    player.strategy = strategy_builder.get_inactive_strategy()
    return player

def create_greedy_player(name, rules):
    player = game.Player()
    player.rules = rules
    player.name = name
    player.type = game.EntityType.competitive_player
    player.strategy = strategy_builder.get_greedy_strategy()
    return player

def create_approx_greedy_player(name, rules, eps=.3, delta=.3):
    player = game.Player()
    player.rules = rules
    player.name = name
    player.type = game.EntityType.competitive_player
    player.strategy = strategy_builder.get_approx_greedy_strategy(EPSILON=eps, DELTA=delta)
    return player

def add_players(game, players):
    for player in players:
        game.add_player(game)
    return game