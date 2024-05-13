from entries import load_configuration, rewrite_configuration, append_entry
from screen import input_screen, present_screen, present_screen_annual
from schedule import input_schedule, present_schedule, present_schedule_annual
from screen_notion import send_last_screen_table
from schedule_notion import send_last_schedule_table, get_entry_from_notion


months = ['ZERO', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

config = load_configuration()
screen_wd = config['screen-working-directory']
schedule_wd = config['schedule-working-directory']
month = config['current']['month']
year = config['current']['year']

print(f"Vladesire Time Manager ~ {months[month]} {year}")
print(f"[ screen / schedule / present / annual / prev / next / exit ]")
print(f"[ query / send ]")

while True:

    command = input("> ")

    if 'screen' in command: 
        entry = input_screen(config['screen-categories'])
        append_entry(entry, screen_wd, month, year)

    elif 'schedule' in command:
        entry = input_schedule(config['schedule-categories'])
        append_entry(entry, schedule_wd, month, year)

    elif 'query' in command:
        start = input(f"    start date: ")
        end = input(f"    end date: ")

        entry = get_entry_from_notion(config['schedule-categories'], start, end)

        print(entry)
        save = input(f'Save? [y/n]: ')

        if 'y' in save:
            append_entry(entry, schedule_wd, month, year)
        else: 
            print('Abort')

    elif 'send' in command:
        send_last_schedule_table(schedule_wd, month, year)
        send_last_screen_table(screen_wd, month, year)

    elif 'present' in command:
        try: 
            present_screen(screen_wd, month, year)
            print('\n    --------------------\n')
        except:
            print('No screen time data for this month. Use command \'screen\' first')

        try: 
            present_schedule(schedule_wd, month, year)
        except:
            print('No schedule time data for this month. Use command \'schedule\' first')

    elif 'annual' in command:
        try: 
            present_screen_annual(screen_wd, year)
            print('\n    --------------------\n')
        except:
            print('No screen time data or data is corrupted.')

        try: 
            present_schedule_annual(schedule_wd, year)
        except:
            print('No schedule time data or data is corrupted.')


    elif 'next' in command: 
        if month < 12: 
            config['current']['month'] = month + 1

        if month == 12: 
            config['current']['month'] = 1
            config['current']['year'] = year + 1

        month = config['current']['month']
        year = config['current']['year']

        rewrite_configuration(config)

        print(f'Screen Time Manager is set for ~ {months[month]} {year}')


    elif 'prev' in command:
        if month > 1:
            config['current']['month'] = month - 1

        if month == 1: 
            config['current']['month'] = 12
            config['current']['year'] = year - 1

        month = config['current']['month']
        year = config['current']['year']

        rewrite_configuration(config)

        print(f'Screen Time Manager is set for ~ {months[month]} {year}')


    elif 'exit' in command:
        break