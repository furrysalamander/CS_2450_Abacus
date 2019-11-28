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
        def __init__(self, center, width, height, label, color, mouse_color, text_color):
            self.color = color
            self.mouse_color = mouse_color
            w, h = width/2, height/2
            x, y = center.getX(), center.getY()
            self.xmax, self.xmin = x+w, x-w
            self.ymax, self.ymin = y+h, y-h
            p1 = Point(self.xmin, self.ymin)
            p2 = Point(self.xmax, self.ymax)
            self.rect = Rectangle(p1, p2)
            self.rect.setFill(color)
            self.rect.setOutline(color)
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
            if (self.xmin <= mouse_x <= self.xmax and self.ymin <= mouse_y <= self.ymax):
                self.rect.setOutline(self.mouse_color)
                self.rect.setFill(self.mouse_color)
                self.hover = True
            else:
                self.rect.setOutline(self.color)
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
    color = color_rgb(94, 69, 102)
    highlight = color_rgb(235, 212, 235)
    mouse_x = 0
    mouse_y = 0

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
            View.graph_win = GraphWin(title, width, height)
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
    def draw_login():
        width = 1000
        height = 700

        if(not 'login' in View.components.keys()):
            View.components['login'] = View.GUIComponent()
        else:
            View.components['login'].clear()

        panel = Rectangle(
                Point(user_width/2, height/2),
                user_width,
                height, 
                username, 
                'white', 
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
                View.highlight,
                'black')
        title.label.setSize(20)
        View.components['topbar'].buttons['user'] = user
        View.components['topbar'].buttons['title'] = title

        user.draw(View.graph_win)
        title.draw(View.graph_win)


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
                View.highlight,
                'black')
        title.label.setSize(20)
        View.components['topbar'].buttons['user'] = user
        View.components['topbar'].buttons['title'] = title

        user.draw(View.graph_win)
        title.draw(View.graph_win)
    
    @staticmethod
    def erase_topbar():
        if(View.components['topbar']):
            View.components['topbar'].clear()
        



# ===============================================================
if __name__ == '__main__':
    View.create_window('CS_2450_Abacus - Team 5')
    View.draw_topbar('Andrew', 'Dashboard')
    
    while(not View.mouse_clicked()):
        pass

    View.erase_topbar()

    while(not View.mouse_clicked()):
        pass

    View.close_window()