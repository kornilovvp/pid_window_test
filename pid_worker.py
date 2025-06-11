# pid_worker.py

# These module-level variables will store the last known input coordinates (e.g., from the green circle)
# They are updated by the PID_UPDATE function.
X_current = 0
Y_current = 0

# Default/target coordinates that PID_UPDATE will return for the blue circle.
# As per the request, these are fixed values for now.
BLUE_CIRCLE_TARGET_X = 450
BLUE_CIRCLE_TARGET_Y = 580

def PID_UPDATE(input_x, input_y):
    """
    Updates internal 'current' X, Y based on the input coordinates.
    Returns target X, Y coordinates for the blue circle.

    Args:
        input_x (int): The X coordinate from the input (e.g., green circle's center).
        input_y (int): The Y coordinate from the input (e.g., green circle's center).

    Returns:
        tuple: (int, int) representing the target X, Y for the blue circle.
    """
    global X_current, Y_current
    X_current = input_x
    Y_current = input_y

    # For now, this function returns fixed target values for the blue circle.
    # In a more complex PID system, these returned values would be calculated
    # based on X_current, Y_current, a setpoint, and PID logic.
    return BLUE_CIRCLE_TARGET_X, BLUE_CIRCLE_TARGET_Y