import pygame
import main as Chess
import os


# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 700
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chessboard")

base_path = '/Users/keeganhill/PycharmProjects/chess/Pieces'
# File paths for chess piece images
white_piece_files = {
    "wk": os.path.join(base_path, "w_king.png"),
    "wq": os.path.join(base_path, "w_queen.png"),
    "wr1": os.path.join(base_path, "w_rook.png"),
    "wr2": os.path.join(base_path, "w_rook.png"),
    "wb1": os.path.join(base_path, "w_bishop.png"),
    "wb2": os.path.join(base_path, "w_bishop.png"),
    "wn1": os.path.join(base_path, "w_knight.png"),
    "wn2": os.path.join(base_path, "w_knight.png"),
    "wp1": os.path.join(base_path, "w_pawn.png"),
    "wp2": os.path.join(base_path, "w_pawn.png"),
    "wp3": os.path.join(base_path, "w_pawn.png"),
    "wp4": os.path.join(base_path, "w_pawn.png"),
    "wp5": os.path.join(base_path, "w_pawn.png"),
    "wp6": os.path.join(base_path, "w_pawn.png"),
    "wp7": os.path.join(base_path, "w_pawn.png"),
    "wp8": os.path.join(base_path, "w_pawn.png")
}

black_piece_files = {
    "bk": os.path.join(base_path, "b_king.png"),
    "bq": os.path.join(base_path, "b_queen.png"),
    "br1": os.path.join(base_path, "b_rook.png"),
    "br2": os.path.join(base_path, "b_rook.png"),
    "bb1": os.path.join(base_path, "b_bishop.png"),
    "bb2": os.path.join(base_path, "b_bishop.png"),
    "bn1": os.path.join(base_path, "b_knight.png"),
    "bn2": os.path.join(base_path, "b_knight.png"),
    "bp1": os.path.join(base_path, "b_pawn.png"),
    "bp2": os.path.join(base_path, "b_pawn.png"),
    "bp3": os.path.join(base_path, "b_pawn.png"),
    "bp4": os.path.join(base_path, "b_pawn.png"),
    "bp5": os.path.join(base_path, "b_pawn.png"),
    "bp6": os.path.join(base_path, "b_pawn.png"),
    "bp7": os.path.join(base_path, "b_pawn.png"),
    "bp8": os.path.join(base_path, "b_pawn.png")
}

# Load chess piece images for white pieces and rescale them
white_pieces = {piece: pygame.transform.scale(pygame.image.load(file), (50, 50)) for piece, file in white_piece_files.items()}

# Load chess piece images for black pieces and rescale them
black_pieces = {piece: pygame.transform.scale(pygame.image.load(file), (50, 50)) for piece, file in black_piece_files.items()}

# Initial positions of chess pieces
piece_positions = {
    # White pieces
    "wk": (350, 650), "wq": (250, 650), "wr1": (50, 650), "wr2": (650, 650),
    "wb1": (150, 650), "wb2": (550, 650), "wn1": (450, 650), "wn2": (350, 650),
    "wp1": (50, 550), "wp2": (150, 550), "wp3": (250, 550), "wp4": (350, 550),
    "wp5": (450, 550), "wp6": (550, 550), "wp7": (650, 550), "wp8": (750, 550),
    # Black pieces
    "bk": (350, 50), "bq": (250, 50), "br1": (50, 50), "br2": (650, 50),
    "bb1": (150, 50), "bb2": (550, 50), "bn1": (450, 50), "bn2": (350, 50),
    "bp1": (50, 150), "bp2": (150, 150), "bp3": (250, 150), "bp4": (350, 150),
    "bp5": (450, 150), "bp6": (550, 150), "bp7": (650, 150), "bp8": (750, 150)
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
dict = {}

# Function to draw the chessboard
def draw_chessboard():
    for i in range(8):
        for j in range(8):
            color = WHITE if (i + j) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (j * (WIDTH // 8), i * (HEIGHT // 8), WIDTH // 8, HEIGHT // 8))

# Function to get array position from mouse position
def get_array_position(mouse_pos):
    col = mouse_pos[0] // (WIDTH // 8)
    row = mouse_pos[1] // (HEIGHT // 8)
    return row, col

# Function to draw valid move regions
def draw_valid_move_regions(valid_moves):
    try:
        for move in valid_moves:
            row, col = move
            pygame.draw.rect(screen, RED, (col * (WIDTH // 8), row * (HEIGHT // 8), WIDTH // 8, HEIGHT // 8))
    except TypeError:
        pass

def draw_piece( new_coordinate):

    WIDTH = 700
    HEIGHT = 700
    x, y = new_coordinate
    WIDTH_BOX = (WIDTH / 8)
    WIDTH_HALF_BOX = WIDTH_BOX/2
    HALF_IMAGE_WIDTH = 50 / 2
    x_coordinate = (y*WIDTH_BOX) + (WIDTH_HALF_BOX - HALF_IMAGE_WIDTH)

    HEIGHT_BOX = HEIGHT/8
    HEIGHT_HALF_BOX = HEIGHT_BOX / 2
    HALF_IMAGE_HEIGHT = 50 / 2
    y_coordinate = (x*HEIGHT_BOX) + (HEIGHT_HALF_BOX - HALF_IMAGE_HEIGHT)

    print(f'{x_coordinate}, {y_coordinate}')
    return x_coordinate, y_coordinate

# Instantiate Chess_Game object
game_chess = Chess.Chess_Game()





# Main loop
running = True
hover_start_time = 0
click_count = 0
while running:
    screen.fill(GRAY)

    # Draw the chessboard
    draw_chessboard()

    # Blit (draw) chess piece images onto the screen
    for piece, position in piece_positions.items():
        if piece.lower().startswith("w"):
            screen.blit(white_pieces[piece], position)
        elif piece.lower().startswith('b'):
            screen.blit(black_pieces[piece], position)




        # Update valid move regions
    mouse_pos = pygame.mouse.get_pos()
    row, col = get_array_position(mouse_pos)
    valid_moves = game_chess.Player_Turn(row, col)
    draw_valid_move_regions(valid_moves)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_count == 0:
                first_click = get_array_position(pygame.mouse.get_pos())
                click_count += 1
            elif click_count == 1:
                second_click = get_array_position(pygame.mouse.get_pos())
                click_count += 1

    # Print first_click and second_click when click_count is equal to 2
    if click_count == 2:

        Draw_move = game_chess.update_board(first_click, second_click)
        # Reset variables for the next pair of clicks
        click_count = 0
        first_click = None
        second_click = None

    pygame.display.flip()

pygame.quit()
