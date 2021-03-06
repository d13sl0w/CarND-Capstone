#!/usr/bin/env python
PKG = 'twist_controller'
import roslib; roslib.load_manifest(PKG) #not needed with catkin

import unittest
from twist_controller import Controller
import rospy

class TestControllerMethods(unittest.TestCase):
    
    def test_make_controller(self):
        c = Controller(8)
        self.assertIsNotNone(c, 'Failed to create controller.')
        
    def test_controller_control_returns_3_values(self):
        c = Controller(8)
        throttle, brake, steer = c.control(1 , 1)
        self.assertIsNotNone(throttle, 'Throttle not returned')
        self.assertIsNotNone(brake, 'Brake not returned')
        self.assertIsNotNone(steer, 'Steering not returned')
        
    def test_controller_default_pid_values(self):
        c = Controller(8)
        self.assertGreater(c.gainp, 0, 'GainP not initialized')
        self.assertEqual(c.max_speed_mps, 22.352, 'Max throttle not initialized')
        self.assertEqual(c.min_speed_mps, 0, 'Min throttle not initialized')
        
    def test_configure_yaw_controller_params(self):
        self.skipTest('Removed yaw_controller code')
        c = Controller(8)
        #c.configure_yaw_controller(2,3,4,5,6)
        self.assertEqual(c.yaw_con.wheel_base, 2, 'Yaw controller wheel_base not initialized')
        self.assertEqual(c.yaw_con.steer_ratio, 3, 'Yaw controller steer_ratio not initialized')
        self.assertEqual(c.yaw_con.min_speed, 4, 'Yaw controller min speed not initialized')
        self.assertEqual(c.yaw_con.max_lat_accel, 5, 'Yaw controller max lat accel not initialized')
        self.assertEqual(c.yaw_con.max_angle, 6, 'Yaw controller max angle not initialized')
        self.assertEqual(c.yaw_con.min_angle, -6, 'Yaw controller max angle not initialized')
    
    def test_throttle_and_brake_during_accel(self):
        c = Controller(8)
        kw = {'current_speed_mps':0,'target_speed_mps':5}
        throttle, brake, steer = c.control(**kw)
        self.assertGreater(throttle, 0, 'Throttle not positive for accel from 0 to 5 m/s')
        self.assertEqual(brake, 0, 'Brake not 0 for accel from 0 to 5 m/s')
        
    def test_throttle_and_brake_during_braking(self):
        c = Controller(8)
        kw = {'current_speed_mps':5,'target_speed_mps':0}
        throttle, brake, steer = c.control(**kw)
        self.assertEqual(throttle, 0, 'Throttle not 0 for decel from 5 to 0 m/s')
        self.assertGreater(brake, 0, 'Brake not 0 for decel from 5 to 0 m/s')

    def test_yaw_controller_negative_steer_for_negative_radius(self):
        c = Controller(8)
        #c.configure_yaw_controller(2.85,14.8,4.,3.,8.)
        kw = {'current_speed_mps':5,'target_speed_mps':0, 'turn_z':1}
        throttle,brake,steer = c.control(**kw)
        self.assertGreater(steer, 0, 'Left turn radius not turning left')
    def test_yaw_controller_positive_steer_for_pos_radius(self):
        c = Controller(8)
        #c.configure_yaw_controller(2.85,14.8,4.,3.,8.)
        kw = {'current_speed_mps':5,'target_speed_mps':0, 'turn_z':-1}
        throttle,brake,steer = c.control(**kw)
        self.assertLess(steer, 0, 'Right turn radius not turning right')
        
if __name__=='__main__':
    import rostest
    rostest.rosrun(PKG, 'Twist Controller Tests', TestControllerMethods)