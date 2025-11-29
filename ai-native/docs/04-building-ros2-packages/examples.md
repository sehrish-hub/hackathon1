## Examples

### Example 1: `package.xml`

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_python_package</name>
  <version>0.0.0</version>
  <description>A simple Python package</description>
  <maintainer email="user@example.com">user</maintainer>
  <license>Apache 2.0</license>

  <buildtool_depend>ament_python</buildtool_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### Example 2: `setup.py`

```python
from setuptools import setup

package_name = 'my_python_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='A simple Python package',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = my_python_package.my_node:main'
        ],
    },
)
```

### Example 3: Publisher Node

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyPublisher(Node):

    def __init__(self):
        super().__init__('my_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    my_publisher = MyPublisher()
    rclpy.spin(my_publisher)
    my_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
