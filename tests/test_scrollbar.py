import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_scrollbar_frame(widget_style, style, orient):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    sb = ttk.Scrollbar(frame, style=widget_style, orient=orient)
    sb.set(0.1, 0.3)
    if orient == tk.HORIZONTAL:
        sb.pack(padx=5, pady=5, fill=tk.X)
    else:
        sb.pack(padx=5, pady=5, fill=tk.Y, side=tk.LEFT)

    # colored
    for i, color in enumerate(style.colors):
        pb_style = f'{color}.{widget_style}'
        ttk.Label(frame, text=pb_style).pack(fill=tk.X)
        sb = ttk.Scrollbar(frame, style=pb_style, orient=orient)
        sb.set(0.1, 0.3)
        if orient == tk.HORIZONTAL:
            sb.pack(padx=5, pady=5, fill=tk.X, expand=tk.YES)
        else:
            sb.pack(padx=5, pady=5, fill=tk.Y, side=tk.LEFT, 
                    expand=tk.YES)

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    test1 = create_scrollbar_frame(
        widget_style='success.Horizontal.TScrollbar', 
        style=style, 
        orient=tk.HORIZONTAL
    )
    test1.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH)
    
    test2 = create_scrollbar_frame(
        widget_style='success.Vertical.TScrollbar',
        style=style, 
        orient=tk.VERTICAL
    )
    test2.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=tk.YES)

    root.mainloop()