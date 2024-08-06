from features.common import present_week_wise, apply_partly, apply_annual, get_dynamics

def get_category_string(time, weeks, dynamics = '~'):
    # Adding 0.001 solved wrong rounding problem
    if weeks == 1: 
        return f"{round(time + 0.001, 1)} / {round(time / 7, 1)} / {round(time / 168 * 100, 1)}% / {dynamics}"
    else:
        return f"{round(time + 0.001, 1)} / {round(time / weeks, 1)} / {round(time / weeks / 7, 1)} / {round(time / weeks / 168 * 100, 1)}% / {dynamics}"

def present(entry, weeks = 1, prev = {}):
    for category in entry: 
        if category in prev and prev[category] > 0:
            dynamics = get_dynamics(entry[category], weeks, prev[category])
        else:
            dynamics = "~"
        
        print(f'    {category}: {get_category_string(entry[category], weeks, dynamics)}')

def week_wise(wd: str, year: int, month: int):
    print(f'The Schedule Stats for {year}-{month}')
    print('Format weekly: total / daily / quotient / dynamics')
    print('Format monthly: total / weekly / daily / quotient / dynamics')
    present_week_wise(present, wd, year, month, ['Sleep'])

def partly(wd: str, year: int, part: int):
    print(f'  The Schedule Time Stats for {year} part {part}')
    apply_partly(present, wd, year, part)

def annual(wd: str, year: int):
    print(f'  Annual The Schedule Time Stats for {year}')
    apply_annual(present, wd, year)