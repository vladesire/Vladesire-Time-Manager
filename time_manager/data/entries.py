import yaml

def file_name(root: str, year: int, month: int): 
    if month > 9:
        return f'{root}/{year}-{month}.yaml'
    else: 
        return f'{root}/{year}-0{month}.yaml'
    
def append_entry(entry, wd, month, year):
    with open(file_name(wd, year, month), 'a+') as file:
        entries = yaml.safe_load(file) or []
        entries.append({'Entry':entry})
        file.truncate()
        yaml.dump(entries, file, sort_keys=False)

def load_entries(wd: str, year: str, month_subset: list[int]):
    total = []
    files = [file_name(wd, year, month) for month in month_subset]

    for file in files:
        try: 
            with open(file, 'r') as file:
                entries = yaml.safe_load(file)
                total += [entry['Entry'] for entry in entries]
        except: 
            continue
            
    return total

def get_annual_entries(wd: str, year: int):
    return load_entries(wd, year, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

def get_partly_entries(wd: str, year: int, part: int):
    subsets = {1: [1, 2, 3, 4], 2: [5, 6, 7, 8], 3: [9, 10, 11, 12]}
    return load_entries(wd, year, subsets[part])

def get_monthly_entries(wd: str, year: int, month: int):
    return load_entries(wd, year, [month])


def total_entry(entries):
    total = {}

    for entry in entries: 
        for category in entry: 
            if category in total: 
                total[category] += entry[category]
            else: 
                total[category] = entry[category]

    return total

def weekly_average_entry(entries):
    weeks = len(entries)
    total = total_entry(entries)

    for category in total:
        total[category] /= weeks

    return total

def get_prev_annual_average(wd: str, year: int):
    try: 
        entries = get_annual_entries(wd, year - 1)
        return weekly_average_entry(entries)
    except:
        return {}

def get_prev_partly_average(wd: str, year: int, part: int):
    try: 
        if part == 1:
            entries = get_partly_entries(wd, year - 1, 3)
        else: 
            entries = get_partly_entries(wd, year, part - 1)

        return weekly_average_entry(entries)
    except:
        return {}

def get_prev_monthly_average(wd: str, year: int, month: int):
    try: 
        if month == 1:
            entries = get_monthly_entries(wd, year - 1, 12)
        else: 
            entries = get_monthly_entries(wd, year, month - 1)

        return weekly_average_entry(entries)
    except:
        return {}