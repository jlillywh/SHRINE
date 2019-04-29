# Vector constructor

# GoldSim script: vector( Demands, if( !~allocated[row] and ~currPrior = ~priorities[row] then row else 1e10 )
def vector(other_vector, *args, if_true=1, if_false=0):
    """Constructs a vector of same size in which teh result follows the condition
    
        Parameters
        ----------
        other_vector : list
        condition : bool
        if_true : float
        if_false : float
    
        Returns
        -------
        new vector
    """
    row = 0
    num_array = [0] * len(other_vector)
    new_vector = other_vector.copy()
    # Walk over the array and look for bool. If found, insert a confirmation for the right side of equality
    for i in range(len(args)):
        if type(args[i]) == bool:
            args.insert(i + 1, True)
        elif type(args[i]) == int or type(args[i]) == float:
            args.insert(i + 1, [0] * len(other_vector))
    
    for i in range(len(other_vector)):
        if args[0][i] and args[1] == args[2][i]:
            new_vector[i] = if_true
        else:
            new_vector[i] = if_false
    return new_vector
            
old_vector = [5,4,3,2,1]
v1 = [True] * 5
v2 = 4
v3 = [3, 4, 2, 3, 3]
true_value = "Hi"
false_value = "shit!"
new_vector = vector(old_vector, v1, v2, v3, if_true=true_value, if_false=false_value)
print(new_vector)