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

from gi.repository import Gtk, Gdk
from shortcircuit.core.transformer import TRANSFORMER_FN_MAP, transform_str

@Gtk.Template(resource_path='/in/bharatkalluri/shortcircuit/ui/transformer_search_entry.ui')
class TransformerSearchEntry(Gtk.SearchEntry):
    __gtype_name__ = 'transformer_search_entry'

    visible = False

    @staticmethod
    def get_transformer_store() -> Gtk.ListStore:
        transformer_store = Gtk.ListStore(str)
        for transformer in TRANSFORMER_FN_MAP.keys():
            transformer_store.append([transformer])
        return transformer_store

    def match_anywhere(
            self,
            completion: Gtk.EntryCompletion,
            string_entered: str,
            tree_iter: Gtk.TreeIter,
            _
    ):
        string_in_model = completion.get_model()[tree_iter][0]
        return string_entered in string_in_model.lower()

    def on_transformer_entry_changed(
            self,
            _: Gtk.EntryCompletion,
            list_store: Gtk.ListStore,
            tree_iter: Gtk.TreeIter
    ):
        if tree_iter is not None:
            transformer_title = list_store[tree_iter][0]
            ShortcircuitWindow.get_instance().apply_transformer(transformer=transformer_title)
            self.toggle_visibility()

    def toggle_visibility(self):
        self.set_text('')
        if self.visible:
            self.hide()
        else:
            self.show()
            self.grab_focus()
        self.visible = not self.visible

    def on_key_release(self, widget, ev):
        if ev.keyval == Gdk.KEY_Escape:
            self.toggle_visibility()

    def _set_completion(self):
        self.entry_completion = Gtk.EntryCompletion()
        self.entry_completion.set_model(self.transformer_store)
        self.entry_completion.connect("match-selected", self.on_transformer_entry_changed)
        self.entry_completion.set_text_column(0)
        self.entry_completion.set_minimum_key_length(0)
        self.entry_completion.set_match_func(self.match_anywhere, None)

        self.set_completion(self.entry_completion)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transformer_store = self.get_transformer_store()
        self._set_completion()

        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)

        self.connect("key-release-event", self.on_key_release)


    instance = None

    @staticmethod
    def get_instance():
        if TransformerSearchEntry.instance is None:
            TransformerSearchEntry.instance = TransformerSearchEntry()
        return TransformerSearchEntry.instance


@Gtk.Template(resource_path='/in/bharatkalluri/shortcircuit/ui/window.ui')
class ShortcircuitWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'shortcircuit_window'

    source_view_overlay: Gtk.Overlay = Gtk.Template.Child()
    source_view: Gtk.TextView = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transformer_search_entry: Gtk.SearchEntry = TransformerSearchEntry.get_instance()

        self.short_circuit_accelerators = Gtk.AccelGroup()
        self.source_view_overlay.add_overlay(self.transformer_search_entry)

        self.setup_accelerators()

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
        print("On Control T")
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

