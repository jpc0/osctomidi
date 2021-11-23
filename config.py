import tkinter as tk
from typing import List
import mido
import yaml

window = tk.Tk()

midi_outs: List = mido.get_output_names()
midi_outs.append("test")
config = {
    "name": "osctomidi",
    "Selected Midi Output": midi_outs[0],
    "Macro List": []
}


def submit():
    global config
    global radiobuttonsvar
    global textinputvar
    config["Selected Midi Output"] = midi_outs[radiobuttonsvar.get()]
    config['Macro List'] = textinputvar.get().split(',')
    stream = open('config.yaml', 'w')
    yaml.dump(config, stream)
    stream.close()
    quit()


label = tk.Label(text="Please select a midi output")
label.pack()
radiobuttonsvar = tk.IntVar(0)
for out in range(len(midi_outs)):
    output_text = str(out+1) + ". " + midi_outs[out]
    button = tk.Radiobutton(
        window, text=output_text, variable=radiobuttonsvar, value=out)
    button.pack(anchor=tk.W)
label2 = tk.Label(
    text="Please type all your Macros, in order, seperated by a comma")
label2.pack()
textinputvar = tk.StringVar()
textinput = tk.Entry(window, textvariable=textinputvar)
textinput.pack(anchor=tk.W)
btn_submit = tk.Button(text="Submit", command=submit).pack()


window.mainloop()
