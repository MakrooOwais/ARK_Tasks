#!/usr/bin/env python3
import rospy
import std_msgs
from sensor_msgs.msg import Image 
from std_msgs.msg import Int16
from cv_bridge import CvBridge
import randimage
import cv2
import numpy as np


height = int(rospy.get_param("/player_node/image_height"))
width = int(rospy.get_param("/player_node/image_width"))
img_size = (height,width,3)


bridge = CvBridge()
global imgMsg_res
imgMsg_res = None

def generateRandomImage():
	img = randimage.get_random_image((img_size[0],img_size[1]))*255
	img = img.astype(np.uint8)
	return img


def strategy():
	global imgMsg_res
	final_r = 127 * np.ones((img_size[0], img_size[1]))
	final_g = 127 * np.ones((img_size[0], img_size[1]))
	final_b = 127 * np.ones((img_size[0], img_size[1]))

	rospy.init_node('player_node')
	rate = rospy.Rate(10)
	pub1 = rospy.Publisher('guess', Image, queue_size=10)
	rospy.Subscriber('result', Image, guessCallback)
	n = 0
	change = 128
	while not rospy.is_shutdown():
		n+=1
		guess = cv2.merge([final_b,final_g,final_r])
		msg = bridge.cv2_to_imgmsg(guess)
		pub1.publish(msg)
		
		rate.sleep()
		if imgMsg_res is not None:
			if (np.sum(imgMsg_res!=127) == 0):
				rospy.signal_shutdown("Task Complete")
				exit()
			print(np.sum(imgMsg_res!=127), np.sum(imgMsg_res==127))
			final_r = final_r * (imgMsg_res[:,:,1] == 127) + (final_r - change) * (imgMsg_res[:,:,1] == 255) + (final_r + change) * (imgMsg_res[:,:,1] == 0)
			final_g = final_g * (imgMsg_res[:,:,0] == 127) + (final_g - change) * (imgMsg_res[:,:,0] == 255) + (final_g + change) * (imgMsg_res[:,:,0] == 0)
			final_b = final_b * (imgMsg_res[:,:,2] == 127) + (final_b - change) * (imgMsg_res[:,:,2] == 255) + (final_b + change) * (imgMsg_res[:,:,2] == 0)
			imgMsg_res = None
			change = change / 2


def guessCallback(data):
	global imgMsg_res
	imgMsg_res = bridge.imgmsg_to_cv2(data)


if __name__ == '__main__':
	try:
		strategy()
	except rospy.ROSInterruptException:
		pass