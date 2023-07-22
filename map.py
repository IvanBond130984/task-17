import sprite
class Map:
	def __init__(self, w, h):
		self.w=w
		self.h=h
		self.matrix=[]
		for i in range(self.w+2):
			vector=[]
			for j in range(self.h+2):
				if (i==0) or (j==0) or (i==self.w+1) or (j==self.h+1):
					x=11
				else:
					x=0
				vector.append(sprite.Tree(x))
			self.matrix.append(vector)
	def set(self, x, y, type):
		self.matrix[x][y].set_img(type)

	def set_helicopter(self, x, y):
		self.matrix[x][y].set_helicopter()

	def del_helicopter(self, x, y):
		self.matrix[x][y].del_helicopter()

	def get_old_img(self, x, y):
		return self.matrix[x][y].get_old_img()

	def set_health(self, x, y):
		self.matrix[x][y].set_health()

	def set_old_img(self, x, y):
		self.matrix[x][y].set_old_img()

	def show(self):
		for i in self.matrix:
			for j in i:
				print(j.show(), end='')
			print()