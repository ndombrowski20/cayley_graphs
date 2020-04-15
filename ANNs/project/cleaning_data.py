import csv

def check_week(a_list):
    init = str(a_list[0])[-1]
    for i in range(len(a_list)):
        current = str(a_list[i])[-1]
        if int(current) != int(init)+ i:
            return False
    return True


def find_week(a_list, init):
    # next_five_days = []
    nfd = []
    for i in range(5):
        nfd.append(a_list[init + i])
    return nfd


def find_dates_sheet(a_str):
    with open(a_str, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        date_sheet = []
        days = []
        for row in reader:
            date_sheet.append(row["Date"])
        for i in range(len(date_sheet)-6):
            nfd = find_week(date_sheet, i)
            if check_week(nfd):
                days += nfd
                i += 6
        return days


def create_data(a_str, days_list):
    with open(a_str, newline='') as csvfile:
        data = []
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row['Date'] in days_list:
                data.append(row)
        return data


def sorting_data(data_list):
    big_list = []
    for i in range(int(len(data_list) / 5)):
        data = []
        data.clear()
        for j in range(5):
            data.append(data_list[i+j]["Volume"])
            data.append(data_list[i+j]["High"])
            data.append(data_list[i+j]["Low"])
            data.append(data_list[i+j]["Open"])
            data.append(data_list[i+j]["Close"])
        big_list.append(data)
    return big_list


date_list = find_dates_sheet('a.us.txt')
new_data = create_data('a.us.txt', date_list)
print(sorting_data(new_data))


