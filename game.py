import map
import os
import sprite
import time
import  random
from pynput import keyboard
class Game:
	def __init__(self, ls_arg):
		self.tick_slip=ls_arg[0]# Время ожидания в секундах
		self.fire_update=ls_arg[1]# период обновления пожаров
		self.tree_update=ls_arg[2]# Период добавления деревьев
		self.w=ls_arg[17][0]# x количество строк
		self.h=ls_arg[17][1]# y количество столбцов
		self.tree_procent=int((self.w*self.h)*(ls_arg[18]/100))# Максимальное количество деревьев
		self.tick=ls_arg[3]# Счётчик кадров
		self.game_map=map.Map(self.w, self.h)# Игровая карта
		self.tree_count=ls_arg[4]# Количество деревьев
		self.ls_tree=ls_arg[5]# Список координат с деревьями
		self.tree_burn_count=ls_arg[6]# Количество горящих деревьев
		self.tree_burn_ls=ls_arg[7]# Список координат с горящими деревьями
		self.health_helicopter=ls_arg[8]# Здоровье вертолёта
		self.x_helicopter=ls_arg[9]# х вертолёта
		self.y_helicopter=ls_arg[10]# у вертолёта
		self.water_count_helicopter=ls_arg[11]# Количество вёдер
		self.lim_water_count_helicopter=ls_arg[12]# Лимит количества вёдер
		self.balls=ls_arg[13]# Очки
		self.step_balls=ls_arg[14]# Шаг изменения баллов
		self.cena_up=ls_arg[15]# Цена улучшений
		self.step_health=ls_arg[16]# Шаг изменения здоровья
		self.exit=False
	def add_repair_shop(self):# Добавление на карту ремонтных мастерских
		self.game_map.set(1, 1, 3)
		self.game_map.set(1, self.h, 3)
		self.game_map.set(self.w, 1, 3)
		self.game_map.set(self.w, self.h, 3)
	def add_upgrade_shop(self):# Добавление на карту магазинов улучшений
		x0=1
		x1=(1+self.w)//2
		y0=1
		y1=(1+self.h)//2
		self.game_map.set(x0, y1, 4)
		self.game_map.set(x1, y0, 4)
		self.game_map.set(x1, y1, 4)
	def set_helicopter(self):# Установка вертолета в центр карты
		x1 = ((1 + self.w) // 2)+1
		y1 = ((1 + self.h) // 2)+1
		self.x_helicopter=x1
		self.y_helicopter=y1
		self.game_map.set_helicopter(x1, y1)
	def generator_xy(self):# Генератор свободных координат
		while True:
			random.seed()
			x = random.randint(1, self.w-1)
			random.seed()
			y = random.randint(1, self.h-1)
			if ((x>=1) and (x<self.w)) and ((y>=1) and (y<self.h)):
				break
		return x, y
	def add_cloud(self):
		temp = sprite.Sprite()
		while True:
			x, y = self.generator_xy()
			if self.game_map.matrix[x][y].s_img == temp.show():
				if x%2==0 and y%2==0:
					self.game_map.set(x, y, 6)
					break
				else:
					self.game_map.set(x, y, 7)
					break

	def add_tree(self):# Добавление дерева на карту
		temp=sprite.Sprite()
		while True:
			x, y = self.generator_xy()
			if self.game_map.matrix[x][y].s_img == temp.show():
				self.game_map.set(x, y, 1)
				return x, y
	def add_water(self):# Добавление воды на карту
		temp = sprite.Sprite()
		while True:
			x, y = self.generator_xy()
			if self.game_map.matrix[x][y].s_img == temp.show():
				self.game_map.set(x, y, 2)
				break

	def fire(self):# Поджигание дерева
		x, y=self.generator_xy()
		for temp in self.ls_tree:
			if x==temp[0] and y==temp[1]:
				self.game_map.matrix[x][y].start_burn()
				temp2=x, y
				self.tree_burn_ls.append(list(temp2))
				self.tree_burn_count+=1
	def del_tree(self):# Удаление сгоревших деревьев с карты
		for temp in self.tree_burn_ls:
			if self.game_map.matrix[temp[0]][temp[1]].end_burn():
				x=temp[0]
				y=temp[1]
				self.game_map.set(x, y, 0)
				self.ls_tree.remove(temp)
				self.tree_count -= 1
				self.tree_burn_ls.remove(temp)
				self.tree_burn_count -= 1
				self.balls-=self.step_balls

	def mov_helicopter(self, direction):# Перемещение вертолёта по карте yf 1 клетку
		if direction == 1:
			if self.x_helicopter > 1:
				#temp = self.x_helicopter
				self.x_helicopter-= 1
				self.game_map.set_helicopter(self.x_helicopter, self.y_helicopter)
				self.game_map.del_helicopter(self.x_helicopter+1, self.y_helicopter)
		if direction == 2:
			if self.x_helicopter < (self.w):
				#temp =self.x_helicopter
				self.x_helicopter += 1
			self.game_map.set_helicopter(self.x_helicopter, self.y_helicopter)
			self.game_map.del_helicopter(self.x_helicopter-1, self.y_helicopter)
		if direction == 3:
			if self.y_helicopter > 1:
				#temp = self.y_helicopter
				self.y_helicopter-= 1
				self.game_map.set_helicopter(self.x_helicopter, self.y_helicopter)
				self.game_map.del_helicopter(self.x_helicopter, self.y_helicopter+1)
		if direction == 4:
			#temp = self.y_helicopter
			if self.y_helicopter<self.h:
				self.y_helicopter += 1
				self.game_map.set_helicopter(self.x_helicopter, self.y_helicopter)
				self.game_map.del_helicopter(self.x_helicopter, self.y_helicopter-1)

	def attitude(self):# Взаимодействие верталёта с объектами
		temp=sprite.Sprite()
		if self.game_map.get_old_img(self.x_helicopter, self.y_helicopter)==temp.img[5] and self.water_count_helicopter>0:
			self.game_map.set_health(self.x_helicopter, self.y_helicopter)
			temp2=[]
			temp2.append(self.x_helicopter)
			temp2.append(self.y_helicopter)
			self.tree_burn_ls.remove(temp2)
			self.tree_burn_count-=1
			self.game_map.set_old_img(self.x_helicopter, self.y_helicopter)
			if self.water_count_helicopter>0:
				self.water_count_helicopter-=1
			self.balls+=self.step_balls
		if self.game_map.get_old_img(self.x_helicopter, self.y_helicopter)==temp.img[2] and self.water_count_helicopter<=self.lim_water_count_helicopter:
			self.water_count_helicopter+=1
		if self.game_map.get_old_img(self.x_helicopter, self.y_helicopter)==temp.img[4] and self.balls==self.cena_up:
			self.lim_water_count_helicopter+=1
			self.cena_up+=self.step_balls
			self.balls-=self.step_balls
		if self.game_map.get_old_img(self.x_helicopter, self.y_helicopter)==temp.img[7]:
			self.health_helicopter-=self.step_health
		if self.game_map.get_old_img(self.x_helicopter, self.y_helicopter)==temp.img[3]:
			self.health_helicopter += self.step_health


	def on_key(self, key):
		#time.sleep(0.1)
		if key.char =='w' or key.char =='ц':
			self.mov_helicopter(1)
		if key.char=='s' or key.char =='ы':
			self.mov_helicopter(2)
		if key.char =='a' or key.char =='ф':
			self.mov_helicopter(3)
		if key.char =='d' or key.char =='в':
			self.mov_helicopter(4)
		if key.char =='e' or key.char =='у':
			self.exit=True

	def frame_gen(self, period):# Формирование кадра
		if period==0:
			self.set_helicopter()
			self.add_repair_shop()
			self.add_upgrade_shop()
			for i in range(6):
				temp = list(self.add_tree())
				self.ls_tree.append(temp)
				self.tree_count += 1
				for j in range(3):
					self.add_water()
				for k in range(6):
					self.add_cloud()
		if period%self.tree_update==0 and self.tree_count<=self.tree_procent:
			temp3=list(self.add_tree())
			self.ls_tree.append(temp3)
			self.tree_count+=1
		if period%self.fire_update==0:
			for i in range(self.w):
				self.fire()
			self.del_tree()
		self.game_map.show()



	def play_game(self):# Игровой процесс
		while True:
			listener = keyboard.Listener(
				on_press=None,
				on_release=self.on_key)
			listener.start()
			os.system('cls')
			tr=sprite.Tree()
			print(f'Период {self.tick} | {tr.show()}{self.tree_count} | {tr.img[5]}{self.tree_burn_count} | {tr.img[10]}{self.water_count_helicopter} | {tr.img[9]}{self.balls} | {tr.img[3]}{self.health_helicopter}')
			self.attitude()
			self.frame_gen(self.tick)
			time.sleep(self.tick_slip)
			self.tick+=1
			listener.stop()
			if (self.tree_count==0) or (self.health_helicopter==0) or  self.exit:
				print(*self.tree_burn_ls)
				break
	def save_game(self):# Сохранение игры
		#print(*self.tree_burn_ls)
		args_game=[]
		args_game.append(str(self.tick_slip))  # Время ожидания в секундах 0
		args_game.append(str(self.fire_update))  # период обновления пожаров
		args_game.append(str(self.tree_update))  # Период добавления деревьев
		args_game.append(str(self.w))  # x количество строк
		args_game.append(str(self.h))  # y количество столбцов
		args_game.append(str(self.tree_procent))  # Максимальное количество деревьев
		args_game.append(str(self.tick))  # Счётчик кадров
		args_game.append(str(self.health_helicopter))  # Здоровье вертолёта
		args_game.append(str(self.x_helicopter))  # х вертолёта
		args_game.append(str(self.y_helicopter))  # у вертолёта
		args_game.append(str(self.water_count_helicopter))  # Количество вёдер
		args_game.append(str(self.lim_water_count_helicopter))  # Лимит количества вёдер
		args_game.append(str(self.balls))  # Очки
		args_game.append(str(self.step_balls))  # Шаг изменения баллов
		args_game.append(str(self.cena_up))  # Цена улучшений
		args_game.append(str(self.step_health))  # Шаг изменения здоровья
		sg=open('save_game.txt', 'a')
		for s in args_game:
			sg.write(s+' ')
		sg.write('\n')
		sg.close()

	def load_game(self, ls):
		self.tick_slip=ls[0]  # Время ожидания в секундах 0
		self.fire_update=ls[1]  # период обновления пожаров
		self.tree_update=ls[2]  # Период добавления деревьев
		self.w=ls[3]  # x количество строк
		self.h=ls[4]  # y количество столбцов
		self.tree_procent=ls[5]  # Максимальное количество деревьев
		self.tick=ls[6]  # Счётчик кадров
		self.health_helicopter=ls[7]  # Здоровье вертолёта
		self.x_helicopter=ls[8]  # х вертолёта
		self.y_helicopter=ls[9]  # у вертолёта
		self.water_count_helicopter=ls[10]  # Количество вёдер
		self.lim_water_count_helicopter=ls[11]  # Лимит количества вёдер
		self.balls=ls[12]  # Очки
		self.step_balls=ls[13]  # Шаг изменения баллов
		self.cena_up=ls[14]  # Цена улучшений
		self.step_health=ls[15]  # Шаг изменения здоровья
		self.add_repair_shop()
		self.add_upgrade_shop()
		for i in range(6):
			temp = list(self.add_tree())
			self.ls_tree.append(temp)
			self.tree_count += 1
			for j in range(3):
				self.add_water()
			for k in range(6):
				self.add_cloud()
