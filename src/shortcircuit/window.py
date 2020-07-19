# window.py
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

from gi.repository import Gtk, Gdk, Gio
from shortcircuit.widgets.transformer_search_entry import TransformerSearchEntry, transform_str


@Gtk.Template(resource_path='/in/bharatkalluri/shortcircuit/ui/window.ui')
class ShortcircuitWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'shortcircuit_window'

    source_view_overlay: Gtk.Overlay = Gtk.Template.Child()
    source_view: Gtk.TextView = Gtk.Template.Child()
    primary_menu_button: Gtk.MenuButton = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transformer_search_entry: Gtk.SearchEntry = TransformerSearchEntry.get_instance()

        self.short_circuit_accelerators = Gtk.AccelGroup()
        self.source_view_overlay.add_overlay(self.transformer_search_entry)

        self.setup_accelerators()
        self.set_menu_items()

    def set_menu_items(self):
        menu: Gio.Menu = Gio.Menu()
        menu.append_item(Gio.MenuItem.new(_("About"), "app.about"))
        self.primary_menu_button.set_menu_model(menu)

    @staticmethod
    def _get_buffer_contents(buffer: Gtk.TextBuffer) -> str:
        start_iter: Gtk.TextIter = buffer.get_start_iter()
        end_iter: Gtk.TextIter = buffer.get_end_iter()
        buffer_contents = buffer.get_text(start_iter, end_iter, True)
        return buffer_contents


    def setup_accelerators(self):
        self.short_circuit_accelerators.connect(
            Gdk.keyval_from_name('T'),
            Gdk.ModifierType.CONTROL_MASK,
            0,
            self.on_ctrl_t,
        )
        self.add_accel_group(self.short_circuit_accelerators)

    def on_ctrl_t(
            self,
            _: Gtk.AccelGroup,
            __: 'ShortcircuitWindow',
            ___: int,
            ____: Gdk.ModifierType,
    ):
        self.transformer_search_entry.toggle_visibility()

    @staticmethod
    def on_transformer_exception(exception: Exception):
        dialog = Gtk.MessageDialog(
            parent=None,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format="Something went wrong!",
        )
        dialog.format_secondary_text(str(exception))
        dialog.run()
        dialog.destroy()

    def apply_transformer(self, transformer: str):
        buffer_contents = self._get_buffer_contents(self.source_view.get_buffer())
        try:
            transformed_buffer_contents = transform_str(buffer_contents, transformer)
            self.source_view.get_buffer().set_text(transformed_buffer_contents)
        except Exception as e:
            self.on_transformer_exception(e)

    instance = None

    @staticmethod
    def get_instance(**kwargs):
        if ShortcircuitWindow.instance is None:
            ShortcircuitWindow.instance = ShortcircuitWindow(**kwargs)
        return ShortcircuitWindow.instance

