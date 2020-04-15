def check_week(a_list):
    if len(a_list) >= 6:
        raise Exception("we're only looking for 5 day weeks bruhv")
    init = str(a_list[0])[-1]
    for i in range(len(a_list)):
        current = str(a_list[i])[-1]
        if int(current) != int(init)+ i:
            return False
    return True

