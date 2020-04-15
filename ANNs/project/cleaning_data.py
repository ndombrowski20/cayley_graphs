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


def run_sheet(a_list):
    for i in range(len(a_list)):
        current_date = a_list[i][0]
        nfd = find_week(a_list, i)
        if check_week(nfd):
            # go code goes here
            print("yay we got here")


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
        print("here")
        return days


def create_data(a_str, days_list):
    with open(a_str, newline='') as csvfile:
        data = []
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row['Date'] in days_list:
                print(row)
                data.append(row)


date_list = find_dates_sheet('a.us.txt')
create_data('a.us.txt', date_list)

