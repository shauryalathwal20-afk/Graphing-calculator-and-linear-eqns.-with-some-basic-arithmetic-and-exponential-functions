import pygame
import sys
import math

# Initialize Canvas Framework
pygame.init()
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nexus-OS: Visual Matrix & Graphing Math Core")
clock = pygame.time.Clock()

# Neon Palette Architecture
BG_DARK = (10, 12, 22)
PANEL_BG = (18, 22, 38)
GRID_LINE = (28, 34, 56)
TEXT_BRIGHT = (0, 255, 190)
ACCENT_BLUE = (0, 160, 255)
ACCENT_PINK = (255, 0, 128)
WHITE = (240, 245, 250)

# Typography Layouts
font_btn = pygame.font.SysFont("Segoe UI", 15, bold=True)
font_display = pygame.font.SysFont("Lucida Console", 22, bold=True)
font_title = pygame.font.SysFont("Segoe UI", 16, bold=True)
font_small = pygame.font.SysFont("Segoe UI", 12)

# Global Application Configurations
calc_expression = ""
calc_result = "0"
graph_function = "x**2 - 4"
graph_scale = 20.0  # Pixels per mathematical step unit

# System Mode state machine: 0 = Scientific Calc & Graphing, 1 = Matrix Solver
active_mode = 0  

# Matrix Equation Variables (Up to 4 Variables: Ax + By + Cz + Dw = E)
matrix_size = 3  # Toggles dynamically between 2, 3, 4
# Form structure: [ [A, B, C, D, E], ... ] max 4 rows, 5 columns
matrix_data = [[0.0 for _ in range(5)] for _ in range(4)]
matrix_focus_row = 0
matrix_focus_col = 0

# Build Button Array layouts for the Scientific Deck
buttons = [
    ('7', 30, 140), ('8', 95, 140), ('9', 160, 140), ('/', 225, 140), ('C', 290, 140),
    ('4', 30, 195), ('5', 95, 195), ('6', 160, 195), ('*', 225, 195), ('sin', 290, 195),
    ('1', 30, 250), ('2', 95, 250), ('3', 160, 250), ('-', 225, 250), ('cos', 290, 250),
    ('0', 30, 305), ('.', 95, 305), ('+', 160, 305), ('=', 225, 305), ('tan', 290, 305),
    ('x', 30, 360), ('**', 95, 360), ('log', 160, 360), ('ln', 225, 360), ('sqrt', 290, 360)
]

def evaluate_scientific(expr):
    """Safely evaluates text expressions converting syntax to mathematical operations."""
    try:
        # Standardize formatting for python parsing evaluation
        safe_expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
        safe_expr = safe_expr.replace('log', 'math.log10').replace('ln', 'math.log').replace('sqrt', 'math.sqrt')
        if not safe_expr.strip(): return "0"
        return str(eval(safe_expr))
    except:
        return "SYNTAX ERROR"

def calculate_determinant(matrix):
    """Calculates matrix determinants using recursive cofactor expansion formulas."""
    n = len(matrix)
    if n == 1: return matrix[0][0]
    if n == 2: return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0.0
    for col in range(n):
        sub_mat = [row[:col] + row[col+1:] for row in matrix[1:]]
        det += ((-1)**col) * matrix[0][col] * calculate_determinant(sub_mat)
    return det

def solve_linear_system(size, data):
    """Resolves dynamic linear equations systems using Cramer's Rule Matrix Operations."""
    try:
        # Extract coefficient matrix A and constants vector B
        A = [[data[r][c] for c in range(size)] for r in range(size)]
        B = [data[r][size] for r in range(size)]
        
        main_det = calculate_determinant(A)
        if abs(main_det) < 1e-9:
            return "NO UNIQUE SOL (DET=0)"
            
        results = []
        labels = ['x', 'y', 'z', 'w']
        
        # Swap constant columns recursively to find individual matrix variables
        for i in range(size):
            A_temp = [row[:] for row in A]
            for r in range(size):
                A_temp[r][i] = B[r]
            var_det = calculate_determinant(A_temp)
            results.append(f"{labels[i]}={round(var_det / main_det, 3)}")
            
        return ", ".join(results)
    except Exception as e:
        return "SOLVER ERROR"

while True:
    clock.tick(60)
    screen.fill(BG_DARK)
    mx, my = pygame.mouse.get_pos()
    
    # -----------------------------------------------------------------
    # GLOBAL NAVIGATION HEADER TABS
    # -----------------------------------------------------------------
    pygame.draw.rect(screen, PANEL_BG, (0, 0, WIDTH, 50))
    pygame.draw.line(screen, GRID_LINE, (0, 50), (WIDTH, 50), 2)
    
    # Tab 1 Trigger Box
    tab1_rect = pygame.Rect(20, 10, 240, 32)
    t1_color = ACCENT_BLUE if active_mode == 0 else PANEL_BG
    pygame.draw.rect(screen, t1_color, tab1_rect, border_radius=4)
    screen.blit(font_title.render("[1] SCIENTIFIC & GRAPHING", True, WHITE), (35, 16))
    
    # Tab 2 Trigger Box
    tab2_rect = pygame.Rect(280, 10, 240, 32)
    t2_color = ACCENT_PINK if active_mode == 1 else PANEL_BG
    pygame.draw.rect(screen, t2_color, tab2_rect, border_radius=4)
    screen.blit(font_title.render("[2] N-VARIABLE SYSTEM SOLVER", True, WHITE), (295, 16))

    # -----------------------------------------------------------------
    # MODE 0: SCIENTIFIC CALCULATOR INTERACTIVE PANEL & GRAPHING ENGINE
    # -----------------------------------------------------------------
    if active_mode == 0:
        # Left Side Display Screen Card
        pygame.draw.rect(screen, PANEL_BG, (20, 70, 340, 55), border_radius=6)
        pygame.draw.rect(screen, GRID_LINE, (20, 70, 340, 55), 1, border_radius=6)
        
        # Display inputs and calculations strings
        screen.blit(font_small.render("MATH INPUT:", True, ACCENT_BLUE), (30, 75))
        screen.blit(font_display.render(calc_expression[-18:], True, WHITE), (30, 92))
        
        # Result panel monitor container
        pygame.draw.rect(screen, PANEL_BG, (20, 425, 340, 45), border_radius=6)
        screen.blit(font_small.render("CORE OUTPUT READOUT:", True, ACCENT_PINK), (30, 430))
        screen.blit(font_display.render(calc_result[:18], True, TEXT_BRIGHT), (30, 445))
        
        # Plot Graph Instructions Card Info
        pygame.draw.rect(screen, PANEL_BG, (20, 485, 340, 195), border_radius=6)
        pygame.draw.rect(screen, ACCENT_BLUE, (20, 485, 340, 195), 1, border_radius=6)
        instructions = [
            "2D COORDINATE ENGINE ACTIVE",
            f"Active Equation: y = {graph_function}",
            "Click [X] on keypad to write equations.",
            "Press [ENTER] to plot input onto graph.",
            "Use [UP/DOWN Arrow Keys] to scaling ZOOM."
        ]
        for i, txt in enumerate(instructions):
            color = ACCENT_BLUE if i == 0 else WHITE
            screen.blit(font_small.render(txt, True, color), (35, 500 + (i * 24)))

        # Draw Calculator Interactive Numeric Grid Deck Buttons
        for btn_text, bx, by in buttons:
            btn_rect = pygame.Rect(bx, by, 55, 45)
            is_hover = btn_rect.collidepoint(mx, my)
            b_color = ACCENT_BLUE if is_hover else PANEL_BG
            
            pygame.draw.rect(screen, b_color, btn_rect, border_radius=4)
            pygame.draw.rect(screen, GRID_LINE, btn_rect, 1, border_radius=4)
            
            txt_surf = font_btn.render(btn_text, True, WHITE if not is_hover else BG_DARK)
            screen.blit(txt_surf, (bx + (55 - txt_surf.get_width()) // 2, by + 13))

        # --- GRAPH VIEWPORT MATRIX CANVAS ---
        graph_x, graph_y, graph_w, graph_h = 390, 70, 680, 610
        pygame.draw.rect(screen, PANEL_BG, (graph_x, graph_y, graph_w, graph_h), border_radius=6)
        
        cx, cy = graph_x + graph_w // 2, graph_y + graph_h // 2
        
        # Draw Cartesian coordinate framework background reference line patterns
        for gx in range(graph_x, graph_x + graph_w, int(graph_scale)):
            pygame.draw.line(screen, GRID_LINE, (gx, graph_y), (gx, graph_y + graph_h), 1)
        for gy in range(graph_y, graph_y + graph_h, int(graph_scale)):
            pygame.draw.line(screen, GRID_LINE, (graph_x, gy), (graph_x + graph_w, gy), 1)
            
        # Draw X and Y Intercept Main Axis Crosshairs
        pygame.draw.line(screen, ACCENT_BLUE, (cx, graph_y), (cx, graph_y + graph_h), 2)
        pygame.draw.line(screen, ACCENT_BLUE, (graph_x, cy), (graph_x + graph_w, cy), 2)

        # Plot Mathematical Calculation Function Coordinates dynamically onto Screen Grid
        points = []
        for px in range(graph_x, graph_x + graph_w, 2):
            math_x = (px - cx) / graph_scale
            try:
                # Format layout strings safely for parsing evaluation arrays
                math_expr = graph_function.replace('sin', 'math.sin').replace('cos', 'math.cos')
                math_expr = math_expr.replace('tan', 'math.tan').replace('sqrt', 'math.sqrt')
                
                # Context evaluate using math_x step positions
                math_y = eval(math_expr, {"x": math_x, "math": math})
                py = cy - int(math_y * graph_scale)
                
                if graph_y <= py <= graph_y + graph_h:
                    points.append((px, py))
            except:
                pass # Skip broken calculations like asymptotes or imaginary square roots
                
        if len(points) > 1:
            pygame.draw.lines(screen, ACCENT_PINK, False, points, 3)

    # -----------------------------------------------------------------
    # MODE 1: N-VARIABLE ADVANCED ALGEBRA MATRIX SYSTEM SOLVER
    # -----------------------------------------------------------------
    elif active_mode == 1:
        pygame.draw.rect(screen, PANEL_BG, (20, 70, 1060, 610), border_radius=8)
        screen.blit(font_display.render("MULTI-VARIABLE LINEAR EQUATION SOLVER MATRIX", True, ACCENT_PINK), (50, 95))
        
        # Render Selection Size Controls
        screen.blit(font_title.render("SELECT MATRIX DIMENSIONS (VARIABLES):", True, WHITE), (50, 145))
        for size_opt in [2, 3, 4]:
            box_x = 420 + ((size_opt - 2) * 80)
            box_rect = pygame.Rect(box_x, 140, 60, 30)
            is_active = (matrix_size == size_opt)
            pygame.draw.rect(screen, ACCENT_BLUE if is_active else BG_DARK, box_rect, border_radius=4)
            screen.blit(font_btn.render(f"{size_opt}x{size_opt}", True, WHITE), (box_x + 15, 145))

        screen.blit(font_small.render("Use Arrow Keys [UP/DOWN/LEFT/RIGHT] to navigate grids. Type numbers directly. Press [BACKSPACE] to clear numbers.", True, TEXT_BRIGHT), (50, 195))

        # Render Equation Input Field Grids dynamically based on variables sizes selected
        labels = ['X', 'Y', 'Z', 'W']
        for r in range(matrix_size):
            y_pos = 240 + (r * 65)
            # Display tracking prefix indicators
            screen.blit(font_title.render(f"EQ {r+1}:", True, ACCENT_BLUE), (50, y_pos + 12))
            
            for c in range(matrix_size + 1):
                x_pos = 130 + (c * 150)
                cell_rect = pygame.Rect(x_pos, y_pos, 100, 40)
                is_focused = (matrix_focus_row == r and matrix_focus_col == c)
                
                pygame.draw.rect(screen, BG_DARK, cell_rect, border_radius=4)
                pygame.draw.rect(screen, ACCENT_PINK if is_focused else GRID_LINE, cell_rect, 1 if not is_focused else 2, border_radius=4)
                
                # Draw the numerical value inside the cell array matrix
                val_str = str(matrix_data[r][c])
                if val_str.endswith(".0"): val_str = val_str[:-2] # Flatten trailing decimals visually
                screen.blit(font_title.render(val_str, True, WHITE), (x_pos + 10, y_pos + 8))
                
                # Print Variable Label suffixes (like '+ Bx')
                if c < matrix_size:
                    screen.blit(font_title.render(labels[c], True, TEXT_BRIGHT), (x_pos + 110, y_pos + 10))
                    if c < matrix_size - 1:
                        screen.blit(font_title.render("+", True, WHITE), (x_pos + 132, y_pos + 10))
                else:
                    screen.blit(font_title.render("=", True, WHITE), (x_pos - 25, y_pos + 10))

        # Perform calculations and output solution parameters down below
        pygame.draw.rect(screen, BG_DARK, (50, 540, 1000, 80), border_radius=6)
        screen.blit(font_title.render("ALGEBRA CORE RESOLUTION ENGINE OUTPUT SOLUTIONS:", True, ACCENT_BLUE), (70, 555))
        
        system_solution = solve_linear_system(matrix_size, matrix_data)
        screen.blit(font_display.render(system_solution, True, TEXT_BRIGHT), (70, 580))

    # -----------------------------------------------------------------
    # CAPTURE MOUSE / KEYBOARD STRING INTERFACE EVENTS
    # -----------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Handle Tab Swapping clicks
                if tab1_rect.collidepoint(mx, my): active_mode = 0
                if tab2_rect.collidepoint(mx, my): active_mode = 1
                
                if active_mode == 0:
                    # Parse Scientific Calculator click arrays
                    for btn_text, bx, by in buttons:
                        if pygame.Rect(bx, by, 55, 45).collidepoint(mx, my):
                            if btn_text == 'C':
                                calc_expression = ""
                                calc_result = "0"
                            elif btn_text == '=':
                                calc_result = evaluate_scientific(calc_expression)
                                # If expression contains variable 'x', transfer to graphing core
                                if 'x' in calc_expression:
                                    graph_function = calc_expression
                            else:
                                calc_expression += btn_text
                                
                elif active_mode == 1:
                    # Switch matrix array selection dimensions sizes on click bounding boxes
                    for size_opt in [2, 3, 4]:
                        box_x = 420 + ((size_opt - 2) * 80)
                        if pygame.Rect(box_x, 140, 60, 30).collidepoint(mx, my):
                            matrix_size = size_opt
                            matrix_focus_row, matrix_focus_col = 0, 0

        elif event.type == pygame.KEYDOWN:
            # Global Layout Toggle shortcuts
            if event.key == pygame.K_1: active_mode = 0
            if event.key == pygame.K_2: active_mode = 1
            
            if active_mode == 0:
                if event.key == pygame.K_UP: graph_scale = min(100.0, graph_scale + 5.0)
                elif event.key == pygame.K_DOWN: graph_scale = max(5.0, graph_scale - 5.0)
                elif event.key == pygame.K_RETURN: # Process whatever expression is typed to the grapher
                    if calc_expression:
                        graph_function = calc_expression
                        calc_result = "PLOTTED TO VECTOR GRAPH"
                elif event.key == pygame.K_BACKSPACE: calc_expression = calc_expression[:-1]
                else:
                    if event.unicode.isprintable() and len(calc_expression) < 30:
                        # Append keyboard typing arrays directly into expressions entries
                        if event.unicode in "0123456789+-*/.x()":
                            calc_expression += event.unicode
                            
            elif active_mode == 1:
                # Arrow key matrix box traversal mechanics
                if event.key == pygame.K_RIGHT: matrix_focus_col = min(matrix_size, matrix_focus_col + 1)
                elif event.key == pygame.K_LEFT: matrix_focus_col = max(0, matrix_focus_col - 1)
                elif event.key == pygame.K_DOWN: matrix_focus_row = min(matrix_size - 1, matrix_focus_row + 1)
                elif event.key == pygame.K_UP: matrix_focus_row = max(0, matrix_focus_row - 1)
                
                # Direct entry array editing inside matrix cells
                elif event.key == pygame.K_BACKSPACE:
                    matrix_data[matrix_focus_row][matrix_focus_col] = 0.0
                else:
                    char = event.unicode
                    if char in "0123456789.-":
                        curr_val = str(matrix_data[matrix_focus_row][matrix_focus_col])
                        if curr_val == "0.0": curr_val = ""
                        try:
                            # Build decimal layout strings dynamically
                            if char == "-" and not curr_val: new_val = "-"
                            else: new_val = curr_val + char
                            
                            if new_val == "-": matrix_data[matrix_focus_row][matrix_focus_col] = -0.0
                            else: matrix_data[matrix_focus_row][matrix_focus_col] = float(new_val)
                        except:
                            pass

    pygame.display.flip()