from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

# Global Variables
window_width = 500
window_height = 500

x_diamond = random.randint(10, window_width - 30)
y_diamond = window_height
speed_diamond = 2
color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))

x_catcher = (window_width - 100) / 2
y_catcher = 10

pause = False
score = 0
missed = 0
game_over = False


# Drawing Functions
def draw_point(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_line(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def draw_arrow():
    n = 30
    teal = (0, 0.8, 0.8)
    draw_line(n, window_height - n, 2 * n, window_height - n, teal)
    draw_line(n, window_height - n, 1.5 * n, window_height - n + 10, teal)
    draw_line(n, window_height - n, 1.5 * n, window_height - n - 10, teal)


def draw_pause():
    n = 30
    amber = (1, 0.749, 0)
    if not pause:
        draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 - 5, window_height - n - 10, amber)
        draw_line(window_width / 2 + 5, window_height - n + 10, window_width / 2 + 5, window_height - n - 10, amber)
    else:
        draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 - 5, window_height - n - 10, amber)
        draw_line(window_width / 2 - 5, window_height - n - 10, window_width / 2 + 15, window_height - n, amber)
        draw_line(window_width / 2 - 5, window_height - n + 10, window_width / 2 + 15, window_height - n, amber)


def draw_cross():
    n = 30
    red = (1, 0, 0)
    draw_line(window_width - n, window_height - n + 10, window_width - 2 * n, window_height - n - 10, red)
    draw_line(window_width - n, window_height - n - 10, window_width - 2 * n, window_height - n + 10, red)


def draw_diamond(x, y):
    global color_diamond
    draw_line(x, y, x + 10, y + 10, color_diamond)
    draw_line(x, y, x + 10, y - 10, color_diamond)
    draw_line(x + 10, y + 10, x + 20, y, color_diamond)
    draw_line(x + 10, y - 10, x + 20, y, color_diamond)


def draw_catcher(x, y):
    global game_over, color_diamond
    if not game_over:
        color = [1, 1, 1]
    else:
        color = [1, 0, 0]
        color_diamond = [0, 0, 0]
    draw_line(x, y + 20, x + 100, y + 20, color)
    draw_line(x + 10, y, x + 90, y, color)
    draw_line(x, y + 20, x + 10, y, color)
    draw_line(x + 90, y, x + 100, y + 20, color)


# Text Functions
def set_text_color(r, g, b):
    glColor3f(r, g, b)


def set_text_position(x, y):
    glRasterPos2f(x, y)


def render_text(text):
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_text(x, y, text):
    set_text_color(1, 1, 1)  # White text
    set_text_position(x, y)
    render_text(text)


# Input Listeners
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
    global x_diamond, y_diamond, speed_diamond, color_diamond, x_catcher, y_catcher, pause, score, missed, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = window_height - y
        n = 30
        if window_height - n - 10 <= y <= window_height - n + 10:
            if n <= x <= 2 * n:  # Restart
                x_diamond = random.randint(10, window_width - 30)
                y_diamond = window_height
                speed_diamond = 2
                color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))

                x_catcher = (window_width - 100) / 2
                y_catcher = 10

                pause = False
                score = 0
                missed = 0
                game_over = False
            elif window_width / 2 - 15 <= x <= window_width / 2 + 15:  # Pause/Unpause
                pause = not pause
            elif (window_width - 2 * n <= x <= window_width - n):  # Exit
                print(f'Goodbye! Score: {score}, Missed: {missed}')
                glutLeaveMainLoop()


# Animation and Display
def animate(x):
    global x_diamond, y_diamond, speed_diamond, color_diamond, score, missed, pause, game_over
    if not pause and not game_over:
        y_diamond -= speed_diamond
        if x_catcher <= x_diamond <= x_catcher + 100 and y_catcher <= y_diamond <= y_catcher + 20:
            score += 1
            print(f"Score: {score}")
            x_diamond = random.randint(10, window_width - 30)
            y_diamond = window_height
            speed_diamond += 0.5
            color_diamond = (random.uniform(0.25, 1), random.uniform(0.25, 1), random.uniform(0.25, 1))
        elif y_diamond < 0:
            missed += 1
            print(f"Missed: {missed}")
            x_diamond = random.randint(10, window_width - 30)
            y_diamond = window_height

        if missed >= 3:  # Game over condition
            game_over = True
            print(f"Game Over! Score: {score}, Missed: {missed}")

    glutTimerFunc(10, animate, 0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_arrow()
    draw_pause()
    draw_cross()
    draw_diamond(x_diamond, y_diamond)
    draw_catcher(x_catcher, y_catcher)
    draw_text(10, window_height - 20, f"Score: {score}")  # Display the score
    draw_text(10, window_height - 40, f"Missed: {missed}")  # Display the missed count
    glutSwapBuffers()


# Main Setup
glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"OpenGL Diamond Catcher")
glOrtho(0, window_width, 0, window_height, -1, 1)
glClearColor(0.2, 0.3, 0.4, 1)  # Dark blue-gray background

glutDisplayFunc(display)
glutIdleFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutTimerFunc(10, animate, 0)
glutMainLoop()

