from features.common import apply_weekly, apply_monthly, apply_partly, apply_annual

def weekly_table(populate_table, wd: str, year: int, month: int, week: int) -> list[list[str]]:
    table = [['', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += apply_weekly(populate_table, wd, year, month, week)
    return table

def monthly_table(populate_table, wd, year, month):
    table = [['', f'Monthly', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += apply_monthly(populate_table, wd, year, month)
    return table

def partly_table(populate_table, wd, year, part):
    table = [['', f'Part {part}', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += apply_partly(populate_table, wd, year, part)
    return table

def annual_table(populate_table, wd, year):
    table = [['', f'{year}', 'Weekly', 'Daily', 'Quotient', 'Dynamics']]
    table += apply_annual(populate_table, wd, year)
    return table