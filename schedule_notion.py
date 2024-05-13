from entries import total_entry, weekly_average_entry, get_entries, get_annual_entries
from notion_api import NotionApi

def get_entry_from_notion(categories, start_date, end_date):
    api = NotionApi()          
    entry = api.query_schedule_database(categories, start_date, end_date)

    return entry

def generate_weekly_schedule_table(entry, prev):
    table = [["", "Weekly", "Daily", "Quotient", "Dynamics"]]

    for category in entry: 
        if category in prev and prev[category] > 0.00000001:
            # prev is weekly value if weeks == 1, otherwise it is weekly average
            percentage = round((entry[category] / prev[category] - 1) * 100, 1)
            dynamics = f"{'+' if percentage >= 0.0 else ''}{percentage}%"
        else:
            dynamics = "~"

        time = entry[category]
        # Adding 0.001 solved wrong rounding problem
        table.append([category, f'{round(time + 0.001, 1)}', f'{round(time / 7, 1)}', f'{round(time / 168 * 100, 1)}%', f'{dynamics}'])
    
    return table

def send_last_schedule_table(wd, month, year):
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

    table = generate_weekly_schedule_table(current, prev)

    api = NotionApi()

    r = api.send_table(table)

    print(f'Sending schedule table: {r.status_code}')
