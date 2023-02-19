import numpy as np
from constants import *


def assign_management_levels_enron(levels, df_employees, df_positions):
    """
    employees position update, based on the number of levels we use for classification

    :type levels: int , number of company hierarchical levels
    :type df_employees: list of employees
    :type df_positions: list of positions of employees

    :rtype: pandas.DataFrame
    """
    if levels == 2:
        df_employees[POSITION] = 2
        # merge first and second management level
        management_level = df_positions[df_positions[POSITION].isin([1, 2])].index
        df_employees.loc[df_employees.index.isin(management_level), POSITION] = 1
    elif levels == 3:
        df_employees[POSITION] = 3

        first_management_level = df_positions[df_positions[POSITION] == 1].index
        second_management_level = df_positions[df_positions[POSITION] == 2].index

        df_employees.loc[df_employees.index.isin(first_management_level), POSITION] = 1
        df_employees.loc[df_employees.index.isin(second_management_level), POSITION] = 2
    else:
        raise Exception("Unsupported number of levels")

    return df_employees
