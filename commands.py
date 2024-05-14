from entries import append_entry, get_entries_subset
from screen import input_screen, present_screen, present_screen_annual
from schedule import input_schedule, present_schedule, present_schedule_annual
from screen_notion import send_last_screen_table
from schedule_notion import send_last_schedule_table, get_entry_from_notion

def enter_screen_manually(
    screen_categories: list[str], 
    screen_wd: str, 
    year: int, 
    month: int
):
    entry = input_screen(screen_categories)
    append_entry(entry, screen_wd, month, year)

    print('    Saved!')

def enter_schedule_manually(
    schedule_categories: list[str], 
    schedule_wd: str, 
    year: int, 
    month: int
):
    entry = input_schedule(schedule_categories)
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

    entry = get_entry_from_notion(schedule_categories, start, end)

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
    send_last_screen_table(screen_wd, month, year)
    send_last_schedule_table(schedule_wd, month, year)

def present_month(
    screen_wd: str, 
    schedule_wd: str, 
    year: int, 
    month: int
): 
    try: 
        present_screen(screen_wd, month, year)
        print('\n    --------------------\n')
    except:
        print('No screen time data for this month. Use command \'screen\' first')

    try: 
        present_schedule(schedule_wd, month, year)
    except:
        print('No schedule time data for this month. Use command \'schedule\' first')

def present_year(
    screen_wd: str, 
    schedule_wd: str, 
    year: int
): 
    try: 
        present_screen_annual(screen_wd, year)
        print('\n    --------------------\n')
    except:
        print('No screen time data or data is corrupted.')

    try: 
        present_schedule_annual(schedule_wd, year)
    except:
        print('No schedule time data or data is corrupted.')