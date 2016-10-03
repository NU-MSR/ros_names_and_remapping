#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt8
from std_srvs.srv import Empty
from std_srvs.srv import EmptyResponse

import sys
import random

DT = 0.1

def control_callback(data):
    rospy.loginfo("received command: (v=%d, w=%d)", data.linear.x, data.angular.z)
    return

def range_callback(event):
    r = random.randint(0,255)
    pub.publish(UInt8(r))
    return

def introspect_callback(req):
    print "========================================"
    print "Node/Master data:"
    print "This node's name = ", rospy.get_name()
    print "This node's namespace = ", rospy.get_namespace()
    print "Root = ", rospy.get_ros_root()
    print "URI = ", rospy.get_node_uri()
    print "========================================"
    
    print ""
    print "========================================"
    print "Testing global vs. local:"
    print "'~test' private ?= ", rospy.names.is_private("~test")
    print "'test' private ?= ", rospy.names.is_private("test")
    print "'/test' global ?= ", rospy.names.is_global("/test")
    print "'test' global ?= ", rospy.names.is_global("test")
    print "========================================"

    print ""
    print "========================================"
    print "Resolving names:"
    print "'test' resolved name = ", rospy.names.resolve_name("test")
    print "'~test' resolved name = ", rospy.names.resolve_name("~test")
    print "'/test' resolved name = ", rospy.names.resolve_name("/test")
    print "'~test' (caller_id='hello') resolved = ", rospy.names.resolve_name("~test", caller_id="hello")
    print "'~test' (caller_id='/hello') resolved = ", rospy.names.resolve_name("~test", caller_id="/hello")
    print "========================================"

    # mappings:
    print ""
    print "========================================"
    print "Mappings:"
    mappings = rospy.names.get_mappings()
    for item,value in mappings.iteritems():
        print "\t", item, "->", value
    print "========================================"

    # mappings:
    print ""
    print "========================================"
    print "Resolved mappings:"
    mappings = rospy.names.get_resolved_mappings()
    for item,value in mappings.iteritems():
        print "\t", item, "->", value
    print "========================================"

    # topics:
    print ""
    print "========================================"
    print "All topics:"
    topics = rospy.get_published_topics()
    for topic,message_type  in topics:
        print "\t", topic, "("+message_type+")"
    print "========================================"
    
    # parameters:
    print ""
    print "========================================"
    print "All parameters:"
    params = rospy.get_param_names()
    for p in params:
        print "\t",p
    print "========================================"

    return EmptyResponse()


if __name__ == '__main__':
    rospy.init_node('fake_robot', log_level=rospy.INFO)

    # create publishers, subscribers, and service servers:
    sub = rospy.Subscriber("controls", Twist, control_callback)
    pub = rospy.Publisher("range", UInt8, latch=True, queue_size=1)
    srv_provider = rospy.Service("ros_introspection", Empty, introspect_callback)

    # now let's read a private parameter that tells us how often to publish a fake range:
    dt = rospy.get_param("~timestep", DT)
    # now let's read a non-private parameter telling us the name of the robot:
    robot_name = rospy.get_param("robot_name", "DEFAULT_ROBOT")

    # let's print the values of the parameters that were received:
    print "timestep = ",dt
    print "robot name = ",robot_name

    # now let's create a timer that publishes the fake range at the freq
    # specified by private parameter:
    range_timer = rospy.Timer(rospy.Duration(dt), range_callback)

    rospy.spin()


