from astropy import units
import numpy as np


###############################################################################
#                                                                             #
#                               Unit string parser                            #
#                                                                             #
###############################################################################
def parse_string(unit):
    """
    Parameters
    ----------
    unit (string)

    Returns
    -------
    new_unit (string)

    Notes
    -----
    This function is used to parse a loosely formatted string into a structured string, with well-defined
    multiplication, division, exponential and parentheses. All the different units and operations are separated by a
    singular space.
    """
    # define the operation symbols and space
    space = ' '
    exponential = '^'
    open_parentheses = '('
    close_parentheses = ')'
    divide = '/'
    multiply = '*'

    # replace Python exponential symbol (**) with ^
    # get rid of any extra spaces
    # convert the string into an array of size equal to the length of the string
    unit = unit.replace('**', '^')
    unit = space.join(unit.split())
    unit_array = np.array(list(unit))

    # loop through the array until the end
    new_unit = str()
    index = 0
    while index < unit_array.size:
        # ignore the white spaces
        if unit[index] == space:
            pass
        # check if the current element is a ^, and if so, add the associated exponent
        elif unit[index] == exponential:
            tmp_num, tmp_index = separate_number_unit(unit[index + len(exponential):])
            new_unit += ' ^ ' + tmp_num + ' '
            index += tmp_index
        # check if the current element is a (
        elif unit[index] == open_parentheses:
            new_unit += ' ( '
        # check if the current element is a )
        elif unit[index] == close_parentheses:
            new_unit += ' ) '
        # check if the current element is a /
        elif unit[index] == divide:
            new_unit += ' / '
        # check if the current element is a *
        elif unit[index] == multiply:
            new_unit += ' * '
        else:
            # check if user input is of form "a b" = "a*b"
            try:
                i_1 = unit[index + 1]
                i_2 = unit[index + 2]
                multi = ((i_1.isspace()) & (i_2 is not exponential) & (i_2 is not open_parentheses) & 
                         (i_2 is not close_parentheses) & (i_2 is not divide) & (i_2 is not multiply))
                # add ' * ' if the next element is a valid unit
                if multi:
                    new_unit += unit[index] + ' * '
                else:
                    new_unit += unit[index]
            except IndexError:
                new_unit += unit[index]
        index += 1
    # get rid of any extra spaces
    new_unit = space.join(new_unit.split())
    return new_unit


def separate_number_unit(array_like):
    """
    Parameters
    ----------
    array_like (np.ndarray)

    Returns
    -------
    number (string), index (int)

    Notes
    -----
    This function is used to extract the first number from a string, and return the number and the index of the rest of
    the string.
    """
    # loop through the array until the end or until a non-number is found
    is_num = True
    index = 0
    number = str()
    while is_num and index < len(array_like):
        i = array_like[index]
        # check if the current element is a number
        if i == '+' or i == '-' or i == '.' or i.isdigit():
            number += i
            index += 1
        # ignore if the current element is a space
        elif i.isspace():
            index += 1
        # end if non-number of space is found
        else:
            is_num = False
    return number, index


def bases_from_string(array_unit):
    """
    Parameters
    ----------
    array_unit (np.ndarray)

    Returns
    -------
    bases (list)

    Notes
    -----
    This function is used to generate a list of unique bases from a structured string.
    """
    # loop through the array and check if the current element is a valid unit
    bases = list()
    for i in array_unit:
        try:  # check if the current element is a valid unit
            getattr(units, i)
            bases.append(i)
        except AttributeError:  # ignore the non-units
            pass
    return bases


def powers_from_bases(array_unit, bases):
    """
    Parameters
    ----------
    array_unit (np.ndarray), bases (list)

    Returns
    -------
    powers (np.ndarray)

    Notes
    -----
    This function is used to generate a list of powers associated with the unique bases from a structured string without
    parentheses.
    """
    # loop through the array and count the number of times a base is raised to a power
    powers = np.zeros(len(bases))
    for num, i in enumerate(bases):
        index_unit = np.where(array_unit == i)[0]
        # check if the parentheses are preceded by a division
        multiplier = 1
        if index_unit.size != 0:
            if index_unit != 0:
                if array_unit[index_unit - 1] == '/':
                    multiplier = -1
            # check if the parentheses are followed by an exponent
            if index_unit != array_unit.size - 1 and array_unit[index_unit + 1] == '^':
                powers[num] += multiplier * float(array_unit[index_unit + 2][0])
            # add one power
            else:
                powers[num] += multiplier * 1
    return powers


def powers_from_parentheses(array_unit, bases):
    """
    Parameters
    ----------
    array_unit (np.ndarray), bases (list)

    Returns
    -------
    powers (np.ndarray)

    Notes
    -----
    This function is used to generate a list of powers associated with the unique bases from a structured string with
    a single set of parentheses.
    """
    # find the indexes of the parentheses
    filter_open = np.where(array_unit == '(')[0]
    filter_close = np.where(array_unit == ')')[0]

    # check if there are any parentheses
    powers = np.zeros(len(bases))
    if filter_open.size != 0:
        # find the outermost parentheses
        open_index = filter_open[0]
        close_index = filter_close[-1]
        # add the powers not inside the parentheses
        powers += powers_from_bases(array_unit[:open_index], bases)
        powers += powers_from_bases(array_unit[close_index + 1:], bases)
        # loop through the array inside the parentheses by calling the function recursively
        tmp_powers = powers_from_parentheses(array_unit[open_index + 1:close_index], bases)
        # check if the parentheses are preceded by a division
        multiplier = 1
        if open_index != 0:
            if array_unit[open_index - 1] == '/':
                multiplier = -1
        # check and add if the parentheses are followed by an exponent
        if close_index != array_unit.size - 1 and array_unit[close_index + 1] == '^':
            powers += multiplier * tmp_powers * float(array_unit[close_index + 2])
        # add the powers inside the parentheses
        else:
            powers += multiplier * tmp_powers
        return powers
    else:
        return powers_from_bases(array_unit, bases)


def powers_from__multiple_parentheses(array_unit, bases):
    """
    Parameters
    ----------
    array_unit (np.ndarray), bases (list)

    Returns
    -------
    powers (np.ndarray)

    Notes
    -----
    This function is used to generate a list of powers associated with the unique bases from a structured string with
    multiple sets of parentheses.
    """
    # find the indexes of the parentheses
    filter_open = np.where(array_unit == '(')[0]
    filter_close = np.where(array_unit == ')')[0]

    # initialize the lists to store the indexes of sets of parentheses
    groups_close = list()
    groups_open = list()

    # loop through the array and find the indexes of the sets of parentheses
    for num, i in enumerate(filter_close):
        if num + 1 == filter_open.size or filter_open[num + 1] > i:
            groups_close.append(i)
    for num, i in enumerate(groups_close):
        if num == 0:
            groups_open.append(filter_open[filter_open < i][0])
        else:
            groups_open.append(filter_open[(i > filter_open) & (filter_open > filter_close[num - 1])][0])

    # loop through the array and add the powers associated with the sets of parentheses
    powers = np.zeros(len(bases))
    prev_index = 0
    for num, open_index in enumerate(groups_open):
        close_index = groups_close[num]
        # add the powers not inside the parentheses
        powers += powers_from_bases(array_unit[prev_index:open_index], bases)
        if num + 1 == len(groups_open):
            powers += powers_from_bases(array_unit[close_index + 1:], bases)
        # loop through the array inside the parentheses by calling the powers_from_parentheses recursively
        tmp_powers = powers_from_parentheses(array_unit[open_index + 1:close_index], bases)
        # check if the parentheses are preceded by a division
        multiplier = 1
        if open_index != 0:
            if array_unit[open_index - 1] == '/':
                multiplier = -1
        # check and add if the parentheses are followed by an exponent
        if close_index != array_unit.size - 1 and array_unit[close_index + 1] == '^':
            powers += multiplier * tmp_powers * float(array_unit[close_index + 2])
        # add the powers inside the parentheses
        else:
            powers += multiplier * tmp_powers
        prev_index = close_index + 1
    return powers


def create_unit_from_string(unit):
    """
    Parameters
    ----------
    unit (string)

    Returns
    -------
    unit (units.core.Unit)

    Notes
    -----
    This function is used to generate an astropy.units.core.Unit object from a loosely formatted string.
    """
    # parse the string into a structured string
    string = parse_string(unit)

    # convert the string into an array
    array_unit = np.array(string.split(' '))

    # generate the list of unique bases
    bases = bases_from_string(array_unit)

    # generate the list of powers associated with the unique bases and check to see if there are parentheses
    filter_open = np.where(array_unit == '(')[0]
    if filter_open.size == 0:
        powers = powers_from_bases(array_unit, bases)
    else:
        powers = powers_from__multiple_parentheses(array_unit, bases)

    # generate the astropy.units.core.Unit object from bases and powers
    units_obj = create_unit(bases, powers)
    return units_obj.unit


def get_bases(value):
    """
    Parameters
    ----------
    value (units.quantity.Quantity)

    Returns
    -------
    bases (list)

    Notes
    -----
    Getter function to get the bases of a unit.
    """
    return value.unit.bases


def get_powers(value):
    """
    Parameters
    ----------
    value (units.quantity.Quantity)

    Returns
    -------
    powers (list)

    Notes
    -----
    Getter function to get the powers of a unit.
    """
    return value.unit.powers


def create_unit(bases, powers):
    """
    Parameters
    ----------
    bases (list), powers (list)

    Returns
    -------
    unit (units.core.Unit)

    Notes
    -----
    This function is used to generate an astropy.units.core.Unit object from a list of bases and powers.
    """
    unit = 1
    # loop through the bases and powers and raise the base by the power
    for num, i in enumerate(bases):
        # check if bases are stored as strings
        if isinstance(i, str):
            unit *= getattr(units, i) ** powers[num]
        # check if bases are stored as astropy.units.core.Unit objects
        elif isinstance(i, units.core.Unit):
            unit *= getattr(units, i.name) ** powers[num]
        else:
            raise TypeError('Input is not a valid unit! Instead, it is of type ' + str(type(i)) + '.')
    return unit

