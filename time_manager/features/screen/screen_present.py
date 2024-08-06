from features.common import present_week_wise, apply_partly, apply_annual, get_dynamics

def get_total_string(minutes, weeks):
    if weeks == 1:
        return f"{round(minutes/60, 1)} / {round(minutes/60/7, 1)}"
    else:
        return f"{round(minutes/60, 1)} / {round(minutes/60/weeks, 1)} / {round(minutes/60/weeks/7, 1)}"

def get_category_string(minutes, weeks, total, dynamics = '~'):
    return f"{get_total_string(minutes, weeks)} / {round(minutes/total*100, 1)}%"

def present(entry, weeks = 1, prev = {}):
    total = entry['Total']
    
    if 'Total' in prev and prev['Total'] > 0:
        dynamics = get_dynamics(total, weeks, prev['Total'])
    else:
        dynamics = '~'

    print(f'    Total: { get_total_string(total, weeks) } / {dynamics}')

    del entry['Total']

    for category in entry:
        minutes = entry[category]

        if category in prev and prev[category] > 0:
            dynamics = get_dynamics(minutes, weeks, prev[category])
        else:
            dynamics = "~"

        print(f'    {category}: { get_category_string(minutes, weeks, total) } / {dynamics}')

def week_wise(wd: str, year: int, month: int):
    print(f'The Screen Time Stats for {year}-{month}')
    print('Format weekly: total / daily / quotient')
    print('Format monthly: total / weekly / daily / quotient')
    present_week_wise(present, wd, year, month, ['Total'])

def partly(wd: str, year: int, part: int):
    print(f'  Screen Time Stats for {year} part {part}')
    print('  Format: total / weekly / daily / quotient / dynamics\n')
    apply_partly(present, wd, year, part)

def annual(wd, year):
    print(f'  Annual Screen Time Stats for {year}')
    print('  Format: total / weekly / daily / quotient / dynamics\n')
    apply_annual(present, wd, year)