"""
This python script is generating the csv files using functions defined in the database.py file.
"""
import pandas as pd
from app.database import equipment_cycle_database
from app.database import user_cycle_database
from app.database import unique_user_equipment_database
from app.database import non_unique_user_equipment_database


# Equipment, Cycles, Check Out Times (string)
def equipment_cycle_csv(db=equipment_cycle_database()):
    equipment_cycle = pd.DataFrame(db, columns=['Equipment', 'Cycles', 'Check Out Times'])
    equipment_cycle.sort_values('Equipment').to_csv('equipment_cycle.csv', index=False)
    return equipment_cycle.sort_values('Equipment')


# Unique Users, User Type, Cycles
def user_cycle_csv(db=user_cycle_database()):
    user_cycle = pd.DataFrame(db, columns=['Unique Users', 'User Type', 'Cycles'])
    user_cycle.to_csv('user_cycle.csv', index=False)
    return user_cycle


#  Equipment, Unique Users (string)
def unique_user_equipment_csv(db=unique_user_equipment_database()):
    unique_user_equipment = pd.DataFrame(db, columns=['Equipment', 'Unique Users'])
    unique_user_equipment.to_csv('unique_user_equipment.csv', index=False)
    return unique_user_equipment


#  Equipment, Non-Unique Users (string)
def non_unique_user_equipment_csv(db=non_unique_user_equipment_database()):
    non_unique_user_equipment = pd.DataFrame(db, columns=['Equipment', 'Users'])
    non_unique_user_equipment.to_csv('non_unique_user_equipment.csv', index=False)
    return non_unique_user_equipment

