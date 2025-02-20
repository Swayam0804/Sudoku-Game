import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import messagebox

# Generate a predefined Sudoku grid with some empty spaces
def generate_sudoku():
    return np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])

# Full solution of the board for hints
solution = np.array([
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
])

# Check if a given number can be placed in the specified position
def is_valid(board, row, col, num):
    if num in board[row, :]: return False  # Check row
    if num in board[:, col]: return False  # Check column
    box_x, box_y = (row // 3) * 3, (col // 3) * 3
    if num in board[box_x:box_x+3, box_y:box_y+3]: return False  # Check 3x3 box
    return True

def solve_sudoku(board):
    empty_pos = find_empty_position(board)
    if not empty_pos:
        return True  # Puzzle solved

    row, col = empty_pos
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row, col] = num
            if solve_sudoku(board):
                return True
            board[row, col] = 0  # Backtrack Algorithm

    return False

def find_empty_position(board):
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                return (i, j)
    return None

mistakes = 0
hints_used = 0

# Draw Sudoku Board
def draw_sudoku(board):
    global mistakes, hints_used
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='#f0f0f0')
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Center the grid properly
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(10))
    ax.set_yticks(np.arange(10))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(left=False, bottom=False)
    ax.grid(True, linewidth=1, color='gray')
    ax.set_title("Sudoku", fontsize=30, fontweight='bold', color='#ff5733')
    
    # Ensure square shape
    ax.set_aspect('equal')
    
    # Draw bold grid lines for 3x3 sections
    for i in range(0, 10, 3):
        ax.axhline(i, color='#222222', linewidth=3)
        ax.axvline(i, color='#222222', linewidth=3)
    
    # Fill board with numbers and shaded blocks
    for i in range(9):
        for j in range(9):
            if (i // 3 + j // 3) % 2 == 0:
                ax.add_patch(Rectangle((j, 8 - i), 1, 1, color='#d3d3d3', alpha=0.5))
            if board[i, j] != 0:
                ax.text(j + 0.5, 8.5 - i, str(board[i, j]), fontsize=14,
                        ha='center', va='center', color='#004488')

    def onclick(event):
            global mistakes, hints_used
            if event.xdata is not None and event.ydata is not None:
                col, row = int(event.xdata), 8 - int(event.ydata)
                if board[row, col] == 0:
                    root = tk.Tk()
                    root.withdraw()  # Hide it initially
            
                    try:
                          # Ensure no other window is holding a grab
                          root.grab_release()
                          # Create the input dialog
                          dialog = tk.Toplevel()
                          dialog.title("Sudoku Input")
                          dialog.geometry("300x150")  # Set a fixed size to prevent resizing issues
                 
                          tk.Label(dialog, text=f"Enter number (1-9) for ({row+1}, {col+1}):").pack(pady=5)
                          entry_var = tk.StringVar()
                          entry = tk.Entry(dialog, textvariable=entry_var)
                          entry.pack(pady=5)

                          def submit():
                                global mistakes  # Access mistakes variable
                                num = entry_var.get() # Retrieve input safely
                                if num.isdigit():  # Validate input
                                     num = int(num)
                                     if num == solution[row, col]:  # Check against the solution
                                         board[row, col] = num
                                         messagebox.showinfo("Correct", "Number added to the board.")
                                         dialog.destroy()
                                         update_board(board, ax)  # Update the board
                                     else:
                                           mistakes += 1
                                           if mistakes >= 5:
                                                 messagebox.showerror("Game Over", "You have made 5 mistakes. Game Over!")
                                                 dialog.destroy()
                                           else:
                                                 messagebox.showerror("Invalid Move", f"Invalid move. Mistakes: {mistakes}/5")
                                                 dialog.destroy()

                          # Function to provide a hint
                          def get_hint():
                                global hints_used
                                if hints_used >= 5:
                                     messagebox.showwarning("Hint Limit Reached", "You have used all 5 hints.")
                                     return

                                correct_num= solution[row,col]

                                if board[row,col] == 0:
                                          board[row, col] = correct_num  # Show correct number
                                          hints_used += 1

                                          messagebox.showinfo(title="Hint", message=f"Hint Used: {hints_used}/5\nCorrect number: {correct_num}")
                                          update_board(board, ax)  # Update only the existing figure without closing it
                                          dialog.destroy()

                          # Buttons for Submit and Hint
                          button_frame = tk.Frame(dialog)
                          button_frame.pack(pady=5)

                          submit_button = tk.Button(button_frame, text="Submit", command=submit)
                          submit_button.pack(side=tk.LEFT, padx=10)

                          hint_button = tk.Button(button_frame, text="Hint", command=get_hint)
                          hint_button.pack(side=tk.RIGHT, padx=10)              

                          dialog.grab_set()  # Set grab to this dialog
                          dialog.mainloop()

                    except Exception as e:
                           print(f"Error: {e}")
                    finally:
                           root.destroy()

            elif event.button == 3:  # Right-click to solve the puzzle
                if solve_sudoku(board):
                    messagebox.showinfo("Sudoku Solved", "The puzzle has been solved!")
                    update_board(board, ax)
                else:
                    messagebox.showerror("No Solution", "No solution exists for the given board.")
    
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    plt.ioff()

def update_board(board, ax):
    ax.clear()
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(10))
    ax.set_yticks(np.arange(10))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, linewidth=1, color='gray')
    ax.set_title("Sudoku", fontsize=30, fontweight='bold', color='#ff5733')
    ax.set_aspect('equal')
    
    for i in range(0, 10, 3):
        ax.axhline(i, color='#222222', linewidth=3)
        ax.axvline(i, color='#222222', linewidth=3)

    for i in range(9):
        for j in range(9):
            if (i // 3 + j // 3) % 2 == 0:
                ax.add_patch(Rectangle((j, 8 - i), 1, 1, color='#d3d3d3', alpha=0.5))
            if board[i, j] != 0:
                ax.text(j + 0.5, 8.5 - i, str(board[i, j]), fontsize=14,
                        ha='center', va='center', color='#004488')

    plt.draw()

sudoku_board = generate_sudoku()
draw_sudoku(sudoku_board)
