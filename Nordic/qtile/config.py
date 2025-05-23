#Imports    
from libqtile import bar, layout, widget, hook
from libqtile import config
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration
import subprocess, os



#Autostart
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.run([home])



#Colorscheme
nord = {
    "bg": "#242831",
    "bg_light": "#2e3440", 
    "fg": "#4c566a",
    "blue": "#81a1c1",
    "red": "#bf616a",
    "white": "#e5e9f0",
    "green": "#a3be8c",
    "orange": "#d08770",
    "yellow": "#dbbc7f",
    "aqua": "#8fbcbb",
    "purple": "#b48ead"
        }
colors = nord



#Keybinds
mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "g", lazy.window.toggle_fullscreen()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),
    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    # Toggle between split and unsplit sides of stack.
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    #Launch Apps
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "c", lazy.spawn("google-chrome-stable"), desc="Launch Chrome"),
    Key([mod], "f", lazy.spawn("thunar"), desc="Launch Thunar"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    #Sound keys
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -D pipewire sset Master 5%-"), desc="lower volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -D pipewire sset Master 5%+"), desc="raise volume"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pipewire sset Master toggle"), desc="mute"),
    #Screenshotting
    Key([mod], "s", lazy.spawn(os.path.expanduser("~/.config/qtile/scripts/screenshot.sh"))),
    Key([mod, "shift"], "s", lazy.spawn(os.path.expanduser("~/.config/qtile/scripts/selectshot.sh"))),
    #Rofi
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Rofi"),
]



#Workspaces
groups = [Group("1", label=""),
          Group("2", label=""),
          Group("3", label=""),
          Group("4", label=""),
          Group("5", label=""),
          Group("6", label=""),
          Group("7", label=""),
          Group("8", label="")
          ]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            Key(
                [mod, "control"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )



#ScratchPads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "Internet",
                "alacritty -e impala",
                width=0.29,
                height=0.55,
                x=0.6155,
                y=0.010,
                opacity=1,
                border_focus="#242831",
                border_width=10,
                on_focus_lost_hide=True
            ),

            DropDown(
                "Bluetooth",
                "alacritty -e bluetui",
                width=0.29,
                height=0.45,
                x=0.6155,
                y=0.010,
                opacity=1,
                on_focus_lost_hide=True
            ),

            DropDown(
                "taskVeiwer",
                "alacritty -e bpytop",
                width=0.3865,
                height=0.95,
                x=0.595,
                y=0.010,
                opacity=1,
                on_focus_lost_hide=True
            ),
        ]
    )
)



#Tiling Layouts
layouts = [
    layout.Bsp(border_focus=colors["bg_light"], border_normal=colors["bg"], border_width=2, margin=10),
    layout.Max(border_focus=colors["bg_light"], border_normal=colors["bg"], border_width=2, margin=10),
    layout.MonadTall(border_focus=colors["bg_light"], border_normal=colors["bg"], border_width=2, margin=10), 
    layout.Columns(border_focus=colors["bg_light"], border_normal=colors["bg"], border_focus_stack=colors["red"], border_normal_stack=colors["bg"], order_width=2, margin=10),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors["bg_light"], 
    border_normal=colors["bg"], 
    border_width=3, 
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)



#Qtile Bar(s)
widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=14,
    padding=10,
)
extension_defaults = widget_defaults.copy()

decoration_group = {
    "decorations": [
        RectDecoration(colour=colors["bg"], radius=6, filled=True, padding_y=5, group=True, clip=True)
    ],
     "padding": 10,
}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(10),
                widget.TextBox(
                    "",
                    foreground = colors["blue"],
                    fontsize = "18",
                    mouse_callbacks = {"Button1": lazy.spawn("rofi -show drun -location 1 -xoffset 10 -yoffset 42")}
                    ),
                widget.Spacer(10),
                widget.GroupBox(
                    **decoration_group,
                    highlight_method="text",
                    visible_groups=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
                    this_current_screen_border = colors["blue"],
                    active = colors["white"],
                    inactive = colors["fg"]
                    ),
                widget.Spacer(10),
                widget.CurrentLayoutIcon(
                    **decoration_group,
                    custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                    scale = 0.5
                    ),
                widget.Spacer(475),
                widget.Clock(
                    # **decoration_group,
                    format = " %a, %b %d  󰥔 %H:%M",
                    foreground = colors["aqua"]
                    ),
                widget.Spacer(),
                widget.Systray(
                    ),
                widget.Spacer(10),
                widget.TextBox(
                    **decoration_group,
                    foreground = colors["green"],
                    text = " 󰣀",
                    mouse_callbacks = {"Button1": lazy.spawn("alacritty -e ssh -p 22 arie@157.131.35.113")}
                    ),
                widget.Spacer(10),
                widget.Mpris2(
                    **decoration_group,
                    foreground = colors["blue"],
                    paused_text = "",
                    playing_text = "",
                    ),
                widget.TextBox(
                    **decoration_group,
                    text = "󰂯",
                    foreground = colors["blue"],
                    mouse_callbacks = {"Button1": lazy.group["scratchpad"].dropdown_toggle("Bluetooth")}
                    ),
                widget.IWD(
                    **decoration_group,
                    active_colour = colors["blue"],
                    inactive_colour = colors["fg"],
                    show_image=True,
                    show_text=False,
                    wifi_shape="rectangle",
                    wifi_rectangle_width=8,
                    foreground = colors["blue"],
                    mouse_callbacks = {"Button1": lazy.group["scratchpad"].dropdown_toggle("Internet")}
                    ),
                widget.Volume(
                    **decoration_group,
                    foreground = colors["blue"],
                    fmt=" {}"
                    ),
                widget.Spacer(10),
                widget.CPU(
                    **decoration_group,
                    foreground = colors["yellow"],
                    format = "󰻠 {load_percent}%",
                    mouse_callbacks = {"Button1": lazy.group["scratchpad"].dropdown_toggle("taskVeiwer")}
                    ),
                widget.Memory(
                    **decoration_group,
                    foreground = colors["yellow"],
                    measure_mem="G",
                    format = "  {MemUsed: .0f}G",
                    mouse_callbacks = {"Button1": lazy.group["scratchpad"].dropdown_toggle("taskVeiwer")}
                    ),
                widget.Spacer(1),
                widget.TextBox(
                    "⏼",
                    fontsize = "18",
                    foreground = colors["blue"],
                    mouse_callbacks = {"Button1": lazy.spawn("poweroff"), "Button3": lazy.spawn("reboot")}
                    ),
                widget.Spacer(15)

            ],
            32,
            background=colors["bg_light"],
            margin = [0, -8, 0, -8]
        ),
    ),
]



#Other settings
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False #Respecting apps auto minimizing on lost focus
wl_input_rules = None #When using the Wayland backend, this can be used to configure input devices.
wmname = "LG3D" #To trick java UI toolkits
