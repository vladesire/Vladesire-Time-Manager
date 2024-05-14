import yaml
import glob

def total_entry(entries):
    total = {}

    for entry in entries: 
        entry = entry['Entry']

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

def file_name(root, month, year): 
    if month > 9:
        return f'{root}/{year}-{month}.yaml'
    else: 
        return f'{root}/{year}-0{month}.yaml'

def append_entry(entry, wd, month, year):
    with open(file_name(wd, month, year), 'a+') as file:
        entries = yaml.safe_load(file) or []
        entries.append({'Entry':entry})
        file.truncate()
        yaml.dump(entries, file, sort_keys=False)

def get_entries(wd, month, year):
    with open(file_name(wd, month, year), 'r') as file:
        entries = yaml.safe_load(file)

    return entries

def get_entries_subset(wd: str, year: str, month_subset: list[int]):
    subset_list = []

    files = [f'{wd}/{year}-{month}.yaml' for month in month_subset]

    for file in files:
        with open(file, 'r') as file:
            entries = yaml.safe_load(file)
            subset_list += entries

    return subset_list

def get_annual_entries(wd, year):
    annual_list = []

    for file in sorted(glob.glob(f'{wd}/{year}*')):
        with open(file, 'r') as file:
            entries = yaml.safe_load(file)
            annual_list += entries

    return annual_list