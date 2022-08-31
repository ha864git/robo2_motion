def get_angle(update_text: str, data: number):
    global temp_1, temp_2, temp_3
    temp_1 = update_text.char_at(0)
    temp_2 = parse_float(update_text.substr(1, len(update_text) - 1))
    temp_3 = data
    if temp_1 == "+":
        temp_3 += temp_2
    elif temp_1 == "-":
        temp_3 += 0 - temp_2
    else:
        temp_3 = parse_float(update_text)
    return temp_3

def on_bluetooth_connected():
    basic.show_icon(IconNames.SQUARE)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.NO)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def play():
    global play_pointer, play_timer, play_cmd, leg_right_angle, leg_left_angle, foot_right_angle, foot_left_angle
    play_pointer = 0
    play_timer = control.millis()
    while play_timer < control.millis():
        pass
    if play_pointer < len(list2):
        play_cmd = list2[play_pointer].split(",")
        if len(play_cmd) == 4:
            play_timer += parse_float(play_cmd[3])
            if cmd[0] == "L":
                leg_right_angle = parse_float(cmd[1]) + (leg_right_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO3, leg_right_angle)
                leg_left_angle = parse_float(cmd[2]) + (leg_left_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO1, leg_left_angle)
            elif cmd[0] == "F":
                foot_right_angle = parse_float(cmd[1]) + (foot_right_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO4, foot_right_angle)
                foot_left_angle = parse_float(cmd[2]) + (leg_left_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO2, foot_left_angle)
            play_pointer += 1

def on_uart_data_received():
    global line, list2, cmd, leg_right_angle, leg_left_angle, foot_right_angle, foot_left_angle
    line = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    bluetooth.uart_write_line(line)
    if line == "init":
        leg_initialize()
        foot_initialize()
        bluetooth.uart_write_line("initialized")
    elif line == "clear":
        list2 = []
        bluetooth.uart_write_line("list cleared !")
    elif line == "play":
        bluetooth.uart_write_line("start:" + convert_to_text(control.millis()))
        play()
        bluetooth.uart_write_line("end:" + convert_to_text(control.millis()))
    elif line == "len":
        bluetooth.uart_write_line("len:" + convert_to_text(len(list2)))
    else:
        cmd = line.split(",")
        if len(cmd) == 3:
            if cmd[0] == "L":
                leg_right_angle = parse_float(cmd[1]) + (leg_right_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO3, leg_right_angle)
                leg_left_angle = parse_float(cmd[2]) + (leg_left_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO1, leg_left_angle)
            elif cmd[0] == "F":
                foot_right_angle = parse_float(cmd[1]) + (foot_right_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO4, foot_right_angle)
                foot_left_angle = parse_float(cmd[2]) + (leg_left_angle_init - 90)
                kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO2, foot_left_angle)
        elif len(cmd) == 5:
            if cmd[0] == "S":
                list2.append("" + cmd[1] + "," + cmd[2] + "," + cmd[3] + "," + cmd[4])
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),
    on_uart_data_received)

def leg_set(right_angle_text: str, left_angle_text: str):
    global leg_right_angle, leg_left_angle
    leg_right_angle = get_angle(right_angle_text, leg_right_angle)
    kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO4, 0 + (0 - 90))
    leg_left_angle = get_angle(left_angle_text, leg_left_angle)
    kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO2, 0 + (0 - 90))
def foot_initialize():
    foot_set("90", "90")
def foot_set(right_angle_text2: str, left_angle_text2: str):
    global foot_right_angle, foot_left_angle
    foot_right_angle = get_angle(right_angle_text2, foot_right_angle)
    kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO3,
        foot_right_angle + (foot_right_angle_init - 90))
    foot_left_angle = get_angle(left_angle_text2, foot_left_angle)
    kitronik_i2c_16_servo.servo_write(kitronik_i2c_16_servo.Servos.SERVO1,
        foot_left_angle + (foot_left_angle_init - 90))
def leg_initialize():
    leg_set("90", "90")
line = ""
foot_left_angle = 0
foot_right_angle = 0
leg_left_angle = 0
leg_right_angle = 0
cmd: List[str] = []
play_cmd: List[str] = []
play_timer = 0
play_pointer = 0
temp_3 = 0
temp_2 = 0
temp_1 = ""
list2: List[str] = []
foot_left_angle_init = 0
foot_right_angle_init = 0
leg_left_angle_init = 0
leg_right_angle_init = 0
basic.show_icon(IconNames.HOUSE)
bluetooth.start_uart_service()
leg_right_angle_init = 85
leg_left_angle_init = 90
foot_right_angle_init = 92
foot_left_angle_init = 88
leg_initialize()
foot_initialize()
list2 = []

def on_forever():
    pass
basic.forever(on_forever)
