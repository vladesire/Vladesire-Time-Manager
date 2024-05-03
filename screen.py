from entries import total_entry, weekly_average_entry, get_entries, get_annual_entries

def parse_time(time_str):
    try: 
        if ':' in time_str:
            hours, minutes = time_str.split(":")
            res = int(hours) * 60 + int(minutes)
        else: 
            res = int(time_str) * 60
    except:
        res = 0

    return res

def input_screen(categories):
    entry = {}
    sum = 0

    for category in categories: 
        time = input(f"    {category}: ")
        minutes = parse_time(time)
        sum += minutes
        entry[category] = minutes

    # Sum counted total, so I need to compensate it
    entry['Other'] = 2*entry['Total'] - sum

    return entry

def present_screen(wd, month, year):
    entries = get_entries(wd, month, year)
    weeks = len(entries)

    if weeks == 0:
        print('Empty month')
        return

    # Count it first, as present_single_screen will remove 'Total' keys, and I don't want to pass a copy. 
    total = total_entry(entries)
    
    print(f'The Screen Time Stats for {year}-{month}')

    print('Format weekly: total / daily / quotient')
    print('Format monthly: total / weekly / daily / quotient')
    
    # Weekly
    for week, entry in enumerate(entries, start=1): 
        print('----------')
        print(f'Week {week}')

        if week > 1: 
            prev = entries[week - 2]['Entry']
        else:
            # Try to load the last entry from previous month
            # If it's January -- consider the first week as a new beginning
            try: 
                prev = get_entries(wd, month - 1, year)[-1]['Entry']
            except:
                prev = {}

        present_single_screen(entry['Entry'].copy(), monthly = total['Total'], prev = prev)

    # Monthly
    print('----------')
    print('Total')
    print(f'    ({weeks} weeks)')

    try: 
        prev = weekly_average_entry(get_entries(wd, month - 1, year))
    except:
        prev = {}

    present_single_screen(total, weeks = weeks, prev = prev)

def get_total_string(minutes, weeks):
    if weeks == 1:
        return f"{round(minutes/60, 1)} / {round(minutes/60/7, 1)}"
    else:
        return f"{round(minutes/60, 1)} / {round(minutes/60/weeks, 1)} / {round(minutes/60/weeks/7, 1)}"

def get_category_string(minutes, weeks, total, dynamics = '~'):
    return f"{get_total_string(minutes, weeks)} / {round(minutes/total*100, 1)}%"


def present_single_screen(entry, weeks = 1, monthly = 0, prev = {}):

    total = entry['Total']

    if monthly != 0:
        print(f'    Weekly quotient: {round(total/monthly*100, 1)}%')
    
    if 'Total' in prev and prev['Total'] > 0.00000001:
        percentage = round((total / weeks / prev['Total'] - 1) * 100, 1)
        dynamics = f"{'+' if percentage >= 0.0 else ''}{percentage}%"
    else:
        dynamics = '~'

    print(f'    Total: { get_total_string(total, weeks) } / {dynamics}')

    del entry['Total']

    for category in entry:
        minutes = entry[category]

        if category in prev and prev[category] > 0.00000001:
            # prev is weekly value if weeks == 1, otherwise it is weekly average
            percentage = round((minutes / weeks / prev[category] - 1) * 100, 1)
            dynamics = f"{'+' if percentage >= 0.0 else ''}{percentage}%"
        else:
            dynamics = "~"

        print(f'    {category}: { get_category_string(minutes, weeks, total) } / {dynamics}')

def present_screen_annual(wd, year):
    entries = get_annual_entries(wd, year)

    weeks = len(entries)
    total = total_entry(entries)

    try: 
        prev = weekly_average_entry(get_annual_entries(wd, year-1))
    except:
        prev = {}

    print(f'    Annual Screen Time Stats for {year}, {weeks} weeks')
    print('    Format: total / weekly / daily / quotient / dynamics\n')
    present_single_screen(total, weeks = weeks, prev = prev)