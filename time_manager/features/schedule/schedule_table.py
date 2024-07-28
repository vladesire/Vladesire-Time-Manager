from data.entries import total_entry, weekly_average_entry, get_entries, get_annual_entries
from features.common import apply_partly, apply_annual

def get_category_list(time, weeks, dynamics = '~') -> list[str]:
    # Adding 0.001 solved wrong rounding problem
    if weeks == 1: 
        return [f'{round(time + 0.001, 1)}', f'{round(time / 7, 1)}', f'{round(time / 168 * 100, 1)}%', f'{dynamics}']
    else:
        return [f'{round(time + 0.001, 1)}', f'{round(time / weeks, 1)}', f'{round(time / weeks / 7, 1)}', f'{round(time / weeks / 168 * 100, 1)}%', f'{dynamics}']

def populate_table(entry, weeks = 1, prev = {}):
    table = []

    for category in entry: 
        if category in prev and prev[category] > 0.00000001:
            # prev is weekly value if weeks == 1, otherwise it is weekly average
            percentage = round((entry[category] / weeks / prev[category] - 1) * 100, 1)
            dynamics = f"{'+' if percentage >= 0.0 else ''}{percentage}%"
        else:
            dynamics = "~"

        table.append([category] + get_category_list(entry[category], weeks, dynamics))
    
    return table

# TODO: These three function are the same for screen
def for_part(wd, year, part):
    table = [['', f'Part {part}', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += apply_partly(wd, year, part, populate_table)
    return table

def for_annual(wd, year):
    table = [['', f'{year}', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += apply_annual(wd, year, populate_table)
    return table

def for_week(
    wd: str, 
    year: int, 
    month: int, 
    week: int
) -> list[list[str]]:
    entries = get_entries(wd, month, year)
    weeks = len(entries)

    if week == -1 and weeks > 1: 
        # The last week is assumed
        prev = entries[-2]['Entry']
    elif week > 1:
        # Convert it to index
        week -= 1
        prev = entries[week - 1]['Entry']
    else:
        # Try to load the last entry from previous month
        # If it's January -- consider the first week as a new beginning
        try: 
            prev = get_entries(wd, month - 1, year)[-1]['Entry']
        except:
            prev = {}

    current = entries[week]['Entry']

    table = [['', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += populate_table(current, 1, prev)

    return table