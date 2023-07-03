def fill_dict_user_equipment(dataframe, user_cycle_df, user_type):
    '''
    this function fills the dictionary with the equipment and the number of unique users that have used it
    :param df: dataframe of the user_equipment database
    :param user_cycle_df: dataframe of the user_cycle database
    :param user_type: string of the user type {'Unique Users', 'Users'}
    :return: dictionary of equipment and number of users
    '''

    equipment_usertype_dict = {'Equipment': [], 'User Type': [], 'Count': []}

    for i in range(len(dataframe['Equipment'])):
        
        user_list = dataframe[user_type][i].split(', ')
        
        for j in user_list:

            if user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Staff':
                equipment_usertype_dict['Equipment'].append(dataframe["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Staff')
                equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Student':
                equipment_usertype_dict['Equipment'].append(dataframe["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Student')
                equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'Faculty':
                equipment_usertype_dict['Equipment'].append(dataframe["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Faculty')
                equipment_usertype_dict['Count'].append(1)

            elif user_cycle_df.loc[user_cycle_df['Unique Users'] == j, 'User Type'].iloc[0] == 'IT':
                equipment_usertype_dict['Equipment'].append(dataframe["Equipment"][i])
                equipment_usertype_dict['User Type'].append('IT')
                equipment_usertype_dict['Count'].append(1)

            else:
                equipment_usertype_dict['Equipment'].append(dataframe["Equipment"][i])
                equipment_usertype_dict['User Type'].append('Other')
                equipment_usertype_dict['Count'].append(1)
        
    return equipment_usertype_dict
