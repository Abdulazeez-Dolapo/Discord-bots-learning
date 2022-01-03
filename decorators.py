def confirm_function_call(func):
    def wrap(*args):
        print(f"{func.__name__} was called successfully with arguments {args}.")
        return func(*args)

    return wrap


@confirm_function_call
def sums(a, b):
    return a + b


numbers = [-1, -2, 1, 0, False, [], 2, 3, 4, 5, 6, 7, -8]
print(list(filter(None, numbers)))

