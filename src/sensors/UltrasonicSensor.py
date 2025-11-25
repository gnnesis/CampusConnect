from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
ultrasonic = GroveUltrasonicRanger(24)

def distance():
	return ultrasonic.get_distance()

def arePeople():
	return distance() < 80
