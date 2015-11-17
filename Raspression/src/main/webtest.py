import threading
import json
import web
import Tkinter

global root

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        return "Fuck right off and fuck off while you're doing it"

    def POST(self):
        global root
        for child in root.winfo_children():
            child.destroy()
        input = web.data()
        w = Tkinter.Label(root, text=input)
        w.pack()

        print input #['c1'], input['c2']

def buildUi():
    global root
    root = Tkinter.Tk()
    w = Tkinter.Label(root, text="Hello, world!")
    w.pack()
    root.mainloop()

def startServer():
    app = web.application(urls, globals())
    app.run()

if __name__ == "__main__":
    uiThread = threading.Thread(target=buildUi)
    uiThread.start()
    serverThread = threading.Thread(target=startServer)
    serverThread.start()

