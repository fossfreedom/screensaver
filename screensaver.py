# -*- coding: utf8 -*-
#
# Copyright (C) 2009 Jannik Heller <scrawl@baseoftrash.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 
 
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject, Peas
 
 
class ScreenSaver(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)
 
    def do_activate(self):
        shell = self.object
        self.player = shell.props.shell_player
        dbus_loop = DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus(mainloop=dbus_loop)
         
        self.active = 1
        self.was_playing = 0
        self.start_listen()
     
    def start_listen(self):
        # get screensaver interface
        screensaver_interface = self.session_bus.get_object(
        'org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
        # add signals
        screensaver_interface.connect_to_signal(
        "ActiveChanged", self.play_pause)
     
    def play_pause(self, arg):
        if self.active:
            if arg:
                # screensaver activated
                self.was_playing = self.player.get_playing()[1]
                self.player.pause()
            else:
                # only resume playback if rb was playing when
                # screensaver activated
                if self.was_playing:
                    self.player.play()
         
    def do_deactivate(self):
        self.active = 0
