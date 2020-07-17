# -*- coding: utf-8 -*-
'''
Author: Jonathan Cen
'''
import pygame
# Initialize pygame
pygame.init()
'''Define Colors'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 150, 0)
RED = (255, 0, 0)
LIGHT_RED = (150, 0, 0)
BLUE = (0,0,255)
LIGHT_BLUE = (0,0,150)
'''Width, height, and Margin of each grid'''
WIDTH = 50
HEIGHT = 50
MARGIN = 8
NUM_OF_GRIDS = 8

GRID_WIDTH = ((MARGIN + WIDTH)*NUM_OF_GRIDS + MARGIN)
# Set the HEIGHT and WIDTH of the screen
WINDOW_WIDTH = int(((WIDTH + MARGIN)*NUM_OF_GRIDS + MARGIN) * 2.5)
WINDOW_HEIGHT = (HEIGHT + MARGIN)*NUM_OF_GRIDS + MARGIN

'''Initialize the fonts for this program'''
generalFont = pygame.font.Font('freesansbold.ttf', WINDOW_WIDTH//30) 
buttonFont = pygame.font.Font('freesansbold.ttf', WINDOW_WIDTH//40)

#Text margins
TEXT_MARGIN = 0.05*(WINDOW_WIDTH - GRID_WIDTH)


#Button variables
button_width = WINDOW_WIDTH//6
button_height = WINDOW_WIDTH//40 + 10
button_x_calculate = GRID_WIDTH + WINDOW_WIDTH//20 #GRID_WIDTH + (WINDOW_WIDTH - GRID_WIDTH)//2 - button_width//2
button_x_reset = int(WINDOW_WIDTH * (4/5))
button_y = WINDOW_HEIGHT//2


def createInitializedPathArray(rows, cols, initValue = 0):
    new_array = []
    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append(initValue)
        new_array.append(new_row)
    return new_array
#Using Dynamic Programming to find the number of paths
def countingPath(grid, row, col, paths):
    if(not validSquare(grid, row, col)):
        return 0
    if(isAtEnd(grid, row, col)):
        return 1
    if(paths[row][col] == 0):
        paths[row][col] = countingPath(grid, row + 1, col, paths) + countingPath(grid, row, col + 1, paths)
    return paths[row][col]

def validSquare(grid, row, col):
    try:
        return grid[row][col] >= 0
    except(IndexError):
        return False

def isAtEnd(grid, row, col):
    try:
        return grid[row][col] == 2
    except(IndexError):
        return False

def countPath(grid):
    start_row = 0
    start_col = 0
    empty = createInitializedPathArray(NUM_OF_GRIDS, NUM_OF_GRIDS)
    return countingPath(grid, start_row, start_col, empty)
    


def getGrid(NUM_OF_GRIDS):     
    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    
    grid = []
    for row in range(NUM_OF_GRIDS):
        grid.append([])
        for column in range(NUM_OF_GRIDS):
            grid[row].append(0)
     
    #Set the end position to red
    grid[-1][-1] = 2
    #Set the start position to blue
    grid[0][0] = 1
    return grid

def showText(screen, message, x, y):
    textSurf = buttonFont.render(message, True, WHITE) 
    textRect = textSurf.get_rect()  
    textRect.center = (x, y) ## (distance from left, distance from top)
    screen.blit(textSurf, textRect)


def blit_text(screen, message, startPosition):
    words = message.split(' ')
    space = generalFont.size(' ')[0]
    max_width = WINDOW_WIDTH - 30
    x,y = startPosition
    for word in words:
        word_surface = generalFont.render(word, True, WHITE)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width:
            x = startPosition[0]
            y += word_height #start a new row
        screen.blit(word_surface, (x, y))
        x += word_width + space
        
def displayButton(screen):
    #Buttons on Screen
        
    mouse = pygame.mouse.get_pos()
    
    if(mouse[0] >= button_x_calculate and mouse[0] <= button_x_calculate + button_width and mouse[1] >= button_y and mouse[1] <= button_y + button_height):
        pygame.draw.rect(screen, GREEN, (button_x_calculate, button_y,button_width,button_height))
    else:
        pygame.draw.rect(screen, LIGHT_GREEN, (button_x_calculate, button_y,button_width,button_height))
    
    showText(screen, "Calculate", button_x_calculate + button_width/2, button_y + button_height/2 + 2)
    
    if(mouse[0] >= button_x_reset and mouse[0] <= button_x_reset + button_width and mouse[1] >= button_y and mouse[1] <= button_y + button_height):
        pygame.draw.rect(screen, RED, (button_x_reset, button_y,button_width,button_height))
    else:
        pygame.draw.rect(screen, LIGHT_RED, (button_x_reset, button_y,button_width,button_height))
    showText(screen, "Reset", button_x_reset + button_width/2, button_y + button_height/2 + 2)

def calculateClicked(pos):
    if(pos[0] >= button_x_calculate and pos[0] <= button_x_calculate + button_width and pos[1] >= button_y and pos[1] <= button_y + button_height):
        return True
    return False

def resetClicked(pos):
    if(pos[0] >= button_x_reset and pos[0] <= button_x_reset + button_width and pos[1] >= button_y and pos[1] <= button_y + button_height):
        return True
    return False
    
def gameLoop():
    grid = getGrid(NUM_OF_GRIDS)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
     
    # Set title of screen window
    pygame.display.set_caption("Count Paths From Blue to Red")
    
    EXIT = False
    paths = None
    clock = pygame.time.Clock()
     
    # -------- Main Program Loop -----------
    while not EXIT:
        screen.fill(BLACK)
        intro_message = "Please specify obstacles by clicking on the grid. Obstacles are coloured in green."
        blit_text(screen, intro_message, (GRID_WIDTH + TEXT_MARGIN, TEXT_MARGIN))
        displayButton(screen)
        
        
        #screen.blit(text, textRect)
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                EXIT = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                #Check if the user clicks the Calculate button:
                if(calculateClicked(pos)):
                    paths = countPath(grid)
                if(resetClicked(pos)):
                    grid = getGrid(NUM_OF_GRIDS)
                    paths = None
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                try:
                    if(grid[row][column] == 0):
                        grid[row][column] = -1
                    elif(grid[row][column] == -1): #allow the user to unselect an obstacle
                        grid[row][column] = 0
                except(IndexError):
                    continue        
        
        if paths == None:
            result_message = "Number of paths from blue to red: " 
        else:
            result_message = "Number of paths from blue to red: " + str(paths)
        blit_text(screen, result_message, (GRID_WIDTH + TEXT_MARGIN, WINDOW_HEIGHT*4/5))
        
        
        
        # Draw the grid
        for row in range(NUM_OF_GRIDS):
            for column in range(NUM_OF_GRIDS):
                color = WHITE
                if grid[row][column] == -1:
                    color = GREEN
                elif grid[row][column] == 2:
                    color = RED
                elif grid[row][column] == 1:
                    color = BLUE
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
        
        
     
    
        clock.tick(60)
        pygame.display.update()
    
    

gameLoop()
pygame.quit()
