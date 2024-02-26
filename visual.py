import pygame
import main as Chess
import os


# Initialize Pygame
pygame.init()
game_chess = Chess.ChessGame()
# Screen dimensions
WIDTH, HEIGHT = 700, 700
BROWN = (210,180,140)
SAND = (236,204,162)
GRAY = (47,79,79)
RED = (255, 0, 0)

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
    # Black pieces
    "br1": (18.75, 18.75), "bn1": (106.25, 18.75), "bb1": (193.75, 18.75), "bq": (281.25, 18.75),
    "bk": (368.75, 18.75), "bb2": (456.25, 18.75), "bn2": (543.75, 18.75), "br2": (631.25, 18.75),
    "bp1": (18.75, 106.25), "bp2": (106.25, 106.25), "bp3": (193.75, 106.25), "bp4": (281.25, 106.25),
    "bp5": (368.75, 106.25), "bp6": (456.25, 106.25), "bp7": (543.75, 106.25), "bp8": (631.25, 106.25),
    # White pieces
    "wr1": (18.75, 631.25), "wn1": (106.25, 631.25), "wb1": (193.75, 631.25), "wq": (281.25, 631.25),
    "wk": (368.75, 631.25), "wb2": (456.25, 631.25), "wn2": (543.75, 631.25), "wr2": (631.25, 631.25),
    "wp1": (18.75, 543.75), "wp2": (106.25, 543.75), "wp3": (193.75, 543.75), "wp4": (281.25, 543.75),
    "wp5": (368.75, 543.75), "wp6": (456.25, 543.75), "wp7": (543.75, 543.75), "wp8": (631.25, 543.75),


}


# Function to draw the chessboard
def draw_chessboard():
    for i in range(8):
        for j in range(8):
            color = BROWN if (i + j) % 2 == 0 else SAND
            pygame.draw.rect(screen, color, (j * (WIDTH / 8), i * (HEIGHT / 8), WIDTH / 8, HEIGHT / 8))

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
            cell_center = (col * (WIDTH / 8) + (WIDTH / 16), row * (HEIGHT / 8) + (HEIGHT / 16))
            radius = 10  # Adjust the radius as needed
            pygame.draw.circle(screen, GRAY, cell_center, radius)
    except TypeError:
        pass

def draw_piece(new_coordinate):

    if new_coordinate == []:
        return
    WIDTH = 700
    HEIGHT = 700
    x, y = new_coordinate
    WIDTH_BOX = (WIDTH // 8)
    WIDTH_HALF_BOX = WIDTH_BOX//2
    HALF_IMAGE_WIDTH = 50 // 2
    x_coordinate = (y*WIDTH_BOX) + (WIDTH_HALF_BOX - HALF_IMAGE_WIDTH)

    HEIGHT_BOX = HEIGHT/8
    HEIGHT_HALF_BOX = HEIGHT_BOX // 2
    HALF_IMAGE_HEIGHT = 50 // 2
    y_coordinate = (x*HEIGHT_BOX) + (HEIGHT_HALF_BOX - HALF_IMAGE_HEIGHT)
    return x_coordinate, y_coordinate

def draw_box(coordinates):
    row_pixels = coordinates[1] * HEIGHT / 8
    column_pixels = coordinates[0] * WIDTH / 8

    return row_pixels, column_pixels


# MAIN LOOP
squares_to_remove = {}
running = True
hover_start_time = 0
click_count = 0
square_visible = True
squares = {}
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
    valid_moves = game_chess.player_turn(row, col)
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
        try:
            Draw_move, new_xy, taking_piece, piece_being_taken, king_check, king_check_pos = game_chess.update_board(first_click, second_click)

        except TypeError:
            pass

        if king_check:
            pygame.draw.rect(screen, RED, (king_check_pos[1] * WIDTH//8, king_check_pos[0] * HEIGHT//8, WIDTH//8, HEIGHT//8))
        click_count = 0
        first_click = None
        second_click = None
        piece_positions[Draw_move] = new_xy


        if taking_piece:

            row_pixels = new_xy[1] * HEIGHT / 8
            column_pixels = new_xy[0] * WIDTH / 8
            color = BROWN if (row_pixels + column_pixels) % 2 == 0 else SAND
            coordinates_of_shape = (row_pixels, column_pixels , WIDTH/8, HEIGHT/8)
            squares[coordinates_of_shape] = color
            piece_positions.pop(piece_being_taken)

        if Draw_move in white_pieces:
            piece_to_move = white_pieces[Draw_move]
            coordinates = draw_piece(new_xy)
            piece_positions[Draw_move] = coordinates

        elif Draw_move in black_pieces.keys():
            piece_to_move = black_pieces[Draw_move]
            coordinates = draw_piece(new_xy)
            piece_positions[Draw_move] = coordinates

    for cover_square in squares:
        color = squares[cover_square]
        pygame.draw.rect(screen, color, cover_square)
        for piece, position in piece_positions.items():
            if piece.lower().startswith("w"):
                screen.blit(white_pieces[piece], position)
            elif piece.lower().startswith('b'):
                screen.blit(black_pieces[piece], position)



    pygame.display.flip()

pygame.quit()
