from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.messagebox import showerror

filename = None


def newFile():
    global filename
    filename = None
    text.delete("1.0", END)


def saveFile():
    global filename
    if filename is None:
        saveAs()
        return
    try:
        content = text.get("1.0", END)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        showerror(
            title="Oops!",
            message=f"Unable to save file:\n{e}"
        )


def saveAs():
    global filename
    f = asksaveasfile(
        mode="w",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if f is None:
        return
    try:
        content = text.get("1.0", END)
        f.write(content.rstrip())
        filename = f.name
    except Exception as e:
        showerror(
            title="Oops!",
            message=f"Unable to save file:\n{e}"
        )
    finally:
        f.close()


def openFile():
    global filename
    f = askopenfile(
        mode="r",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if f is None:
        return
    try:
        content = f.read()
        text.delete("1.0", END)
        text.insert("1.0", content)
        filename = f.name
    except Exception as e:
        showerror(
            title="Oops!",
            message=f"Unable to open file:\n{e}"
        )
    finally:
        f.close()


root = Tk()
root.title("PyNote")
root.geometry("600x400")

text = Text(root)
text.pack(fill=BOTH, expand=True)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As...", command=saveAs)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)
root.mainloop()

