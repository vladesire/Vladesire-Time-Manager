from data.entries import total_entry, weekly_average_entry, get_monthly_entries, get_partly_entries, get_annual_entries, get_prev_monthly_average, get_prev_partly_average, get_prev_annual_average
from data.configuration import months

def get_dynamics(current: int, weeks: int, prev: int) -> str:
    percentage = round((current / weeks / prev - 1) * 100, 1)
    return f"{'+' if percentage > 0 else ''}{percentage}%"

'''    
    categories -- list for distribution

    present is lambda:
        1. entry / total
        2. weeks
        3. prev average
'''

def present_week_wise(present, wd: str, year: int, month: int, categories: list[str] = []):
    entries = get_monthly_entries(wd, year, month)
    weeks = len(entries)
    total = total_entry(entries)

    if weeks == 0:
        print('No data for this month!')
        return 

    for week, entry in enumerate(entries, start = 1):
        if week == 1:
            # If it's the first week of January, then no comparison is needed
            prev = get_monthly_entries(wd, year, month-1)[-1]
        else:
            prev = entries[week - 2]

        print(f'\n--- [ Week {week} ] ---\n')


        for category in categories:
            if category in total and total[category] > 0:
                print(f'    Weekly {category} quotient: {round(entry[category]/total[category]*100, 1)}%')

            

        present(entry, 1, prev)

    print('\n--- Monthly ---\n')
    present(total, weeks, get_prev_monthly_average(wd, year, month))


'''
    apply is lambda which takes three arguments:
        - entry/total: sum of all weekly entries
        - weeks: number of weeks 
        - prev: weekly average of the previous period
'''

def apply_weekly(apply, wd: str, year: int, month: int, week: int):
    entries = get_monthly_entries(wd, year, month)
    weeks = len(entries)

    if week == -1 and weeks > 1: 
        # The last week is assumed
        prev = entries[-2]
    elif week > 1:
        # Convert it to index
        week -= 1
        prev = entries[week - 1]
    else:
        # Try to load the last entry from previous month
        # If it's January -- consider the first week as a new beginning
        try: 
            prev = get_monthly_entries(wd, year, month - 1)[-1]
        except:
            prev = {}

    return apply(
        entries[week],
        weeks = 1,
        prev = prev
    )

def apply_monthly(apply, wd: str, year: int, month: int):
    entries = get_monthly_entries(wd, year, month)

    return apply(
        total_entry(entries),
        weeks = len(entries),
        prev = get_prev_monthly_average(wd, year, month)
    )

def apply_partly(apply, wd: str, year: int, part: int):
    entries = get_partly_entries(wd, year, part)

    return apply(
        total_entry(entries),
        weeks = len(entries),
        prev = get_prev_partly_average(wd, year, part)
    )

def apply_annual(apply, wd: str, year: int):
    entries = get_annual_entries(wd, year)

    return apply(
        total_entry(entries),
        weeks = len(entries),
        prev = get_prev_annual_average(wd, year)
    )


def monthly_distribution_table(wd, year, month):
    entries = get_monthly_entries(wd, year, month)
    total = total_entry(entries)
    weeks = len(entries)

    table = [[''] + [f'Week {week}' for week in range(1, weeks+1)]]

    for category in total:
        if total[category] > 0:
            row = [category]

            for entry in entries:
                if category in entry:
                    row.append(f'{round(entry[category]/total[category]*100, 1)}%')
                else:
                    row.append('~')
            
            table += [row]

    return table

def partly_distribution_table(wd, year, part):
    subsets = {1: [1, 2, 3, 4], 2: [5, 6, 7, 8], 3: [9, 10, 11, 12]}

    all_entries = get_partly_entries(wd, year, part)
    total = total_entry(all_entries)

    monthly_entries = [get_monthly_entries(wd, year, month) for month in subsets[part]]
    month_wise_entries = [total_entry(monthly_entry) for monthly_entry in monthly_entries]

    offset = (part - 1) * 4
    table = [[''] + [f'{months[month]}' for month in range(1 + offset, 5 + offset)]]

    for category in total:
        if total[category] > 0:
            row = [category]

            for entry in month_wise_entries:
                if category in entry:
                    row.append(f'{round(entry[category]/total[category]*100, 1)}%')
                else:
                    row.append('~')
            
            table += [row]

    return table


def annual_distribution_table(wd, year):
    all_entries = get_annual_entries(wd, year)
    total = total_entry(all_entries)

    partly_entries = [get_partly_entries(wd, year, part) for part in [1, 2, 3]]
    part_wise_entries = [total_entry(partly_entry) for partly_entry in partly_entries]

    table = [['', 'Part I', 'Part II', 'Part III']]

    for category in total:
        if total[category] > 0:
            row = [category]

            for entry in part_wise_entries:
                if category in entry:
                    row.append(f'{round(entry[category]/total[category]*100, 1)}%')
                else:
                    row.append('~')
            
            table += [row]

    return table