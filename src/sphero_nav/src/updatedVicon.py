#!/usr/bin/env python

import rospy
import tf
import threading
import time
from numpy import *
import sys

import std_msgs

class ViconTracker(object):

	Xx = 0
	Yy = 0
	Oo = 0

	def __init__(self, name):

		#init_node()
		#rospy.init_node('Whatever')
		self.target = 'vicon/' + name + '/' + name

		self.x = 0
		self.y = 0
		self.o = 0

		self.t = tf.TransformListener()

		self.thread = threading.Thread(target=self.updatePose)
		self.thread.daemon = True
		self.thread.start()


	def updatePose(self):
		#rospy
		#while True:
		#a = self.t.lookupTransform('world',self.target, rospy.Time(0))
		self.t.waitForTransform('world',self.target, rospy.Time(0), rospy.Duration(4.0))
#			while not rospy.is_shutdown():
#				try:
#					now = rospy.Time.now()
#					self.t.waitForTransform('world',self.target, now, rospy.Duration(4.0))
		a = self.t.lookupTransform('world',self.target, rospy.Time(0))
		self.x = a[0][0]
		self.y = a[0][1]
		euler = tf.transformations.euler_from_quaternion(a[1])
		self.o = euler[2]
		Xx = self.x
		Yy = self.y
		Oo = self.o

	def _stop(self):
		print( "Vicon pose handler quitting..." )
		self.thread.join()
		print( "Terminated." )

	def getPose(self, cached=False):
		#print "({t},{x},{y},{o})".format(t=t,x=x,y=y,o=o)
		self.updatePose()
		return array([self.x, self.y, self.o])


def getViconData():
	rospy.init_node('XXX_listener')
	a = ViconTracker(2)
	print(a.getPose())
	time.sleep(1)

	while True:
		time.sleep(0.5)
		b = a.getPose()
		print( b )

if __name__ == "__main__":

	#rospy.init_node('Hexbug_listener')
	rospy.init_node('XXX_listener')

	pub = rospy.Publisher('vicon222',std_msgs.msg.Float32,queue_size=2)

	rate = rospy.Rate(12)

	'''startNum = int(sys.argv[-2])
	endNum = int(sys.argv[-1])

	N = endNum-startNum+1

	posData = zeros([N,2])

	while True:

		for i in range(N):
			posData[i,:] = ViconTracker(i+startNum).getPose()[0:2]

		pub.publish(posData[0,0])

		rospy.loginfo(posData)t

		rate.sleep()'''



#	helmet = ViconTracker('Helmet_1')
	sphero13 = ViconTracker('Sphero13')
#	print(helmet.getPose())
	print(sphero13.getPose())
	time.sleep(1)

	while True:
		time.sleep(0.5)
#		print('helmet:',helmet.getPose())
		print('sphero13',sphero13.getPose())
