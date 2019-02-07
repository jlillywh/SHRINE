def checkPositive(myValue, myVariableName):
    """Checks the value to see if it's negative
    :param myValue : float
    :param myVariableName : str
    :return: valueError
    """
    if myValue < 0.0:
        negValueError = ValueError(myVariableName + ' should be a positive')
        raise negValueError

def checkEqualValues(v1, v2):
    if v1 != v2:
        nonEqualError = ValueError("The depths are not the same.")
        raise nonEqualError

def checkValuesAddTo1(my_array):
    """Checks for the sum of all depths in array < 1.0

        Parameters
        ----------
            args : array
                list of fractions that should add to 1.0
        Raises
        ----------
            ValueError
        Returns

        """
    if sum(my_array) != 1.0:
        sumValuesError = ValueError("The depths in the array do not sum to 1.0.")
        raise sumValuesError

def checkInRange(value, lower_bound=0.0, upper_bound=1.0):
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
        outOfRangeError = ValueError("The value is out of range. It should be between 0 and 1.")
        raise outOfRangeError


def checkEqualLength(array_old, array_new):
    """Check to see if 2 arrays have the same length.s"""
    length_old = len(array_old)
    length_new = len(array_new)
    if length_old != length_new:
        nonEqualError = ValueError("The new array size is different from the old.")
        raise nonEqualError
