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

def manual(categories):
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