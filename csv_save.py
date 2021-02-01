import csv


data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]


with open('sw_data_new.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)

with open('sw_data_new.csv') as f:
    for i, line in enumerate(f, start=1):
        print(f'{i:3}', line)



# data = []
# data.append(input().split())
# # data.append(['qwe', '123'])
#
# with open('test.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for row in data:
#         writer.writerow(row)
#
# with open('test.csv', 'r', newline='') as f:
#     for i in f:
#         print(i)