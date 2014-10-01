from multiprocessing import Pool

def add(arguments, cores=4):
    if len(arguments) < 2:
        return None
    for argument in arguments:
         if not hasattr(argument, '__add__'):
            return None
    return do_mapping(sum, arguments, cores=cores)

def subtract(arguments, cores=4):
    if len(arguments) < 2:
        return None
    for argument in arguments:
        if not hasattr(argument, '__sub__'):
            return None
    
    minuend = arguments[0]
    subtrahend = do_mapping(sum, arguments[1:], cores)
    return minuend - subtrahend


def average(arguments, cores=4):
    if len(arguments) < 1:
        return None

    for argument in arguments:
        if not hasattr(argument, '__sub__') or not hasattr(argument, '__truediv__'):
            return None 

    total = add(arguments, cores=cores)
    return total/len(arguments)

def permutate(n, r, cores=4):
    pass

def power(base, exponent, cores=4):
    pass

def factorial(n, cores=4):
    factors = range(1, n + 1)
    return multiply(factors, cores=cores)

def combination(n, r, cores=4):
    pass
#    n! /(k! * (n-k)!)

def divide(arguments, cores=4):
    if len(arguments) < 2:
        return None
    for argument in arguments[1:]:
        if not argument:
            return None
    numerator = arguments[0]
    denominator = multiply(arguments[1:], cores=cores)
    return numerator/denominator        # TODO will this fail because of integer division ???

def multiply(arguments, cores=4):
    if len(arguments) < 2:
        return None
    return do_mapping(__multi_list, arguments, cores)

def __multi_list(my_list):
    total = 1
    for argument in my_list:
        total *= argument
    return total


# TODO arrange to return pairs of results when cores > arguments, so computation time is log2(n)
def split_fold(arguments, cores):
    """
    Cores is the number of subprocesses you intend to spawn
    arguments is the list whose elements are the values you want to compute over.
    """
    assert type(arguments) == list, 'Your first positional argument is not a list. Please pass in a list.'
    result = []
    if len(arguments) < cores:
        result.append(arguments)
        return result

    size = len(arguments)/cores # the size of each computed chunk
    start = end = 0
    for num in range(cores):
        start = num*size
        end = (num+1)*size
        if num == cores - 1:
            result.append(arguments[start:])
            break
        result.append(arguments[start:end])
    return result


def do_mapping(function, arguments, cores):
    """
    Function is the function over which you intend to fold.
    Arguments is a list containing all of the elements in the fold
    Cores is the number of cores you want to spread this bad boy across.
    What is returned is the LIST containing each of the mapped values.
    """
    assert type(arguments) == list, 'Your first positional argument is not a list. Please pass in a list.'
    chunks = split_fold(arguments, cores)
    pool = Pool(processes=cores)
    partials = pool.map(function, chunks)
    return function(partials)


if __name__ == '__main__':
    def f(x):
        return x*x
    pool = Pool(processes=4)              # start 4 worker processes
    print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"
