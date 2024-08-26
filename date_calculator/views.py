from django.shortcuts import render, redirect
import calendar
from datetime import datetime

month_names = {'1': 'Jan', '2': 'Fev', '3': 'Mar', '4': 'Abr', '5': 'Mai', '6': 'Jun', '7': 'Jul', '8': 'Ago',
               '9': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'}
last_days = {0: 31, 1: 28, 2: 31, 3: 30, 4: 31, 5: 30, 6: 31, 7: 31, 8: 30, 9: 31, 10: 30, 11: 31}


def work_days(work_date, day_off):
    date = [int(i) for i in work_date]

    for m in last_days.keys():
        if m == date[1] - 1:
            date[0] += day_off + 1  # A próxima data de trabalho é 1 dia após o último dia de folga.
            if date[0] > last_days[m]:
                date[0] -= last_days[m]
                date[1] += 1
            if date[1] > 12:
                date[2] += 1
                date[1] = 1
            break

    work_date = [str(x) for x in date]

    return work_date


def calculate(request):
    work = request.GET.get('work_day', '')
    off = request.GET.get('day_off', '').strip()

    if work == '' or off == '':
        return redirect('date_calculator:index')

    work = list(reversed(work.split('-')))
    work[1] = str(int(work[1]))
    off = int(off)

    print('work', work)
    print('off', off)

    list_dates = []
    current_year = datetime.now().year

    while int(work[2]) == current_year:
        list_dates.append(work)
        work = work_days(work, off)

    months = []
    for i in range(len(list_dates)):
        m = month_names[list_dates[i][1]]
        if m not in months:
            months.append(m)

    cal = calendar.Calendar()
    con = dict()
    for i in months:
        con[i] = [[], [[], [], [], [], [], []]]  # the key is the month | con[i][0] -> working days | con[i][1] -> days of the month
        for j in list_dates:
            if month_names[j[1]] != i:
                continue
            con[i][0].append(int(j[0]))
            con[i].append(j[1]) if j[1] not in con[i] else None
        row = 0
        for d in cal.itermonthdays(current_year, int(con[i][2])):
            if len(con[i][1][row]) > 6:
                row += 1
            con[i][1][row].append(d)

    context = {
        'year': list_dates[0][2],
        'con': con,
        'range6': range(6),
        'range7': range(7),
    }

    return render(
        request,
        'date_calculator/index.html',
        context,
    )


def index(request):
    return render(
        request,
        'date_calculator/index.html',
    )
