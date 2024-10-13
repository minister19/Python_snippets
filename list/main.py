my_list = [1, 2, 3, 4, 5]

# Find the index of the last occurrence of the item
item_to_find = 3
index = len(my_list) - 1 - my_list[::-1].index(item_to_find)
print("Index of", item_to_find, "in the list:", index)

# Let's break down the syntax:

# - `len(my_list)`: This returns the length of the list `my_list`.
# - `- 1`: This subtracts 1 from the length of the list. Since list indices are zero-based in Python, the last index of a list of length `n` is `n - 1`.
# - `my_list[::-1]`: This creates a reversed copy of the list `my_list`. The syntax `[::-1]` is a slice that starts from the end of the list and goes towards the beginning, effectively reversing the order of the elements in the list.
# - `.index(item_to_find)`: This returns the index of the first occurrence of `item_to_find` in the reversed list `my_list[::-1]`.

# So, in summary, `len(my_list) - 1 - my_list[::-1].index(item_to_find)` calculates the index of the last occurrence of `item_to_find` in the original list `my_list` by reversing the list, finding the index of the first occurrence of `item_to_find` in the reversed list, and then converting it back to the original index.

my_list = [1, 2, 3, 4, 5]
my_list_sublist = my_list[0:0 + 10]  # my_list_sublist = [1, 2, 3, 4, 5]

# Find the index of the last occurrence of the item
item_to_find = 3
reverse_index = None
for i in range(len(my_list) - 1, -1, -1):
    if my_list[i] == item_to_find:
        reverse_index = i
        break

if reverse_index is not None:
    index = len(my_list) - 1 - reverse_index
    print("Index of", item_to_find, "in the list:", index)
else:
    print(item_to_find, "not found in the list")
