# -*- coding: utf-8 -*-

# ba_meta require api 6


from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast
import shutil, sys
import _ba
import ba
import random
from bastd.ui.mainmenu import MainMenuWindow
from bastd.ui.watch import WatchWindow

sel_replay = None
oldWatch = WatchWindow._refresh_my_replays
s_clr = (0.55,0.5,0.6)
l_clr = (0.55,0.5,0.6)
def _new_watch(self):
    oldWatch(self)
    global sel_replay
    def lol():
        global sel_replay
        WatchWindow()._refresh_my_replays()
        sel_replay = self._my_replay_selected
        _saver()
    
    self._load = btn = ba.buttonwidget(

                  parent=self._root_widget,

                  position=(self._width * 0.5+145, self._height -125),
                  size=(150, 45),
                  label="Load",
                  color=l_clr,
                  textcolor=(0.75, 0.7, 0.8),
                  autoselect=True,
                  on_activate_call=_loader)

    self._save = btn = ba.buttonwidget(

                  parent=self._root_widget,

                  position=(self._width * 0.5+300, self._height -125),
                  size=(150, 45),
                  label="Save",
                  color=s_clr,
                  textcolor=(0.75, 0.7, 0.8),
                  autoselect=True,
                  on_activate_call=lol)
    self._discord = btn = ba.buttonwidget(

                  parent=self._root_widget,

                  position=(self._width * 0.5-295, self._height -125),
                  size=(150, 45),
                  label="Discord",
                  color=(0,0,1),
                  textcolor=(0.75, 0.7, 0.8),
                  autoselect=True,
                  on_activate_call=_dis)
    self._git = btn = ba.buttonwidget(

                  parent=self._root_widget,

                  position=(self._width * 0.5-450, self._height -125),
                  size=(150, 45),
                  label="GitHub",
                  color=(0,0,0),
                  textcolor=(0.75, 0.7, 0.8),
                  autoselect=True,
                  on_activate_call=_git)



def _dis():
    links = ["https://discord.gg/NKQeTQGcW8","https://discord.gg/UnPaNW7bzf","https://discord.gg/PNxKHhHVEZ"]
    _ba.open_url(random.choice(links))
def _git():
    _ba.open_url("https://github.com/Ayush-Deep")
def _saver():
    global s_clr
    pth=os.path.join(_ba.env()["python_directory_user"],"Replays" + os.sep)
    if not sel_replay is None:
        shutil.copyfile(_ba.get_replays_dir() + '/' +sel_replay,pth+"/"+sel_replay)
        _ba.screenmessage(f"Replay {sel_replay} Saved")
        s_clr = (0,1,0)
        WatchWindow()._refresh_my_replays()
        s_clr = (0.55,0.5,0.6)
    else:
        _ba.screenmessage("No Replay Selected")
        s_clr = (1,0,0)
        WatchWindow()._refresh_my_replays()
        s_clr = (0.55,0.5,0.6)
def _loader():
    global l_clr
    pth=os.path.join(_ba.env()["python_directory_user"],"Replays" + os.sep)
    new = []
    for p in os.listdir(_ba.get_replays_dir()):
        new.append(p.lower())
    if len(os.listdir(pth)) == 0:
        val = 0
        _ba.screenmessage("No Replay Found")
    else:
        try:
            files = []
            for file in os.listdir(pth):
                if file.endswith(".brp"):
                    files.append(file.lower())
            if files == []:
                _ba.screenmessage("No Replay Found")
                val = 0
            else:
                for fi in files:
                    if fi in new:
                        files.remove(fi)
            if files == []:
                val = 0
                _ba.screenmessage("Files Already Loaded")
            elif files != []:
                for fil in files:
                    if fil not in new:
                        shutil.copyfile(pth+"/"+fil,_ba.get_replays_dir() + '/' +fil)
                        val = 1
                    else:
                        _ba.screenmessage(f"Replay {fil} Already Exsist[Delete Old One]")
                        val = 0
        except:
            val = 0
    if val == 1:
        l_clr = (0,1,0)
        WatchWindow()._refresh_my_replays()
        l_clr = (0.55,0.5,0.6)
    elif val == 0:
        l_clr = (1,0,0)
        WatchWindow()._refresh_my_replays()
        l_clr = (0.55,0.5,0.6)
# ba_meta export plugin
class xD(ba.Plugin):

    def __init__(self):
        
        if _ba.env().get("build_number",0) >= 20124:
            WatchWindow._refresh_my_replays = _new_watch
    ph=os.path.join(_ba.env()["python_directory_user"],"Replays" + os.sep)
    if not os.path.isdir(ph):
        os.makedirs(ph)