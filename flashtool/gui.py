# This GUI is a fork of the brilliant https://github.com/marcelstoer/nodemcu-pyflasher
import re
import sys
import threading
import builtins

import wx
import wx.adv
import wx.lib.inspection
import wx.lib.mixins.inspection
from wx.lib.embeddedimage import PyEmbeddedImage
from flashtool.flasher import Flasher
from flashtool.helpers import list_serial_ports

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            title,
            size=(725, 650),
            style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE,
        )

        self._firmware = None
        self._port = None
        self.flasher = Flasher()
        self.interrupt = False
        self.ports=[]
        self._init_ui()

        frame=self

        def print(*args, **kwargs):
            frame.addText(*args, **kwargs)

        builtins.print = print

        self.SetMinSize((640, 480))
        self.Centre(wx.BOTH)
        self.Show(True)

    def addText(self,*args,**kwargs):
        first=True
        for k in args:
            self.console_ctrl.AppendText(k)
            if not first:
                self.console_ctrl.AppendText(',')
            first=False
        if kwargs.get('end') is None:
            self.console_ctrl.AppendText("\n")
        else:
            self.console_ctrl.AppendText(kwargs.get('end'))
        self.console_ctrl.SetInsertionPoint(-1)
        wx.Yield()
        if self.interrupt:
            self.interrupt=False
            raise Exception("User cancel")


    def _init_ui(self):
        def on_reload(event):
            self.choice.SetItems(self._get_serial_ports())

        def changeButtons(run):
            if run:
                self.button.Disable()
                self.check_button.Disable()
                self.cancel_button.Enable()
            else:
                self.button.Enable()
                self.check_button.Enable()
                self.cancel_button.Disable()
            wx.Yield()
        def isFull():
            return self.mode.GetSelection() == 0
        def onFlash(event):
            self.interrupt=False
            changeButtons(True)
            self.console_ctrl.SetValue("")
            self.flasher.runFlash(self.flasher.runCheck(self._port, self._firmware, isFull()))
            changeButtons(False)
        def onCheck(event):
            self.interrupt=False
            changeButtons(True)
            self.console_ctrl.SetValue("")
            self.flasher.runCheck(self._port, self._firmware, isFull())
            changeButtons(False)
        def onCancel(event):
            self.interrupt=True
        def onMode(event):
            self._firmware=''
            self.file_picker.SetPath('')
            pass
        def on_select_port(event):
            choice = event.GetEventObject()
            self._port = self.ports[choice.GetSelection()]

        def on_pick_file(event):
            self._firmware = event.GetPath().replace("'", "")
            result=self.flasher.checkImageFile(self._firmware,isFull())
            self.firmwareInfo.SetLabel(result['info'])
            if result['error']:
                self.firmwareInfo.SetForegroundColour(wx.RED)
            else:
                self.firmwareInfo.SetForegroundColour(wx.BLACK)

        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(10, 2, 10, 10)
        self.mode = wx.RadioBox(panel,choices=['initial','update'],label="mode")
        self.mode.Bind(wx.EVT_RADIOBOX,onMode)
        self.choice = wx.Choice(panel, choices=self._get_serial_ports())
        self.choice.Bind(wx.EVT_CHOICE, on_select_port)
        reload_button = wx.Button(
            panel,
            id=wx.ID_ANY,
            label="Reload"
        )
        reload_button.Bind(wx.EVT_BUTTON, on_reload)
        reload_button.SetToolTip("Reload serial device list")

        self.file_picker = wx.FilePickerCtrl(panel, style=wx.FLP_USE_TEXTCTRL)
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, on_pick_file)

        serial_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        serial_boxsizer.Add(self.choice, 1, wx.EXPAND)
        serial_boxsizer.AddStretchSpacer(0)
        serial_boxsizer.Add(reload_button, 0, wx.ALIGN_NOT, 20)

        self.firmwareInfo=wx.StaticText(panel)

        self.button = wx.Button(panel, -1, "Flash ESP")
        self.button.Bind(wx.EVT_BUTTON, onFlash)

        self.check_button = wx.Button(panel, -1, "Check")
        self.check_button.Bind(wx.EVT_BUTTON, onCheck)
        self.cancel_button = wx.Button(panel, -1, "Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, onCancel)
        self.cancel_button.Disable()

        self.console_ctrl = wx.TextCtrl(
            panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        )
        self.console_ctrl.SetFont(
            wx.Font(
                (0, 13),
                wx.FONTFAMILY_TELETYPE,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
            )
        )
        self.console_ctrl.SetBackgroundColour(wx.BLACK)
        self.console_ctrl.SetForegroundColour(wx.WHITE)
        self.console_ctrl.SetDefaultStyle(wx.TextAttr(wx.WHITE))

        port_label = wx.StaticText(panel, label="Serial port")
        file_label = wx.StaticText(panel, label="Firmware")

        console_label = wx.StaticText(panel, label="Console")

        fgs.AddMany(
            [
                (wx.StaticText(panel, label="")),
                (wx.StaticText(panel, label=self.flasher.getVersion()),1,wx.EXPAND),
                (wx.StaticText(panel, label="")),
                (self.mode,1,wx.EXPAND),
                # Port selection row
                port_label,
                (serial_boxsizer, 1, wx.EXPAND),
                # Firmware selection row (growable)
                file_label,
                (self.file_picker, 1, wx.EXPAND),
                (wx.StaticText(panel, label="")),
                (self.firmwareInfo,1,wx.EXPAND),
                # Flash ESP button
                (wx.StaticText(panel, label="")),
                (self.button, 1, wx.EXPAND),
                # View Logs button
                (wx.StaticText(panel, label="")),
                (self.check_button, 1, wx.EXPAND),
                (wx.StaticText(panel, label="")),
                (self.cancel_button, 1, wx.EXPAND),
                # Console View (growable)
                (console_label, 1, wx.EXPAND),
                (self.console_ctrl, 1, wx.EXPAND),
            ]
        )
        fgs.AddGrowableRow(8, 1)
        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)
        panel.SetSizer(hbox)

    def _get_serial_ports(self):
        self.ports = []
        rt=[]
        for port,desc in list_serial_ports():
            self.ports.append(port)
            rt.append("%s[%s]"%(port,desc))
        if not self.ports:
            self.ports.append("")
            rt.append("")
        return rt

    # Menu methods
    def _on_exit_app(self, event):
        self.Close(True)

    def log_message(self, message):
        self.console_ctrl.AppendText(message)


class App(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    # pylint: disable=invalid-name
    def OnInit(self):
        title="esp32-nmea2000 flasher (based on esphome-flasher)"
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName(title)

        self.frame = MainFrame(None, title)
        self.frame.Show()

        return True




def main():
    app = App(False)
    app.MainLoop()
