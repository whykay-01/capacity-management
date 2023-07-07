"""
This python script is using the database snapshot file called test.csv to generate functions
which are used to produce the csv files.
"""

def generate_main_db():
    main_database = []
    with open('../data/test.csv', encoding='utf-8') as f:
        for line in f:
            main_database.append(line.rstrip("\n").split(",")[0:9])
            if line[0] == '':
                break
    # oldest to newest
    print(len(main_database))
    main_database.reverse()


def equipment_cycle_database(main_database=generate_main_db()):
    # [classification, cycles, check out times]
    equipment_cycle_usage_database = []

    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for j in range(i + 1, len(main_database)):
                # checks if same barcode and check in
                if main_database[j][2] == main_database[i][2] and main_database[j][7] == "还":
                    equipment_exist = False

                    # Fixing calendar format
                    date = ''
                    if main_database[i][8][2] != '/':
                        date = '0' + main_database[i][8][:9]
                        if date[5] != '/':
                            date = date[:3] + '0' + date[3:]
                    elif main_database[i][8][5] != '/':
                        date = main_database[i][8][:3] + '0' + main_database[i][8][3:10]
                    else:
                        date = main_database[i][8][:10]
                    date = date[:10]

                    for k in equipment_cycle_usage_database:
                        try:
                            if k[0] == f"{main_database[j][3][0].upper() + main_database[j][3][1:]}":
                                k[1] += 1
                                k[2] += ", " + date

                                equipment_exist = True
                                break
                        # since some equipment name is empty
                        except IndexError:
                            if k[0] == main_database[j][3]:
                                k[1] += 1
                                k[2] += ", " + date
                                equipment_exist = True
                                break
                    if not equipment_exist:
                        try:
                            equipment_cycle_usage_database.append(
                            [main_database[j][3][0].upper()+main_database[j][3][1:], 1, date])
                        except IndexError:
                            equipment_cycle_usage_database.append(
                                [main_database[j][3], 1, date])

                    break

    return equipment_cycle_usage_database


def user_cycle_database(main_database=generate_main_db()):
    # checks how many times a user has checked out and checked in an equipment
    # [user, type, cycles]
    user_usage_database = []
    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for k in range(i + 1, len(main_database)):
                # checks if same user and barcode and check in
                if main_database[k][5] == main_database[i][5] and main_database[k][2] == main_database[i][2] and \
                        main_database[k][7] == "还":
                    user_exist = False
                    for j in user_usage_database:
                        if j[0] == main_database[i][5]:
                            user_exist = True
                            j[2] += 1
                            break
                    if not user_exist:
                        if main_database[k][6] == 'Academia':
                            user_usage_database.append([main_database[k][5], 'IT', 1])
                        elif main_database[k][6] == 'Contractor':
                            user_usage_database.append([main_database[k][5], 'Others', 1])
                        elif main_database[k][6] == '#N/A':
                            user_usage_database.append([main_database[k][5], 'Others', 1])
                        else:
                            user_usage_database.append([main_database[k][5], main_database[k][6], 1])
                    break

    return user_usage_database


def unique_user_equipment_database(main_database=generate_main_db()):
    # [equipment, [unique_users]]
    user_per_equipment_database = []
    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for k in range(i + 1, len(main_database)):
                # checks if same user, barcode and checkin
                if main_database[k][5] == main_database[i][5] and main_database[k][2] == main_database[i][2] and \
                        main_database[k][7] == "还":
                    equipment_exist = False
                    user_exist = False
                    for j in user_per_equipment_database:
                        if j[0] == main_database[k][3]:
                            equipment_exist = True
                            unique_user_list = j[1].split(', ')
                            for l in unique_user_list:
                                if l == main_database[k][5]:
                                    user_exist = True
                                    break
                            if not user_exist:
                                j[1] += ', ' + main_database[k][5]
                                break
                    if not equipment_exist:
                        user_per_equipment_database.append([main_database[k][3], main_database[k][5]])
                        break

    # [equipment, unique_users]
    user_num_equipment_database = []
    for i in range(len(user_per_equipment_database)):
        user_num_equipment_database.append([user_per_equipment_database[i][0], len(user_per_equipment_database[i][1])])
    return user_per_equipment_database


def non_unique_user_equipment_database(main_database=generate_main_db()):
    # [equipment, [non_unique_users]]
    user_per_equipment_database = []
    for i in range(len(main_database)):
        if main_database[i][7] == "借":
            for k in range(i + 1, len(main_database)):
                # checks if same user, barcode and checkin
                if main_database[k][5] == main_database[i][5] and main_database[k][2] == main_database[i][2] and \
                        main_database[k][7] == "还":
                    equipment_exist = False
                    for j in user_per_equipment_database:
                        if j[0] == main_database[k][3]:
                            equipment_exist = True
                            j[1] += ', ' + main_database[k][5]
                            break
                    if not equipment_exist:
                        user_per_equipment_database.append([main_database[k][3], main_database[k][5]])
                        break
                    break

    # [equipment, unique_users]
    user_num_equipment_database = []
    for i in range(len(user_per_equipment_database)):
        user_num_equipment_database.append([user_per_equipment_database[i][0], len(user_per_equipment_database[i][1])])
    return user_per_equipment_database
