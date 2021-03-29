# The idea of this code is a tree, that it wil take the number one by one and do the works. The output is the number of coffee
# that's meet Noel's expectation.
def shoffee(data, expectation, total = [], group = 1):
    if group == len(data):
        a = sum(data)/group
        if a >= expectation:
            total.append(1)
            return sum(total)
        else:
            return sum(total)
    else:
        for i in range(len(data)-group+1):
            shoffee(data[i:i+group], expectation, total, group)
        return shoffee(data, expectation, total, group + 1)


# The case
# Default input is:
# 3 3
# 1 3 4
# the output: 3

N, K = [int(x) for x in input().split(" ")] # N: number of coffee bean flavors, K: Noel's expectation for the coffee
V = [int(x) for x in input().split(" ")] # V: Noel's preference value for each type coffee bean
print(shoffee(V, K))
