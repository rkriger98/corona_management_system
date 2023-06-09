import re
import datetime


def is_validate_id_number(id_number):
    if not (str(id_number)).isdigit():
        raise ValueError("Invalid ID format")
    id_12_digits = [1, 2, 1, 2, 1, 2, 1, 2, 1]
    id_num = str(id_number)
    id_num = '0' * (9 - len(id_num)) + id_num
    result = 0
    for i in range(9):
        num = int(id_num[i]) * id_12_digits[i]
        num = (num // 10) + (num % 10) if (num >= 10) else num
        result += num
    if result % 10 == 0:
        return True
    raise ValueError("Incorrect ID number")


def is_valid_mobile_phone_number(phone_number):
    """
    Information from: https://en.wikipedia.org/wiki/Telephone_numbers_in_Israel
    X = any number
    N = any number excluding 0
    """
    patterns = [
        r'^07(18|22|23)\d{6}$',  # 0718XXXXXX, 0722XXXXXX, 0723XXXXXX
        r'^073[237]\d{6}$',  # 0732XXXXXX, 0733XXXXXX, 0737XXXXXX
        r'^0747\d{6}$',  # 0747XXXXXX
        r'^076[58]\d{6}$',  # 0765XXXXXX, 0768XXXXXX
        r'^077[1-9]\d{6}$',  # 077NXXXXXX
        r'^079[2-9]\d{6}$',  # 0792XXXXXX - 0799XXXXXX
        r'^051[25]\d{6}$',  # 0512XXXXXX, 0515XXXXXX
        r'^05[0234689][1-9]\d{6}$',  # 05YNXXXXXX (Y is one of 0,2,3,4,6,8,9)
        r'^055[23]{2}\d{5}$',  # 055YYXXXXX (Y is 2 or 3)
        r'^055(44|55|77)\d{5}$',  # 05544XXXXX, ‎05555XXXXX, 05577XXXXX
        r'^0555[01]\d{6}$',  # 0555YXXXXX (Y is 0 or 1)
        r'^0556[678]\d{5}$',  # 0556YXXXXX (Y is 6 or 7 or 8)
        r'^0557[012]\d{5}$',  # 0557YXXXXX (Y is 0 or 1 or 2)
        r'^0558[789]\d{5}$',  # 0558YXXXXX (Y is 7 or 8 or 9)
        r'^0559[1-9]\d{5}$']  # 0559NXXXXX
    for pattern in patterns:
        if re.match(pattern, str(phone_number)):
            return True
    raise ValueError("Incorrect mobile phone number")


def is_valid_landline_phone_number(phone_number):
    """
    Information from: https://en.wikipedia.org/wiki/Telephone_numbers_in_Israel
    X = any number
    """
    patterns = [
        r'^0[23489](30|31)[0-9]{4}$',  # (0A) = 02,03,04,08,09: (0A)30XXXXX, (0A)31XXXXX
        r'^0[23489]37[02-8]{3}$',  # (0A)370XXXX, (0A)372XXXX - (0A)379XXXX
        r'^0[23489]38[01]{4}$',  # (0A)380XXXX, (0A)381XXXX
        r'^0[23489][56789][0-9]{6}$']  # (0A)YXXXXXX (Y is one of 5,6,7,8,9)
    for pattern in patterns:
        if re.match(pattern, str(phone_number)):
            return True
    raise ValueError("Incorrect telephone number")


def is_valid_dob(dob):
    dob_datetime = parse_date(dob)
    hundred_years_ago = datetime.datetime.now() - datetime.timedelta(days=36524.25)
    # the average length of the calendar year (the mean year) is 365.2425 days
    if hundred_years_ago <= dob_datetime <= datetime.datetime.now():
        return True
    else:
        raise ValueError("Date of birth doesn't make sense")


def is_only_letters(user_input):
    for word in user_input:
        if not bool(re.match("^[a-zA-Z' -]+$", str(word))):
            raise ValueError("Input contains non-letter characters")
    return True


def parse_date(date):
    try:
        return datetime.datetime.strptime(str(date), "%Y-%m-%d")
    except ValueError:
        raise ValueError("The dates must be in the format of 'yyyy-mm-dd'")
