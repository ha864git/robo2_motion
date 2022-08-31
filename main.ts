function get_angle (update_text: string, data: number) {
    temp_1 = update_text.charAt(0)
    temp_2 = parseFloat(update_text.substr(1, update_text.length - 1))
    temp_3 = data
    if (temp_1 == "+") {
        temp_3 += temp_2
    } else if (temp_1 == "-") {
        temp_3 += 0 - temp_2
    } else {
        temp_3 = parseFloat(update_text)
    }
    return temp_3
}
function set_leg (right_angle_text: string, left_angle_text: string) {
    leg_right_angle = get_angle(right_angle_text, leg_right_angle)
    kitronik_i2c_16_servo.servoWrite(kitronik_i2c_16_servo.Servos.Servo3, leg_right_angle + (leg_right_angle_init - 90))
    leg_left_angle = get_angle(left_angle_text, leg_left_angle)
    kitronik_i2c_16_servo.servoWrite(kitronik_i2c_16_servo.Servos.Servo1, leg_left_angle + (leg_left_angle_init - 90))
}
bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Square)
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})
function play () {
    play_pointer = 0
    play_timer = control.millis()
    while (play_pointer < list.length) {
        while (play_timer > control.millis()) {
        	
        }
        play_cmd = list[play_pointer].split(",")
        if (play_cmd.length == 4) {
            play_timer += parseFloat(play_cmd[3])
            if (play_cmd[0] == "l") {
                set_leg(play_cmd[1], play_cmd[2])
            } else if (play_cmd[0] == "f") {
                set_foot(play_cmd[1], play_cmd[2])
            }
        }
        play_pointer += 1
    }
}
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    line = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
    if (line == "init") {
        set_leg("90", "90")
        set_foot("90", "90")
        bluetooth.uartWriteLine("initialized")
    } else if (line == "clear") {
        list = []
        bluetooth.uartWriteLine("list cleared !")
    } else if (line == "play") {
        bluetooth.uartWriteLine("play start:" + convertToText(control.millis()))
        play()
        bluetooth.uartWriteLine("play end:" + convertToText(control.millis()))
    } else if (line == "len") {
        bluetooth.uartWriteLine("len:" + convertToText(list.length))
    } else {
        cmd = line.split(",")
        if (cmd.length == 3) {
            if (cmd[0] == "l") {
                set_leg(cmd[1], cmd[2])
                bluetooth.uartWriteLine("" + convertToText(leg_right_angle) + "," + convertToText(leg_left_angle))
            } else if (cmd[0] == "f") {
                set_foot(cmd[1], cmd[2])
                bluetooth.uartWriteLine("" + convertToText(foot_right_angle) + "," + convertToText(foot_left_angle))
            }
        } else if (cmd.length == 5) {
            if (cmd[0] == "s") {
                list.push("" + cmd[1] + "," + cmd[2] + "," + cmd[3] + "," + cmd[4])
            }
        }
    }
})
function set_foot (right_angle_text: string, left_angle_text: string) {
    foot_right_angle = get_angle(right_angle_text, foot_right_angle)
    kitronik_i2c_16_servo.servoWrite(kitronik_i2c_16_servo.Servos.Servo4, foot_right_angle + (foot_right_angle_init - 90))
    foot_left_angle = get_angle(left_angle_text, foot_left_angle)
    kitronik_i2c_16_servo.servoWrite(kitronik_i2c_16_servo.Servos.Servo2, foot_left_angle + (foot_left_angle_init - 90))
}
let foot_left_angle = 0
let foot_right_angle = 0
let cmd: string[] = []
let line = ""
let play_cmd: string[] = []
let play_timer = 0
let play_pointer = 0
let leg_left_angle = 0
let leg_right_angle = 0
let temp_3 = 0
let temp_2 = 0
let temp_1 = ""
let list: string[] = []
let foot_right_angle_init = 0
let leg_right_angle_init = 0
let foot_left_angle_init = 0
let leg_left_angle_init = 0
basic.showIcon(IconNames.House)
bluetooth.startUartService()
leg_left_angle_init = 96
foot_left_angle_init = 86
leg_right_angle_init = 88
foot_right_angle_init = 95
set_leg("90", "90")
set_foot("90", "90")
list = []
