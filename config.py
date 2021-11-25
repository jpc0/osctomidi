import wx
from typing import List
import mido
import yaml
import os

from osctomidi import main


def get_config():
    stream = open('config.yaml', 'r')
    config = yaml.safe_load(stream)
    stream.close()
    return config


class OsctoMidi(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        self.InitFrame()

    def InitFrame(self):
        frame = OsctomidiFrame(
            parent=None, title="OsctoMidi Config")
        frame.Show()
        return


class OsctomidiFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.OnInit()

    def OnInit(self):
        panel = OsctomidiPanel(parent=self)
        self.Fit()


class OsctomidiPanel(wx.Panel):
    midi_outs = mido.get_output_names()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self._selectedmidiout = ''
        self._macros = []

        if os.path.isfile('config.yaml'):
            config = get_config()
            self._selectedmidiout = config["Selected Midi Output"]
            self._macros = config['Macro List']

        self._label = wx.StaticText(
            self, label="Please select a midi output")

        self._radio_midiins = wx.RadioBox(
            self, choices=self.midi_outs, style=wx.RA_VERTICAL)

        if self._selectedmidiout:
            if self._selectedmidiout in self._radio_midiins.GetStrings():
                self._radio_midiins.SetSelection(
                    self._radio_midiins.GetStrings().index(self._selectedmidiout))

        self._label2 = wx.StaticText(
            self, label="Please insert all your Macros")
        self._textinput = wx.TextCtrl(self)

        self._listboxItems = wx.ListBox(
            self, choices=self._macros)

        self._btn_add = wx.Button(self, label="Add")
        self._btn_add.Bind(event=wx.EVT_BUTTON, handler=self.add)

        self._btn_remove = wx.Button(self, label="Remove")
        self._btn_remove.Bind(event=wx.EVT_BUTTON, handler=self.remove)

        self._btn_up = wx.Button(self, label="Up")
        self._btn_up.Bind(event=wx.EVT_BUTTON, handler=self.up)

        self._btn_down = wx.Button(self, label="Down")
        self._btn_down.Bind(event=wx.EVT_BUTTON, handler=self.down)

        self._btn_submit = wx.Button(self, label="Submit")
        self._btn_submit.Bind(event=wx.EVT_BUTTON, handler=self.submit)

        self._btn_cancel = wx.Button(self, label="Cancel")
        self._btn_cancel.Bind(event=wx.EVT_BUTTON, handler=self.cancel)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        textSizer = wx.BoxSizer()
        radiobuttonSizer = wx.BoxSizer()
        text2Sizer = wx.BoxSizer()
        textinputSizer = wx.BoxSizer()
        listboxsizer = wx.BoxSizer()
        buttonsizer = wx.BoxSizer()
        button2sizer = wx.BoxSizer()

        textSizer.Add(self._label, proportion=0, flag=wx.ALL, border=10)
        radiobuttonSizer.Add(self._radio_midiins,
                             1, wx.ALL | wx.EXPAND, border=10)
        text2Sizer.Add(self._label2, proportion=0, flag=wx.ALL, border=10)
        textinputSizer.Add(self._textinput, 1, wx.ALL | wx.EXPAND, 10)
        listboxsizer.Add(self._listboxItems,
                         1, wx.ALL | wx.EXPAND, border=10)

        buttonsizer.Add(self._btn_add, proportion=0, flag=wx.ALL, border=10)
        buttonsizer.Add(self._btn_remove, proportion=0, flag=wx.ALL, border=10)
        buttonsizer.Add(self._btn_up, proportion=0, flag=wx.ALL, border=10)
        buttonsizer.Add(self._btn_down, proportion=0, flag=wx.ALL, border=10)
        button2sizer.Add(self._btn_submit, proportion=0,
                         flag=wx.ALL, border=10)
        button2sizer.Add(self._btn_cancel, proportion=0,
                         flag=wx.ALL, border=10)

        mainSizer.Add(textSizer, 0, flag=wx.ALL)
        mainSizer.Add(radiobuttonSizer, 0, flag=wx.ALL)
        mainSizer.Add(text2Sizer, 0, flag=wx.ALL)
        mainSizer.Add(textinputSizer, 0, wx.ALL | wx.EXPAND)
        mainSizer.Add(listboxsizer, 1, wx.ALL | wx.EXPAND)
        mainSizer.Add(buttonsizer, 0, flag=wx.CENTER)
        mainSizer.Add(button2sizer, 0, flag=wx.CENTER)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()

    def add(self, event):
        if not self._textinput.Value:
            return
        for i in self._textinput.GetValue().split(','):
            self._listboxItems.Append(i.strip())
        self._textinput.Value = ''

    def remove(self, event):
        selecteditem = self._listboxItems.GetSelection()
        self._listboxItems.Delete(selecteditem)

    def up(self, event):
        selecteditem: 'int' = self._listboxItems.GetSelection()
        selecteditemstring: 'str' = self._listboxItems.GetStringSelection()
        self._listboxItems.Delete(selecteditem)
        self._listboxItems.Insert(selecteditemstring, selecteditem-1)
        self._listboxItems.Select(selecteditem-1)

    def down(self, event):
        selecteditem: 'int' = self._listboxItems.GetSelection()
        selecteditemstring: 'str' = self._listboxItems.GetStringSelection()
        self._listboxItems.Delete(selecteditem)
        self._listboxItems.Insert(selecteditemstring, selecteditem+1)
        self._listboxItems.Select(selecteditem+1)

    def submit(self, event):
        selectedmidiout = self._radio_midiins.GetSelection()
        config = {
            'Macro List': self._listboxItems.GetStrings(),
            "Selected Midi Output": self.midi_outs[selectedmidiout],
            "Name": "osctomidi",
        }
        stream = open('config.yaml', 'w')
        yaml.dump(config, stream)
        stream.close()
        quit()

    def cancel(self, event):
        quit()


if __name__ == "__main__":
    app = OsctoMidi()
    app.MainLoop()
