from data.notion.api import NotionApi

def pull_from_notion(
    categories: list[str], 
    start_date: str, 
    end_date: str
) -> dict[str, int]:
    return NotionApi().query_schedule_database(categories, start_date, end_date)

def manual(categories: list[str]) -> dict[str, int]: 
    entry = {}
    sum = 0.0

    for category in categories: 
        time = input(f"    {category}: ")
        
        try: 
            time = float(time)
        except:
            time = 0

        sum += time    
        entry[category] = time

    entry['Sleep'] = 168 - sum

    return entry