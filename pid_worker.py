# pid_worker.py


# Default target setpoint for the blue circle.
DEF_TARGET_X = 333
DEF_TARGET_Y  = 580


x_current = 0
y_current = 0

x_target = DEF_TARGET_X
y_target = DEF_TARGET_Y

x_return = 0
y_return = 0

x_error = 0
y_error = 0



pid_coff_t_scale: float = 1
pid_coeff_p: float  = 0.03
pid_coeff_i: float = 1



def PID_UPDATE(x_cur, y_cur, x_tar, y_tar):

    global x_current, y_current, x_target, y_target, x_error, y_error, x_return, y_return
    global pid_coff_t_scale, pid_coeff_p, pid_coeff_i


    x_current = x_cur  
    y_current = y_cur 
    
    x_target = x_tar
    y_target = y_tar

    x_error = x_tar - x_cur
    y_error = y_tar - y_cur


    x_return = x_current + (x_error * pid_coeff_p) * pid_coff_t_scale

    y_return = y_current + (y_error * pid_coeff_p) * pid_coff_t_scale


    # Print the 6 parameters to the console
    print(f"PID_UPDATE: x_cur={x_current:.2f}, y_cur={y_current:.2f}, x_tar={x_target:.2f}, y_tar={y_target:.2f}, x_ret={x_return:.2f}, y_ret={y_return:.2f}")




    return x_return, y_return

def PID_GET_ERROR():

    global x_error, y_error

    return x_error, y_error
