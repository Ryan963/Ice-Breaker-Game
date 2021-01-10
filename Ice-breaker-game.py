# Name: Ryan Thabet
# ID: 3087460


from graphics import *

'''
purpose: create rectangle creates a rectangle object and draw it to the window 
parameters: the window object and the x and y components for the points 
return rectangle object
'''
def create_rectangle(win,x1,y1,x2,y2):
    rect = Rectangle(Point(x1, y1), Point(x2, y2)).draw(win)
    return rect

'''
purpose: creates a rectangle object with a text inside it to function as a button
parameters: window object, x and y for the points, text inside the button
return: rectangle object
'''
def create_Btn(win, x1, y1,x2,y2, txt):
    rect = Rectangle(Point(x1,y1),Point(x2,y2)).draw(win)
    text = Text(Point(x2 - 30,y2 - 10), txt).draw(win)
    return rect

'''
purpose: creates a text object
parameters: window object, x and y for the point where the text is located, the text 
return the text object
'''
def create_message(win, x, y, txt):
    message = Text(Point(x, y), txt).draw(win)
    return message

'''
purpose: create the board for the icebreaker game using the create_rectangle helper function 
parameters: window object
return: list of lists containing every individual square in every row in the board
'''
def create_board(win):
    board = []
    x1, y1 = (0, 0)
    x2, y2 = (50, 50)
    for row in range(8):
        rows = []
        for column in range(10):
            square = create_rectangle(win,x1, y1, x2, y2)
            square.setFill('white')
            x1 += 50
            x2 += 50
            rows.append(square)
        y1 += 50
        y2 += 50
        x1 = 0
        x2 = 50
        board.append(rows)
    return board

'''
purpose: creates 2 image objects for the players and place them in their starting position
parameters: window object
return: a tuple containing the images objects 
'''
def create_players(win):
    player_1 = Image(Point(25,225),"Player_Popeye.gif").draw(win)
    player_2 = Image(Point(475,225),"Player_Brutus.gif").draw(win)
    return player_1, player_2

'''
purpose: checks if the clicked point is in the rectangle passed as parameters
parameters: the licked point, rectangle object
returns true if the point in the rectangle and false if it's not
'''
def in_Rectangle(pt, rect):
    x = pt.getX()
    y = pt.getY()
    firstPt = rect.getP1()
    secondPt = rect.getP2()
    x1, y1 = firstPt.getX(), firstPt.getY()
    x2, y2 = secondPt.getX(), secondPt.getY()
    return (x >= x1 and x <= x2) and (y >= y1 and y <= y2)


'''
purpose: loops throw the board list of lists and check every individual square using in_rectangle to see if the click is 
in the square then it returns the square with the row and column of it
parameters: board, clicked point
return: the clicked square, row, column 
'''
def clicked_square(board,pt):
    count_row = 1
    for row in board:
        count_column = 1
        for column in row:
            if in_Rectangle(pt, column):
                return column, count_row, count_column
            count_column += 1
        count_row += 1


'''
purpose: resets the game   
parameters: window object, the players which are 2 image objects and the board 
return none
'''


def reset(win,player_1,player_2,board, turn):
    player_1.undraw()
    player_2.undraw()
    player_1 = Image(Point(25, 225), "Player_Popeye.gif")
    player_1.draw(win)
    player_2 = Image(Point(475, 225), "Player_Brutus.gif")
    player_2.draw(win)
    turn = 0
    for row in board:
        for column in row:
            column.setFill('white')
    return player_1, player_2, turn


'''
purpose: this function moves the player from it's current position to the square were the clicked happened
parameters: window object, the player which is image object, the new centre point for the image, the name of the image 
return: the player
'''
def move(win,player, pt, name):
    player.undraw()
    player = Image(pt, name)
    player.draw(win)
    return player

'''
purpose: find centre finds the centre of a square and return the point of the centre
paramters: square which is a rectangle object
return centre point
'''
def find_centre(square):
    p1 = square.getP1()
    x1, y1 = p1.getX(), p1.getY()
    return Point(x1 + 25, y1 + 25)


'''
purpose: checks if a move of a player is legal or not
parameters: board list of lists, square were the point clicked,row and column of that square, x and y which are row and column
of the player, the first player image object, the second player image object
return true if move is legal and false if it's not
'''


def check_move(board, square, row, column,x, y, player_1, player_2):
    if square.config['fill'] == 'blue':
        return False
    if clicked_square(board, player_1.getAnchor()) == (square,row,column):
        return False
    if clicked_square(board, player_2.getAnchor()) == (square,row,column):
        return False
    if (row - 1 == x or row + 1 == x or row == x) and (column - 1 == y or column == y or column + 1 == y):
        return True
    return False


'''
purpose: check if ice can be broken in this square
parameters: square of the point clicked, row and column of square, board list of lists, image objects of first and second player
return: true if ice can be broken in this square and false if it cannot
'''
def check_ice(square, row, column,  board, player_1, player_2):
    if clicked_square(board, player_1.getAnchor()) == (square,row,column):
        return False
    if clicked_square(board, player_2.getAnchor()) == (square,row,column):
        return False
    if square.config['fill'] != 'blue':
        return True
    return False


'''
purpose: check turn manages the turns in the game and uses helper functions to act depending on who's turn to do what
parameters: window object,turn, both players image objects, square clicked with it's row and column, text object,the board
return: first player image object,second player image object, turn 
'''
def check_turn(win,turn,player_1, player_2, square, row, column,update_message, board):
    if turn == 0:
        position, x, y = clicked_square(board, player_1.getAnchor())
        if check_move(board, square, row, column, x, y, player_1, player_2):
            player_1 = move(win, player_1, find_centre(square), "Player_Popeye.gif")
            turn += 1
            update_message.setText('Player 0 turn to break ice')
            return player_1,player_2, turn
        else:
            update_message.setText("illegal move try again!")
            return player_1,player_2, turn
    elif turn == 1:
        if check_ice(square, row, column, board, player_1, player_2):
            square.setFill('blue')
            update_message.setText("player 1 turn to move")
            turn += 1
            return player_1, player_2, turn
        else:
            update_message.setText('Cannot break ice on this square')
            return player_1, player_2, turn
    elif turn == 2:
        position, x, y = clicked_square(board, player_2.getAnchor())
        if check_move(board, square, row, column, x, y, player_1, player_2):
            player_2 = move(win, player_2, find_centre(square), "Player_Brutus.gif")
            turn += 1
            update_message.setText("player 1 turn to break ice")
            return player_1,player_2, turn
        else:
            update_message.setText("illegal move try again!")
            return player_1,player_2, turn
    else:
         if check_ice(square, row, column, board, player_1, player_2):
            square.setFill('blue')
            turn = 0
            update_message.setText('Player 0 turn to move ')
            return player_1, player_2, turn
         else:
            update_message.setText('Cannot break ice on this square')
            return player_1, player_2, turn


'''
purpose:takes row and column and return the square object where that row and column is
parameters: board list of lists, tuple of row and column
return: square object
'''
def find_coord(board, coord):
    count_row = 1
    for row in board:
        count_column = 1
        for column in row:
            if coord == (count_row, count_column):
                return column
            count_column += 1
        count_row += 1
    return None


'''
purpose: checks if the player is trapped and can't make any more moves
parameters: player image object, board lol, the other player's image object
return: true if player is trapped and false if he's not
'''
def is_trapped(player,board, opponent):
    position_1,row, column = clicked_square(board, player.getAnchor())
    position_2, x, y = clicked_square(board,opponent.getAnchor())
    adjacent = [(row - 1, column - 1), (row, column - 1), (row, column + 1), (row - 1, column), (row + 1,column), (row + 1,column + 1), (row - 1, column + 1), (row + 1, column - 1)]
    if (x, y) in adjacent:
        adjacent.remove((x, y))

    for coord in adjacent:
        square = find_coord(board, coord)
        if square == None:
            pass
        elif square.config['fill'] != 'blue':
            return False
    return True


'''
purpose: create 2 buttons with text inside for the start window and the window that declares the winner
parameters: window object, text inside first button, text inside second button
return first button object, second button object
'''
def player_options(win, first_text, second_text):
    first_btn = create_rectangle(win, 70, 80, 160, 110)
    create_message(win, 115, 95, first_text)
    second_btn = create_rectangle(win, 70, 140, 160, 170)
    create_message(win, 115, 155, second_text)
    return first_btn, second_btn
'''
purpose: opens a new window when one player is trapped and announce the winner in this new window
parameters: the winner player, name of the player
return: true if player wants to reset game and false to to exit
'''
def declare_winner(player, name):
    win = GraphWin('Winner', 250, 250)
    win.setBackground('red')
    message = create_message(win, 125, 50, f"Player {name} is the winner")
    reset_btn, exit_btn = player_options(win, "Reset Game", 'Exit Game')
    while True:
        try:
            pt = win.getMouse()
        except:
            win.close()
        if in_Rectangle(pt, reset_btn):
            win.close()
            return True
        elif in_Rectangle(pt, exit_btn):
            win.close()
            return False


'''
purpose: main creates a window object and uses the helper functions to creates the ice breaker game and check where the mouse click
has occurred and acts accordingly using the helper functions. 
parameters: none
return none
'''



def main():
    start_win = GraphWin('start game',250, 250)
    start_win.setBackground('blue')
    start_btn, exit_btn = player_options(start_win, "Play Game", "Exit Game")
    while True:
        try:
            click = start_win.getMouse()
        except:
            start_win.close()
        if in_Rectangle(click, start_btn):
            start_win.close()
            break
        elif in_Rectangle(click, exit_btn):
            start_win.close()
            return
    win = GraphWin('Ice Breaker', 500, 500)
    quit_btn = create_Btn(win,420,430,480,450,'QUIT')
    reset_btn = create_Btn(win,420,455,480,475,"RESET")
    board_rect = Rectangle(Point(0,0),Point(500,400))
    update_msg = create_message(win,150,430,"PLAYER: 0")
    board = create_board(win)
    player_1, player_2 = create_players(win)
    turn = 0
    while True:
        try:
            pt = win.getMouse()
        except:
            win.close()
        if in_Rectangle(pt, board_rect):
            square, row, column = clicked_square(board, pt)
            player_1, player_2, turn = check_turn(win,turn, player_1, player_2, square, row, column, update_msg, board)
            if is_trapped(player_1,board,player_2):
                winner = declare_winner(player_2, 'P2')
                if winner == True:
                    player_1, player_2, turn = reset(win, player_1, player_2, board, turn)
                else:
                    win.close()
            elif is_trapped(player_2, board, player_1):
                winner = declare_winner(player_1,'P1')
                if winner:
                    player_1, player_2, turn = reset(win, player_1, player_2, board,turn)
                else:
                    win.close()
        elif in_Rectangle(pt, reset_btn):
            player_1, player_2, turn= reset(win,player_1, player_2, board, turn)
            update_msg.setText('RESET')
        elif in_Rectangle(pt, quit_btn):
            update_msg.setText("BYE BYE")
            break
        else:
            x, y = pt.getX(), pt.getY()
            update_msg.setText(f"Click at {x, y}")
    try:
        pt = win.getMouse()
        win.close()
    except:
        win.close()



main()