import psutil, time, datetime

while True:
    cpu = psutil.cpu_percent()
    ozu = psutil.virtual_memory().percent
    print(f'CPU = {cpu}%, OZU = {ozu}%')
    if ozu > 70.0: #70.0:
        print(f'{datetime.datetime.now().strftime("%H:%M:%S")}')
        print('OZU problem')
        # print(f'CPU = {cpu}%, OZU = {ozu}%')
    if cpu > 50.0:
        print('CPU problem')
    time.sleep(0.5)