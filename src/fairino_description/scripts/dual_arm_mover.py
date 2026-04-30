#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time

class SlowDualArmMover(Node):
    def __init__(self):
        super().__init__('slow_dual_arm_mover')
        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/dual_arm_position_controller/commands',
            10
        )
        self.angle = -3.14/2
        self.direction = 1
        self.timer = self.create_timer(0.1, self.step)  # publish every 1s

    def step(self):
        msg = Float64MultiArray()
        # Example: move shoulder joints slowly
        msg.data = [
            -3.14-self.angle, self.angle, 3.14/2, 0.0, 3.14, 0.0,   # left arm
            3.14+self.angle, -3.14-self.angle, -3.14/2, 3.14, 3.14, 0.0   # right arm
        ]
        self.publisher.publish(msg)
        self.get_logger().info(f"Sent {msg.data}")

        # Increment angle slowly
        self.angle += 0.01 * self.direction
        if abs(self.angle) < 0.6 or abs(self.angle) > (3.14/2):
            self.direction *= -1

def main(args=None):
    rclpy.init(args=args)
    node = SlowDualArmMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
