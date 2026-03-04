def digital_root(n):
    i = 0
    result = 0
    number_array = []

    for c in str(n):
        number_array += c

    while i < len(number_array):
        result += int(number_array[i])
        i += 1

    if result < 10:

        return result
    else:
        return digital_root(result)
    pass


print(digital_root(132189))
