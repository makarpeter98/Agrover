#navigation/navigation_controller.py

class NavigationController:

	def __init__(self):

		self.forward_tolerance = 15
		self.turn_tolerance = 20

	def calculate_command(self, error):

		if abs(error) <= self.forward_tolerance:
			return "FORWARD"

		if abs(error) <= self.turn_tolerance:
			return "FORWARD"

		if error > 0:
			return "TURN_RIGHT"
		else: 
			return "TURN_LEFT"
