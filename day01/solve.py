def load_input():
    with open('input.txt') as f:
        text = f.readlines()
    return [int(row.strip()) for row in text]

assert type(load_input()) == list

nums = load_input()
nums.sort()

i, j = 0, -1

while nums[i] + nums[j] != 2020:
    if nums[i] + nums[j] > 2020:
        j -= 1
    else:
        i += 1
    if i == j:
        raise Exception()

print(nums[i] * nums[j])

i, j, k = 0, 1, -1

total = sum(nums[x] for x in (i, j, k))
while total != 2020:
    if total > 2020:
        k -= 1
    else:
        j += 1
    if j == k:
        i += 1
        j, k = i + 1, -1
    total = sum(nums[x] for x in (i, j, k))

print(nums[i] * nums[j] * nums[k])
