import commands
from data.configuration import ConfigurationManager

cfg = ConfigurationManager()

print(f'-- Vladesire Time Manager -- {cfg.get_date()}', end = '')

if cfg.has_notion:
    print(' -- Notion Integrated --')
else:
    print('')

print('[ screen / schedule / present / help / ... / exit ]')

while True:
    command = input("> ")

    if 'screen' in command: 
        commands.enter_screen_manually(cfg.screen_categories, cfg.screen_wd, cfg.year, cfg.month)
        
    elif 'schedule' in command:
        commands.enter_schedule_manually(cfg.schedule_categories, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'pull' in command and cfg.has_notion:
        commands.pull_schedule_from_notion(cfg.schedule_categories, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'send' in command and cfg.has_notion:
        commands.send_last_week_tables(cfg.screen_wd, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'present' in command:
        commands.present_month(cfg.screen_wd, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'part' in command: 
        commands.present_part(cfg.screen_wd, cfg.schedule_wd, cfg.year)

    elif 'annual' in command:
        commands.present_year(cfg.screen_wd, cfg.schedule_wd, cfg.year)

    elif 'next' in command: 
        cfg.next_month()
        print(f'Vladesire Time Manager is set for ~ {cfg.get_date()}')

    elif 'prev' in command: 
        cfg.prev_month()
        print(f'Vladesire Time Manager is set for ~ {cfg.get_date()}')

    elif 'help' in command:
        print('  Enter manually: screen / schedule') 
        print('  Present data: present / part / annual')
        print('  Select month: prev / next') 
    
        if cfg.has_notion:
            print('  Get schedule data from Notion: pull')
            print('  Send tables to Notion page: send')

    elif 'exit' in command:
        break