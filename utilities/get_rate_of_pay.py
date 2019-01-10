def main(salary_string):
    if "a year" in salary_string or\
        "per year" in salary_string:
        return 'yearly'
    if "a month" in salary_string or\
        "per month" in salary_string:
        return 'monthly'
    if "a week" in salary_string or\
        "per week" in salary_string:
        return 'weekly'
    if "a day" in salary_string or\
        "per day" in salary_string:
        return 'daily'
    if "an hour" in salary_string or\
        "per hour" in salary_string:
        return 'hourly'