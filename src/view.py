# ===============================================================
# Model-View-Controller Architecture for CS_2450_Abacus
# 
# The View handles the presentation of data to the user
#
# ===============================================================


# Ensure access to lib folder
import sys
sys.path.insert(1, '../lib')

# Import graphics library
from graphics import *


class View(object):

    # ===============================================================
    # Button Class
    # Modified from the button example in the python textbook
    class Button:
        def __init__(self, center, width, height, label, color, color_o, mouse_color, mouse_color_o, text_color):
            self.color = color
            self.color_o = color_o
            self.mouse_color = mouse_color
            self.mouse_color_o = mouse_color_o
            w, h = width/2, height/2
            x, y = center.getX(), center.getY()
            self.xmax, self.xmin = x+w, x-w
            self.ymax, self.ymin = y+h, y-h
            p1 = Point(self.xmin, self.ymin)
            p2 = Point(self.xmax, self.ymax)
            self.rect = Rectangle(p1, p2)
            self.rect.setFill(color)
            self.rect.setOutline(color_o)
            self.label = Text(center, label)
            self.label.setTextColor(text_color)
            self.hover = False
        
        def draw(self, win):
            self.rect.draw(win)
            self.label.draw(win)
        
        def undraw(self):
            self.rect.undraw()
            self.label.undraw()

        def update(self, mouse_x, mouse_y):
            if (self.xmin <= mouse_x < self.xmax and self.ymin <= mouse_y < self.ymax):
                self.rect.setOutline(self.mouse_color_o)
                self.rect.setFill(self.mouse_color)
                self.hover = True
            else:
                self.rect.setOutline(self.color_o)
                self.rect.setFill(self.color)
                self.hover = False
        
        def clicked(self):
            return self.hover
        

    # ===============================================================
    # Window attributes and variables

    title = 'Window'
    width = 1200
    height = 900
    graph_win = None
    mouse_x = 0
    mouse_y = 0

    abacus_color = color_rgb(232, 194, 88)
# Purple
    #color = color_rgb(94, 69, 102)
    #highlight = color_rgb(235, 212, 235)
# Green
    color = color_rgb(46, 105, 66)
    highlight = color_rgb(200, 232, 210)
# Blue
    #color = color_rgb(41, 68, 117)
    #highlight = color_rgb(181, 199, 232)

    # Graphics components
    class GUIComponent():
        def __init__(self):
            self.objects = dict()
            self.buttons = dict()

        def clear(self):
            def cleardict(d):
                for o in d.values():
                    if(o):
                        o.undraw()
                    del o
                d.clear()
            cleardict(self.objects)
            cleardict(self.buttons)

    components = dict()    


    # ===============================================================
    # View static functions

    @staticmethod
    def create_window(title, width=-1, height=-1):
        if(width == -1):
            width = View.width
        if(height == -1):
            height = View.height
        if(View.graph_win == None):
            View.graph_win = GraphWin(title, width, height, autoflush=False)
            View.graph_win.setBackground(View.color)
            View.graph_win.bind('<Motion>', View._mouse_moved)

    @staticmethod
    def close_window():
        View.graph_win.close()

    @staticmethod
    def mouse_clicked():
        click = View.graph_win.checkMouse()
        return not click == None
    
    @staticmethod
    def get_clicked_button():
        for component in View.components.values():
            for b in component.buttons.values():
                if(b.clicked()):
                    return b.label.getText()
        return None

    @staticmethod
    def _mouse_moved(event):
        View.mouse_x = event.x
        View.mouse_y = event.y
        View._update()

    @staticmethod
    def _update():
        for component in View.components.values():
            for b in component.buttons.values():
                b.update(View.mouse_x, View.mouse_y)

    @staticmethod
    def draw_abacus(center, height, numColumns, showValues=False):
        buffer = height*0.04
        cwidth = height*0.15
        twidth = cwidth*numColumns + buffer*(numColumns+1)
        bheight = (height - buffer*3)/8
        x1 = center.getX() - twidth/2
        y1 = center.getY() - height/2
        x2 = x1 + twidth
        y2 = y1 + height

        if(not 'abacus' in View.components.keys()):
            View.components['abacus'] = View.GUIComponent()
        else:
            View.components['abacus'].clear()

        # Background
        bgr1 = Rectangle(
                Point(x1 + buffer, y1),
                Point(x2 - buffer, y2))
        bgr1.setOutline(View.abacus_color)
        bgr1.setFill(View.abacus_color)
        bgr2 = Rectangle(
                Point(x1, y1 + buffer),
                Point(x2, y2 - buffer))
        bgr2.setOutline(View.abacus_color)
        bgr2.setFill(View.abacus_color)
        bgc1 = Circle(
                Point(x1 + buffer, y1 + buffer),
                buffer)
        bgc1.setOutline(View.abacus_color)
        bgc1.setFill(View.abacus_color)
        bgc2 = Circle(
                Point(x2 - buffer, y1 + buffer),
                buffer)
        bgc2.setOutline(View.abacus_color)
        bgc2.setFill(View.abacus_color)
        bgc3 = Circle(
                Point(x1 + buffer, y2 - buffer),
                buffer)
        bgc3.setOutline(View.abacus_color)
        bgc3.setFill(View.abacus_color)
        bgc4 = Circle(
                Point(x2 - buffer, y2 - buffer),
                buffer)
        bgc4.setOutline(View.abacus_color)
        bgc4.setFill(View.abacus_color)
        bghole = Rectangle(
                Point(x1 + buffer, y1 + buffer),
                Point(x2 - buffer, y2 - buffer))
        bghole.setOutline('white')
        bghole.setFill('white')
        bgdeckbar = Rectangle(
                Point(x1, y1 + buffer + 2.5*bheight),
                Point(x2, y1 + 2*buffer + 2.5*bheight))
        bgdeckbar.setOutline(View.abacus_color)
        bgdeckbar.setFill(View.abacus_color)

        View.components['abacus'].objects['bgr1'] = bgr1
        View.components['abacus'].objects['bgr2'] = bgr2
        View.components['abacus'].objects['bgc1'] = bgc1
        View.components['abacus'].objects['bgc2'] = bgc2
        View.components['abacus'].objects['bgc3'] = bgc3
        View.components['abacus'].objects['bgc4'] = bgc4
        View.components['abacus'].objects['bghole'] = bghole
        View.components['abacus'].objects['bgdeckbar'] = bgdeckbar

        bgr1.draw(View.graph_win)
        bgr2.draw(View.graph_win)
        bgc1.draw(View.graph_win)
        bgc2.draw(View.graph_win)
        bgc3.draw(View.graph_win)
        bgc4.draw(View.graph_win)
        bghole.draw(View.graph_win)
        bgdeckbar.draw(View.graph_win)

        # Column Dividers
        for i in range(numColumns-1):
            bar = Rectangle(
                    Point(x1 + (i+1)*buffer + (i+1)*cwidth, y1 + buffer),
                    Point(x1 + (i+2)*buffer + (i+1)*cwidth, y1 + height - buffer))
            bar.setFill(View.abacus_color)
            bar.setOutline(View.abacus_color)
            View.components['abacus'].objects['bgdiv' + str(i)] = bar
            bar.draw(View.graph_win)
        
        # Columns
        for i in range(numColumns):
            bar = Rectangle(
                    Point(x1 + (i+1)*buffer + i*cwidth + cwidth/2 - buffer/4, y1 + buffer),
                    Point(x1 + (i+1)*buffer + i*cwidth + cwidth/2 + buffer/4, y1 + height - buffer))
            bar.setFill(View.abacus_color)
            bar.setOutline(View.abacus_color)
            View.components['abacus'].objects['colbar' + str(i)] = bar
            bar.draw(View.graph_win)

            # Beads
            # Upper
            for b in range(2):
                bead = View.Button(
                        Point(x1 + (i+1)*buffer + i*cwidth + cwidth/2, y1 + buffer + b*bheight + bheight/2),
                        cwidth,
                        bheight,
                        '',
                        View.color,
                        View.color,
                        View.highlight,
                        View.highlight,
                        None)
                oval = Oval(
                        Point(bead.xmin, bead.ymin),
                        Point(bead.xmax, bead.ymax))
                oval.setFill(bead.color)
                oval.setOutline(bead.color_o)
                del bead.rect
                bead.rect = oval
                View.components['abacus'].buttons['c' + str(i) + 'u' + str(b)] = bead
                bead.draw(View.graph_win)
            # Lower
            for b in range(5):
                bead = View.Button(
                        Point(x1 + (i+1)*buffer + i*cwidth + cwidth/2, y2 - buffer - b*bheight - bheight/2),
                        cwidth,
                        bheight,
                        '',
                        View.color,
                        View.color,
                        View.highlight,
                        View.highlight,
                        None)
                oval = Oval(
                        Point(bead.xmin, bead.ymin),
                        Point(bead.xmax, bead.ymax))
                oval.setFill(bead.color)
                oval.setOutline(bead.color_o)
                del bead.rect
                bead.rect = oval
                View.components['abacus'].buttons['c' + str(i) + 'l' + str(b)] = bead
                bead.draw(View.graph_win)
            # Textboxes
            if(showValues):
                size = int(height*(30/500))
                if(size > 36): size = 36
                if(size < 5): size = 5
                box = Rectangle(
                        Point(x1 + (i+1)*buffer + i*cwidth + buffer/2, y2 + buffer/2),
                        Point(x1 + (i+1)*buffer + (i+1)*cwidth - buffer/2, y2 - buffer/2 + cwidth))
                box.setFill(View.color)
                box.setOutline('white')
                text = Text(
                        Point(x1 + (i+1)*buffer + i*cwidth + cwidth/2, y2 + cwidth/2),
                        '0')
                text.setTextColor('white')
                text.setSize(size)
                text.setStyle('bold')

                View.components['abacus'].objects['c' + str(i) + 'textbox'] = box
                View.components['abacus'].objects['c' + str(i) + 'text'] = text

                box.draw(View.graph_win)
                text.draw(View.graph_win)

    @staticmethod
    def draw_create_user():
        width = 1000
        height = 700
        x = (View.width - width)/2
        y = (View.height - height)/2

        if(not 'create_user' in View.components.keys()):
            View.components['create_user'] = View.GUIComponent()
        else:
            View.components['create_user'].clear()

        panel = Rectangle(
                Point(x, y),
                Point(x + width, y + height))
        panel.setFill('white')
        panel.setOutline('white')
        title = Text(
                Point(View.width/2, 300),
                'Create New User')
        title.setSize(30)
        idt = Text(
                Point(400, 400),
                'User ID')
        idt.setSize(20)
        passt = Text(
                Point(400, 480),
                'Temp Password')
        passt.setSize(20)
        ide = Entry(
                Point(700, 400),
                20)
        ide.setSize(20)
        ide.setFill('white')
        passe = Entry(
                Point(700, 480),
                20)
        passe.setSize(20)
        passe.setFill('white')
        quit = View.Button(
                Point(300, 700),
                200,
                50, 
                'Quit', 
                'white', 
                'black',
                View.highlight, 
                'black',
                'black')
        quit.label.setSize(20)
        create = View.Button(
                Point(View.width - 300, 700),
                200,
                50, 
                'Create', 
                'white', 
                'black',
                View.highlight, 
                'black',
                'black')
        create.label.setSize(20)

        View.components['create_user'].objects['panel'] = panel
        View.components['create_user'].objects['title'] = title
        View.components['create_user'].objects['idt'] = idt
        View.components['create_user'].objects['passt'] = passt
        View.components['create_user'].objects['ide'] = ide
        View.components['create_user'].objects['passe'] = passe
        View.components['create_user'].buttons['quit'] = quit
        View.components['create_user'].buttons['create'] = create

        panel.draw(View.graph_win)
        title.draw(View.graph_win)
        idt.draw(View.graph_win)
        passt.draw(View.graph_win)
        ide.draw(View.graph_win)
        passe.draw(View.graph_win)
        quit.draw(View.graph_win)
        create.draw(View.graph_win)

    @staticmethod
    def draw_cts():
        width = 900
        height = 600
        x = (View.width - width)/2
        y = (View.height - height)/2

        if(not 'cts' in View.components.keys()):
            View.components['cts'] = View.GUIComponent()
        else:
            View.components['cts'].clear()

        panel = Rectangle(
                Point(x, y),
                Point(x + width, y + height))
        panel.setFill('white')
        panel.setOutline('white')
        title = Text(
                Point(View.width/2, 300),
                'Connect to Server')
        title.setSize(30)
        entry = Entry(
                Point(View.width/2, 400),
                40)
        entry.setSize(20)
        entry.setFill('white')
        quit = View.Button(
                Point(400, 600),
                200,
                50, 
                'Quit', 
                'white', 
                'black',
                View.highlight, 
                'black',
                'black')
        quit.label.setSize(20)
        connect = View.Button(
                Point(View.width - 400, 600),
                200,
                50, 
                'Connect', 
                'white', 
                'black',
                View.highlight, 
                'black',
                'black')
        connect.label.setSize(20)


        View.components['cts'].objects['panel'] = panel
        View.components['cts'].objects['title'] = title
        View.components['cts'].objects['entry'] = entry
        View.components['cts'].buttons['quit'] = quit
        View.components['cts'].buttons['connect'] = connect

        panel.draw(View.graph_win)
        title.draw(View.graph_win)
        entry.draw(View.graph_win)
        quit.draw(View.graph_win)
        connect.draw(View.graph_win)

    @staticmethod
    def draw_login():
        width = 900
        height = 600
        x = (View.width - width)/2
        y = (View.height - height)/2

        if(not 'login' in View.components.keys()):
            View.components['login'] = View.GUIComponent()
        else:
            View.components['login'].clear()

        panel = Rectangle(
                Point(x, y),
                Point(x + width, y + height))
        panel.setFill('white')
        panel.setOutline('white')
        title = Text(
                Point(View.width/2, 300),
                'Login')
        title.setSize(30)
        idt = Text(
                Point(400, 400),
                'User ID')
        idt.setSize(20)
        passt = Text(
                Point(400, 480),
                'Password')
        passt.setSize(20)
        ide = Entry(
                Point(700, 400),
                20)
        ide.setSize(20)
        ide.setFill('white')
        passe = Entry(
                Point(700, 480),
                20)
        passe.setSize(20)
        passe.setFill('white')
        quit = View.Button(
                Point(400, 600),
                200,
                50, 
                'Quit', 
                'white', 
                'black',
                View.highlight, 
                'black',
                'black')
        quit.label.setSize(20)
        login = View.Button(
                Point(View.width - 400, 600),
                200,
                50, 
                'Login', 
                'white', 
                'black',
                View.highlight, 
                'black',
                'black')
        login.label.setSize(20)

        View.components['login'].objects['panel'] = panel
        View.components['login'].objects['title'] = title
        View.components['login'].objects['idt'] = idt
        View.components['login'].objects['passt'] = passt
        View.components['login'].objects['ide'] = ide
        View.components['login'].objects['passe'] = passe
        View.components['login'].buttons['quit'] = quit
        View.components['login'].buttons['login'] = login

        panel.draw(View.graph_win)
        title.draw(View.graph_win)
        idt.draw(View.graph_win)
        passt.draw(View.graph_win)
        ide.draw(View.graph_win)
        passe.draw(View.graph_win)
        quit.draw(View.graph_win)
        login.draw(View.graph_win)

    @staticmethod
    def draw_topbar(username, title):
        height = 75
        user_width = 300
        title_width = 0

        if(not 'topbar' in View.components.keys()):
            View.components['topbar'] = View.GUIComponent()
        else:
            View.components['topbar'].clear()

        user = View.Button(
                Point(user_width/2, height/2),
                user_width,
                height, 
                username, 
                'white',
                'white', 
                View.highlight, 
                View.highlight, 
                'black')
        user.label.setSize(20)
        title_width = View.width - user_width - 20
        title = View.Button(
                Point(View.width - title_width/2, height/2),
                title_width,
                height,
                title,
                'white',
                'white',
                View.highlight, 
                View.highlight,
                'black')
        title.label.setSize(20)
        View.components['topbar'].buttons['user'] = user
        View.components['topbar'].buttons['title'] = title

        user.draw(View.graph_win)
        title.draw(View.graph_win)
    
    @staticmethod
    def erase(name):
        if(View.components[name]):
            View.components[name].clear()
        



# ===============================================================
if __name__ == '__main__':
    View.create_window('CS_2450_Abacus - Team 5')

    View.draw_cts()

    while(not View.mouse_clicked()):
        pass

    View.erase('cts')
    View.draw_login()

    while(not View.mouse_clicked()):
        pass

    View.erase('login')
    View.draw_topbar('Andrew', 'Abacus Practice')
    View.draw_abacus(Point(View.width/2, 400), 500, 7, True)

    while(not View.mouse_clicked()):
        pass

    View.erase('topbar')
    View.erase('abacus')

    View.close_window()