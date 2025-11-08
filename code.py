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

# for iterating through CCs

key_ind = [0, 1, 3, 4, 6, 7, 9, 10]

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

# Default array of key parameter references.

key_param = [12, 13, 71, 26, 27, 72, 40, 41, 72, 54, 55, 72]

# gettings values back into cc_vals a little more complicated
new_arr = list(microcontroller.nvm[0:61])

for i in range(0, 12, 1):
    key_param[i] = new_arr[i]
print(key_param)

k = 0
for i in range(0, 4, 1):
    for j in range(0, 12, 1):
        cc_vals[i][j] = new_arr[k+12]
        k += 1

# Saved MIDI channel
chan = new_arr[60]

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
modulator = 0x330066
effect = 0xDD3300

# set up mode checker.

set_up = False

# all of the CCs that I need to be able to switch to. Just emitters for now. FX later if things work out.

tempera_ccs = [
            [19, "rmx", effect, 0], #0
            [23, "dmx", effect, 0], #1
            [29, "cmx", effect, 0], #2
            [24, "fcu", effect, 127], #3
            [25, "fre", effect, 64], #4
            [40, "1vo", emitter1Color, 80], #5
            [41, "1ln", emitter1Color, 16], #6
            [43, "1dn", emitter1Color, 8], #7
            [44, "1ge", emitter1Color, 64], #8
            [46, "1pn", emitter1Color, 64], #9
            [47, "1tn", emitter1Color, 0], #10
            [48, "1ov", emitter1Color, 64], #11
            [49, "1rx", emitter1Color, 64], #12
            [50, "1ry", emitter1Color, 64], #13
            [51, "1sx", emitter1Color, 0], #14
            [52, "1sy", emitter1Color, 0], #15
            [53, "1tw", emitter1Color, 127], #16
            [54, "1tc", emitter1Color, 64], #17
            [55, "1fx", emitter1Color, 127], #18
            [56, "2vo", emitter2Color, 80], #19
            [57, "2ln", emitter2Color, 16], #20
            [59, "2dn", emitter2Color, 8], #21
            [60, "2ge", emitter2Color, 64], #22
            [62, "2pn", emitter2Color, 64], #23
            [63, "2tn", emitter2Color, 0], #24
            [65, "2ov", emitter2Color, 64], #25
            [67, "2rx", emitter2Color, 64], #26
            [68, "2ry", emitter2Color, 64], #27
            [69, "2sx", emitter2Color, 0], #28
            [70, "2sy", emitter2Color, 0], #29
            [72, "2tw", emitter2Color, 127], #30
            [73, "2tc", emitter2Color, 64], #31
            [75, "2fx", emitter2Color, 127], #32
            [76, "3vo", emitter3Color, 80], #33
            [77, "3ln", emitter3Color, 16], #34
            [79, "3dn", emitter3Color, 8], #35
            [80, "3ge", emitter3Color, 64], #36
            [82, "3pn", emitter3Color, 64], #37
            [83, "3tn", emitter3Color, 0], #38
            [84, "3ov", emitter3Color, 64], #39
            [85, "3rx", emitter3Color, 64], #40
            [86, "3ry", emitter3Color, 64], #41
            [87, "3sx", emitter3Color, 0], #42
            [88, "3sy", emitter3Color, 0], #43
            [89, "3tw", emitter3Color, 127], #44
            [90, "3tc", emitter3Color, 64], #45
            [91, "3fx", emitter3Color, 127], #46
            [92, "4vo", emitter4Color, 80], #47
            [93, "4ln", emitter4Color, 16], #48
            [95, "4dn", emitter4Color, 8], #49
            [96, "4ge", emitter4Color, 64], #50
            [98, "4pn", emitter4Color, 64], #51
            [99, "4tn", emitter4Color, 0], #52
            [102, "4ov", emitter4Color, 64],#53
            [103, "4rx", emitter4Color, 64],#54
            [104, "4ry", emitter4Color, 64],#55
            [105, "4sx", emitter4Color, 0],#56
            [106, "4sy", emitter4Color, 0],#57
            [107, "4tw", emitter4Color, 127],#58
            [108, "4tc", emitter4Color, 64],#59
            [109, "4fx", emitter4Color, 127],#60
            [110, "M01", modulator, 0], #61
            [111, "M02", modulator, 0], #62
            [112, "M03", modulator, 0], #63
            [113, "M04", modulator, 0], #64
            [114, "M05", modulator, 0], #65
            [115, "M06", modulator, 0], #66
            [116, "M07", modulator, 0], #67
            [117, "M08", modulator, 0], #68
            [118, "M09", modulator, 0], #69
            [119, "M10", modulator, 0], #70
            [0, "S:", pressed, 0],        #71
            [0, "S:", offColor, 0]        #72
]

# name for title

name_arr = [
            "Perform",
            "Set up "
]

name_ref = 0

# Don't forget to assign cc_nums
for i in range(0, 12, 1):
    cc_nums[i] = tempera_ccs[key_param[i]]

# Key brightness.
macropad.pixels.brightness = 0.2

# Set up text display?
text_lines = macropad.display_text()

# knob position
last_knob_pos = macropad.encoder

# Paint the LEDs!
for i in range(0, 12, 1):
    macropad.pixels[i] = tempera_ccs[key_param[i]][2]

while True:

    # check for set up mode
    macropad.encoder_switch_debounced.update()
    if  macropad.encoder_switch_debounced.released:
        set_up = not set_up
        if not set_up:
            macropad.pixels[scIndex * 3 + 2] = pressed
            name_ref = 0
            # OK an attempt to make a bytearray of cc_vals and key_param.
            temp_arr = []
            temp_arr += key_param
            #i = 0
            for i in range(0, 4, 1):
                temp_arr += cc_vals[i]
            temp_arr.append(chan)
            ba = bytearray(temp_arr)
            # write values to nvm
            microcontroller.nvm[0:61] = ba
            print("Data Saved:")
            print(temp_arr)
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
                    if key == 2 or key == 5 or key == 8 or key == 11:
                        for i in range(0, 4, 1):
                            if key == ((3*i)+2):
                                scIndex = i
                            else:
                                macropad.pixels[(3*i)+2] = offColor
            if key_event.released:
                key = key_event.key_number
                key_state[key] = False
                if key != 2 and key != 5 and key != 8 and key != 11:
                    macropad.pixels[key] = tempera_ccs[key_param[key]][2]

    # encoder management

    if macropad.encoder != last_knob_pos:
        if set_up:
            i = 0
            for i in range(0, 12, 1):
                if key_state[i]:
                    if i != 2 and i != 5 and i != 8 and i != 11:
                        key_param[i] += macropad.encoder - last_knob_pos
                        key_param[i] = min(max(key_param[i], 0), 70)
                        macropad.pixels[i] = tempera_ccs[key_param[i]][2]
                        cc_nums[i] = tempera_ccs[key_param[i]][0]
                        for j in range(0, 4, 1):
                            cc_vals[j][i] = tempera_ccs[key_param[i]][3]
            if not any(key_state):
                chan += macropad.encoder - last_knob_pos
                chan = min(max(chan, 0), 15)
        else:
            i = 0
            for i in range(0, 12, 1):
                if key_state[i]:
                    cc_vals[scIndex][i] += macropad.encoder - last_knob_pos
                    cc_vals[scIndex][i] = min(max(cc_vals[scIndex][key], 0), 127)
                    macropad.midi.send(macropad.ControlChange(cc_nums[i], cc_vals[scIndex][i]), chan)
        last_knob_pos = macropad.encoder

    # scene checker and switcher
    if scIndex != scTest:
        for i in range(0, 8, 1):
            macropad.midi.send(macropad.ControlChange(cc_nums[key_ind[i]], cc_vals[scIndex][key_ind[i]]), chan)
        scTest = scIndex

    # print text to the display

    text_lines[0].text = f"{name_arr[name_ref]}:{chan + 1}  S:{scIndex + 1}".center(20)
    text_lines[1].text = f"{tempera_ccs[key_param[0]][1]}: {cc_vals[scIndex][0]:{0}{3}}  {tempera_ccs[key_param[1]][1]}: {cc_vals[scIndex][1]:{0}{3}}"
    text_lines[2].text = f"{tempera_ccs[key_param[3]][1]}: {cc_vals[scIndex][3]:{0}{3}}  {tempera_ccs[key_param[4]][1]}: {cc_vals[scIndex][4]:{0}{3}}"
    text_lines[3].text = f"{tempera_ccs[key_param[6]][1]}: {cc_vals[scIndex][6]:{0}{3}}  {tempera_ccs[key_param[7]][1]}: {cc_vals[scIndex][7]:{0}{3}}"
    text_lines[4].text = f"{tempera_ccs[key_param[9]][1]}: {cc_vals[scIndex][9]:{0}{3}}  {tempera_ccs[key_param[10]][1]}: {cc_vals[scIndex][10]:{0}{3}}"
    text_lines.show()

