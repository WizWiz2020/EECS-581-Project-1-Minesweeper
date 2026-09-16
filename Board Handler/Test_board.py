import minesweeper2 as ms

def print_grid(reveal_all=False): #function to print the grid
    print("X 0 1 2 3 4 5 6 7 8 9") #prints header
    for y in range(ms.GRID_HEIGHT): #itrates through the rows
        row = str(y) + " " #prints row number
        for x in range(ms.GRID_WIDTH): #iterates through the columns
            cell = ms.grid[y][x] #sets x and y equal to cell
            if cell.is_flagged and not reveal_all: #checks if cell is flagged and not revealed
                symbol = "F"
            elif not cell.is_revealed and not reveal_all: #sets cell symbol if not revealed
                symbol = "*"
            elif cell.is_mine: #sets cell symbol to mine if mine is true
                symbol = "M"
            elif cell.adjacent_mines == 0: #sets cell symbol blank if adjacent mines is and been revealed
                symbol = "."
            else: #sets cell symbol to number of adjacent mines if revealed
                symbol = str(cell.adjacent_mines)
            row += symbol + " " #spacing between symbols
        print(row) #prints row
    print()


if __name__ == "__main__": #main function to run the game
    print("Starting Minesweeper with this many mines: ", ms.NUM_MINES)
    first_click = True #Varaible to check if first click
    
    while True: #while statement to handle user input and game looping
        try: #try except block for x and y inputs
            if first_click: #first click statement
                print("Enter first cell click coords: ") #prompt
                x = int(input("Enter x coordinate: ")) #x coord input
                y = int(input("Enter y coordinate: ")) # y coord input
                ms.onLeftClick(x, y) #calls minesweeper.py's left click function
                first_click = False #sets first click to fale
                if ms.grid[y][x].is_mine: #checks if first click si a mine, set to auto fail right now
                        print_grid(reveal_all=True) #reveals the grid when fail
                        break #ends loop
            else: #if not first click then prompts user for input and flagging
                num_mines_remain = ms.mines_remaining
                print("Number of mines remaining: ", num_mines_remain) #prints number of mines remaining
                action = input("Enter p to pick a cell, f to flag a cell or rf to remove a flag: ") #asks for either click or flag
                x = int(input("Enter x coordinate: ")) #x coord input
                y = int(input("Enter y coordinate: ")) #y coord input
                if action == "p": #p for pick, calls left click function
                    ms.onLeftClick(x, y)
                    if ms.grid[x][y].is_mine and ms.grid[x][y].is_flagged: #checks if the cell is a mine and hasn't been flagged yet, if flagged it wont kill program
                        print_grid(reveal_all=True)
                        break
                elif action == "f": #f for flag, calls right click function
                    ms.onRightClick(x, y)
                elif action == "rf": #remove flag, its same as to place but for user sake it makes sense
                    ms.onRightClick(x, y)
                else: #catch miss inputs
                    print("Unknown command")
                    continue
        except ValueError: #except block for errors in input
            print("Invalid input.")
            continue

        print_grid() #prints grid after each action
        print_grid(reveal_all=True) #reveals grid unhiddden for testing
        if ms.game_state.get_game_status() == ms.game_state.VICTORY: #checks victory condition
            print("Congratulations! You've won the game!")
            break