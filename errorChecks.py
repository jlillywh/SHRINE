def checkPositive(myValue, myVariableName):
    """ Checks the value to see if it's negative
    :param myValue : float
    :param myVariableName : str
    :return: valueError
    """
    if myValue < 0.0:
        negValueError = ValueError(myVariableName + ' should be a positive')
        raise negValueError

def checkEqualValues(v1, v2):
    if v1 != v2:
        nonEqualError = ValueError("The values are not the same.")
        raise nonEqualError

def checkValuesAddTo1(my_array):
    ''' Checks for the sum of all values in array < 1.0

        Parameters
        ----------
            args : array
                list of fractions that should add to 1.0
        Raises
        ----------
            ValueError
        Returns

        '''
    if sum(my_array) != 1.0:
        sumValuesError = ValueError("The values in the array do not sum to 1.0.")
        raise sumValuesError


def checkEqualLength(array_old, array_new):
    length_old = len(array_old)
    length_new = len(array_new)
    if length_old != length_new:
        nonEqualError = ValueError("The new array size is different from the old.")
        raise nonEqualError