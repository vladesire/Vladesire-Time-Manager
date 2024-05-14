import commands
from configuration_manager import ConfigurationManager

cfg = ConfigurationManager()

print(f"Vladesire Time Manager ~ {cfg.get_date()}")
print(f"[Enter manually: screen / schedule] [Present data: present / part / annual]")
print(f'[Select month: prev / next] [Notion: pull / send] [exit]')

while True:
    command = input("> ")

    if 'screen' in command: 
        commands.enter_screen_manually(cfg.screen_categories, cfg.screen_wd, cfg.year, cfg.month)
        
    elif 'schedule' in command:
        commands.enter_schedule_manually(cfg.schedule_categories, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'pull' in command:
        commands.pull_schedule_from_notion(cfg.schedule_categories, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'send' in command:
        commands.send_last_week_tables(cfg.screen_wd, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'present' in command:
        commands.present_month(cfg.screen_wd, cfg.schedule_wd, cfg.year, cfg.month)

    elif 'part' in command: 
        pass

    elif 'annual' in command:
        commands.present_year(cfg.screen_wd, cfg.schedule_wd, cfg.year)

    elif 'next' in command: 
        cfg.next_month()
        print(f'Vladesire Time Manager is set for ~ {cfg.get_date()}')

    elif 'prev' in command: 
        cfg.prev_month()
        print(f'Vladesire Time Manager is set for ~ {cfg.get_date()}')

    elif 'exit' in command:
        break