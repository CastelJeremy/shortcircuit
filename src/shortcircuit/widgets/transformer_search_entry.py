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
            # TODO: Most probably a hack, try to remove this in the future
            from shortcircuit.window import ShortcircuitWindow
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
        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        css = b"""
        .transformer_dropdown {
            box-shadow: 0px 0px 50px -5px rgba(0,0,0,0.75);
        }
        """
        provider.load_from_data(css)

        self.connect("key-release-event", self.on_key_release)


    instance = None

    @staticmethod
    def get_instance():
        if TransformerSearchEntry.instance is None:
            TransformerSearchEntry.instance = TransformerSearchEntry()
        return TransformerSearchEntry.instance
