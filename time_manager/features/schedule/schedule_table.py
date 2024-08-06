from features.common_tables import weekly_table, monthly_table, partly_table, annual_table
from features.common import get_dynamics

def get_category_list(time, weeks, dynamics = '~') -> list[str]:
    # Adding 0.001 solved wrong rounding problem
    if weeks == 1: 
        return [f'{round(time + 0.001, 1)}', f'{round(time / 7, 1)}', f'{round(time / 168 * 100, 1)}%', f'{dynamics}']
    else:
        return [f'{round(time + 0.001, 1)}', f'{round(time / weeks, 1)}', f'{round(time / weeks / 7, 1)}', f'{round(time / weeks / 168 * 100, 1)}%', f'{dynamics}']

def populate_schedule_table(entry, weeks = 1, prev = {}):
    table = []

    for category in entry: 
        if category in prev and prev[category] > 0:
            dynamics = get_dynamics(entry[category], weeks, prev[category])
        else:
            dynamics = "~"

        table.append([category] + get_category_list(entry[category], weeks, dynamics))
    
    return table

def for_week(wd, year, month, week):
    return weekly_table(populate_schedule_table, wd, year, month, week)

def for_month(wd, year, month):
    return monthly_table(populate_schedule_table, wd, year, month)

def for_part(wd, year, part):
    return partly_table(populate_schedule_table, wd, year, part)

def for_year(wd, year):
    return annual_table(populate_schedule_table, wd, year)