from .process_salary import main as process_salary
from .convert_rate_of_pay_to_annual import main as convert_rate_of_pay_to_annual
from .get_summary import main as get_summary


def generate_result(search_vector, div):
    indeed_url = "https://www.indeed.com"
    titles = div.find_all(name='a', attrs={'data-tn-element':'jobTitle'})
    companies = div.find_all(name='span', attrs={'class': 'company'})
    salaries = div.find_all(name='span', attrs={'class': 'salary no-wrap'})
    locations = div.find_all(name='span', attrs={'class': 'location'})
    summary = div.find_all(name='span', attrs={'class': 'summary'})
    if summary:
        summary = summary[0]\
            .text\
            .strip()\
            .replace('`', '')\
            .replace('\\', '')

    # Process salary information
    salary = process_salary(salaries)
    sal = salary.get('salary')
    rop = salary.get('rate_of_pay')
    min_sal = convert_rate_of_pay_to_annual(
        rop,
        salary.get('min_sal'))
    max_sal = convert_rate_of_pay_to_annual(
        rop,
        salary.get('max_sal'))

    link = f"{indeed_url}{titles[0]['href']}"

    return dict(
            search_term=search_vector.term.strip(),
            title=titles[0]['title'],
            company=companies[0].text.strip() if companies else None,
            salary=sal,
            min_salary=min_sal,
            max_salary=max_sal,
            summary=summary,
            location=locations[0].text.strip()
                if locations
                else search_vector.loc.replace('+', ' '),
            url=link)

def main(search_vector, soup, goto=-1):
    divs = soup\
        .find_all(name='div', attrs={'class': 'jobsearch-SerpJobCard'})
    if len(divs) == 0:
        return [], 0
    retdata = (generate_result(search_vector, div)
        for div in divs[:goto])
    return retdata, len(divs)
