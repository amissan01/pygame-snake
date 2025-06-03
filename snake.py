import pygame, sys, random
from pygame.math import Vector2

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        
    def update(self):
        self.snake.move_snake()  # Move the snake in the update method
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.fruit.draw()
        self.snake.draw_snake()
        self.draw_score()  # Draw the score on the screen
    
    def check_collision(self):
        if self.fruit.pos.distance_to(self.snake.body[0]) < 1:  # Checks if the snake's head touches the fruit
            self.fruit.randomize()
            self.snake.add_block()
    
    def check_fail(self):
        # Check if the snake's head is out of bounds
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        # Check if the snake collides with itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        pygame.quit()
        sys.exit()
    
    def draw_score(self):
        score_text = str(len(self.snake.body)-3)  # The score is the length of the snake minus initial 3 blocks
        score_surface = game_font.render(score_text, True,(0, 0, 0) )  # Peach color for score
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)  # Draw the score on the screen at the bottom-right corner

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # Snake body segments in grid coordinates
        self.direction = Vector2(1, 0)  # Initial direction: moving to the right
        self.new_block = False
        
    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * cell_size  # Convert x-coordinate to pixels
            y_pos = block.y * cell_size  # Convert y-coordinate to pixels
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color("purple"), block_rect)  # Draw each block
    
    def move_snake(self):
        if self.new_block:
            # If the snake is growing, don't remove the last segment
            body_copy = self.body[:]  # Copy the entire body
            body_copy.insert(0, body_copy[0] + self.direction)  # Add a new head in the direction of movement
            self.body = body_copy[:]
            self.new_block = False  # Reset after adding a block
        else:
            # Normal snake movement without growing
            body_copy = self.body[:-1]  # Copy all but the last segment
            body_copy.insert(0, body_copy[0] + self.direction)  # Add a new head in the direction of movement
            self.body = body_copy[:]  # Update snake body to include new head

    def add_block(self):
        self.new_block = True  # Flag to add a new block
    
    def change_direction(self, new_direction):
        # Avoid the snake going back on itself
        if self.direction.x == 0 and new_direction.x != 0:  # Moving vertically, can change to horizontal
            self.direction = new_direction
        elif self.direction.y == 0 and new_direction.y != 0:  # Moving horizontally, can change to vertical
            self.direction = new_direction

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw(self):
        fruit_rect = pygame.Rect(
            self.pos.x * cell_size,  # X position in pixels
            self.pos.y * cell_size,  # Y position in pixels
            cell_size,               # Width of the fruit
            cell_size                # Height of the fruit
        )
        pygame.draw.rect(screen, pygame.Color("skyblue"), fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 25)  # Font file location (no need for a custom font)

# Set a timer event for the screen update
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # Set timer to trigger every 150ms

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Ensures the program exits completely
        
        # Timer to trigger update every 150ms
        if event.type == SCREEN_UPDATE:
            main_game.update()

        # Handle keypress to change snake's direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:  # Prevent reversing direction
                    main_game.snake.change_direction(Vector2(0, -1))
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:  # Prevent reversing direction
                    main_game.snake.change_direction(Vector2(0, 1))
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:  # Prevent reversing direction
                    main_game.snake.change_direction(Vector2(-1, 0))
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:  # Prevent reversing direction
                    main_game.snake.change_direction(Vector2(1, 0))

    # Clear the screen each frame
    screen.fill(pygame.Color("pink"))  # Fill the screen with pink

    # Draw the fruit and the snake
    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)  # Limit the loop to 60 FPS
