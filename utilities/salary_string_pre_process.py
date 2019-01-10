def main(salary):
    salary = salary.replace("$", "")\
        .replace('(indeed est.)', '').strip()
    salary = salary\
        .replace("an hour", "")\
        .replace("per year", "")\
        .replace("a year", "")\
        .replace("per month", "")\
        .replace("a month", "")\
        .replace("per week", "")\
        .replace("a week", "")\
        .replace("per day", "")\
        .replace("a day", "")\
        .replace("$", "")\
        .strip()
    salary = list(map(lambda x: x.strip(), salary.split("-")))
    salary = "-".join(salary)
    return salary