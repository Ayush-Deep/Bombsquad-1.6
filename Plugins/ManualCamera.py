# -*- coding: utf-8 -*-
# ba_meta require api 6

"""
Made By Its Blitz Check GitHub/Ayush-Deep

How It Works


1.Go To Playlist Create A New Game
(You Will See Manual Camera Game)

Text Position Taken From Mr.Smoothy Mods #Credits
2.Use (Punch,Jump,Bomb,Pick) To Change Camera Positions
3.Once You Have Idea About It You Can Change Camera Position Of Any Map .....

Not As Good As Manual Camera In Computer But Yeah, Its Way Cool Though

Useful Commands

/dark -> Use Dark Mode In Any Mode
/log -> Turn Off/On Chat Message When You Are In (Manual Camera)
/save (name) -> Save A Camera Position
/load (name) -> Load A Camera Position
/run -> Run A Loaded Camera Position
/cM -> Change Camera Mode
/inc (val) -> Increse/Decrese Value Increment(You Will Know What It Means)
(val) Must Be Integer/Decimal

Also Join Discord
Star GitHub Or Fork It To Get Latest Updates
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import _ba
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.scoreboard import Scoreboard

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Tuple, Union, Sequence, Optional
import os, json

class Player(ba.Player['Team']):
    """Our player type for this game."""


class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0
new_dict = {}
save_dict = {}
set_dict = {"Right":0,"Up-Down":0,"Back-Forth":0,"Left":0,"Focus(Up-Down)":0,"Focus(Back-Forth)":0}
log = True
inc = 1
# ba_meta export game
class CameraPos(ba.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = 'Manual Camera'
    description = 'Adjust The Camera'
    # Print messages when players die since it matters here.
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: Type[ba.Session]) -> List[ba.Setting]:
        settings = [
            ba.IntSetting(
                'Kills to Win Per Player',
                min_value=1,
                default=5,
                increment=1,
            ),
            ba.IntChoiceSetting(
                'Time Limit',
                choices=[
                    ('None', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('5 Minutes', 300),
                    ('10 Minutes', 600),
                    ('20 Minutes', 1200),
                ],
                default=0,
            ),
            ba.FloatChoiceSetting(
                'Respawn Times',
                choices=[
                    ('Shorter', 0.25),
                    ('Short', 0.5),
                    ('Normal', 1.0),
                    ('Long', 2.0),
                    ('Longer', 4.0),
                ],
                default=1.0,
            ),
            ba.BoolSetting('Epic Mode', default=False),
        ]

        # In teams mode, a suicide gives a point to the other team, but in
        # free-for-all it subtracts from your own score. By default we clamp
        # this at zero to benefit new players, but pro players might like to
        # be able to go negative. (to avoid a strategy of just
        # suiciding until you get a good drop)
        if issubclass(sessiontype, ba.FreeForAllSession):
            settings.append(
                ba.BoolSetting('Allow Negative Scores', default=False))

        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        return ['Bridgit', 'Courtyard', 'Crag Castle', 'Doom Shroom','Monkey Face', 'Rampage', 'Roundabout', 'Step Right Up', 'The Pad', 'Zigzag']

    def __init__(self, settings: dict):
        super().__init__(settings)
        _ba.set_party_icon_always_visible(True)
        self._score_to_win: Optional[int] = None
        self._dingsound = ba.getsound('dingSmall')
        self._epic_mode = bool(settings['Epic Mode'])
        self._kills_to_win_per_player = int(
            settings['Kills to Win Per Player'])
        self._time_limit = float(settings['Time Limit'])
        self._allow_negative_scores = bool(
            settings.get('Allow Negative Scores', False))
        self.set_index = 0
        self.set_dict = set_dict
        self._val = 0
        self._setting= ba.newnode(
                        'text',
                        attrs={
                            'text': "<Choose Settings>",
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 0, 1),
                            'h_align': 'center',
                            'position': (-4,6,-4)
                        })
        self._value = ba.newnode(
                        'text',
                        attrs={
                            'text': "<Choose Values>",
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 0, 1),
                            'h_align': 'center',
                            'position': (6,6,-4)
                        })

        # Base class overrides.
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.EPIC if self._epic_mode else
                              ba.MusicType.TO_THE_DEATH)

    def get_instance_description(self) -> Union[str, Sequence]:
        return 'Manual Camera By Blitz'

    def get_instance_description_short(self) -> Union[str, Sequence]:
        return 'Manual Camera Setup'

    def on_team_join(self, team: Team) -> None:
        if self.has_begun():
            pass
    def on_begin(self) -> None:
        super().on_begin()
        global save_dict
        self.set_dict = {"Right":0,"Up-Down":0,"Back-Forth":0,"Left":0,"Focus(Up-Down)":0,"Focus(Back-Forth)":0}
        save_dict = {}
    def chatMsg(self,sett,val,icre):
        if log:
            _ba.chatmessage(f"Settings : {sett}, Value : {val}, Increment : {icre}")
    def nextSetting(self):
        if self.set_index < len(self.set_dict)-1:
            self.set_index +=1
        setng = list(self.set_dict.keys())[self.set_index]
        self._val = self.set_dict[setng]
        self.setng = setng
        self._setting.delete()
        self._setting=ba.newnode(
                        'text',
                        attrs={
                            'text': self.setng,
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 1, 1),
                            'h_align': 'center',
                            'position': (-4,6,-4)
                        })
        self._value.delete()
        self._value=ba.newnode(
                        'text',
                        attrs={
                            'text': str(self._val),
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 1, 1),
                            'h_align': 'center',
                            'position': (6,6,-4)
                        })
        self.chatMsg(self.setng,self._val,inc)
    def prevSetting(self):
        if self.set_index > 0:
            self.set_index -=1
        setng = list(self.set_dict.keys())[self.set_index]
        self._val = self.set_dict[setng]
        self.setng = setng
        self._setting.delete()
        self._setting=ba.newnode(
                        'text',
                        attrs={
                            'text': self.setng,
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 1, 1),
                            'h_align': 'center',
                            'position': (-4,6,-4)
                        })
        self._value.delete()
        self._value=ba.newnode(
                        'text',
                        attrs={
                            'text': str(self._val),
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 1, 1),
                            'h_align': 'center',
                            'position': (6,6,-4)
                        })
        self.chatMsg(self.setng,self._val,inc)
    def nextValue(self):
        global save_dict
        setng = list(self.set_dict.keys())[self.set_index]
        self.setng = setng
        val = self.set_dict[setng]
        self._val = round(val+inc,1)
        self.set_dict[setng] = self._val
        self._value.delete()
        self._value=ba.newnode(
                        'text',
                        attrs={
                            'text': str(self._val),
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 1, 1),
                            'h_align': 'center',
                            'position': (6,6,-4)
                        })
        save_dict = self.set_dict
        self.chatMsg(self.setng,self._val,inc)
        self.applyer()
    def prevValue(self):
        global save_dict
        setng = list(self.set_dict.keys())[self.set_index]
        self.setng = setng
        val = self.set_dict[setng]
        self._val = round(val-inc,1)
        self.set_dict[setng] = self._val
        self._value.delete()
        self._value=ba.newnode(
                        'text',
                        attrs={
                            'text': str(self._val),
                            'in_world': True,
                            'scale': 0.02,
                            'color': (1, 1, 1, 1),
                            'h_align': 'center',
                            'position': (6,6,-4)
                        })
        save_dict = self.set_dict
        self.chatMsg(self.setng,self._val,inc)
        self.applyer()
    def applyer(self):
        gnodee = _ba.getactivity().globalsnode
        gnodee.area_of_interest_bounds = (self.set_dict["Right"],self.set_dict["Up-Down"],self.set_dict["Back-Forth"],self.set_dict["Left"],self.set_dict["Focus(Up-Down)"],self.set_dict["Focus(Back-Forth)"])
    def spawn_player(self, player: Player) -> ba.Actor:
        
        spaz = self.spawn_player_spaz(player)

        # Let's reconnect this player's controls to this
        # spaz but *without* the ability to attack or pick stuff up.
        spaz.connect_controls_to_player(enable_punch=False,
                                        enable_jump=False,
                                        enable_bomb=False,
                                        enable_pickup=False)
        intp = ba.InputType
        player.assigninput(intp.JUMP_PRESS, self.prevSetting)
        player.assigninput(intp.PICK_UP_PRESS, self.nextSetting)
        player.assigninput(intp.PUNCH_PRESS, self.prevValue)
        player.assigninput(intp.BOMB_PRESS, self.nextValue)
        # Also lets have them make some noise when they die.
        spaz.play_big_death_sound = True
        return spaz

    def handlemessage(self, msg: Any) -> Any:

        if isinstance(msg, ba.PlayerDiedMessage):

            # Augment standard behavior.
            super().handlemessage(msg)

            player = msg.getplayer(Player)
            self.respawn_player(player)

        else:
            return super().handlemessage(msg)
        return None

    def _update_scoreboard(self) -> None:
        for team in self.teams:
            self._scoreboard.set_team_value(team, team.score,
                                            self._score_to_win)

    def end_game(self) -> None:
        global save_dict
        self.set_dict = {"Right":0,"Up-Down":0,"Back-Forth":0,"Left":0,"Focus(Up-Down)":0,"Focus(Back-Forth)":0}
        save_dict = {}
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)

def _save(name):
    global save_dict
    new = {name:list(save_dict.values())}
    path=os.path.join(_ba.env()["python_directory_user"],"ManualCamera" + os.sep)
    if not os.path.isdir(path):
        os.makedirs(path)
    if _ba.get_foreground_host_activity()!=None and len(save_dict) == 6:
        file = open(path+name+".json","w")
        file.write(json.dumps(new))
        file.close()
        _ba.screenmessage(f"Camera {name} Saved")
    else:
        _ba.screenmessage("Not Saved")

def _load(name):
    path=os.path.join(_ba.env()["python_directory_user"],"ManualCamera" + os.sep)
    file = open(path+name+".json","r")
    fl = json.loads(file.read())
    if name in fl:
        mapCamera = fl[name]
        new_dict["Right"] = mapCamera[0]
        new_dict["Up-Down"] = mapCamera[1]
        new_dict["Back-Forth"] = mapCamera[2]
        new_dict["Left"] = mapCamera[3]
        new_dict["Focus(Up-Down)"] = mapCamera[4]
        new_dict["Focus(Back-Forth)"] = mapCamera[5]
        _ba.screenmessage(f"Loaded {name}")
    else:
        _ba.screenmessage("Enter Correct Camera Name")

def _applyer():
    activity = _ba.get_foreground_host_activity()
    gnode = activity.globalsnode
    gnode.area_of_interest_bounds = (new_dict["Right"],new_dict["Up-Down"],new_dict["Back-Forth"],new_dict["Left"],new_dict["Focus(Up-Down)"],new_dict["Focus(Back-Forth)"])

def _camera():
    activity = _ba.get_foreground_host_activity()
    gl = activity.globalsnode
    if gl.camera_mode == "follow":
        gl.camera_mode = "rotate"
    else:
        gl.camera_mode = "follow"

def _dark():
    activity = _ba.get_foreground_host_activity()
    gl = activity.globalsnode
    gl.tint = (0.5,0.7,1)
def _log():
    global log
    if log:
        log = False
    else:
        log = True
def _inc(val):
    global inc
    try:
        if float(val) > 0.0 and float(val) <= 2.0:
            inc = float(val[0:3])
            _ba.screenmessage(f"Increment Changed To {inc}")
        else:
            _ba.screenmessage("Increment Should Be Less Than 2 And Greater Than 0")
    except:
        _ba.screenmessage("Must Be A Integer/Decimal")
cm=_ba.chatmessage

def _new_chatmessage(msg):
    if msg.split(" ")[0]=="/save":
        if len(msg.split(" "))>1:
            _save(msg.split(" ")[1].lower())
        else:
            _ba.screenmessage("Enter Camera Name")
    elif msg.split(" ")[0]=="/load":
        if len(msg.split(" "))>1:
            try:
                _load(msg.split(" ")[1].lower())
            except:
                _ba.screenmessage("Camera Not Found")
        else:
            _ba.screenmessage("Enter Camera Name")
    elif msg == "/cameraMode" or msg == "/cM":
        _camera()
    elif msg == "/dark":
        _dark()
    elif msg == "/run":
        _applyer()
    elif msg == "/log":
        _log()
    elif msg.split(" ")[0] == "/inc":
        if len(msg.split(" ")) > 1:
            _inc(msg.split(" ")[1])
    else:
        cm(msg)
_ba.chatmessage=_new_chatmessage

# ba_meta export plugin
class xD(ba.Plugin):
    def __init__(self):
        _ba.set_party_icon_always_visible(True)