# The idea of this code is tree, it's getting all possibilities of total noises in every sequence

def divider(data, the_group, total_group, pointer, my_val = []): 
    if the_group == total_group: # code for the last group's total noises, also this is the sign of the last branch of the tree
        return sum(data)*len(data)
    else:
        for i in range(1,len(data)-total_group+the_group+1): # the possibilities of how many noises could be taken in each group,
                                                             # except the last group
            value = sum(data[:i])*len(data[:i]) + divider(data[i:], the_group+1, total_group, i, [])
            my_val.append(value)
        return min(my_val)

# This is the code if you want to use a file. I'm not sure this one is good to use because it's gonna take more time

# file = open("divider.txt")
# a = file.readlines()
# N, K = [int(x) for x in a.pop(0).split(" ")]
# noises = [int(x) for x in a.pop(0).split(" ")]
# print("The minimum total noise: ", divider(noises, 1, K, 1))
# file.close()

# or

# N = int(input("insert how many people in the room: ")) # number of people in the rom
# K = int(input("insert how many group you would like to make: ")) # Total group
# A = input("inser the noise of each people in the same order: ") # The noise of each people
# noises = [int(x) for x in A.split(" ")]
# print("The minimum total noise: ", divider(noises, 1, K, 1))

# or

# first_line = input("insert the value of N (number of engineer) and K (total group), separated by 'space': ")
# N, K = [int(x) for x in first_line.split(" ")]
# second_line = input("insert the noise factor of each engineer separated by spaces")
# noises = [int(x) for x in second_line.split(" ")]
# print("The minimum total noise: ", divider(noises, 1, K, 1))

# if you want to try it on hackearth, you can use this instead

first_line = input()
N, K = [int(x) for x in first_line.split(" ")]
second_line = input()
noises = [int(x) for x in second_line.split(" ")]
print(divider(noises, 1, K, 1))
