from typing import Dict, List, Set, Tuple, Any, Callable
from ngt.rules import Rules, ActionSpace

from ngt.functions.action import Action

import pickle
import os
import errno


def fetch_adequate_function(rules: Rules, functions: Dict[ActionSpace, Callable[[Any], Any]]):
    """Helper method to fetch the function adapted to the rules

    Since the action space can vary, the functions can have various signatures. The solution implemented
    is to store all the functions corresponding to each action space in a map and then fetch the
    adequate one using this function. Eg: store greedy_strategy_node (when the action space is the set of nodes)
    and greedy_strategy_edge (when the action space is the set of edges) and later call the right one according
    to the rules of the game.

    Args:
        rules: Rules of the game
        functions: Map containing the functions associated to an action space

    Returns:
        Valid function according to the rules
    """
    return functions[rules.action_space]


def check_action_type(rules: Rules, action: Any):
    """Helper method to check the action returned by a player is rules compliant

    Args:
        rules: Rules of the game
        action: Action chosen by a player

    Returns:
        Boolean indicating type validity of the action
    """
    if action is None:
        return True
    elif (rules.action_space == ActionSpace.edge or \
          rules.action_space == ActionSpace.dynamic_edge):
        return isinstance(action, Action)
    elif rules.action_space == ActionSpace.node and (type(action) != int):
        return False
    elif rules.action_space == ActionSpace.boolean and (type(action) != bool):
        return False
    else:
        return True


def save_object(obj: Any, dir_name: str, file_name: str, suffix: str = '.pkl') -> None:
    """Helper method to save the game object to a pickle object for persistence

    https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence
    https://stackoverflow.com/questions/7132861/building-full-path-filename-in-python

    Args:
        obj: object to be saved
        dir_name: Directory name
        file_name: File name
        suffix: Suffix

    Returns:
        Boolean indicating if the file has successfully been saved
    """
    file_path = os.path.join(dir_name, file_name + suffix)

    with open(file_path, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(dir_name: str, file_name: str, suffix: str = '.pkl') -> Any:
    """Helper method to save the game object to a pickle object for persistence

    https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence
    https://stackoverflow.com/questions/7132861/building-full-path-filename-in-python

    Args:
        obj: object to be saved
        dir_name: Directory name
        file_name: File name
        suffix: Suffix

    Returns:
        Boolean indicating if the file has successfully been saved
    """
    file_path = os.path.join(dir_name, file_name + suffix)

    with open(file_path, 'rb') as inpt:
        obj = pickle.load(inpt)
        return obj


def make_sure_path_exists(path: str) -> None:
    """Helper method to create a folder

    https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist

    Args:
        path: Folder path to create

    Returns:
        None
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def get_players_id(folder_name: str) -> Set[int]:
    """Helper function to get a set of players' id rom pickle files

    Args:
        folder_name: folder containing pickles of saved game

    Returns:
        Set of players' name
    """
    files = os.listdir(folder_name)
    players_files = filter(lambda x: 'player_' in x, files)
    players_id = map(lambda x: int(x.split('_')[1]), players_files)
    return set(players_id)


def get_increments_id(folder_name: str) -> Set[int]:
    """Helper function to get a set of increments' id (time steps number)

    Args:
        folder_name: folder containing pickles of saved game

    Returns:
        Set of increments' id
    """
    files = os.listdir(folder_name)
    increment_files = filter(lambda x: 'increment_' in x, files)
    increment_id = map(lambda x: int(x.split('_')[1]), increment_files)
    return set(increment_id)
