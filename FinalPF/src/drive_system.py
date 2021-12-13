#!/home/pi/.pyenv/versions/rospy/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.scanned = []
        self.turtle_vel = Twist()
        self.sum_val = 0
        self.mean_val = 0
        self.cos = 0

    def lds_callback(self, scan):
        self.scanned = scan.ranges
        self.obstacle()
        
        if scan.ranges[90] > 0.40:   
            if scan.ranges[270] > 0.2:   
                self.right()
            if scan.ranges[330] != 0:
                self.cos = scan.ranges[225] / scan.ranges[315] 
            if self.mean_val <= 0.45:
                self.left()  
            elif scan.ranges[0] > 0.25:
                self.straight()
                if self.cos > 0.25:
                    self.adjust_right()
                elif self.cos <= 0.25:
                    self.straight()
        elif (scan.ranges[200] / scan.ranges[225]) > 0.25:
            self.right()

        
    def obstacle(self):   
        for i in range(30):
            self.sum_val += self.scanned[329+i]
            print("{} : ".format(self.scanned[329+i]))
        self.mean_val = self.sum_val / 30
        self.sum_val = 0

    def straight(self):  
        self.turtle_vel.linear.x = 0.15  
        self.turtle_vel.angular.z = 0.0  
        self.publisher.publish(self.turtle_vel)

    def left(self):   
        self.turtle_vel.linear.x = 0.07
        self.turtle_vel.angular.z = 2   
        self.publisher.publish(self.turtle_vel)

    def right(self):    
        self.turtle_vel.linear.x = 0.15  
        self.turtle_vel.angular.z = -1.571  
        self.publisher.publish(self.turtle_vel)

    def adjust_right(self):  
        self.turtle_vel.angular.x = 0.15
        self.turtle_vel.angular.z = -0.25  
        self.publisher.publish(self.turtle_vel)

def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
