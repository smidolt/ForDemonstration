import csv
import re


def validate_date(date_str):
    # Check date format (day/month/year)
    pattern = r'\d{1,2}/\d{1,2}/\d{4}'
    return re.match(pattern, date_str)


def validate_platform(platform):
    return platform in ['iOS', 'Android']


def validate_positive_integer(value):
    try:
        num = int(value)
        return num > 0
    except ValueError:
        return False


def validate_revenue(revenue_str):
    # Check revenue format (€ number)
    pattern = r'€\d+\.\d{2}'
    return re.match(pattern, revenue_str)


def validate_revenue_usd(revenue_str):
    # Check revenue format (positive number)
    try:
        num = float(revenue_str)
        return num >= 0
    except ValueError:
        return False


def validate_totals_row(row):
    required_columns = ['Date', 'App', 'Platform', 'Requests', 'Impressions', 'Revenue (usd)']
    for column in required_columns:
        if column not in row:
            return False

    return row['Date'] == 'Totals'


def validate_requests_impressions(row, filename):
    requests = int(row['Requests'])
    impressions = int(row['Impressions'])
    return requests >= impressions, filename


column_validators_type1 = {
    'Date': validate_date,
    'Platform': validate_platform,
    'Requests': validate_positive_integer,
    'Impressions': validate_positive_integer,
    'Revenue': validate_revenue
}

column_validators_type2 = {
    'Date': validate_date,
    'Platform': validate_platform,
    'Requests': validate_positive_integer,
    'Impressions': validate_positive_integer,
    'Revenue (usd)': validate_revenue_usd
}


def validate_file(filename, column_validators):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for line_number, line in enumerate(reader, start=1):
            if validate_totals_row(line):
                continue

            is_valid_row = all(validator(line[column]) for column, validator in column_validators.items())

            result, file = validate_requests_impressions(line, filename)
            if not result:
                print(f"Error in file {file}, line {line_number}: Impressions value is greater than Requests value")

            if not is_valid_row:
                print(f"Error in file {filename}, line {line_number}: {line}")


validate_file('2017-09-15.csv', column_validators_type1)
validate_file('2017-09-16.csv', column_validators_type1)
validate_file('adumbrella-15_9_2017.csv', column_validators_type2)
validate_file('adumbrella-16_9_2017.csv', column_validators_type2)
