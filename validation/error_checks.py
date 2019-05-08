from validation.error import WrongUnits


def check_all_items_positive(my_list):
    for i in range(len(my_list)):
        check_positive(my_list[i])


def check_positive(my_value, my_variable_name='var1'):
    """Checks the value to see if it's negative
    :param my_value : float
    :param my_variable_name : str
    :return: valueError
    """
    if my_value < 0.0:
        neg_value_error = ValueError(my_variable_name + ' should be a positive')
        raise neg_value_error


def check_equal_values(v1, v2):
    if v1 != v2:
        non_equal_error = ValueError("The depths are not the same.")
        raise non_equal_error


def check_values_add_to_1(my_array):
    """Checks for the sum of all depths in array < 1.0

        Parameters
        ----------
            my_array : array
                list of fractions that should add to 1.0
        Raises
        ----------
            ValueError
        Returns

        """
    if sum(my_array) != 1.0:
        sum_values_error = ValueError("The depths in the array do not sum to 1.0.")
        raise sum_values_error


def check_in_range(value, lower_bound=0.0, upper_bound=1.0):
    """Check to see if a value fits within a specified range.
        Parameters
        ----------
            value : float
                the value to be questioned
            lower_bound : float
                default is 0.0
            upper_bound : float
                default is 1.0
        """
    if value < lower_bound or value > upper_bound:
        out_of_range_error = ValueError("The value is out of range. It should be between 0 and 1.")
        raise out_of_range_error


def check_equal_length(array_old, array_new):
    """Check to see if 2 arrays have the same length.s"""
    length_old = len(array_old)
    length_new = len(array_new)
    if length_old != length_new:
        non_equal_error = ValueError("The new array size is different from the old.")
        raise non_equal_error


def check_dimensions(value):
    try:
        if value.check(value.units):
            return value.units
        else:
            message = "Wrong dimension. Should be in terms of " + str(value.units) + '.'
            raise WrongUnits(message)
    except AttributeError:
        return value
