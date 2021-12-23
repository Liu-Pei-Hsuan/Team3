def food():
    import random
    import time
    food = ["麥當勞","大四喜","素食","迷豆子","711關東煮","雙贏涼麵","早到晚到","排骨酥麵","八方雲集"]
    good = random.choice(food)

    print('我即將從'+str(len(food))+'家美食裡，推薦你一樣！！！')
    time.sleep(1)
    print('讓我們一起倒數  ～～')
    for i in range(6,1,-1):
        print(f'期待嗎？ 還剩下{i}秒')
        time.sleep(1)
    print(f'今天吃什麼 == > {good}')

food()
