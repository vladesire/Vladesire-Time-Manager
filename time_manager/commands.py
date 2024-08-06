from data.entries import append_entry
from data.notion.api import NotionApi
from data.configuration import months
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


def pull_dispatcher(
    command: str,
    schedule_categories: list[str], 
    schedule_wd: str, 
    year: int, 
    month: int
): 
    if command == 'pull':
        start = input(f'  Start date: ')
        end = input(f'  End date:   ')
    elif command == 'pull last':
        # TODO: HERE I MUST AUTOMATICALLY DETERMINE BOUNDARIES OF THE PREVIOUS WEEK
        print('IN DEVELOPMENT')
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



def push_dispatcher(
    command: str, 
    screen_wd: str, 
    schedule_wd: str, 
    year: int, 
    month: int
): 
    
    api = NotionApi()
    
    if command == 'push' or command[:9] == 'push week':

        if command == 'push' or len(command) == 9:
            # Assume previous week
            week = -1
        else:
            # Get week from command
            week = int(command[10:])

        r = api.send_table(
            table = screen_table.for_week(screen_wd, year, month, week)
        )

        print(f'  Pushing screen table for {months[month]} {year} Week {week}: {r.status_code}')

        r = api.send_table(
            table = schedule_table.for_week(schedule_wd, year, month, week)
        )

        print(f'  Pushing schedule table for {months[month]} {year} Week {week}: {r.status_code}')

    elif command[:10] == 'push month':

        if command != 'push month':
            month = int(command[11:])

        # Otherwise, current week is assumed

        r = api.send_table(
            table = screen_table.for_month(screen_wd, year, month)
        )

        print(f'  Pushing screen table for {months[month]} {year}: {r.status_code}')

        r = api.send_table(
            table = schedule_table.for_month(schedule_wd, year, month)
        )

        print(f'  Pushing schedule table for {months[month]} {year}: {r.status_code}')

    elif command[:9] == 'push part':

        # TODO: DO SOME VALIDATION OF COMMAND

        if len(command) == 9:
            # TODO: DETERMINE THE LAST PART ON MY OWN
            part = 1
        else:
            part = int(command[10:])

        if part == 1 or part == 2 or part == 3:
            
            r = api.send_table(
                table = screen_table.for_part(screen_wd, year, part)
            )

            print(f'  Pushing screen table for {year} part {part}: {r.status_code}')

            r = api.send_table(
                table = schedule_table.for_part(schedule_wd, year, part)
            )

            print(f'  Pushing schedule table for {year} part {part}: {r.status_code}')
        else:
            print('There are only three part in the year')

    elif command[:9] == 'push year':

        # TODO: IF YEAR IS SPECIFIED -- CHECK IF IT IS VALID

        if len(command) == 9:
    
            r = api.send_table(
                table = screen_table.for_year(screen_wd, year)
            )

            print(f'  Pushing screen table for {year}: {r.status_code}')

            r = api.send_table(
                table = schedule_table.for_year(schedule_wd, year)
            )

            print(f'  Pushing schedule table for {year}: {r.status_code}')


def present_dispatcher(
    command: str,
    screen_wd: str, 
    schedule_wd: str, 
    year: int, 
    month: int
):
    if command == 'present' or command[0:13] == 'present month':
        if len(command) > 13:
            month = int(command[14:])

        try: 
            screen_present.week_wise(screen_wd, year, month)
        except:
            print('No screen time data for this month. Use command \'screen\' first')

        print('\n    --------------------\n')
        
        try: 
            schedule_present.week_wise(schedule_wd, year, month)
        except:
            print('No schedule time data for this month. Use command \'schedule\' first')

    elif command[0:12] == 'present part':
        if len(command) == 12:
            # TODO: DETERMINE THE LAST PART ON MY OWN
            part = 1
        else: 
            part = int(command[13:])
    
        try: 
            screen_present.partly(screen_wd, year, part)
        except:
            print('No screen time data or data is corrupted.')

        print('\n    --------------------\n')

        try: 
            schedule_present.partly(schedule_wd, year, part)
        except:
            print('No screen time data or data is corrupted.')

    elif command[0:12] == 'present year':
        if len(command) != 12:
            year = int(command[13:])
        
        try: 
            screen_present.annual(screen_wd, year)
        except:
            print('No screen time data or data is corrupted.')

        print('\n    --------------------\n')

        try: 
            schedule_present.annual(schedule_wd, year)
        except:
            print('No schedule time data or data is corrupted.')