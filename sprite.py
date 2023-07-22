class Sprite:
	def __init__(self,  type=0):
		self.img='🟩🌳🌊🏥🏪🔥💭⛈🚁🏆🪣⬛'#🟩🌳🌊🏥🏪🔥💭🌩🚁🏆🪣⬛
		self.s_img=self.img[type]
	def show(self):
		return self.s_img
class Tree(Sprite):
	def __init__(self, type_img=1):
		super().__init__(type_img)
		self.health=100
		self.burn=False
		self.old_img=-1
	def set_img(self, type_img):
		self.s_img=self.img[type_img]
	def start_burn(self):
		self.old_img=self.s_img
		self.s_img=self.img[5]
		self.burn=True
	def end_burn(self):
		if self.health>=1 and self.burn:
			self.health-=10
			self.old_img=-1
			return False
		if self.burn and self.health==0:
			self.burn=False
			return True
	def set_helicopter(self):
		self.old_img=self.s_img
		self.s_img=self.img[8]

	def del_helicopter(self):
		self.s_img, self.old_img = self.old_img, self.s_img

	def get_old_img(self):
		return self.old_img

	def set_health(self):
		self.health=100

	def set_old_img(self):
		self.old_img=self.img[1]