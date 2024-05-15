from data.entries import total_entry, weekly_average_entry, get_entries, get_annual_entries
from features.common import apply_partly

def get_total_list(minutes, weeks):
    if weeks == 1:
        return [f'{round(minutes/60, 1)}', f'{round(minutes/60/7, 1)}']
    else:
        return [f'{round(minutes/60, 1)}', f'{round(minutes/60/weeks, 1)}', f'{round(minutes/60/weeks/7, 1)}']

def get_category_list(minutes, weeks, total, dynamics = '~'):
    return get_total_list(minutes, weeks) + [f'{round(minutes/total*100, 1)}%', dynamics]

def populate_table(entry, weeks = 1, prev = {}):
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
        minutes = entry[category]

        if category in prev and prev[category] > 0.00000001:
            # prev is weekly value if weeks == 1, otherwise it is weekly average
            percentage = round((minutes / weeks / prev[category] - 1) * 100, 1)
            dynamics = f"{'+' if percentage >= 0.0 else ''}{percentage}%"
        else:
            dynamics = "~"

        table.append([category] + get_category_list(minutes, weeks, total, dynamics))
        # table.append([category, f'{round(minutes/60, 1)}', f'{round(minutes/60/7, 1)}', f'{round(minutes/total*100, 1)}%', f'{dynamics}'])

    return table

def for_part(wd, year, part):
    table = [['', f'Part {part}', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += apply_partly(wd, year, part, populate_table)
    return table

def for_last_entry(
    wd: str, 
    year: int, 
    month: int
) -> list[list[str]]:
    entries = get_entries(wd, month, year)
    weeks = len(entries)

    if weeks > 1: 
        prev = entries[-2]['Entry']
    else:
        # Try to load the last entry from previous month
        # If it's January -- consider the first week as a new beginning
        try: 
            prev = get_entries(wd, month - 1, year)[-1]['Entry']
        except:
            prev = {}

    current = entries[-1]['Entry']

    return populate_weekly_table(current, prev)