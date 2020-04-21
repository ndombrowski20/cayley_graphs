import csv
import os

# first we need to be able to tell if a list is a proper week


def check_week(a_list):
    # first, cause i'm paranoid
    if len(a_list) != 6:
        raise Exception("It's monday to monday bruh")

    # so first, we grab the number of the date which is the last value. This means we're limiting ourselves to
    # sequential data, which is kinda alright.
    init = str(a_list[0])[-1]
    # was the length of the list
    # now changed to 6 so it checks the first 5 days, and then asks if the next one in the list is 2 days more.
    # i.e. whether the next day in the list is the next monday after our friday
    for i in range(5):
        current = str(a_list[i])[-1]
        if int(current) != int(init)+ i:
            return False
    if int(init) + 7 >= 10:
        new = int(init) + 7 - 10
        if new != a_list[5]:
            return False
    elif int(init) + 7 != int(str(a_list[5])[-1]):
        return False
    return True

# next, we try to see if we can find proper weeks within a list of dates


def find_week(a_list, init):
    # next five days
    # nfd = []
    # now next 6 days for the monday too
    nsd = []
    for i in range(6):
        nsd.append(a_list[init + i])
    return nsd


# now we can simply find the dates from a datasheet and feed them to the previous functions


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


# now we write the data to a new place, so that we can copy/export it later


def create_data(a_str, days_list):
    with open(a_str, newline='') as csvfile:
        data = []
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row['Date'] in days_list:
                data.append(row)
        return data


# now we sort the data in a way that makes sense for the program, obtaining both our x and y data


def sorting_data(data_list):
    big_list = []
    for i in range(int(len(data_list) / 6)):
        data = []
        data.clear()
        for j in range(5):
            data.append(data_list[i+j]["Volume"])
            data.append(data_list[i+j]["High"])
            data.append(data_list[i+j]["Low"])
            data.append(data_list[i+j]["Open"])
            data.append(data_list[i+j]["Close"])
        final = data_list[i+5]["Close"]
        friday = data[-1]
        y = float(final) - float(friday)
        data.append(y)
        big_list.append(data)
    return big_list


# now that we can produce data from a sheet, we can take


def complete_automation(location_str, filename_list):
    mondo_data = []
    date_list = []
    new_data = []
    for name in filename_list:
        filename = location_str + name
        date_list.clear()
        new_data.clear()
        print(filename)
        date_list = find_dates_sheet(filename)
        new_data = create_data(filename, date_list)
        new_sorted = sorting_data(new_data)
        mondo_data += new_sorted
    return mondo_data


# specifically for running this script in a certain folder so that we can get the data
# with open('filenames.txt', newline='') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
#     files = []
#     for row in reader:
#         files.append(row['name'])

complete_data = complete_automation("", ['a.us.txt', 'aa.us.txt'])

with open('data_full.csv', 'w', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for item in complete_data:
        print(item)
        datawriter.writerow(item)