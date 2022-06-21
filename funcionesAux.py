import datetime as dt

CONVERSION_MESES = {1:"ENE",
                    2:"FEB",
                    3:"MAR",
                    4:"ABR",
                    5:"MAY",
                    6:"JUN",
                    7:"JUL",
                    8:"AGO",
                    9:"SEP",
                    10:"OCT",
                    11:"NOV",
                    12:"DIC"}

CIERRES = {2: dt.date(2022,2, 18),
           4: dt.date(2022, 4, 15),
           6: dt.date(2022, 6, 16),
           8: dt.date(2022, 8, 19),
           10: dt.date(2022, 10, 21),
           12: dt.date(2022, 12, 16)}

def getFuturesDate(date):
    for key in CIERRES.keys():
        try:
            if date > CIERRES[key] and date < CIERRES[key+2]:
                return {"PASADO": CONVERSION_MESES[key] + str(CIERRES[key].year)[-2:],
                        "ACTUAL": CONVERSION_MESES[key+2] + str(CIERRES[key+2].year)[-2:],
                        "FUTURO": CONVERSION_MESES[key+4] + str(CIERRES[key+4].year)[-2:],
                        "FECHA ACTUAL": CIERRES[key + 2],
                        "FECHA PASADO": CIERRES[key],
                        "FECHA FUTURO": CIERRES[key + 4]
                        }
        except KeyError:
            return "La fecha ingresada es muy lejana"


def convert_datetime_to_date(datetime):
    return datetime.date()

def days_to_maturity(current_date, maturity_date):
    current_date = convert_datetime_to_date(current_date)
    return (maturity_date - current_date).days

if __name__ == '__main__':
    fecha = dt.date(2022,10,12)
    a = getFuturesDate(fecha)
    print(a)
    dt = dt.datetime(2022,10,15,18,33,56)
    b = convert_datetime_to_date(dt)
    print(b)
    print(type(b))