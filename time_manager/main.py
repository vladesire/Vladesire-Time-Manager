import commands
import signal
from data.configuration import ConfigurationManager

def exit_handler(signum, frame):
    print("")
    print("Have a nice day!")
    exit(1)

signal.signal(signal.SIGINT, exit_handler)

cfg = ConfigurationManager()

print(f'-- Vladesire Time Manager -- {cfg.get_date()}', end = '')

if cfg.has_notion:
    print(' -- Notion Integrated --')
else:
    print('')

print('[ screen / pull / push / present / help / ... / exit ]')

# TODO: DO SOME VALIDATION OF COMMANDS
# TODO: DO SOME VALIDATION OF COMMANDS
# TODO: DO SOME VALIDATION OF COMMANDS

while True:
    command = input("> ")

    if 'screen' in command: 
        commands.enter_screen_manually(cfg.screen_categories, cfg.screen_wd, cfg.year, cfg.month)
        
    elif 'schedule' in command:
        commands.enter_schedule_manually(cfg.schedule_categories, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'pull' in command and cfg.has_notion:
        commands.pull_dispatcher(command, cfg.schedule_categories, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'push' in command and cfg.has_notion:
        commands.push_dispatcher(command, cfg.screen_wd, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'present' in command:
        commands.present_dispatcher(command, cfg.screen_wd, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'export' in command: 
        commands.export_dispatcher(command, cfg.screen_wd, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'next' in command: 
        cfg.next_month()
        print(f'Vladesire Time Manager is set for ~ {cfg.get_date()}')

    elif 'prev' in command: 
        cfg.prev_month()
        print(f'Vladesire Time Manager is set for ~ {cfg.get_date()}')

    elif 'help' in command:
        print('  Enter manually: screen / schedule') 
        print('  Select month: prev / next') 
    
        print('  Present data: present [month / part / year] [number]')
        print('    When period is not specified, month (week wise) is assumed')
        print('    When number is not specified, the last one is assumed')

        if cfg.has_notion:
            print('  Get schedule data from Notion: pull [last]')
            print('    Pull without arguments will prompt date range')
            print('    \'pull last\' will automatically determine date range of the previous week')

            print('  Push tables to Notion page: push [week/month/part/year] [number]')
            print('    When period is not specified, week is assumed')
            print('    When number is not specified, the last one is assumed')

    elif 'exit' in command:
        break

    else:
        print('Unknown command')