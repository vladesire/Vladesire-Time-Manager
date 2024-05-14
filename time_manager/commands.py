from data.entries import append_entry
from data.notion.api import NotionApi
from features.schedule import schedule_input, schedule_present, schedule_table
from features.screen import screen_input, screen_present, screen_table


def enter_screen_manually(
    screen_categories: list[str], 
    screen_wd: str, 
    year: int, 
    month: int
):
    entry = screen_input.manual(screen_categories)
    append_entry(entry, screen_wd, month, year)

    print('    Saved!')


def enter_schedule_manually(
    schedule_categories: list[str], 
    schedule_wd: str, 
    year: int, 
    month: int
):
    entry = schedule_input.manual(schedule_categories)
    append_entry(entry, schedule_wd, month, year)

    print('    Saved!')


def pull_schedule_from_notion(
    schedule_categories: list[str], 
    schedule_wd: str, 
    year: int, 
    month: int
): 
    start = input(f'  Start date: ')
    end = input(f'  End date:   ')

    entry = schedule_input.pull_from_notion(schedule_categories, start, end)

    print(f'  {entry}')
    save = input(f'  Save? [y/n]: ')

    if 'y' in save:
        append_entry(entry, schedule_wd, month, year)
        print('  Saved!')
    else: 
        print('  Abort.')



def send_last_week_tables(
    screen_wd: str, 
    schedule_wd: str, 
    year: int, 
    month: int
): 
    api = NotionApi()

    r = api.send_table(
        table = screen_table.for_last_entry(screen_wd, year, month)
    )

    print(f'  Sending schedule table: {r.status_code}')

    r = api.send_table(
        table = schedule_table.for_last_entry(schedule_wd, year, month)
    )

    print(f'  Sending schedule table: {r.status_code}')


def present_month(
    screen_wd: str, 
    schedule_wd: str, 
    year: int, 
    month: int
): 
    try: 
        screen_present.monthly(screen_wd, month, year)
    except:
        print('No screen time data for this month. Use command \'screen\' first')

    print('\n    --------------------\n')
    
    try: 
        schedule_present.monthly(schedule_wd, month, year)
    except:
        print('No schedule time data for this month. Use command \'schedule\' first')


def present_year(
    screen_wd: str, 
    schedule_wd: str, 
    year: int
): 
    try: 
        screen_present.annual(screen_wd, year)
        print('\n    --------------------\n')
    except:
        print('No screen time data or data is corrupted.')

    try: 
        schedule_present.annual(schedule_wd, year)
    except:
        print('No schedule time data or data is corrupted.')