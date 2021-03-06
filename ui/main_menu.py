import urwid

def menu_button(caption, callback):
    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')

def sub_menu(caption, choices):
    contents = menu(caption, choices)
    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button):
    response = urwid.Text([u'Menu: ', button.label, u'\n'])

    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))

def do_pembelian_barang():
    pass


def item_chosen_exit(button):
    response = urwid.Text([u'Exit or Quit Apps? ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    top.open_dialog_box(urwid.Filler(urwid.Pile([response, done])))

def exit_program(button):
    raise urwid.ExitMainLoop()

menu_top = menu(u'Main Menu', [
    sub_menu(u'Applications', [
        sub_menu(u'Transaksi', [
            menu_button(u'Pembelian DO', item_chosen),
            menu_button(u'Pembayaran', item_chosen),
        ]),
        sub_menu(u'Laporan Transaksi', [
            menu_button(u'Transaksi Masuk', item_chosen),
            menu_button(u'Transaksi Biaya', item_chosen),
        ]),

    ]),
    sub_menu(u'System', [
        sub_menu(u'Preferences', [
            menu_button(u'Inisialisasi', item_chosen),
        ]),
        menu_button(u'Lock Screen', item_chosen),
    ]),
    menu_button(u'Exit/Quit', item_chosen_exit),
])

class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u'0x167'))
        self.box_level = 0
#         self.fill_form_do(box)
        self.open_box(box)
#         self.open_dialog_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def open_dialog_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            align='center', width=('relative', 40),
            valign='middle', height=('relative', 40),
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

#     def fill_form_do(self, box):
#         self.original_widget = urwid.Overlay(urwid.LineBox(box),
#             align='center', width=('relative', 40),
#             valign='middle', height=('relative', 40),
#             min_width=24, min_height=8,
#             left=self.box_level * 3,
#             right=(self.max_box_levels - self.box_level - 1) * 3,
#             top=self.box_level * 2
#         self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)

top = CascadingBoxes(menu_top)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
