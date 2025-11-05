# Beetlecrab-Audio-Tempera-CC-Switcher-for-Adafruit-Macropad
Circuitpython code for Adafruit Macropad that turns it into a CC switcher for Beetlecrab Audio Tempera with MIDI over USB.

**DISCLAIMER!!!**

I am a hobbyist coder. I've been coding things off-and-on since the early 90s. I took one beginner coding course in university some 30ish years ago. My code may be ugly, but 
I can usually make it work. I also like to swear in comments, though I have curbed that desire of late.

//DISCLAIMER

I don't really have a good name for this project.

The first thing you're going to want to do if you want to run this code on your Macropad is to install Circuitpython on it.

It's very easy to do. There's a guide here: https://learn.adafruit.com/adafruit-macropad-rp2040/circuitpython

After that, you have to put some libraries that the code uses into the/lib folder on the Macropad.

They are: adafruit_display_text, adafruit_hid, adafruit_midi, adfruit_debouncer, adafruit_macropad, adafruit_simple_text_display, adafruit_ticks, and neopixel.

They are all in the adafruit-circuitpython-bundle-10.x-mpy-20251105.zip that you can download here: https://circuitpython.org/libraries



Once you've done that, just plop code.py from the repository here onto the root of the drive that it mounts as and you should be good to go.

Now, onto how to use it!

Usage:

It boots in "perform" mode. Here, the left 8 keys have been assigned the CCs for relative X and Y of emitters 1-4 in each row denoted by 1rx, 1ry, 2rx, 2ry, etc. 
The right column are the "Scenes". The top key should be lit and it is scene #1.

You can hold one of the left 8 keys in perform mode, and turn the encoder to adjust its value. As you adjust, it also sends that CC to Tempera (provided you have it plugged into Tempera's host jack and
have set the MIDI channel accordingly). As you adjust the value, it is stored in the currently active scene.

If you press another scene key, the CC values stored in that scene will be sent immediately to Tempera. If you haven't adjusted them, they will just be the default values (all at 64 as of November 3rd, 2025, I'm
working on a new set of default values because while 64 works for relative X and Y as default, it's not so good for other parameters like grain length or density.)

That's about it for perform mode.


If you press the encoder, the Macropad enters "set up" mode.

Here, you can adjust the MIDI channel by turning the encoder knob while not holding any keys.

Holding one of the 8 CC keys and turning the encoder changes its assignment. I chose 14 CCs per emitter and included those. (I might add more of them later, and I also might add the other CC accessible parameters like
track volumes, FX settings, etc. at a later date as well.)

The current existing accessible CCs are:

1vo = emitter 1 volume

1ln = emitter 1 grain length

1dn = emitter 1 grain density

1ge = emitter 1 grain envelope

1pn = emitter 1 panning

1tn = emitter 1 tuning

1ov = emitter 1 octave

1rx = emitter 1 relative X

1ry = emitter 1 relative Y

1sx = emitter 1 spray X

1sy = emitter 1 spray Y

1tw = emitter 1 tone width

1tc = emitter 1 tone center

1fx = emitter 1 effects send


Then, each of these again for emitters 2-4 just replacing the "1" with the emitter number.
Each CC setting also has a color associated with it that the LED is lit to when you choose it. ie choose 1vo for emitter 1's volume, and the key will be blue. Choose 2vo for a key, and it will be red for emitter 2. etc.

Adding more to this list is trivial. I just kept it to the most useful (IMO) CCs accessible. If you know anything about code, you can probably add or remove items from this list as you see fit. Just be careful as the array of arrays that contains all these values has two other
arrays at the end that contain settings for the scene keys and you would have to adjust reference to those elsewhere in the code if the length of the array changes.

Clicking the encoder again brings it back to perform mode.

That's about it.

Really, there's no reason to not use this to control just about anything with USB MIDI. It should work fine on any hardware synth with a host jack, and using it with a DAW on PC would also be easy enough. It would just be a matter of editing the CC values in various arrays in the code to the ones
you want.


Have fun!



















