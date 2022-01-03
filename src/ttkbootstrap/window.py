"""
    This module contains a class of the same name that wraps the 
    tkinter.Tk and ttkbootstrap.style.Style classes to provide a more
    consolidated api for initial application startup.
"""
import tkinter
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from ttkbootstrap.icons import Icon
from ttkbootstrap import utility


class Window(tkinter.Tk):
    """A class that wraps the tkinter.Tk class in order to provide a
    more convenient api with additional bells and whistles. For more
    information on how to use the inherited `Tk` methods, see the
    [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Tk).

    ![](../../assets/window/window-toplevel.png)

    Examples:

        ```python
        app = Window(title="My Application", themename="superhero")
        app.mainloop()
        ```
    """

    def __init__(
        self,
        title="ttkbootstrap",
        themename="litera",
        iconphoto=None,
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        hdpi=True,
        scaling=None,
        transient=None,
        overrideredirect=False,
        alpha=1.0,
    ):
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            themename (str):
                The name of the ttkbootstrap theme to apply to the
                application.

            iconphoto (PhotoImage):
                The titlebar icon. This image is applied to all future
                toplevels as well.

            size (Tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Window.geometry` method.

            position (Tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Window.geometry`
                method.

            minsize (Tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.minsize` method.

            maxsize (Tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.maxsize` method.

            resizable (Tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Window.resizable` method.

            hdpi (bool):
                Enable high-dpi support for Windows OS. This option is
                enabled by default.

            scaling (float):
                Sets the current scaling factor used by Tk to convert
                between physical units (for example, points, inches, or
                millimeters) and pixels. The number argument is a
                floating point number that specifies the number of pixels
                per point on window's display.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Window.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is passed to the
                `Window.overrideredirect(1)` method.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.
        """
        if hdpi:
            utility.enable_high_dpi_awareness()

        super().__init__()
        winsys = self.tk.call('tk', 'windowingsystem')

        if scaling is not None:
            utility.enable_high_dpi_awareness(self, scaling)

        try:
            self._icon = iconphoto or tkinter.PhotoImage(data=Icon.icon)
            self.iconphoto(True, self._icon)
        except tkinter.TclError:
            # icon photo has already been applied in previous window creation
            pass

        self.title(title)

        if size is not None:
            width, height = size
            self.geometry(f"{width}x{height}")
        
        if position is not None:
            xpos, ypos = position
            self.geometry(f"+{xpos}+{ypos}")
        
        if minsize is not None:
            width, height = minsize
            self.minsize(width, height)
        
        if maxsize is not None:
            width, height = maxsize
            self.maxsize(width, height)
        
        if resizable is not None:
            width, height = resizable
            self.resizable(width, height)
        
        if transient is not None:
            self.transient(transient)
        
        if overrideredirect:
            self.overrideredirect(1)
        
        if alpha is not None:
            if winsys == 'x11':
                self.wait_visibility(self)
            self.attributes("-alpha", alpha)

        self._apply_entry_type_class_binding()
        self._style = Style(themename)


    @property
    def style(self):
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return self._style

    def place_window_center(self):
        """Position the toplevel in the center of the screen. Does not
        account for titlebar height."""
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')

    position_center = place_window_center # alias

    def _apply_entry_type_class_binding(self):
        self.bind_class(
            className="TEntry", 
            sequence="<Configure>", 
            func=self._disabled_state_cursor,
            add="+"
        )
        self.bind_class(
            className="TSpinbox", 
            sequence="<Configure>", 
            func=self._disabled_state_cursor,
            add="+"
        )
        self.bind_class(
            className="TCombobox", 
            sequence="<Configure>", 
            func=self._disabled_state_cursor,
            add="+"
        )

    def _disabled_state_cursor(self, event):
        """Change the cursor of entry type widgets to 'arrow' if in a disabled
        or readonly state."""
        try:
            widget = self.nametowidget(event.widget)
            state = str(widget.cget('state'))
            cursor = str(widget.cget('cursor'))
            if state in (DISABLED, READONLY):
                if cursor == 'arrow':
                    return
                else:
                    widget['cursor'] = 'arrow'
            else:
                if cursor in ('ibeam', ''):
                    return
                else:
                    widget['cursor'] = None
        except:
            pass
        

class Toplevel(tkinter.Toplevel):
    """A class that wraps the tkinter.Toplevel class in order to
    provide a more convenient api with additional bells and whistles.
    For more information on how to use the inherited `Toplevel`
    methods, see the [tcl/tk documentation](https://tcl.tk/man/tcl8.6/TkCmd/toplevel.htm)
    and the [Python documentation](https://docs.python.org/3/library/tkinter.html#tkinter.Toplevel).

    ![](../../assets/window/window-toplevel.png)

    Examples:

        ```python
        app = Toplevel(title="My Toplevel")
        app.mainloop()
        ```
    """

    def __init__(
        self,
        title="ttkbootstrap",
        iconphoto=None,
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        transient=None,
        overrideredirect=False,
        windowtype=None,
        topmost=False,
        toolwindow=False,
        alpha=1.0,
        **kwargs,
    ):
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            iconphoto (PhotoImage):
                The titlebar icon. This image is applied to all future
                toplevels as well.

            size (Tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Toplevel.geometry` method.

            position (Tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Toplevel.geometry`
                method.

            minsize (Tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.minsize` method.

            maxsize (Tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.maxsize` method.

            resizable (Tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Toplevel.resizable` method.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Toplevel.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is processed as
                `Toplevel.overrideredirect(1)`.

            windowtype (str):
                On X11, requests that the window should be interpreted by
                the window manager as being of the specified type. Internally,
                this is passed to the `Toplevel.attributes('-type', windowtype)`.

                See the [-type option](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm#M64)
                for a list of available options.

            topmost (bool):
                Specifies whether this is a topmost window (displays above all
                other windows). Internally, this processed by the window as
                `Toplevel.attributes('-topmost', 1)`.

            toolwindow (bool):
                On Windows, specifies a toolwindow style. Internally, this is
                processed as `Toplevel.attributes('-toolwindow', 1)`.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        super().__init__(**kwargs)
        winsys = self.tk.call('tk', 'windowingsystem')

        if iconphoto:
            self._icon = iconphoto or tkinter.PhotoImage(data=Icon.icon)
            self.iconphoto(False, self._icon)

        self.title(title)

        if size is not None:
            width, height = size
            self.geometry(f'{width}x{height}')

        if position is not None:
            xpos, ypos = position
            self.geometry(f"+{xpos}+{ypos}")
        
        if minsize is not None:
            width, height = minsize
            self.minsize(width, height)
        
        if maxsize is not None:
            width, height = maxsize
            self.maxsize(width, height)

        if resizable is not None:
            width, height = resizable
            self.resizable(width, height)
        
        if transient is not None:
            self.transient(transient)
        
        if overrideredirect:
            self.overrideredirect(1)
        
        if windowtype is not None:
            if winsys == 'x11':
                self.attributes("-type", windowtype)
        
        if topmost:
            self.attributes("-topmost", 1)
        
        if toolwindow:
            if winsys == 'win32':
                self.attributes("-toolwindow", 1)
        
        if alpha is not None:
            if winsys == 'x11':
                self.wait_visibility(self)
            self.attributes("-alpha", alpha)

    @property
    def style(self):
        """Return a reference to the `ttkbootstrap.style.Style` object."""
        return Style()

    def place_window_center(self):
        """Position the toplevel in the center of the screen. Does not
        account for titlebar height."""
        self.update_idletasks()
        w_height = self.winfo_height()
        w_width = self.winfo_width()
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        xpos = (s_width - w_width) // 2
        ypos = (s_height - w_height) // 2
        self.geometry(f'+{xpos}+{ypos}')

    position_center = place_window_center # alias

if __name__ == "__main__":

    root = Window(themename="superhero", alpha=0.5, size=(1000, 1000))
    #root.withdraw()
    root.place_window_center()
    #root.deiconify()

    top = Toplevel(title="My Toplevel", alpha=0.4, size=(1000, 1000))
    top.place_window_center()

    root.mainloop()
