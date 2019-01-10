from .get_rate_of_pay import main as get_rate_of_pay
from .salary_string_pre_process import main as salary_string_pre_process
from .split_salary import main as split_salary


def main(salary):
    if salary == []:
        return dict()
    salary = salary[0].text.lower().strip()
    rate_of_pay = get_rate_of_pay(salary)
    sal = salary_string_pre_process(salary)
    min_sal, max_sal = split_salary(sal)
    return dict(
            rate_of_pay=rate_of_pay,
            salary=sal,
            min_sal=min_sal,
            max_sal=max_sal)