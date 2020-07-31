# main.py
#
# Copyright 2020 Bharat Kalluri
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk, GLib, Gio, Gdk, GObject

from .window import ShortcircuitWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='in.bharatkalluri.shortcircuit',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.setup_actions()

    def _add_action(self, key, callback, prop=None):
        action = Gio.SimpleAction.new(key, None)
        action.connect("activate", callback)
        if prop:
            self.bind_property(prop, action, "enabled", GObject.BindingFlags.INVERT_BOOLEAN)
        self.add_action(action)
        return action

    def setup_actions(self):
        self._add_action("about", self._on_about)


    def _on_about(a,b,c):
        builder = Gtk.Builder()
        builder.add_from_resource("/in/bharatkalluri/shortcircuit/ui/about_dialog.ui")
        dialog = builder.get_object("about_dialog")
        dialog.set_transient_for(ShortcircuitWindow.get_instance())
        dialog.run()
        dialog.destroy()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ShortcircuitWindow.get_instance(application=self)
        win.present()


def main(version):
    app = Application()
    return app.run(sys.argv)
