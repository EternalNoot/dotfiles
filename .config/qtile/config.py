#        _______ __        __________  _   __________________
#  ____ /_  __(_) /__     / ____/ __ \/ | / / ____/  _/ ____/
# / __ `// / / / / _ \   / /   / / / /  |/ / /_   / // / __  
#/ /_/ // / / / /  __/  / /___/ /_/ / /|  / __/ _/ // /_/ /  
#\__, //_/ /_/_/\___/   \____/\____/_/ |_/_/   /___/\____/   
#  /_/                                                       
#                   ###ETERNALNOOT###


# IMPORTS

import os
import subprocess
import re
import socket

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

# VARS

mod = "mod4"
terminal = "kitty"
browser = "firefox"
fBrowser = terminal+" -e ranger"
tEditor = "vscodium"

# KEYSTROKES 

keys = [
    # Window movement keys Keys
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()),

    #Spawn Applications
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "space", lazy.spawn("dmenu_run -c -l 20")),
    Key([mod, "mod1"], "f", lazy.spawn(browser)),
    Key([mod, "mod1"], "v", lazy.spawn(tEditor)),
    Key([mod, "mod1"], "e", lazy.spawn(fBrowser)),
    Key([mod, "mod1"], "e", lazy.spawn(terminal )),
    Key([mod, "mod1"], "m", lazy.spawn("./.config/qtile/wallpaper.sh")),
    Key([mod, "mod1"], "n", lazy.spawn("networkmanager_dmenu -c -l 20")),
    Key([mod, "mod1"], "i", lazy.spawn(terminal+" -e nvim")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    # System controls
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),

    # backlight control
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

    # audio control
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 -q set Master 1dB+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 -q set Master 1dB-")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle")),
    Key([], "XF86AudioMicMute", lazy.spawn("amixer -c 0 -q set Capture toggle")),
]

# GROUPS

groups = [
    Group(
        "a",
        label="WWW",
        layout = "max",
        ),
    Group(
        "s",
        label="DEV",
        layout = "monadtall"
        ),
    Group(
        "d",
        label="SYS",
        layout = "monadtall"
        ),
    Group(
        "f",
        label="MUS",
        layout = "monadtall"
        ),
]

# CHANGE GROUPS

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

# LAYOUTS

layouts = [
    layout.MonadTall(
        border_focus = "ffffff",
        border_normal = "466bb0",
        border_width = 2,
        margin = 6,
    ),
    layout.Max()
]

# WIDGET DEFAULTS

widget_defaults = dict(
    font='hack',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# SCREEN WIDGETS AND BAR

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method = 'line',
                    highlight_color = ['000000', '000000'],
                    this_current_screen_border = '466bb0',
                ),
                widget.Image(
                    filename = "~/.config/qtile/whiteOnBlack.png",
                ),
                widget.currentlayout.CurrentLayout(
                    background = 'FFFFFF',
                    foreground = '000000',
                ),
                widget.Image(
                    filename = "~/.config/qtile/blackOnWhite.png",
                ),
                widget.WindowName(),
                widget.Image(
                    filename = "~/.config/qtile/whiteOnBlack.png",
                ),
                widget.Cmus(
                    max_chars = 40,
                    update_interval = 0.5,
                    background = 'FFFFFF',
                    play_color = '000000',
                    noplay_color = 'CECECE',
                ),
                widget.Image(
                    filename = "~/.config/qtile/blackOnWhite.png",
                ),
                widget.CPU(
                    format = "{load_percent}%",
                ),
                widget.Sep(),
                widget.ThermalSensor(
                    tag_sensor = 'Core 0',
                ),
                widget.Sep(),
                widget.Memory(
                    format = "{MemUsed}M",
                    update_interval = 2.0,
                ),
                widget.Sep(),
                widget.Net(
                    interface = "wlp4s0",
                    format = '{down} ↓↑ {up}',
                ),
                widget.Sep(),
                widget.CheckUpdates(
                    execute = terminal+" -e sudo pacman -Syu",
                    display_format = "{updates} 🛈",
                    update_interval = 60,
                ),
                widget.Sep(
                    padding = 5
                ),
                widget.Volume(),
                widget.TextBox(
                    text = "🕪"
                ),
                widget.Image(
                    filename = "~/.config/qtile/whiteOnBlack.png",
                ),
                widget.Battery(
                    battery = 'BAT0',
                    charge_char = '🡅',
                    discharge_char = '🡇',
                    unknown_char = '🡆',
                    full_char = '🗲',
                    empty_char = '🕱',
                    fontsize = 14,
                    padding = 5,
                    format = '{percent:2.0%} {char}',
                    update_interval = 30,
                    background = 'FFFFFF',
                    foreground = '000000',
                ),
                widget.Sep(
                    background = 'FFFFFF',
                    foreground = '000000',
                ),
                widget.Battery(
                    battery = 'BAT1',
                    charge_char = '🡅',
                    discharge_char = '🡇',
                    unknown_char = '🡄',
                    full_char = '🗲',
                    empty_char = '🕱',
                    fontsize = 14,
                    padding = 5,
                    format = '{percent:2.0%} {char}',
                    update_interval = 30,
                    background = 'FFFFFF',
                    foreground = '000000',
                ),
                widget.Image(
                    filename = "~/.config/qtile/blackOnWhite.png",
                ),
                widget.Clock(
                    padding = 3,
                    fontsize = 16,
                    format='%a %H:%M'
                ),
            ],
            26,
        ),
    ),
]

# FLOATING LAYOUT

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# ON STARTUP
@hook.subscribe.startup_once
def autostart():
    autostart = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([autostart])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
