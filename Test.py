# n = int(input())
#
# arr = []
#
# for index in range(n):
#     arr.append(int(input()))
#
# max_val = None
#
# for index in arr:
#     if index % 10 == 1:
#         if not max_val:
#             max_val = index
#             continue
#         if max_val < index:
#             max_val = index
# if max_val:
#     print(max_val)
# else:
#     print('Нет')

len = 100

for index in range(1, 10000):
    if (index % 3 == 1 and index % 5 == 2 and index%15):
        print(index)
        print(f'{index} mod 15 = {index%15}')
#    arr.append(int(input()))

# max_val = None
#
# for index in arr:
#     if index % 10 == 1:
#         if not max_val:
#             max_val = index
#             continue
#         if max_val < index:
#             max_val = index
# if max_val:
#     print(max_val)
# else:
#     print('Нет')


