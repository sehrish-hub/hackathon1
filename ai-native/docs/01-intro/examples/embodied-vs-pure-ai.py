"""
Example: Understanding Embodied AI vs Pure AI
Difficulty: Beginner
Time: 5 minutes
No prerequisites
"""

# Pure Digital AI - No understanding of physics
def pure_ai_command():
    # This is a placeholder for a call to a large language model
    # response = llm.ask("Pick up a 10kg box")
    response = "I will pick up the box"
    return response

# Embodied AI - Understands physics through simulation
def embodied_ai_command():
    # This is a placeholder for a robotics simulation environment
    class Robot:
        def __init__(self):
            self.max_force = 50  # in Newtons

        def simulate_grasp(self, obj):
            if obj == "10kg_box":
                return 98  # Force in Newtons (10kg * 9.8m/s^2)
            return 0

        def grasp(self, obj):
            pass

        def check_success(self):
            return "Grasped object successfully."

    robot = Robot()

    # Step 1: Simulate action in digital twin
    arm_force = robot.simulate_grasp(object="10kg_box")

    # Step 2: Check if physically possible
    if arm_force > robot.max_force:
        return "I cannot pick up this box (too heavy)"

    # Step 3: Execute in real world
    robot.grasp(object="10kg_box")
    feedback = robot.check_success()
    return feedback

print(f"Pure AI response: {pure_ai_command()}")
print(f"Embodied AI response: {embodied_ai_command()}")
