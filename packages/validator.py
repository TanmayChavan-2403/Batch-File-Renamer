import os 

class Validator():
	def __init__(self):
		pass

	def validateDisks(self, disks):
		for disk in disks:
			try:
				print(disk)
				os.listdir('/media/hackytech/' + disk)
			except FileNotFoundError:
				return False

		return True