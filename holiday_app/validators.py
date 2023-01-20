from datetime import datetime


def date_validator(start_dt=None, end_dt=None):

    FORMAT = "%Y-%m-%d"
    res = True

    dict1 = {}
    errors = {}

    if start_dt:
        try:
            res = bool(datetime.strptime(start_dt, FORMAT))
        except ValueError:
            res = False
            errors["start_date"] = ["Start Date not valid format."]

    if end_dt:
        try:
            res = bool(datetime.strptime(end_dt, FORMAT))
        except ValueError:
            res = False
            errors["end_date"] = ["End Date not valid format."]

    start_dt = datetime.strptime(start_dt, "%Y-%m-%d")
    end_dt = datetime.strptime(end_dt, "%Y-%m-%d")
    if start_dt > end_dt:
        errors["start_date"] = ["Enter Valid Start date and End date."]

    dict1["errors"] = errors

    if len(errors.keys()) > 0:
        return dict1
