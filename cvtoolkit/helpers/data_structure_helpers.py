from typing import Dict


def flatten_dict_to_list_of_dicts(dictionary: Dict[str, list]) -> list:
    """
    Flattens a dictionary to a list of dictionaries.

    Parameters
    ----------
    dictionary : Dict[str, List[Dict[str, list]]]
        A dictionary containing lists grouped by some key.

    Returns
    -------
    list
        A flattened list of dictionaries.
    """
    return [item for sublist in dictionary.values() for item in sublist]
