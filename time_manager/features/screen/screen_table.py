from features.common_tables import weekly_table, monthly_table, partly_table, annual_table
from features.common import get_dynamics

def get_total_list(minutes, weeks):
    if weeks == 1:
        return [f'{round(minutes/60, 1)}', f'{round(minutes/60/7, 1)}']
    else:
        return [f'{round(minutes/60, 1)}', f'{round(minutes/60/weeks, 1)}', f'{round(minutes/60/weeks/7, 1)}']

def get_category_list(minutes, weeks, total, dynamics = '~'):
    return get_total_list(minutes, weeks) + [f'{round(minutes/total*100, 1)}%', dynamics]

def populate_screen_table(entry, weeks = 1, prev = {}):
    table = []

    total = entry['Total']

    if 'Total' in prev and prev['Total'] > 0.00000001:
        percentage = round((total / weeks / prev['Total'] - 1) * 100, 1)
        dynamics = f"{'+' if percentage >= 0.0 else ''}{percentage}%"
    else:
        dynamics = '~'

    table.append(['Total'] + get_total_list(total, weeks) + ['', f'{dynamics}'])

    del entry['Total']

    for category in entry:
        if category in prev and prev[category] > 0:
            dynamics = get_dynamics(entry[category], weeks, prev[category])
        else:
            dynamics = "~"

        table.append([category] + get_category_list(entry[category], weeks, total, dynamics))
        
    return table

def for_week(wd, year, month, week):
    return weekly_table(populate_screen_table, wd, year, month, week)

def for_month(wd, year, month):
    return monthly_table(populate_screen_table, wd, year, month)

def for_part(wd, year, part):
    return partly_table(populate_screen_table, wd, year, part)

def for_year(wd, year):
    return annual_table(populate_screen_table, wd, year)