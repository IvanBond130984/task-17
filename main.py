import game

while True:# Меню игры
    print('Привет!')
    print('Новая игра(1): ')
    print('Загрузить игру(2): ')
    print('Сохранить игру(3): ')
    print('Выйти из игры(4): ')
    komanda = int(input())
    if komanda in [1, 2, 3, 4]:
        if komanda == 1:
            args_games = []
            args_games.append(1)# Время ожидания в секундах 0
            args_games.append(26)# Период обновления пожаров 1
            args_games.append(52)# Период добавления деревьев 2
            args_games.append(0)# Счётчик кадров 3
            args_games.append(0)# Количество деревьев 4
            temp0=[]
            args_games.append(temp0)# Список координат с деревьями 5
            args_games.append(0)# Количество горящих деревьев 6
            temp1=[]
            args_games.append(temp1)# Список координат с горящими деревьями 7
            args_games.append(100)# Здоровье вертолёта 8
            args_games.append(0)# х вертолёта 9
            args_games.append(0)# у вертолёта 10
            args_games.append(0)# Количество вёдер 11
            args_games.append(1)# Лимит количества вёдер 12
            args_games.append(0)# Очки 13
            args_games.append(100)# Шаг изменения баллов 14
            args_games.append(100)# Цена улучшений 15
            args_games.append(5)# Шаг изменения здоровья 16
            print('Введите размер   карты ')
            temp = [int(st) for st in input().split()]
            args_games.append(temp)# Размер карты x на y
            print('Введите процент деревьев на карте')
            args_games.append(int(input()))# процент площади деревьев от площади карты
            pg = game.Game(args_games)
            pg.play_game()
        if komanda == 2:
            print('Загружаю игру)')
            lg=open('save_game.txt', 'r')
            args_game=lg.readlines()
            st_games=args_game[0].strip()
            temp_ls=[int(s) for s in st_games.split()]
            args_games = []
            args_games.append(1)  # Время ожидания в секундах 0
            args_games.append(26)  # Период обновления пожаров 1
            args_games.append(52)  # Период добавления деревьев 2
            args_games.append(0)  # Счётчик кадров 3
            args_games.append(0)  # Количество деревьев 4
            temp0 = []
            args_games.append(temp0)  # Список координат с деревьями 5
            args_games.append(0)  # Количество горящих деревьев 6
            temp1 = []
            args_games.append(temp1)  # Список координат с горящими деревьями 7
            args_games.append(100)  # Здоровье вертолёта 8
            args_games.append(0)  # х вертолёта 9
            args_games.append(0)  # у вертолёта 10
            args_games.append(0)  # Количество вёдер 11
            args_games.append(1)  # Лимит количества вёдер 12
            args_games.append(0)  # Очки 13
            args_games.append(100)  # Шаг изменения баллов 14
            args_games.append(100)  # Цена улучшений 15
            args_games.append(5)  # Шаг изменения здоровья 16
            m_ls=[13, 13]
            args_games.append(m_ls)
            args_games.append(26)  # процент площади деревьев от площади карты
            pg = game.Game(args_games)
            pg.load_game(temp_ls)
            pg.play_game()
        if komanda == 3:
            print(' Сохраняю игру)')
            pg.save_game()
        if komanda == 4:
            print('Выхожу из игры(')
            break
    else:
        print('Введите число от 1 до 4')
        continue
