"""
This python script is generating dataframes using functions defined in the database.py file.
"""
import pandas as pd
from app.database import equipment_cycle_database
from app.database import user_cycle_database
from app.database import unique_user_equipment_database
from app.database import non_unique_user_equipment_database


# Equipment, Cycles, Check Out Times (string)
def equipment_cycle_csv(db):
    equipment_cycle = pd.DataFrame(db, columns=['Equipment', 'Cycles', 'Check Out Times'])
    return equipment_cycle.sort_values('Equipment')


# Unique Users, User Type, Cycles
def user_cycle_csv(db):
    user_cycle = pd.DataFrame(db, columns=['Unique Users', 'User Type', 'Cycles'])
    return user_cycle


#  Equipment, Unique Users (string)
def unique_user_equipment_csv(db):
    unique_user_equipment = pd.DataFrame(db, columns=['Equipment', 'Unique Users'])
    return unique_user_equipment


#  Equipment, Non-Unique Users (string)
def non_unique_user_equipment_csv(db):
    non_unique_user_equipment = pd.DataFrame(db, columns=['Equipment', 'Users'])
    return non_unique_user_equipment

