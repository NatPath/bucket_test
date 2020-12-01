import xlsxwriter
import tkinter as tk
import time
from random import *
from math import *
from functools import partial
#main function , open tkinter windows and sets them to full screen.
#Also creates a canvas and draws an arrow on it, with its base in the middle of the screen
#creates a binding function which reads scrolling events on the canvas, scrolling input leads to the function mouse_wheel
#the function mouse_wheel moves the tip of the arrow line acordingly, scroll up moves the line in an angle which encloses it to the right, scroll down does the opposite
#creates a mouse_click function, which saves the current angle in the line details in its class, and counts untill 3 clicks, so we can sum the results
#created the global variables, they might be primitive but they are usefull
def main():
    #counts the number of clicks, so we can use the mouse_click function with out adding arguements. primitive but effective.
    global number
    #actually has no use, it counts the 'state' of the scroll wheel, a scrollup will add 1 and a scrolldown will subtract 1.
    global count
    #user global variable so all functions can call and change it.
    global user
    global start_time
    start_time=time.time()
    user = user_id()
    number=0
    radius= 300
    #angle_const=100
    angle=150
    #randint(-angle_const, angle_const)
    count = angle
    win = tk.Tk()
    win.title("The Whirly Dirly")
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    canvas = tk.Canvas(win,width=screen_width,height=screen_height)
    canvas.pack(fill="both",expand=True)
    win.attributes('-fullscreen',True)
    canvas.config(bd=0)   
    canvas['bg'] = 'white'
    axis = point(screen_width/2,screen_height/2)
    global line1
    new_point = correlate_angle_to_peripheral(axis,radius,angle)
    line_bit = create_line_by_two_points(canvas,axis,new_point)
    line1= line(canvas,axis,new_point,line_bit,radius,angle)
    iconify_window_wrapper = partial(iconify_window,win)
    win.bind("<ButtonRelease-1>",mouse_click)
    win.bind("<ButtonRelease-3>",iconify_window_wrapper)
    win.bind("<Escape>",iconify_window_wrapper)
    win.bind("<MouseWheel>",mouse_wheel)
    win.mainloop()
def iconify_window(win,event):
    win.iconify()
#gets a canvas and two points, creates a line accordingly on the canvas between the two points, the line has spesifics on an arrow on his LAST end.
#returns the line and draws it
def create_line_by_two_points(canvas,axis,new_point):
    lastendX=2*axis.getX()-new_point.getX()
    lastendY=2*axis.getY()-new_point.getY()
    line = canvas.create_line(lastendX,lastendY,new_point.getX(),new_point.getY(),smooth=1,splinesteps=1,dash=(1,1),width=1)
    return line
#a class for the arrow line spesifics, a line is drawn on a 'canvas', from 'point1' to 'point2'.
# the 'line_bit' is important so we can erase the line whenever we want.
#the radius is the length of the line
#angle is the angle of it duhh
class line():
    def __init__(self,canvas,point1,point2,line_bit,radius,angle):
        self.canvas=canvas
        self.point1=point1
        self.point2=point2
        self.angle=angle
        self.line_bit=line_bit
        self.radius=radius
        self.timestamps=[]
    def get_point1(self):
        return self.point1
    def get_point2(self):
        return self.point2
    def set_point1(self,point1):
        self.point1=point1
    def set_point2(self,point2):
        self.point2=point2
    def create_line_by_two_points(self,canvas,axis,new_point):
        lastendX=2*axis.getX()-new_point.getX()
        lastendY=2*axis.getY()-new_point.getY()
        line = self.canvas.create_line(lastendX,lastendY,new_point.getX(),new_point.getY(),smooth=1,splinesteps=1,dash=(1,1),width=1)
        return line
    def delete_line(self):
        self.canvas.delete(line)
    def angle_up(self):
        self.angle+=1
        self.point2= correlate_angle_to_peripheral(self.point1,self.radius,self.angle)
        self.render_line()
        current_time=time.time()-start_time
        time_stamp=timeStamp(self.angle,current_time)
        self.timestamps.append(time_stamp)
    def angle_down(self):
        self.angle-=1
        self.point2= correlate_angle_to_peripheral(self.point1,self.radius,self.angle)
        self.render_line()
        current_time=time.time()-start_time
        time_stamp=timeStamp(self.angle,current_time)
        self.timestamps.append(time_stamp)
    def angle_random(self):
        new_angle= randint(-100, 100)
        self.angle=new_angle
        self.point2= correlate_angle_to_peripheral(self.point1,self.radius,self.angle)
        self.render_line()
    def render_line(self):
        self.canvas.delete(self.line_bit)
        self.line_bit=self.create_line_by_two_points(self.canvas,self.point1,self.point2)
    def print_timestamps(self):
        name_of_file=user.name+' whirly dirly test'+'.xlsx'
        workbook=xlsxwriter.Workbook(name_of_file)
        table=workbook.add_worksheet()
        headline_format=workbook.add_format()
        headline_format.set_bg_color('red')
        headline_format.set_bold()
        headline_format.set_font_size(20)
        headline_format.set_font_color('white')
        data_text_format=workbook.add_format()
        data_text_format.set_align('center')
        #table.write_number(Y,X,data)
        i=1
        print(" $$$$$$$$$$$$$$$$$$$$$$$$$ ")
        print ("The time Stamps are:- ")
        table.write(0,1,'time(sec)',headline_format)
        for timestamp in self.timestamps:
            timedata=timestamp.getTime()
            print(timedata)
            table.write_number(i,1,timedata,data_text_format)
            table.write_number(i,0,i-1,data_text_format)
           # print("__________________________")
           # print("time stamp number", i)
           # timestamp.print_data()
            i=i+1
        print(" $$$$$$$$$$$$$$$$$$$$$$$$$ ")
        print ("The angles are:- ")
        table.write(0,2,'angle(deg)',headline_format)
        j=1
        for timestamp in self.timestamps:    
            angledata=timestamp.getAngle()/10
            print(angledata)
            table.write_number(j,2,angledata,data_text_format)
            j=j+1
        print("   Done    ")
        workbook.close
        
                
    
class point():
    def __init__(self,X,Y):
        self.x=X
        self.y=Y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
def correlate_angle_to_peripheral(axis_point,radius,angle):
    axis_x=axis_point.getX()
    axis_y=axis_point.getY()
    angle = angle/10.0
    rad_angle=radians(angle)
    y_plus=radius*cos(rad_angle)
    x_plus=radius*sin(rad_angle)
    new_point = point(axis_x+x_plus,axis_y-y_plus)
    return new_point
def mouse_click(event):
    global number
    number+=1  
    user.new_result(line1.angle)
    line1.angle_random()
    if number==3:
        print("you have clicked ",number," times")
        user.print_results()
def mouse_wheel(event):
    global count
    if number<3:
        if event.num == 5 or event.delta == -120:
            count -= 1
            line1.angle_down()            
        if event.num == 4 or event.delta == 120:
            count += 1
            line1.angle_up()
    else:
        pass

    
class user_id():
    def __init__(self,name,id_number):
        self.name=name
        self.id_number=id_number
        self.results=[]
    def __init__(self):
        details= tk.Tk()
        tk.Label(details, text="Name").grid(row=0)
        tk.Label(details, text="ID").grid(row=1)

        name = tk.Entry(details)
        id_number = tk.Entry(details)
        self.name=name.get()
        self.id_number=id_number.get()
        details_ok_button_wrapper = partial(details_ok_button,details,name,id_number)
        ok_button= tk.Button(details,text="Save",command=details_ok_button_wrapper)
        ok_button.grid(row=3,column=3)

        name.grid(row=0, column=1)
        id_number.grid(row=1, column=1)
        self.results=[]
    def new_result(self,result):
        self.results.append(result)
    def print_results(self):
        print ("Name:- ",self.name ,"\n","ID:- ", self.id_number, "\n" ,"Results:--- ",self.results)
        print ("Your relative average result was:-  ", self.relative_average_result())
        print ("Your absolute average result was:-  ", self.absolute_average_result())
        line1.print_timestamps()
    def set_details(self,name,id_number):
        self.name=name.get()
        self.id_number=id_number.get()
        start_time=time.time()
    def relative_average_result(self):
        result_sum=0
        for result in self.results:
            result_sum+=result
        length= len(self.results)
        average=result_sum/length
        return average
    def absolute_average_result(self):
        result_sum=0
        for result in self.results:
            result_sum+=abs(result)
        length= len(self.results)
        average=result_sum/length
        return average
class timeStamp():
    def __init__(self,angle,time):
        self.angle=angle
        self.time=time
    def getTime(self):
        return self.time
    def getAngle(self):
        return self.angle
    def setTime(self,time):
        self.time=time
    def setAngle(self,angle):
        self.angle=angle
    def print_data(self):
        print("The time:-", self.time)
        print("The angle:-", self.angle)
                  
def details_ok_button(details,name,id_number):
    user.set_details(name,id_number)
    details.destroy()
    
    
main()
