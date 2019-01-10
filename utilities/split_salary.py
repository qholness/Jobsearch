def main(salary):
    salary = salary.split('-')
    min_val = None
    max_val = None
    min_val = float(salary[0].replace(',',''))
    if len(salary) == 2:
        max_val = float(salary[1].replace(',',''))
    return min_val, max_val