# Underwaterbob's Tempera CC scene morpher. Or switcher. We'll see.
# Keys 1, 2, 4, 5, 7, 8, 10, 11 are assigned CCs. Keys 3, 6, 9, 12 are assigned scenes.
# Two modes: set up and perform. In set up mode. Holding a key and turning the encoder chooses
# a CC# for that key. Holding a scene key and turning the encoder chooses a morph time (maybe not yet)
# In perform mode, the left 8 keys can be held to modify their values. The right four are pressed to switch
# to their respective scenes.

from adafruit_macropad import MacroPad
from adafruit_macropad import adafruit_midi
import microcontroller

macropad = MacroPad()

# boot variable

boot = True

# encoder delta

#enc_del = 0

# array of keystate booleans

key_state = [
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False
]

# MIDI channel defaults to 4 because of my Tempera habits. Which is 3 because of zero indexing.

chan = 3

# Array of CC#s for the left keys.

cc_nums = [49, 50, 0, 67, 68, 0, 85, 86, 0, 103, 104, 0]

# Array of initial CC values for each key and each scene.

cc_vals = [
        [64, 64, 0, 64, 64, 0, 64, 64, 0, 64, 64, 0],
        [64, 64, 0, 64, 64, 0, 64, 64, 0, 64, 64, 0],
        [64, 64, 0, 64, 64, 0, 64, 64, 0, 64, 64, 0],
        [64, 64, 0, 64, 64, 0, 64, 64, 0, 64, 64, 0]
]

# Array of key parameters

key_param = [
            7,
            8,
            56,
            21,
            22,
            57,
            35,
            36,
            57,
            49,
            50,
            57
]

# put the values in nvm into those two arrays to load last settings saved  WTFFF!

key_param = list(microcontroller.nvm[0:12])
print(key_param)

# gettings values back into cc_vals a little more complicated
new_arr = list(microcontroller.nvm[0:60])
print(new_arr)

i = 0
for i in range(0, 11, 1):
    cc_vals[0][i] = new_arr[i+12]
    cc_vals[1][i] = new_arr[i+24]
    cc_vals[2][i] = new_arr[i+36]
    cc_vals[3][i] = new_arr[i+48]

    #j = 0
    #for j in range(0, 11, 1):
    #    cc_vals[i][j] = new_arr[k+12]
    #    k += 1
print(cc_vals)

# Scene indicator

scIndex = 0

# scene tester

scTest = scIndex

# Tempera and scene colors.

emitter1Color = 0x0800FF
emitter2Color = 0xFF0064
emitter3Color = 0xF7FF00
emitter4Color = 0x00FF50
offColor = 0x000000
pressed = 0xFFFFFF

# set up mode checker.

set_up = False

# all of the CCs that I need to be able to switch to. Just emitters for now. FX later if things work out.

tempera_ccs = [
            [40, "1vo", emitter1Color, 80], #0
            [41, "1ln", emitter1Color, 16], #1
            [43, "1dn", emitter1Color, 8], #2
            [44, "1ge", emitter1Color, 64], #3
            [46, "1pn", emitter1Color, 64], #4
            [47, "1tn", emitter1Color, 0], #5
            [48, "1ov", emitter1Color, 64], #6
            [49, "1rx", emitter1Color, 64], #7
            [50, "1ry", emitter1Color, 64], #8
            [51, "1sx", emitter1Color, 0], #9
            [52, "1sy", emitter1Color, 0], #10
            [53, "1tw", emitter1Color, 127], #11
            [54, "1tc", emitter1Color, 64], #12
            [55, "1fx", emitter1Color, 127], #13
            [56, "2vo", emitter2Color, 80], #14
            [57, "2ln", emitter2Color, 16], #15
            [59, "2dn", emitter2Color, 8], #16
            [60, "2ge", emitter2Color, 64], #17
            [62, "2pn", emitter2Color, 64], #18
            [63, "2tn", emitter2Color, 0], #19
            [65, "2ov", emitter2Color, 64], #20
            [67, "2rx", emitter2Color, 64], #21
            [68, "2ry", emitter2Color, 64], #22
            [69, "2sx", emitter2Color, 0], #23
            [70, "2sy", emitter2Color, 0], #24
            [72, "2tw", emitter2Color, 127], #25
            [73, "2tc", emitter2Color, 64], #26
            [75, "2fx", emitter2Color, 127], #27
            [76, "3vo", emitter3Color, 80], #28
            [77, "3ln", emitter3Color, 16], #29
            [79, "3dn", emitter3Color, 8], #30
            [80, "3ge", emitter3Color, 64], #31
            [82, "3pn", emitter3Color, 64], #32
            [83, "3tn", emitter3Color, 0], #33
            [84, "3ov", emitter3Color, 64], #34
            [85, "3rx", emitter3Color, 64], #35
            [86, "3ry", emitter3Color, 64], #36
            [87, "3sx", emitter3Color, 0], #37
            [88, "3sy", emitter3Color, 0], #38
            [89, "3tw", emitter3Color, 127], #39
            [90, "3tc", emitter3Color, 64], #40
            [91, "3fx", emitter3Color, 127], #41
            [92, "4vo", emitter4Color, 80], #42
            [93, "4ln", emitter4Color, 16], #43
            [95, "4dn", emitter4Color, 8], #44
            [96, "4ge", emitter4Color, 64], #45
            [98, "4pn", emitter4Color, 64], #46
            [99, "4tn", emitter4Color, 0], #47
            [102, "4ov", emitter4Color, 64],#48
            [103, "4rx", emitter4Color, 64],#49
            [104, "4ry", emitter4Color, 64],#50
            [105, "4sx", emitter4Color, 0],#51
            [106, "4sy", emitter4Color, 0],#52
            [107, "4tw", emitter4Color, 127],#53
            [108, "4tc", emitter4Color, 64],#54
            [109, "4fx", emitter4Color, 127],#55
            [0, "S:", pressed, 0],        #56
            [0, "S:", offColor, 0]        #57
]
# array of the colors

key_colors = [
    emitter1Color,
    emitter1Color,
    offColor,
    emitter2Color,
    emitter2Color,
    offColor,
    emitter3Color,
    emitter3Color,
    offColor,
    emitter4Color,
    emitter4Color,
    offColor,
]

# name for title

name_arr = [
            "Perform",
            "Set up "
]

name_ref = 0

# Key brightness.
macropad.pixels.brightness = 0.1

# Set up text display?
text_lines = macropad.display_text()

# knob position
last_knob_pos = macropad.encoder

while True:

    # Check to see if this is the first time through and
    # populate the LED colors

    if boot:
        i = 0
        for i in range(0, 11, 1):
            macropad.pixels[i] = tempera_ccs[key_param[i]][2]
        boot = False

    # check for set up mode
    macropad.encoder_switch_debounced.update()
    if  macropad.encoder_switch_debounced.released:
        set_up = not set_up
        if not set_up:
            macropad.pixels[scIndex * 3 + 2] = pressed
            name_ref = 0
            # OK an attempt to make a bytearray of cc_vals and key_param.
            temp_arr = []
            print(temp_arr)
            print(key_param)
            temp_arr += key_param
            print("temp_arr")
            print(temp_arr)
            #i = 0
            #for i in range(0, 3, 1):
            #    temp_arr += cc_vals[i]
            #    print(temp_arr)
            # new trial
            temp_arr += cc_vals[0]
            print(temp_arr)
            temp_arr += cc_vals[1]
            print(temp_arr)
            temp_arr += cc_vals[2]
            print(temp_arr)
            temp_arr += cc_vals[3]
            print(temp_arr)
            ba = bytearray(temp_arr)
            print(list(ba))
            print(len(ba))
            # write values to nvm
            microcontroller.nvm[0:60] = ba
            print("crud")
            print(cc_vals)
        else:
            macropad.pixels[scIndex * 3 + 2] = offColor
            name_ref = 1

    # check for key presses and do the appropriate action

    while macropad.keys.events:
        key_event = macropad.keys.events.get()
        if key_event:
            if key_event.pressed:
                key = key_event.key_number
                key_state[key] = True
                if not set_up:
                    macropad.pixels[key] = pressed
                    if key == 2:
                        #macropad.pixels[2] = pressed
                        macropad.pixels[5] = offColor
                        macropad.pixels[8] = offColor
                        macropad.pixels[11] = offColor
                        scIndex = 0
                    elif key == 5:
                        macropad.pixels[2] = offColor
                        #macropad.pixels[5] = pressed
                        macropad.pixels[8] = offColor
                        macropad.pixels[11] = offColor
                        scIndex = 1
                    elif key == 8:
                        macropad.pixels[2] = offColor
                        macropad.pixels[5] = offColor
                        #macropad.pixels[8] = pressed
                        macropad.pixels[11] = offColor
                        scIndex = 2
                    elif key == 11:
                        macropad.pixels[2] = offColor
                        macropad.pixels[5] = offColor
                        macropad.pixels[8] = offColor
                        #macropad.pixels[11] = pressed
                        scIndex = 3


            if key_event.released:
                key = key_event.key_number
                key_state[key] = False
                if key != 2 and key != 5 and key != 8 and key != 11:
                    macropad.pixels[key] = tempera_ccs[key_param[key]][2]

    # encoder management

    if macropad.encoder != last_knob_pos:
        if set_up:
            i = 0
            for i in range(0, 11, 1):
                if key_state[i]:
                    if i != 2 and i != 5 and i != 8 and i != 11:
                        key_param[i] += macropad.encoder - last_knob_pos
                        key_param[i] = min(max(key_param[i], 0), 55)
                        macropad.pixels[i] = tempera_ccs[key_param[i]][2]
                        cc_nums[i] = tempera_ccs[key_param[i]][0]
                        for j in range(0, 3, 1):
                            cc_vals[j][i] = tempera_ccs[key_param[i]][3]
            if not any(key_state):
                chan += macropad.encoder - last_knob_pos
                chan = min(max(chan, 0), 15)
        else:
            i = 0
            for i in range(0, 11, 1):
                if key_state[i]:
                    cc_vals[scIndex][i] += macropad.encoder - last_knob_pos
                    cc_vals[scIndex][i] = min(max(cc_vals[scIndex][key], 0), 127)
                    macropad.midi.send(macropad.ControlChange(cc_nums[i], cc_vals[scIndex][i]), chan)
        last_knob_pos = macropad.encoder

    # scene checker and switcher
    if scIndex != scTest:
        macropad.midi.send(macropad.ControlChange(cc_nums[0], cc_vals[scIndex][0]), chan)
        macropad.midi.send(macropad.ControlChange(cc_nums[1], cc_vals[scIndex][1]), chan)
        macropad.midi.send(macropad.ControlChange(cc_nums[3], cc_vals[scIndex][3]), chan)
        macropad.midi.send(macropad.ControlChange(cc_nums[4], cc_vals[scIndex][4]), chan)
        macropad.midi.send(macropad.ControlChange(cc_nums[6], cc_vals[scIndex][6]), chan)
        macropad.midi.send(macropad.ControlChange(cc_nums[7], cc_vals[scIndex][7]), chan)
        macropad.midi.send(macropad.ControlChange(cc_nums[9], cc_vals[scIndex][9]), chan)
        macropad.midi.send(macropad.ControlChange(cc_nums[10], cc_vals[scIndex][10]), chan)
        scTest = scIndex


    # print text to the display

    text_lines[0].text = f"{name_arr[name_ref]}:{chan + 1}  S:{scIndex + 1}".center(20)
    text_lines[1].text = f"{tempera_ccs[key_param[0]][1]}: {cc_vals[scIndex][0]:{0}{3}}  {tempera_ccs[key_param[1]][1]}: {cc_vals[scIndex][1]:{0}{3}}"
    text_lines[2].text = f"{tempera_ccs[key_param[3]][1]}: {cc_vals[scIndex][3]:{0}{3}}  {tempera_ccs[key_param[4]][1]}: {cc_vals[scIndex][4]:{0}{3}}"
    text_lines[3].text = f"{tempera_ccs[key_param[6]][1]}: {cc_vals[scIndex][6]:{0}{3}}  {tempera_ccs[key_param[7]][1]}: {cc_vals[scIndex][7]:{0}{3}}"
    text_lines[4].text = f"{tempera_ccs[key_param[9]][1]}: {cc_vals[scIndex][9]:{0}{3}}  {tempera_ccs[key_param[10]][1]}: {cc_vals[scIndex][10]:{0}{3}}"
    text_lines.show()

