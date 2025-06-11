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



pid_coff_t_scale = 1
pid_coeff_p = 0.03
pid_coeff_i = 1



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


    '''
    # Calculate x_resp (intended next position or adjustment)
    if x_cur > x_tar:
        x_resp_calculated =  x_cur - 1
    elif x_cur < x_tar:
        x_resp_calculated = x_cur + 1
    else: # x_cur == x_tar
        x_resp_calculated = x_cur # or x_tar, they are equal
    x_resp = x_resp_calculated

    # Calculate y_resp symmetrically
    if y_cur > y_tar:
        y_resp_calculated = y_cur - 1
    elif y_cur < y_tar:
        y_resp_calculated = y_cur + 1
    else: # y_cur == y_tar
        y_resp_calculated = y_cur # or y_tar, they are equal
    y_resp = y_resp_calculated
    '''

    return x_return, y_return

def PID_GET_ERROR():

    global x_error, y_error

    return x_error, y_error
