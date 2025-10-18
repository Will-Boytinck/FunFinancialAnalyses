import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

START_DATE = '03/1998'
END_DATE = '03/2025'

def main():
    filenames = ['TD1.csv', 'RY1.csv', 'CIBC1.csv', 'BMO1.csv', 'SCOTIA1.csv']
    dates = create_ranges()
    for filename in filenames:
        data = read_csv(filename)
        create_blocks(dates,data, filename)


def read_csv(filename):
    df = pd.read_csv(filename)
    # using a dictionary, store the column 'date' as the key and the column 'close' as the value
    data_dict = pd.Series(df.Close.values, index=df.Date).to_dict()
    return data_dict

def create_blocks(valid_dates, data_dict, filename):
    # we define a block as a period of 60 months. For every valid date there is a period of 60 months starting from that date ending (inclusive) 03/2020
    count = 0
    blocks = []
    cur_block = []
    for i, date in enumerate(valid_dates):
        for sub_date in valid_dates[i:]:
            if sub_date != '03/2020' and count != 60:
                cur_block.append([sub_date, data_dict[sub_date]])
                count += 1
            elif count == 60:
                blocks.append(cur_block)
                cur_block = []
                count = 0
            elif sub_date == '03/2020':
                break

    flags = []
    OOI = []
    for block in blocks:
        if block[0][1] > block[59][1]:
            flags.append(True)
        else:
            OOI.append([block[0][0], block[59][0], filename])
            flags.append(False)

    #print(flags)
    # print(len(OOI))
    # print(OOI)
    # print("--------------------------------------------------")

def create_ranges():
    valid_dates = []
    start_dt = datetime.strptime(START_DATE, '%m/%Y')
    end_dt = datetime.strptime(END_DATE, '%m/%Y')
    current_dt = start_dt
    while current_dt <= end_dt:
        date_str = current_dt.strftime('%m/%Y')
        valid_dates.append(date_str)
        # Move forward one month
        if current_dt.month == 12:
            current_dt = current_dt.replace(year=current_dt.year + 1, month=1)
        else:
            current_dt = current_dt.replace(month=current_dt.month + 1)
    return valid_dates

def factor_in_yields():
    # for any 5 year period where the capital gains is negative, do we lose money when we consider yields?
    # todo
    pass

if __name__ == "__main__":
    main()

