from data.entries import total_entry, weekly_average_entry, get_entries, get_annual_entries

def monthly(
    wd: str, 
    month: int, 
    year: int
):
    entries = get_entries(wd, month, year)
    weeks = len(entries)

    if weeks == 0:
        print('Empty month')
        return

    total = total_entry(entries)
    
    print(f'The Schedule Stats for {year}-{month}')

    print('Format weekly: total / daily / quotient / dynamics')
    print('Format monthly: total / weekly / daily / quotient / dynamics')
    
    # weekly 
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

        present_single_schedule(entry['Entry'].copy(), prev = prev)


    # monthly
    print('----------')
    print('Total')
    print(f'    ({weeks} weeks)')

    try: 
        prev = weekly_average_entry(get_entries(wd, month - 1, year))
    except:
        prev = {}

    present_single_schedule(total, weeks = weeks, prev = prev)

def get_category_string(time, weeks, dynamics = '~'):
    # Adding 0.001 solved wrong rounding problem
    if weeks == 1: 
        return f"{round(time + 0.001, 1)} / {round(time / 7, 1)} / {round(time / 168 * 100, 1)}% / {dynamics}"
    else:
        return f"{round(time + 0.001, 1)} / {round(time / weeks, 1)} / {round(time / weeks / 7, 1)} / {round(time / weeks / 168 * 100, 1)}% / {dynamics}"

def present_single_schedule(entry, weeks = 1, prev = {}):
    for category in entry: 
        if category in prev and prev[category] > 0.00000001:
            # prev is weekly value if weeks == 1, otherwise it is weekly average
            percentage = round((entry[category] / weeks / prev[category] - 1) * 100, 1)
            dynamics = f"{'+' if percentage >= 0.0 else ''}{percentage}%"
        else:
            dynamics = "~"
        
        print(f'    {category}: {get_category_string(entry[category], weeks, dynamics)}')

def present_schedule_annual(wd, year):
    entries = get_annual_entries(wd, year)

    weeks = len(entries)
    total = total_entry(entries)

    try: 
        prev = weekly_average_entry(get_annual_entries(wd, year-1))
    except:
        prev = {}

    print(f'    Annual The Schedule Time Stats for {year}, {weeks} weeks')
    present_single_schedule(total, weeks, prev)