from data.entries import total_entry, weekly_average_entry, get_entries, get_annual_entries, get_entries_subset

# dist_cat -- monthly distrubution categories

def present_monthly(wd: str, month: int, year: int, present, dist_cat: list[str] = []):
    entries = get_entries(wd, month, year)
    weeks = len(entries)

    if weeks == 0:
        print('Empty month')
        return

    total = total_entry(entries)

    # Weekly
    for week, entry in enumerate(entries, start=1): 
        print('  ----------')
        print(f'  Week {week}')

        if week > 1: 
            prev = entries[week - 2]['Entry']
        else:
            # Try to load the last entry from previous month
            # If it's January -- consider the first week as a new beginning
            try: 
                prev = get_entries(wd, month - 1, year)[-1]['Entry']
            except:
                prev = {}

        entry = entry['Entry'].copy()

        for category in dist_cat:
            print(f'    Weekly {category} quotient: {round(entry[category]/total[category]*100, 1)}%')

        present(entry = entry, prev = prev)

    # Monthly
    print('  ----------')
    print('  Total')
    print(f'    ({weeks} weeks)')

    try: 
        prev = weekly_average_entry(get_entries(wd, month - 1, year))
    except:
        prev = {}

    present(entry = total, weeks = weeks, prev = prev)

def apply_partly(wd: str, year: int, part: int, apply): 
    subsets = {1: [1, 2, 3, 4], 2: [5, 6, 7, 8], 3: [9, 10, 11, 12]}

    entries = get_entries_subset(wd, year, subsets[part])

    weeks = len(entries)

    total = total_entry(entries)

    try: 
        if part == 1:
            prev = weekly_average_entry(get_entries_subset(wd, year - 1, subsets[3]))
        else: 
            prev = weekly_average_entry(get_entries_subset(wd, year, subsets[part - 1]))
    except:
        prev = {}


    print(f'    {weeks} weeks')

    return apply(entry = total, weeks = weeks, prev = prev)

def apply_annual(wd: str, year: int, apply):
    entries = get_annual_entries(wd, year)

    weeks = len(entries)
    total = total_entry(entries)

    try: 
        prev = weekly_average_entry(get_annual_entries(wd, year-1))
    except:
        prev = {}

    print(f'    {weeks} weeks')    

    return apply(total, weeks = weeks, prev = prev)


def get_dynamics(current: int, weeks: int, prev: int) -> str:
    percentage = round((current / weeks / prev - 1) * 100, 1)
    return f"{'+' if percentage > 0 else ''}{percentage}%"