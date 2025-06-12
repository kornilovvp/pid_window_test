# pid_worker.py


# Default target setpoint for the blue circle.
DEF_TARGET_X = 333
DEF_TARGET_Y  = 580


x_current: float = 0
y_current: float = 0

x_target: float = DEF_TARGET_X
y_target: float = DEF_TARGET_Y

x_return: float = 0
y_return: float = 0

x_error: float = 0
y_error: float = 0


#time scaling

pid_coff_t_scale: float = 1


#acceptable errors
acceptable_error_x: float = 20
acceptable_error_y: float = 20




#proportional

p_enable = 1

pid_coeff_p: float  = 0.1
pid_coeff_p_min_step: float = 1

x_calculated_p_error: float = 0
y_calculated_p_error: float = 0


#integrator

i_enable = 1


pid_coeff_i: float = 0.01
pid_coeff_i_min_step: float = 1
pid_coeff_i_max_limit: float = 5

x_calculated_i_error: float = 0
y_calculated_i_error: float = 0

x_i_integrator: float = 0
y_i_integrator: float = 0











def PID_UPDATE(x_cur, y_cur, x_tar, y_tar):
 
    global pid_coff_t_scale
    global acceptable_error_x, acceptable_error_y
    global x_current, y_current, x_target, y_target, x_error, y_error, x_return, y_return
    global p_enable, pid_coeff_p, pid_coeff_p_min_step, x_calculated_p_error, y_calculated_p_error
    global i_enable, pid_coeff_i, pid_coeff_i_min_step, pid_coeff_i_max_limit, x_calculated_i_error, y_calculated_i_error, x_i_integrator, y_i_integrator



    # Saving coordinates
    x_current = x_cur  
    y_current = y_cur 
    
    x_target = x_tar
    y_target = y_tar

    # Calculate error position
    x_error = x_tar - x_cur
    y_error = y_tar - y_cur

    # check if located inside range acceptable error
    if abs(x_error) < acceptable_error_x :
        x_error  = 0

    if abs(y_error) < acceptable_error_y :
        y_error  = 0




    # Proportional regulator calculate error
    x_calculated_p_error = (x_error * pid_coeff_p)
    y_calculated_p_error = (y_error * pid_coeff_p) * pid_coff_t_scale


    # if P enable
    if p_enable == 1:
        # if error is big add it to movement
        if abs(x_calculated_p_error) >= pid_coeff_p_min_step:
            x_return = x_current + x_calculated_p_error
        else:
            x_return = x_current

        if abs(y_calculated_p_error) >= pid_coeff_p_min_step:
            y_return = y_current + y_calculated_p_error
        else:
            y_return = y_current
    else:
        x_return = x_current
        y_return = y_current



    # Integrator regulator calculate error
    x_calculated_i_error = (x_error * pid_coeff_i) * pid_coff_t_scale
    y_calculated_i_error = (y_error * pid_coeff_i) * pid_coff_t_scale


    # Integrator calculation
    x_i_integrator += x_calculated_i_error
    y_i_integrator += y_calculated_i_error


    # Limit integrator
    if x_i_integrator > pid_coeff_i_max_limit:
        x_i_integrator = pid_coeff_i_max_limit
    elif x_i_integrator < -pid_coeff_i_max_limit:
        x_i_integrator = -pid_coeff_i_max_limit


    if y_i_integrator > pid_coeff_i_max_limit:
        y_i_integrator = pid_coeff_i_max_limit
    elif y_i_integrator < -pid_coeff_i_max_limit:
        y_i_integrator = -pid_coeff_i_max_limit



    # If integrator error bigger than threshold add it to common error
    if i_enable == 1:
        if abs(x_i_integrator) >= pid_coeff_i_min_step:
            if x_i_integrator > 0:
                x_return += pid_coeff_i_min_step
                x_i_integrator -= pid_coeff_i_min_step
            else:
                x_return -= pid_coeff_i_min_step
                x_i_integrator += pid_coeff_i_min_step

        if abs(y_i_integrator) >= pid_coeff_i_min_step:
            if y_i_integrator > 0:
                y_return += pid_coeff_i_min_step
                y_i_integrator -= pid_coeff_i_min_step
            else:
                y_return -= pid_coeff_i_min_step
                y_i_integrator += pid_coeff_i_min_step







    # Print the 6 parameters to the console
    print(f"PID_UPDATE:"
    #      f" xC {x_current:.2f}, yC {y_current:.2f}, xT {x_target:.2f}, yT {y_target:.2f},"
          f" xE {x_error:.2f}, yE {y_error:.2f},"
    #      f" xPer {x_calculated_p_error:.2f}, yPer {y_calculated_p_error:.2f},"
          f" xIer {x_calculated_i_error:.2f}, yIer {y_calculated_i_error:.2f}"
          f" xSum {x_i_integrator:.2f}, ySum {y_i_integrator:.2f}"
          f" xR {x_return:.2f}, xR {y_return:.2f}"
    )

    



    return x_return, y_return

def PID_GET_ERROR():

    global x_error, y_error

    return x_error, y_error
