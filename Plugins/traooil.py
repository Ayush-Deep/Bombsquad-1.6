# -*- coding: utf-8 -*-

# ba_meta require api 6


from __future__ import annotations
from typing import TYPE_CHECKING
import ba,_ba
from bastd.game.elimination import Player
from bastd.actor import spaz
from bastd.actor import playerspaz
from bastd.ui.popup import PopupWindow
from bastd.ui.mainmenu import MainMenuWindow as MMW
from bastd.actor.playerspaz import *
from bastd.actor.popuptext import PopupText
import random
if TYPE_CHECKING:

    from typing import Any, Type, Optional, Tuple, List, Dict

tt = ba.TimeType.SIM
tf = ba.TimeFormat.MILLISECONDS
newConfig = {'defaultTrails':True,'emojiTrails':True,'custom':"HeHeBoi"
}
if "Trails" in ba.app.config:
    old_config = ba.app.config["Trails"]

    for setting in newConfig:

        if setting not in old_config:
            ba.app.config["Trails"] = newConfig
else:
    ba.app.config["Trails"] = newConfig
ba.app.config.apply_and_commit()
class TrailWindow(ba.Window):

    def __init__(self,
                 transition: Optional[str] = 'in_right'):

        uiscale = ba.app.ui.uiscale
        self._width = 1240 if uiscale is ba.UIScale.SMALL else 1040
        self._height = (578 if uiscale is ba.UIScale.SMALL else
                        670 if uiscale is ba.UIScale.MEDIUM else 800)
        extra_x = 100 if uiscale is ba.UIScale.SMALL else 0
        self.extra_x = extra_x

        super().__init__(root_widget=ba.containerwidget(
            size=(self._width, self._height),
            transition=transition,
            scale=(1.3 if uiscale is ba.UIScale.SMALL else
                   0.97 if uiscale is ba.UIScale.MEDIUM else 0.8)))
        ba.textwidget(parent=self._root_widget,

                      position=((self._width-0.4*extra_x)*0.25,

                                self._height*0.4-extra_x*0.221),
                      size=(0, 0),
                      color=(0, 1.0, 0.0),
                      scale=1.3,
                      h_align='center',
                      v_align='center',
                      text='Custom Trails:-',
                      maxwidth=350)
        ba.textwidget(parent=self._root_widget,

                      position=((self._width-0.4*extra_x)*0.5,

                                (self._height*0.4-extra_x*0.321)*0.5),
                      size=(0, 0),
                      color=(0, 1.0, 0.0),
                      scale=1.5,
                      h_align='center',
                      v_align='center',
                      text=':- Made By Blitz |Bs Revolution |GitHub/Ayush-Deep',
                      maxwidth=700)
        self._text = ba.textwidget(parent=self._root_widget, position=(self._width*0.05+extra_x*4,self._height*0.4-extra_x*0.6),color=(1,1,1),editable=True,max_chars= 7,description="Custom Trails",scale=0.9, size=(600, 60),maxwidth=800, max_height=80, h_align='center',v_align='center', text=ba.app.config["Trails"]["custom"])
        self.default = ba.checkboxwidget(parent=self._root_widget,position=(self._width*0.05+extra_x*4,self._height*0.8-extra_x*0.6),scale = 1.5,value=ba.app.config["Trails"]["defaultTrails"],maxwidth=200,text= "defaultTrails",on_value_change_call=ba.Call(self._set_setting,"defaultTrails"),autoselect=True)
        self.emoji = ba.checkboxwidget(parent=self._root_widget,position=(self._width*0.05+extra_x*4,self._height*0.6-extra_x*0.6),scale = 1.5,value=ba.app.config["Trails"]["emojiTrails"],maxwidth=200,text= "emojiTrails",on_value_change_call=ba.Call(self._set_setting,"emojiTrails"),autoselect=True)

        self._back_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(70 + extra_x,
                      self._height - 74 - extra_x*0.2),
            size=(60, 60),
            scale=1.1,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            on_activate_call=self._back)
        ba.containerwidget(edit=self._root_widget, cancel_button=btn)

        ba.textwidget(parent=self._root_widget,
                      position=(self._width * 0.5,
                                self._height - 38 - extra_x*0.2),
                      size=(0, 0),
                      color=(0,1,0),
                      scale=1.5,
                      h_align='center',
                      v_align='center',
                      text='Trail Settings',
                      maxwidth=400)
    def _set_setting(self,setting,m):

        ba.app.config["Trails"][setting] = False if m==0 else True

        ba.app.config.apply_and_commit()
    def _save(self):
        self._name = ba.textwidget(query=self._text) 

        ba.app.config["Trails"]["custom"] = self._name
        ba.app.config.apply_and_commit()
    def _back(self) -> None:
        self._save()

        from bastd.ui.mainmenu import MainMenuWindow

        ba.containerwidget(edit=self._root_widget,
                           transition='out_scale')
        ba.app.ui.set_main_menu_window(
            MainMenuWindow(transition='in_left').get_root_widget())

name_button = 'Trails'
image_button = 'chestIcon'

def doTrailButton(self):
    ba.containerwidget(edit=self._root_widget,transition='out_left')
    TrailWindow()

# ba_meta export plugin
class byBlitz(ba.Plugin):
    
    MMW._old_refresh = MMW._refresh

    def _new_refresh(self) -> None:

        self._old_refresh()
        if not self._in_game:
            uiscale = ba.app.ui.uiscale
            extra_y = 100 if uiscale is ba.UIScale.SMALL else 0
            this_b_width = self._button_width * 0.25 * 1.7
            this_b_height = self._button_height * 0.82 * 1.7
            self._Trail_button = tb = ba.buttonwidget(
                parent=self._root_widget,
                position=(-130, -77 + extra_y*0.55),
                size=(this_b_width, this_b_height),
                autoselect=self._use_autoselect,
                button_type='square',
                label='',
                transition_delay=self._tdelay,
                on_activate_call=ba.Call(doTrailButton,self))
            ba.textwidget(parent=self._root_widget,
                          position=(-89, -59 + extra_y*0.55),
                          size=(0, 0),
                          scale=0.75,
                          transition_delay=self._tdelay,
                          draw_controller=tb,
                          color=(0.75, 1.0, 0.7),
                          maxwidth=self._button_width * 0.33,
                          text=name_button,
                          h_align='center',
                          v_align='center')
            icon_size = this_b_width * 0.6
            ba.imagewidget(parent=self._root_widget,
                           size=(icon_size, icon_size),
                           draw_controller=tb,
                           transition_delay=self._tdelay,
                           position=(-112, -53.5 + extra_y*0.55),
                           texture=ba.gettexture(image_button))
    MMW._refresh = _new_refresh
    
    PlayerSpaz.oldInit = PlayerSpaz.__init__
    def newInit(self,player: ba.Player,

                 color: Sequence[float] = (1.0, 1.0, 1.0),
                 highlight: Sequence[float] = (0.5, 0.5, 0.5),
                 character: str = 'Spaz',
                 powerups_expire: bool = True):
        self.oldInit(player,color,highlight,character,powerups_expire)
        def txt():
            trs = []
            if ba.app.config["Trails"]["defaultTrails"]:
                for i in ["π","¶","×","@","#"]:
                    trs.append(i)
            if ba.app.config["Trails"]["emojiTrails"]:
                for i in [u"\ue00c","💀","❤️","❌","😡","✨","⭐","⚡","🔥","💢"]:
                    trs.append(i)
            else:
                p = ba.app.config["Trails"]["custom"]
                trs.append(p)
            t = random.choice(trs)
            if self.is_alive():
                PopupText(t,scale=1.25,color=(1,0,0),position=(self.node.position[0],self.node.position[1]-1.5,self.node.position[2])).autoretain()
        self._timer = ba.Timer(200, txt,timeformat=tf,repeat = True)

    PlayerSpaz.__init__ = newInit
