from django.shortcuts import render, redirect
from datetime import datetime

def work_days(work_date, day_off):

    date = [int(i) for i in work_date]
    
    last_days = {0: 31, 1: 28, 2: 31, 3: 30, 4: 31, 5: 30, 6: 31, 7: 31, 8: 30, 9: 31, 10: 30, 11: 31}
    for m in last_days.keys():
        if m == date[1] - 1:
            date[0] += day_off + 1
            if date[0] > last_days[m]:
                date[0] -= last_days[m]
                date[1] += 1
            if date[1] > 12:
                date[2] += 1
                date[1] = 1
            break

    work_date = [str(x) for x in date]

    return work_date

def index(request):

    work = request.GET.get('work_day', '')
    off = request.GET.get('day_off', '').strip()

    if request.GET:
        if work == '' or off == '':
            return redirect('date_calculator:index')
        
    work = list(reversed(work.split('-')))
    off = int(off)
    
    print('work', work)
    print('off', off)

    list_dates = []

    while int(work[2]) == 2023:
        list_dates.append(work)
        work = work_days(work, off)

    for i in list_dates:
        print(i)

    return render(
        request,
        'date_calculator/index.html',
    )
