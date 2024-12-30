from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math
import time

window_width=500
window_height=500
pause=False
score=0
missed_diamonds=0
game_over=False
speed_diamond=3
x_diamond = (window_width*(time.time()%1))-10
y_diamond=window_height
color_diamond=(0.3, 0.5, 0.7)  
x_catcher=(window_width-100)/2
y_catcher=10
time_limit=30
start_time=time.time()

clouds = []
for i in range(5):
    cloud = {"x": i * (window_width // 5), "y": (window_height // 2) + (i * 10)}
    clouds.append(cloud)

obstacles = []
def draw_point(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_background():
    glBegin(GL_QUADS)
    glColor3f(0.53, 0.81, 0.92)  
    glVertex2f(0, window_height)
    glVertex2f(window_width, window_height)
    glColor3f(0.56, 0.93, 0.56)  
    glVertex2f(window_width, 0)
    glVertex2f(0, 0)
    glEnd()
def draw_cloud(x, y):
    glColor4f(1, 1, 1, 0.8)
    glBegin(GL_POINTS)
    for i in range(100):  
        angle=2*math.pi*random.random()
        radius_x=30*random.uniform(0.8, 1.2)
        radius_y =15*random.uniform(0.8, 1.2)
        glVertex2f(x+radius_x*math.cos(angle),y+radius_y*math.sin(angle))
    glEnd()

def animate_clouds():
    for cloud in clouds:
        cloud["x"]-=1
        if cloud["x"]<-50:
            cloud["x"]=window_width + 50
            cloud["y"]=random.randint(window_height//2,window_height)


def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            zone = 0
        elif dx < 0 and dy > 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx > 0 and dy > 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6

    x1, y1 = zone_0(x1, y1, zone)
    x2, y2 = zone_0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1

    for x in range(int(x1), int(x2)):
        original_x, original_y = original(x, y, zone)
        draw_point(original_x, original_y)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

def zone_0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def original(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_arrow():
    n=20
    teal=(0, 0.8, 0.8)
    draw_line(n, window_height - n, 2 * n, window_height - n, teal)
    draw_line(n, window_height - n, 1.5 * n, window_height - n + 10, teal)
    draw_line(n, window_height - n, 1.5 * n, window_height - n - 10, teal)

def draw_pause():
    n=20
    amber = (1, 0.749, 0)
    if not pause:
        draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 - 5, window_height - n - 10, amber)
        draw_line(window_width / 2 + 5, window_height - n + 10, window_width / 2 + 5, window_height - n - 10, amber)
    else:
        draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 - 5, window_height - n - 10, amber)
        draw_line(window_width / 2 - 5, window_height - n - 10, window_width / 2 + 15, window_height - n, amber)
        draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 + 15, window_height - n, amber)

def draw_cross():
    n=20
    red = (1, 0, 0)
    draw_line(window_width - n, window_height - n + 10, window_width - 2 * n, window_height - n - 10, red)
    draw_line(window_width - n, window_height - n - 10, window_width - 2 * n, window_height - n + 10, red)

def draw_diamond(x, y):
    global color_diamond
    glColor3f(*color_diamond)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + 10, y + 10)
    glVertex2f(x + 20, y)
    glVertex2f(x + 10, y - 10)
    glEnd()


def draw_obstacle(x, y):
    glColor3f(1, 0, 0)
    draw_line(x, y, x + 10, y + 10, (1, 0, 0))
    draw_line(x, y, x + 10, y - 10, (1, 0, 0))
    draw_line(x + 10, y + 10, x + 20, y, (1, 0, 0))
    draw_line(x + 10, y - 10, x + 20, y, (1, 0, 0))

def draw_catcher(x, y, size):
    global game_over, color_diamond
    if not game_over:
        color = [0.6, 0.3, 0]  # Brown color
    else:
        color = [1, 0, 0]  # Red color when game is over
        color_diamond = [0, 0, 0]  # Black for diamonds
    draw_line(x, y + 20, x + size, y + 20, color)
    draw_line(x + 10, y, x + size - 10, y, color)
    draw_line(x, y + 20, x + 10, y, color)
    draw_line(x + size - 10, y, x + size, y + 20, color)


def specialKeyListener(key, x, y):
    global x_catcher
    if not pause and not game_over:
        if key == GLUT_KEY_LEFT:
            x_catcher -= 15
            if x_catcher < 10:
                x_catcher = 10
        elif key == GLUT_KEY_RIGHT:
            x_catcher += 15
            if x_catcher + 100 > window_width - 10:
                x_catcher = (window_width - 10) - 100

def mouseListener(button, state, x, y):
    global x_diamond, y_diamond, speed_diamond, color_diamond, x_catcher, y_catcher, pause, score, game_over, missed_diamonds
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = window_height - y
        n = 30
        if window_height - n - 10 <= y <= window_height - n + 10:
            if n <= x <= 2 * n:
                print('Starting Over')
                x_diamond = random.randint(10, window_width - 30)
                y_diamond = window_height
                speed_diamond = 0.05
                color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))
                missed_diamonds = 0
                x_catcher = (window_width - 100) / 2
                y_catcher = 10
                pause = False
                score = 0
                game_over = False
            elif window_width / 2 - 15 <= x <= window_width / 2 + 15:
                if not pause:
                    pause = True
                else:
                    pause = False
            elif (window_width - 2 * n <= x <= window_width - n):
                print(f'Goodbye! Score: {score}')
                glutLeaveMainLoop()

def check_time_limit():
    global game_over  # Corrected line
    elapsed_time = time.time() - start_time
    if elapsed_time > time_limit:
        print(f"Time's up! Final Score: {score}")
        game_over = True

def animate(x):
    global x_diamond, y_diamond, speed_diamond, color_diamond, score, missed_diamonds, pause, game_over
    if not pause and not game_over:
        y_diamond -= speed_diamond
        for obstacle in obstacles:
            obstacle[1] -= 1  # Move obstacles downward

        # Diamond collision
        if x_catcher <= x_diamond <= x_catcher + 100 and y_catcher <= y_diamond <= y_catcher + 20:
            score += 1
            print(f'Score: {score}')
            x_diamond = random.randint(10, window_width - 30)
            y_diamond = window_height
            speed_diamond += 0.05
            color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))

        if y_diamond < 0:
            missed_diamonds += 1
            if missed_diamonds >= 3:
                game_over = True
                print(f'Game Over! Score: {score}')
            else:
                x_diamond = random.randint(10, window_width - 30)
                y_diamond = window_height

        # Obstacle collision
        for obstacle in obstacles:
            if x_catcher <= obstacle[0] <= x_catcher + 100 and y_catcher <= obstacle[1] <= y_catcher + 20:
                game_over = True
                print(f'Game Over! Hit an obstacle! Score: {score}')

        # Check for time limit
        check_time_limit()
        animate_clouds()
        
    glutTimerFunc(10, animate, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_background()
    for cloud in clouds:
        draw_cloud(cloud["x"], cloud["y"])
    draw_arrow()
    draw_pause()
    draw_cross()
    draw_diamond(x_diamond, y_diamond)
    draw_catcher(x_catcher, y_catcher,100+score//5*20)  
    draw_text(10, window_height - 40, f"Score: {score}")
    draw_text(10, window_height - 60, f"Missed: {missed_diamonds}")
    glutSwapBuffers()

def set_text_color(r, g, b):
    glColor3f(r, g, b)
def set_text_position(x, y):
    glRasterPos2f(x, y)
def render_text(text):
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
def draw_text(x, y, text):
    set_text_color(1, 1, 1) 
    set_text_position(x, y)
    render_text(text)        


glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"OpenGL Game with Features")
glOrtho(0, window_width, 0, window_height, -1, 1)
glClearColor(0, 0, 0, 0)
glutDisplayFunc(display)
glutIdleFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutTimerFunc(10, animate, 0)
glutMainLoop()
