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

# Ensure access to image folder
import os
PATH = os.path.dirname(os.path.abspath(__file__))



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
    #color = color_rgb(46, 105, 66)
    #highlight = color_rgb(200, 232, 210)
# Blue
    color = color_rgb(41, 68, 117)
    highlight = color_rgb(181, 199, 232)

    # Graphics components
    class GUIComponent():
        def __init__(self):
            self.data = dict()
            self.objects = dict()
            self.buttons = dict()
            self.active = True
            self.sub = list()

        def clear(self):
            def cleardict(d):
                for o in d.values():
                    if(o):
                        o.undraw()
                    del o
                d.clear()
            self.data.clear()
            cleardict(self.objects)
            cleardict(self.buttons)
            self.active = True
            self.sub = list()
            

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
    def get_component_clicked(component):
        if(component in View.components.keys()):
            for key in View.components[component].buttons.keys():
                if(View.components[component].buttons[key].clicked()):
                    return key
        return None

    @staticmethod
    def _mouse_moved(event):
        View.mouse_x = event.x
        View.mouse_y = event.y
        View._update()

    @staticmethod
    def _update():
        for component in View.components.values():
            if(component.active):
                for b in component.buttons.values():
                    b.update(View.mouse_x, View.mouse_y)

    @staticmethod
    def set_component_active(component, active=True):
        if(component in View.components.keys()):
            View.components[component].active = active

    @staticmethod
    def bead_to_column_index(key):
        if(key[0] is 'c'):
            if(key[2] is 'u'):
                return True, int(key[1]), int(key[3])
            else:
                return False, int(key[1]), int(key[3])

    @staticmethod
    def _build_arrow(left, x, y, width, height):
        lip = 0.8
        length = width - height/2
        if(length < 0):
            length = 0
        thickness = height/(2*lip + 1)
        sign = 1
        if(left):
            sign = -1

        points = list()
        points.append(Point(x, y - thickness/2))
        points.append(Point(x + sign*length, y - thickness/2))
        points.append(Point(x + sign*length, y - thickness/2 - lip*thickness))
        points.append(Point(x + sign*length + sign*(thickness/2 + lip*thickness), y))
        points.append(Point(x + sign*length, y + thickness/2 + lip*thickness))
        points.append(Point(x + sign*length, y + thickness/2))
        points.append(Point(x, y + thickness/2))
        return points

    @staticmethod
    def draw_tutorial(text, pagetext, prev=False, next=False, text_x=0, text_y=0, text_width=0, \
                      abacus_x=-1, abacus_y=-1, abacus_height=-1, abacus_columns=7, \
                      abacus_values=False, abacus_enabled=False):
        buffer = 100
        x1, x2 = buffer, View.width - buffer
        y1, y2 = 75 + buffer, View.height - buffer
        rounding = 25
        ix1, ix2 = x1 + 2*rounding, x2 - 2*rounding
        iy1, iy2 = y1 + 2*rounding, y2 - 2*rounding
        width = ix2 - ix1
        height = iy2 - iy1

        if(not 'tutorial' in View.components.keys()):
            View.components['tutorial'] = View.GUIComponent()
        else:
            View.components['tutorial'].clear()

        # Background
        bgr1 = Rectangle(
                Point(x1 + rounding, y1),
                Point(x2 - rounding, y2))
        bgr1.setOutline('white')
        bgr1.setFill('white')
        bgr2 = Rectangle(
                Point(x1, y1 + rounding),
                Point(x2, y2 - rounding))
        bgr2.setOutline('white')
        bgr2.setFill('white')
        bgc1 = Circle(
                Point(x1 + rounding, y1 + rounding),
                rounding)
        bgc1.setOutline('white')
        bgc1.setFill('white')
        bgc2 = Circle(
                Point(x2 - rounding, y1 + rounding),
                rounding)
        bgc2.setOutline('white')
        bgc2.setFill('white')
        bgc3 = Circle(
                Point(x1 + rounding, y2 - rounding),
                rounding)
        bgc3.setOutline('white')
        bgc3.setFill('white')
        bgc4 = Circle(
                Point(x2 - rounding, y2 - rounding),
                rounding)
        bgc4.setOutline('white')
        bgc4.setFill('white')
        # clipart
        image = Image(
                Point(0, 0),
                PATH + '\\..\\image\\kid.png')
        image_width = image.getWidth()
        image_height = image.getHeight()
        image_x = View.width - image_width/2
        image_y = View.height - image_height/2
        image.move(image_x, image_y)
        # Text
        textobj = Text(
                Point(ix1 + text_x, iy1 + text_y),
                text)
        textobj.setSize(19)
        textobj.config['anchor'] = 'nw'
        textobj.config['justify'] = 'left'
        textobj.config['width'] = width*text_width
        pagetextobj = Text(
                Point(View.width/2, View.height - buffer/2),
                pagetext)
        pagetextobj.setSize(25)
        pagetextobj.setTextColor('white')
        pagetextobj.setStyle('bold')

        View.components['tutorial'].objects['bgr1'] = bgr1
        View.components['tutorial'].objects['bgr2'] = bgr2
        View.components['tutorial'].objects['bgc1'] = bgc1
        View.components['tutorial'].objects['bgc2'] = bgc2
        View.components['tutorial'].objects['bgc3'] = bgc3
        View.components['tutorial'].objects['bgc4'] = bgc4
        View.components['tutorial'].objects['image'] = image
        View.components['tutorial'].objects['text'] = textobj
        View.components['tutorial'].objects['pagetext'] = pagetextobj

        bgr1.draw(View.graph_win)
        bgr2.draw(View.graph_win)
        bgc1.draw(View.graph_win)
        bgc2.draw(View.graph_win)
        bgc3.draw(View.graph_win)
        bgc4.draw(View.graph_win)
        image.draw(View.graph_win)
        textobj.draw(View.graph_win)
        pagetextobj.draw(View.graph_win)

        # Previous and Next
        if(prev):
            bx = View.width/2 - buffer/2
            by = View.height - buffer/2
            bw = 3*buffer/4
            bh = buffer/2
            prevobj = View.Button(
                    Point(bx - bw/2, by),
                    bw,
                    bh,
                    '',
                    'white',
                    'white',
                    View.highlight,
                    View.highlight,
                    'white')
            arrow = Polygon(View._build_arrow(True,
                                              bx,
                                              by,
                                              bw,
                                              bh))
            arrow.setOutline('white')
            arrow.setFill('white')
            del prevobj.rect
            prevobj.rect = arrow
            View.components['tutorial'].buttons['prev'] = prevobj
            prevobj.draw(View.graph_win)
        if(next):
            bx = View.width/2 + buffer/2
            by = View.height - buffer/2
            bw = 3*buffer/4
            bh = buffer/2
            nextobj = View.Button(
                    Point(bx + bw/2, by),
                    bw,
                    bh,
                    '',
                    'white',
                    'white',
                    View.highlight,
                    View.highlight,
                    'white')
            arrow = Polygon(View._build_arrow(False,
                                              bx,
                                              by,
                                              bw,
                                              bh))
            arrow.setOutline('white')
            arrow.setFill('white')
            del nextobj.rect
            nextobj.rect = arrow
            View.components['tutorial'].buttons['next'] = nextobj
            nextobj.draw(View.graph_win)
            
        # Abacus
        if(abacus_x >= 0 and abacus_y >= 0 and abacus_height > 0 and abacus_columns > 0):
            View.draw_abacus(Point(ix1 + abacus_x*width, iy1 + abacus_y*height),
                    abacus_height*height,
                    abacus_columns,
                    abacus_values)
            View.set_component_active('abacus', abacus_enabled)
            View.components['tutorial'].sub.append('abacus')

    @staticmethod
    def draw_abacus(center, height, numColumns, showValues=False):
        buffer = height*0.04
        cwidth = height*0.12
        twidth = cwidth*numColumns + buffer*(numColumns+1)
        gap_bead_ratio = 1.0
        bheight = (height - buffer*3)/(7 + 2*gap_bead_ratio)
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
                Point(x1, y1 + buffer + (2 + gap_bead_ratio)*bheight),
                Point(x2, y1 + 2*buffer + (2 + gap_bead_ratio)*bheight))
        bgdeckbar.setOutline(View.abacus_color)
        bgdeckbar.setFill(View.abacus_color)

        View.components['abacus'].data['movdist'] = bheight * gap_bead_ratio
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
            View.components['abacus'].objects['colbar' + str(numColumns-1-i)] = bar
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
                View.components['abacus'].buttons['c' + str(numColumns-1-i) + 'u' + str(1-b)] = bead
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
                View.components['abacus'].buttons['c' + str(numColumns-1-i) + 'l' + str(4-b)] = bead
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

                View.components['abacus'].objects['c' + str(numColumns-1-i) + 'textbox'] = box
                View.components['abacus'].objects['c' + str(numColumns-1-i) + 'text'] = text

                box.draw(View.graph_win)
                text.draw(View.graph_win)

    @staticmethod
    def draw_create_class():
        buffer = 150
        text_width = 250
        row_height = 70
        entry_width = 400
        x1, x2 = buffer, buffer + text_width
        y1 = 75 + buffer

        if(not 'create_class' in View.components.keys()):
            View.components['create_class'] = View.GUIComponent()
        else:
            View.components['create_class'].clear()

        title = Text(
                Point(x1, y1),
                'Create New Class')
        title.setSize(30)
        title.setTextColor('white')
        title.config['anchor'] = 'w'
        idt = Text(
                Point(x1, y1 + row_height),
                'Class ID:')
        idt.setSize(20)
        idt.setTextColor('white')
        idt.config['anchor'] = 'w'
        namet = Text(
                Point(x1, y1 + row_height*2),
                'Class Name:')
        namet.setSize(20)
        namet.setTextColor('white')
        namet.config['anchor'] = 'w'
        teachert = Text(
                Point(x1, y1 + row_height*3),
                'Assigned Teacher ID:')
        teachert.setSize(20)
        teachert.setTextColor('white')
        teachert.config['anchor'] = 'w'
        ide = Entry(
                Point(x2 + entry_width/2, y1 + row_height),
                25)
        ide.setSize(20)
        ide.setFill('white')
        namee = Entry(
                Point(x2 + entry_width/2, y1 + row_height*2),
                25)
        namee.setSize(20)
        namee.setFill('white')
        teachere = Entry(
                Point(x2 + entry_width/2, y1 + row_height*3),
                25)
        teachere.setSize(20)
        teachere.setFill('white')
        # Create Button
        create = View.Button(
                Point(x2, View.height - buffer - 25),
                200,
                50,
                'Create New Class',
                'white',
                'white',
                View.highlight,
                View.highlight,
                'black')
        create.label.setSize(20)

        View.components['create_class'].objects['title'] = title
        View.components['create_class'].objects['idt'] = idt
        View.components['create_class'].objects['namet'] = namet
        View.components['create_class'].objects['teachert'] = teachert
        View.components['create_class'].objects['ide'] = ide
        View.components['create_class'].objects['namee'] = namee
        View.components['create_class'].buttons['teachere'] = teachere
        View.components['create_class'].buttons['create'] = create

        title.draw(View.graph_win)
        idt.draw(View.graph_win)
        namet.draw(View.graph_win)
        teachert.draw(View.graph_win)
        ide.draw(View.graph_win)
        namee.draw(View.graph_win)
        teachere.draw(View.graph_win)
        create.draw(View.graph_win)

    @staticmethod
    def draw_create_user():
        buffer = 150
        text_width = 250
        row_height = 70
        entry_width = 400
        x1, x2 = buffer, buffer + text_width
        y1 = 75 + buffer

        bw = 200
        bh = row_height - 10
        bcor = bh/2 * 0.4
        bcir = 0.7*bcor

        if(not 'create_user' in View.components.keys()):
            View.components['create_user'] = View.GUIComponent()
        else:
            View.components['create_user'].clear()

        title = Text(
                Point(x1, y1),
                'Create New User')
        title.setSize(30)
        title.setTextColor('white')
        title.config['anchor'] = 'w'
        idt = Text(
                Point(x1, y1 + row_height),
                'User ID:')
        idt.setSize(20)
        idt.setTextColor('white')
        idt.config['anchor'] = 'w'
        passt = Text(
                Point(x1, y1 + row_height*2),
                'Temp Password:')
        passt.setSize(20)
        passt.setTextColor('white')
        passt.config['anchor'] = 'w'
        typet = Text(
                Point(x1, y1 + row_height*3),
                'User Type:')
        typet.setSize(20)
        typet.setTextColor('white')
        typet.config['anchor'] = 'w'
        ide = Entry(
                Point(x2 + entry_width/2, y1 + row_height),
                25)
        ide.setSize(20)
        ide.setFill('white')
        passe = Entry(
                Point(x2 + entry_width/2, y1 + row_height*2),
                25)
        passe.setSize(20)
        passe.setFill('white')
        # Student, Teacher, Admin - buttons
        x, y = x2 + bw/2, y1 + row_height*3
        student = View.Button(
                Point(x, y),
                bw,
                bh, 
                'Student', 
                View.color, 
                View.color,
                View.highlight,
                View.highlight,
                'white')
        student.label.setSize(20)
        student.label.config['anchor'] = 'w'
        student.label.move(bh - bw/2, 0)
        student_co = Circle(
                Point(x - bw/2 + bh/2, y),
                bcor)
        student_co.setOutline('white')
        student_co.setFill('white')
        student_ci = Circle(
                Point(x - bw/2 + bh/2, y),
                bcir)
        student_ci.setOutline('black')
        student_ci.setFill('black')
        teacher = View.Button(
                Point(x, y + bh),
                bw,
                bh, 
                'Teacher', 
                View.color, 
                View.color,
                View.highlight, 
                View.highlight,
                'white')
        teacher.label.setSize(20)
        teacher.label.config['anchor'] = 'w'
        teacher.label.move(bh - bw/2, 0)
        teacher_co = Circle(
                Point(x - bw/2 + bh/2, y + bh),
                bcor)
        teacher_co.setOutline('white')
        teacher_co.setFill('white')
        teacher_ci = Circle(
                Point(x - bw/2 + bh/2, y + bh),
                bcir)
        teacher_ci.setOutline('white')
        teacher_ci.setFill('white')
        admin = View.Button(
                Point(x, y + bh*2),
                bw,
                bh, 
                'Admin', 
                View.color, 
                View.color,
                View.highlight, 
                View.highlight,
                'white')
        admin.label.setSize(20)
        admin.label.config['anchor'] = 'w'
        admin.label.move(bh - bw/2, 0)
        admin_co = Circle(
                Point(x - bw/2 + bh/2, y + bh*2),
                bcor)
        admin_co.setOutline('white')
        admin_co.setFill('white')
        admin_ci = Circle(
                Point(x - bw/2 + bh/2, y + bh*2),
                bcir)
        admin_ci.setOutline('white')
        admin_ci.setFill('white')
        # Create Button
        create = View.Button(
                Point(x2, View.height - buffer - 25),
                200,
                50,
                'Create User',
                'white',
                'white',
                View.highlight,
                View.highlight,
                'black')
        create.label.setSize(20)

        View.components['create_user'].objects['title'] = title
        View.components['create_user'].objects['idt'] = idt
        View.components['create_user'].objects['passt'] = passt
        View.components['create_user'].objects['typet'] = typet
        View.components['create_user'].objects['ide'] = ide
        View.components['create_user'].objects['passe'] = passe
        View.components['create_user'].buttons['student'] = student
        View.components['create_user'].objects['student_co'] = student_co
        View.components['create_user'].objects['student_ci'] = student_ci
        View.components['create_user'].buttons['teacher'] = teacher
        View.components['create_user'].objects['teacher_co'] = teacher_co
        View.components['create_user'].objects['teacher_ci'] = teacher_ci
        View.components['create_user'].buttons['admin'] = admin
        View.components['create_user'].objects['admin_co'] = admin_co
        View.components['create_user'].objects['admin_ci'] = admin_ci
        View.components['create_user'].buttons['create'] = create

        title.draw(View.graph_win)
        idt.draw(View.graph_win)
        passt.draw(View.graph_win)
        typet.draw(View.graph_win)
        ide.draw(View.graph_win)
        passe.draw(View.graph_win)
        student.draw(View.graph_win)
        student_co.draw(View.graph_win)
        student_ci.draw(View.graph_win)
        teacher.draw(View.graph_win)
        teacher_co.draw(View.graph_win)
        teacher_ci.draw(View.graph_win)
        admin.draw(View.graph_win)
        admin_co.draw(View.graph_win)
        admin_ci.draw(View.graph_win)
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
    def draw_topbar_dropdown():
        height = 75
        button_height = 60
        width = 300
        buffer = 20
        line_color = color_rgb(200, 200, 200)

        if(not 'topbar_dropdown' in View.components.keys()):
            View.components['topbar_dropdown'] = View.GUIComponent()
        else:
            View.components['topbar_dropdown'].clear()

        panel = View.Button(
                Point(width/2, height + (View.height - height)/2),
                width,
                View.height - height, 
                '', 
                'white',
                'white', 
                'white', 
                'white', 
                'white')
        line = Line(
                Point(buffer, height),
                Point(width - buffer, height))
        line.setOutline(line_color)
        dash = View.Button(
                Point(width/2, height + buffer + button_height/2),
                width,
                button_height,
                'Dashboard',
                'white',
                'white',
                View.highlight, 
                View.highlight,
                'black')
        dash.label.setSize(17)
        dash.label.config['anchor'] = 'w'
        dash.label.move(buffer - dash.label.getAnchor().getX(), 0)
        practice = View.Button(
                Point(width/2, height + buffer + button_height/2 + button_height),
                width,
                button_height,
                'Abacus Practice',
                'white',
                'white',
                View.highlight, 
                View.highlight,
                'black')
        practice.label.setSize(17)
        practice.label.config['anchor'] = 'w'
        practice.label.move(buffer - practice.label.getAnchor().getX(), 0)
        tutorial = View.Button(
                Point(width/2, height + buffer + button_height/2 + button_height*2),
                width,
                button_height,
                'Tutorial',
                'white',
                'white',
                View.highlight, 
                View.highlight,
                'black')
        tutorial.label.setSize(17)
        tutorial.label.config['anchor'] = 'w'
        tutorial.label.move(buffer - tutorial.label.getAnchor().getX(), 0)
        logout = View.Button(
                Point(width/2, View.height - button_height/2 - buffer),
                width,
                button_height,
                'Logout',
                'white',
                'white',
                View.highlight, 
                View.highlight,
                'black')
        logout.label.setSize(17)
        logout.label.config['anchor'] = 'w'
        logout.label.move(buffer - logout.label.getAnchor().getX(), 0)

        View.components['topbar_dropdown'].buttons['panel'] = panel
        View.components['topbar_dropdown'].objects['line'] = line
        View.components['topbar_dropdown'].buttons['dash'] = dash
        View.components['topbar_dropdown'].buttons['practice'] = practice
        View.components['topbar_dropdown'].buttons['tutorial'] = tutorial
        View.components['topbar_dropdown'].buttons['logout'] = logout

        panel.draw(View.graph_win)
        line.draw(View.graph_win)
        dash.draw(View.graph_win)
        practice.draw(View.graph_win)
        tutorial.draw(View.graph_win)
        logout.draw(View.graph_win)

    @staticmethod
    def draw_topbar(username, title):
        height = 75
        user_width = 300
        title_width = 0
        buffer = 20

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
        user.label.setSize(23)
        title_width = View.width - user_width - buffer
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
        title.label.setSize(23)
        View.components['topbar'].buttons['user'] = user
        View.components['topbar'].buttons['title'] = title

        user.draw(View.graph_win)
        title.draw(View.graph_win)
    
    @staticmethod
    def erase(name):
        if(View.components[name]):
            print('Erasing component "{}"'.format(name))
            old = list()
            for s in View.components[name].sub:
                print('  Found sub-component "{}"'.format(s))
                old.append(s)
            View.components[name].sub.clear()
            for s in old:
                View.erase(s)
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

    View.draw_topbar_dropdown()
    View.set_component_active('abacus', False)

    while(not View.mouse_clicked()):
        pass

    View.erase('topbar_dropdown')
    View.erase('abacus')
    View.erase('topbar')
    View.draw_topbar('Andrew', 'Tutorial')
    View.draw_tutorial(
            'Welcome students! Behold--the UVBacus! \n\nThis is an interactive abacus that is a great way to expand your math skills in a fun and exciting way. It is a whole lot of fun being able to use an abacus and this tutorial will teach you how to do addition and subtraction using the exchange method. \n\nThe abacus will surely make math fun and will provide a neat way to learn the math!',
            '1',
            False,
            True, 
            0,
            0,
            1,
            0.5,
            0.7,
            0.3,
            13)

    while(not View.mouse_clicked()):
        pass

    View.erase('tutorial')
    View.draw_tutorial(
            'Bead Placement:\n\nThe abacus used in the UVBacus is called a 5:2 abacus. That means that there are 5 beads on the bottom and 2 beads on the top. The abacus has a wall separating the 5 beads on the bottom and the 2 beads on the top.',
            '3',
            True,
            True, 
            0,
            0,
            0.65,
            0.8,
            0.5,
            0.85,
            1)

    while(not View.mouse_clicked()):
        pass

    View.erase('tutorial')
    View.erase('topbar')
    View.draw_topbar('Andrew', 'Admin Settings - Create User')
    View.draw_create_class()

    while(not View.mouse_clicked()):
        pass

    View.erase('create_class')
    View.erase('topbar')
    View.draw_topbar('Andrew', 'Admin Settings - Create User')
    View.draw_create_user()

    while(not View.mouse_clicked()):
        pass

    View.erase('create_user')
    View.erase('topbar')

    while(not View.mouse_clicked()):
        pass

    View.close_window()