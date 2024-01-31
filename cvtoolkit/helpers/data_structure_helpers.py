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

    Example
    -------
    input_dict = {
        'group1': [
            {'gender': 'Male', 'age': 25, 'skin_tone': 'Light'},
            {'gender': 'Female', 'age': 30, 'skin_tone': 'Light'}
        ],
        'group2': [
            {'gender': 'Male', 'age': 22, 'skin_tone': 'Medium'},
            {'gender': 'Female', 'age': 28, 'skin_tone': 'Dark'}
        ]
    }

    result_list = flatten_dict_to_list_of_dicts(input_dict)

    result_list = [
        {'gender': 'Male', 'age': 25, 'skin_tone': 'Light'},
        {'gender': 'Female', 'age': 30, 'skin_tone': 'Light'},
        {'gender': 'Male', 'age': 22, 'skin_tone': 'Medium'},
        {'gender': 'Female', 'age': 28, 'skin_tone': 'Dark'}
    ]
    """
    return [item for sublist in dictionary.values() for item in sublist]
