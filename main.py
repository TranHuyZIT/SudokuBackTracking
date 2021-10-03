import random
import pygame

# Init Pygame
WIDTH = 540 # Board Width
MENU = 200 # Menu Width
ROWS = 9 # 9x9 Grid Board
WIN = pygame.display.set_mode((WIDTH + MENU,WIDTH))
pygame.display.set_caption("Solve Sudoku With Backtracking")
pygame.init()

# Color RGB
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
BTN = (82, 183, 233)
BTN_HOV = (24, 157, 228)
WHITE = (255, 255, 255)
MAIN = (119, 114, 226)
BLACK = (0, 0, 0)
GRIDLINE = (36, 36, 68)
GRIDLINETHIN = (70, 100, 140)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Classes:
class Cell:
    def __init__(self, row, col, num):
        self.color = MAIN
        self.num = num
        self.gap = WIDTH // ROWS
        self.x = col * self.gap + MENU
        self.y = row * self.gap

    def draw(self):
        if self.num != 0:
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(str(self.num), True, self.color)
            WIN.blit(text, (self.x + (self.gap / 2 - text.get_width() / 2), self.y + (self.gap / 2 - text.get_height() / 2)))


    def switch_color(self):
        if self.color == MAIN:
            self.color = GREEN
        else:
            self.color = GREEN

class Button:
    def __init__(self, color, x, y,width, height,text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win, outline = None):
        if outline:  # Draw ouline
            pygame.draw.rect(win, outline, (self.x - 2,self.y - 2 ,self.width + 4, self.height + 4),0)
        pygame.draw.rect(win, self.color,(self.x, self.y, self.width,self.height), 0)
        if self.text != "":
            font = pygame.font.SysFont('comicsans',30)
            text = font.render(self.text,True,BLACK)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/ 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

class Menu:
    def __init__(self):
        self.x = MENU
        self.y = WIDTH
        self.bgColor = GREY
        self.btnColor = BTN
        self.start = Button(self.btnColor,30, 100,140,80,'Start')
        self.custom = Button(self.btnColor,self.start.x, self.start.y + 100, 140,80,'Custom')
        self.exit = Button(self.btnColor,self.custom.x, self.custom.y + 100, 140,80,'Exit')
    
    def draw(self):
        font = pygame.font.SysFont('comicsans',80)
        text = font.render('MENU',True,MAIN)
        WIN.blit(text,(20,20,100,100))
        self.start.draw(WIN,BLACK)
        self.custom.draw(WIN, BLACK)
        self.exit.draw(WIN, BLACK)

    def checkHover(self, pos):
        if (self.start.is_over(pos)):
            self.start.color = BTN_HOV
        else:
            self.start.color = self.btnColor
        
        if (self.custom.is_over(pos)):
            self.custom.color = BTN_HOV
        else:
            self.custom.color = self.btnColor
        
        if (self.exit.is_over(pos)):
            self.exit.color = BTN_HOV
        else:
            self.exit.color = self.btnColor
    
    def solveClick(self, pos, board, menu ,num):
        if solve(num,board, menu):
            WIN.fill(WHITE)
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render("SOLVED!", True, RED)
            WIN.blit(text, (0 + ((WIDTH + MENU) / 2 - text.get_width() / 2), 0 + ((WIDTH) / 2 - text.get_height() / 2)))
            pygame.display.update()
            pygame.time.wait(3000)
    
    def customClick(self,pos,board,menu):
        return customInput()

# Input Handling:
def drawBoardInput(board, current_pos, btn):
    # Draw Title
    WIN.fill(WHITE)
    font = pygame.font.SysFont('comicsans', 40)
    text = font.render("Custom Mode", True, MAIN)
    WIN.blit(text, (5,100))
    
    # Draw Button
    btn.draw(WIN, BLACK)
    # Draw Gridlines:
    draw_gridlines()

    # Draw Tiles:
    for row in board:
        for cell in row:
            cell.draw()
    gap = WIDTH // ROWS
    if (current_pos[0] < ROWS and current_pos[0] >= 0) and (current_pos[1] < ROWS and current_pos[1] >= 0):
        current = board[current_pos[0]][current_pos[1]]
        pygame.draw.rect(WIN,RED, (current.x,current.y, gap,gap),width=5)

def customInput():
    # Draw Empty Screen
    run = True
    num = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]
    board = make_board(num)
    current = (0,0)
    enter = Button(BTN, 10,200, 180,80,'ENTER')
    while(run):
        m_pos = pygame.mouse.get_pos()
        drawBoardInput(board, current, enter)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if enter.is_over(m_pos):
                enter.color = BTN_HOV
            else:
                enter.color = BTN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # LEFT
                    if (current[1] > 0):
                        current = (current[0],current[1] - 1)
                elif event.key == pygame.K_RIGHT: # RIGHT
                    if (current[1] < ROWS - 1):
                        current = (current[0],current[1] + 1)
                elif event.key == pygame.K_UP: # UP
                    if (current[0] > 0):
                        current = (current[0] - 1,current[1])
                elif event.key == pygame.K_DOWN: # DOWN
                    if (current[0] < ROWS - 1):
                        current = (current[0] + 1,current[1])
                elif event.key == pygame.K_1:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 1)
                    num[current[0]][current[1]] = 1
                elif event.key == pygame.K_2:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 2)
                    num[current[0]][current[1]] = 2
                elif event.key == pygame.K_3:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 3)
                    num[current[0]][current[1]] = 3
                elif event.key == pygame.K_4:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 4)
                    num[current[0]][current[1]] = 4
                elif event.key == pygame.K_5:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 5)
                    num[current[0]][current[1]] = 5
                elif event.key == pygame.K_6:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 6)
                    num[current[0]][current[1]] = 6
                elif event.key == pygame.K_7:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 7)
                    num[current[0]][current[1]] = 7
                elif event.key == pygame.K_8:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 8)
                    num[current[0]][current[1]] = 8
                elif event.key == pygame.K_9:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 9)
                    num[current[0]][current[1]] = 9
                elif event.key == pygame.K_BACKSPACE:
                    board[current[0]][current[1]] = Cell(current[0],current[1], 0)
                elif event.key == pygame.K_SPACE:
                    return num, board
            if pygame.mouse.get_pressed()[0]:
                m_pos = pygame.mouse.get_pos()
                if (enter.is_over(m_pos)):
                    return num,board
# Solve Utilities: 
def solve(num,bo, menu):
    find = find_empty(num)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        draw(bo, menu)
        if valid(num, i, (row, col)):
            num[row][col] = i
            (bo[row][col]).num = i
            (bo[row][col]).switch_color()

            if solve(num,bo, menu):
                return True

            num[row][col] = 0
            (bo[row][col]).num = 0
            (bo[row][col]).switch_color()


    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

# Initialize new board
def make_board(num):
    board = []
    for row in range(ROWS):
        board.append([])
        for col in range(ROWS):
            cell = Cell(row, col, num[row][col])
            board[row].append(cell)

    return board

# Draw:
def draw_gridlines():
    gap = WIDTH // ROWS
    for i in range(ROWS + 1):
        if i % 3 ==0:
            pygame.draw.line(WIN, GRIDLINE, (MENU, i * gap), (WIDTH + MENU, i * gap),4)
        else:
            pygame.draw.line(WIN, GRIDLINETHIN, (MENU, i * gap), (WIDTH + MENU, i * gap),3)
        for j in range(ROWS + 1):
            if j % 3 ==0:
                pygame.draw.line(WIN, GRIDLINE, (j * gap + MENU, 0), (j * gap + MENU, WIDTH),4)
            else:
                pygame.draw.line(WIN, GRIDLINETHIN, (j*gap + MENU, 0), (j*gap + MENU, WIDTH),3)

def draw(board, menu):
    WIN.fill(WHITE)
    for row in board:
        for cell in row:
            cell.draw()
    
    menu.draw()
    draw_gridlines()
    pygame.display.update()

# Main 
def main():
    num = [
        [7,8,0,4,0,0,1,2,0],
        [6,0,0,0,7,5,0,0,9],
        [0,0,0,6,0,1,0,7,8],
        [0,0,7,0,4,0,2,6,0],
        [0,0,1,0,5,0,9,3,0],
        [9,0,4,0,6,0,0,0,5],
        [0,7,0,3,0,0,0,1,2],
        [1,2,0,0,0,7,4,0,0],
        [0,4,9,2,0,6,0,0,7]
    ]
    run = True
    menu = Menu()
    board = make_board(num)
    while run:
        draw(board, menu)
        m_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            menu.checkHover(m_pos)
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                m_pos = pygame.mouse.get_pos()
                if menu.exit.is_over(m_pos):
                    run = menu.exitClick(m_pos)
                elif menu.custom.is_over(m_pos):
                    num, board = menu.customClick(m_pos,board,menu)
                elif menu.start.is_over:
                    menu.solveClick(m_pos,board,menu, num)

if __name__ =="__main__":
    main()