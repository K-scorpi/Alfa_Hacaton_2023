import pandas as pd

# загружаем данные по времени работы АТМ и стоимости инкассации
df_atm_info = pd.read_csv("atm_info.csv", sep=';', header=None)
df_in_out_train = pd.read_csv("test_private.csv", header=None)
funding_rate = 0.089


def massives_dt(csvfiles, n):
    row = []
    if n == 1:
        for i in csvfiles[n]:
            row.append(i)
        print()
        row.pop(0)
        list(map(float, row))
    elif n == 2:
        for i in csvfiles[n]:
            row_string = ''.join(str(x) for x in i)
            row.append(row_string)
        row.pop(0)
    else:
        for i in csvfiles[n]:
            row.append(i)
        row.pop(0)
    return row


def cost_dt(csvfiles, n):
    row = []
    for i in csvfiles[n]:
        row.append(i)
    row.pop(0)
    row = list(map(float, row))
    return row


def times(worktime_split, n):
    new_time = list(worktime_split[n])
    new_time = ''.join(str(x) for x in new_time if x == '1' or x == '0')
    return new_time


atm_id = massives_dt(df_atm_info, 0)
incasationcost = massives_dt(df_atm_info, 1)
worktime_split = massives_dt(df_atm_info, 2)

remains = cost_dt(df_in_out_train, 1)
date_1 = cost_dt(df_in_out_train, 2); new_date_1 = [0] * len(remains)
date_2 = cost_dt(df_in_out_train, 3); new_date_2 = [0] * len(remains)
date_3 = cost_dt(df_in_out_train, 4); new_date_3 = [0] * len(remains)
date_4 = cost_dt(df_in_out_train, 5); new_date_4 = [0] * len(remains)
date_5 = cost_dt(df_in_out_train, 6); new_date_5 = [0] * len(remains)
date_6 = cost_dt(df_in_out_train, 7); new_date_6 = [0] * len(remains)
date_7 = cost_dt(df_in_out_train, 8); new_date_7 = [0] * len(remains)


new_incasationcost = 0
tof = len(remains)

for i in range(tof): # 1
    new_time = times(worktime_split, 0)
    if new_time[0] == '1':
        if (remains[i] + date_1[i]) < 0:
            # print(remains[i] - date_1[i], i, remains[i], date_1[i])
            shag = abs(remains[i] + date_1[i] + abs(date_2[i]))
            if shag < 500000:
                new_date_1[i] = 750_000
            else:
                new_date_1[i] = shag
                new_incasationcost += int(incasationcost[i])


def datecount(ndate1, date2, date3, ndate2, n):
    global tof, new_incasationcost, incasationcost, worktime_split
    for i in range(tof):  # n
        new_time = times(worktime_split, i)
        if new_time[n] == '1':
            if (ndate1[i] + date2[i]) < 0:
                shag = abs(date3[i]) + abs(date2[i])
                if shag < 500000:
                    ndate2[i] = 750_000
                else:
                    ndate2[i] = shag
                    new_incasationcost += int(incasationcost[i])
    ''' 
    for i in range(len(remains)): # 2

        if (new_date_1[i] + date_2[i]) < 0:
            shag = abs(date_3[i]) + abs(date_2[i])
            new_date_2[i] = shag
            new_incasationcost += int(incasationcost[i])
    '''


datecount(new_date_1, date_2, date_3, new_date_2, 1)
datecount(new_date_2, date_3, date_4, new_date_3, 2)
datecount(new_date_3, date_4, date_5, new_date_4, 3)
datecount(new_date_4, date_5, date_6, new_date_5, 4)
datecount(new_date_5, date_6, date_7, new_date_6, 5)
datecount(new_date_6, date_7, new_date_6, new_date_7, 6)

fonding = list(map(sum, [new_date_1, new_date_2, new_date_3,
                         new_date_4, new_date_5, new_date_6, new_date_7]))
fonding = sum(fonding)
print(fonding, new_incasationcost, fonding+new_incasationcost)


df = pd.DataFrame({'atm_id': atm_id, '2023-09-01':new_date_1, '2023-09-02':new_date_2, '2023-09-03':new_date_3, '2023-09-04':new_date_4,
                '2023-09-05':new_date_5, '2023-09-06':new_date_6, '2023-09-07':new_date_7})
# Сохранение DataFrame в файл CSV
df.to_csv('output.csv', index=False)

