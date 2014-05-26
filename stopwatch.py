# template for "Stopwatch: The Game"
import simpleguitk as simplegui
# define global variables
CANVAS_HEIGHT = 200
CANVAS_WIDTH = 400
FONT_SIZE = 24
FONT_SIZE_SCORE = 12
timer_counter = 0
success_counter = 0
stop_counter =0
is_whole_second = 0
timer_is_stopped = 0

# define helper function format that converts time
def convert(number):
    return str(number)
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global is_whole_second
    A = t//600
    B = (t-600*A)//100
    C = (t-600*A - B*100)//10
    D = (t-600*A)%10
    formatted_time = str(A)+":"+str(B)+str(C)+"."+str(D) 
    if t !=0 and C==0:
        is_whole_second = 1
    else: is_whole_second = 0
    return formatted_time
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global is_whole_second
    global timer_is_stopped
    timer_is_stopped = 0
    is_whole_second = 0
    timer.start()
    return
def stop_handler():
    global stop_counter
    global success_counter
    global timer_is_stopped
    
    timer.stop()
        
    if not timer_is_stopped:
       stop_counter +=1
       if is_whole_second:
            success_counter+=1
    
    print success_counter,stop_counter,format(timer_counter)
    timer_is_stopped = 1
    return

def reset_handler():
    global timer_counter
    global stop_counter
    global success_counter
    global timer_is_stopped
  
    timer.stop()
    timer_counter = 0
    stop_counter = 0
    success_counter = 0
    timer_is_stopped = 1
    return      
# define event handler for timer with 0.1 sec interval
def timerhandler():
    global timer_counter
    timer_counter +=1
    return
# define draw handler    
def draw_handler(canvas):
    canvas.draw_text(format(timer_counter), (CANVAS_WIDTH//2, CANVAS_HEIGHT//2), FONT_SIZE, "Red")
    score="Score: "+ convert(success_counter)+"/"+ convert(stop_counter)
    canvas.draw_text(score, (10,20), FONT_SIZE_SCORE, "White")




    
# create frame
frame = simplegui.create_frame("Stopwatch", CANVAS_WIDTH, CANVAS_HEIGHT)

# register event handlers

timer = simplegui.create_timer(10, timerhandler)
frame.set_draw_handler(draw_handler)
start_button = frame.add_button("Start", start_handler, 100)
stop_button = frame.add_button("Stop", stop_handler, 100)
reset_button = frame.add_button("Reset", reset_handler, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
