import pygame
import numpy as np
import random
from enum import Enum
from typing import List, Tuple, Optional
import colorsys

class CellType(Enum):
    EMPTY = 0
    DATA = 1
    FIREWALL = 2
    VIRUS = 3
    ANTIVIRUS = 4
    ENCRYPTED = 5

class GameMode(Enum):
    CLASSIC = "classic"
    HACKING = "hacking"
    DEFENSE = "defense"
    ATTACK = "attack"

class HackingGameOfLife:
    def __init__(self, width=80, height=60, cell_size=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = np.zeros((height, width), dtype=int)
        self.next_grid = np.zeros((height, width), dtype=int)
        
        # Game state
        self.generation = 0
        self.score = 0
        self.energy = 100
        self.game_mode = GameMode.HACKING
        self.running = False
        self.paused = False
        self.selected_tool = CellType.DATA
        
        # Hacking mechanics
        self.firewall_strength = {}
        self.virus_spread_rate = 1.0
        self.antivirus_effectiveness = 0.8
        self.encrypted_cells = set()
        
        # Visual settings
        self.colors = {
            CellType.EMPTY: (10, 10, 20),
            CellType.DATA: (0, 255, 100),
            CellType.FIREWALL: (255, 100, 0),
            CellType.VIRUS: (255, 0, 100),
            CellType.ANTIVIRUS: (0, 100, 255),
            CellType.ENCRYPTED: (255, 255, 0)
        }
        
        # Initialize pygame
        pygame.init()
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size + 100  # Extra space for UI
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Hacking Game of Life")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Initialize with some patterns
        self.initialize_patterns()
    
    def initialize_patterns(self):
        """Initialize the grid with interesting patterns"""
        # Add some data clusters
        for _ in range(5):
            x, y = random.randint(10, self.width-10), random.randint(10, self.height-10)
            self.add_glider(x, y, CellType.DATA)
        
        # Add some viruses
        for _ in range(3):
            x, y = random.randint(10, self.width-10), random.randint(10, self.height-10)
            self.add_block(x, y, CellType.VIRUS)
        
        # Add firewall barriers
        for _ in range(2):
            x, y = random.randint(5, self.width-15), random.randint(5, self.height-15)
            self.add_line_horizontal(x, y, 10, CellType.FIREWALL)
    
    def add_glider(self, x, y, cell_type):
        """Add a glider pattern at position (x, y)"""
        pattern = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]
        self.add_pattern(x, y, pattern, cell_type)
    
    def add_block(self, x, y, cell_type):
        """Add a block pattern at position (x, y)"""
        pattern = [
            [1, 1],
            [1, 1]
        ]
        self.add_pattern(x, y, pattern, cell_type)
    
    def add_line_horizontal(self, x, y, length, cell_type):
        """Add a horizontal line"""
        for i in range(length):
            if 0 <= x + i < self.width and 0 <= y < self.height:
                self.grid[y, x + i] = cell_type.value
    
    def add_pattern(self, x, y, pattern, cell_type):
        """Add a pattern to the grid"""
        for dy, row in enumerate(pattern):
            for dx, cell in enumerate(row):
                if cell and 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    self.grid[y + dy, x + dx] = cell_type.value
    
    def count_neighbors(self, x, y, cell_type=None):
        """Count neighbors of a specific type or all non-empty cells"""
        count = 0
        type_counts = {ct: 0 for ct in CellType}
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor_type = CellType(self.grid[ny, nx])
                    type_counts[neighbor_type] += 1
                    if neighbor_type != CellType.EMPTY:
                        count += 1
        
        if cell_type:
            return type_counts[cell_type]
        return count, type_counts
    
    def apply_hacking_rules(self, x, y, current_type, neighbor_counts):
        """Apply hacking-specific rules to cell evolution"""
        total_neighbors, type_counts = neighbor_counts
        current_cell = CellType(current_type)
        
        # Special rules for different cell types
        if current_cell == CellType.DATA:
            # Data cells survive with 2-3 neighbors, can be converted by viruses
            virus_neighbors = type_counts[CellType.VIRUS]
            if virus_neighbors >= 2:
                return CellType.VIRUS.value  # Infected by virus
            elif 2 <= total_neighbors <= 3:
                return CellType.DATA.value
            else:
                return CellType.EMPTY.value
                
        elif current_cell == CellType.VIRUS:
            # Viruses are aggressive and spread easily
            if 1 <= total_neighbors <= 4:
                return CellType.VIRUS.value
            else:
                return CellType.EMPTY.value
                
        elif current_cell == CellType.FIREWALL:
            # Firewalls are defensive and stable
            firewall_neighbors = type_counts[CellType.FIREWALL]
            if firewall_neighbors >= 2:
                return CellType.FIREWALL.value
            elif total_neighbors >= 4:
                return CellType.EMPTY.value  # Overwhelmed
            else:
                return CellType.FIREWALL.value
                
        elif current_cell == CellType.ANTIVIRUS:
            # Antivirus cells combat viruses
            virus_neighbors = type_counts[CellType.VIRUS]
            if virus_neighbors >= 3:
                return CellType.VIRUS.value  # Overwhelmed
            elif 2 <= total_neighbors <= 3:
                return CellType.ANTIVIRUS.value
            else:
                return CellType.EMPTY.value
                
        elif current_cell == CellType.ENCRYPTED:
            # Encrypted cells are very stable
            return CellType.ENCRYPTED.value
            
        else:  # EMPTY
            # Birth rules based on neighbors
            if type_counts[CellType.DATA] >= 3:
                return CellType.DATA.value
            elif type_counts[CellType.VIRUS] >= 2:
                return CellType.VIRUS.value
            elif type_counts[CellType.ANTIVIRUS] >= 3:
                return CellType.ANTIVIRUS.value
            elif type_counts[CellType.FIREWALL] >= 4:
                return CellType.FIREWALL.value
            else:
                return CellType.EMPTY.value
    
    def update(self):
        """Update the grid according to Game of Life rules with hacking mechanics"""
        if self.paused:
            return
        
        self.generation += 1
        
        # Calculate next state
        for y in range(self.height):
            for x in range(self.width):
                current_type = self.grid[y, x]
                neighbor_counts = self.count_neighbors(x, y)
                self.next_grid[y, x] = self.apply_hacking_rules(x, y, current_type, neighbor_counts)
        
        # Swap grids
        self.grid, self.next_grid = self.next_grid, self.grid.copy()
        
        # Update score based on cell counts
        self.update_score()
        
        # Check win/lose conditions
        self.check_game_state()
    
    def update_score(self):
        """Update score based on current grid state"""
        unique, counts = np.unique(self.grid, return_counts=True)
        cell_counts = dict(zip(unique, counts))
        
        # Score calculation based on game mode
        if self.game_mode == GameMode.HACKING:
            self.score = cell_counts.get(CellType.VIRUS.value, 0) * 10
            self.score += cell_counts.get(CellType.DATA.value, 0) * 5
            self.score -= cell_counts.get(CellType.ANTIVIRUS.value, 0) * 3
        elif self.game_mode == GameMode.DEFENSE:
            self.score = cell_counts.get(CellType.ANTIVIRUS.value, 0) * 10
            self.score += cell_counts.get(CellType.FIREWALL.value, 0) * 5
            self.score -= cell_counts.get(CellType.VIRUS.value, 0) * 3
        else:  # CLASSIC
            self.score = cell_counts.get(CellType.DATA.value, 0) * 1
    
    def check_game_state(self):
        """Check win/lose conditions"""
        unique = np.unique(self.grid)
        
        if self.game_mode == GameMode.HACKING:
            if CellType.VIRUS.value not in unique:
                self.energy -= 10
            if len(unique) == 1:  # Only one cell type remains
                self.running = False
        elif self.game_mode == GameMode.DEFENSE:
            if CellType.VIRUS.value in unique:
                self.energy -= 1
            if self.energy <= 0:
                self.running = False
    
    def draw(self):
        """Draw the game state"""
        self.screen.fill((20, 20, 30))
        
        # Draw grid
        for y in range(self.height):
            for x in range(self.width):
                cell_type = CellType(self.grid[y, x])
                color = self.colors[cell_type]
                
                # Add some visual effects
                if cell_type == CellType.VIRUS:
                    # Pulsing effect for viruses
                    pulse = abs(np.sin(self.generation * 0.1 + x * 0.1 + y * 0.1))
                    color = tuple(int(c * (0.7 + 0.3 * pulse)) for c in color)
                elif cell_type == CellType.ENCRYPTED:
                    # Rainbow effect for encrypted cells
                    hue = (self.generation * 0.02 + x * 0.01 + y * 0.01) % 1.0
                    rgb = colorsys.hsv_to_rgb(hue, 0.8, 1.0)
                    color = tuple(int(c * 255) for c in rgb)
                
                pygame.draw.rect(self.screen, color, 
                               (x * self.cell_size, y * self.cell_size, 
                                self.cell_size - 1, self.cell_size - 1))
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw the user interface"""
        ui_y = self.height * self.cell_size
        
        # Background for UI
        pygame.draw.rect(self.screen, (30, 30, 40), 
                        (0, ui_y, self.screen_width, 100))
        
        # Game info
        info_text = [
            f"Generation: {self.generation}",
            f"Score: {self.score}",
            f"Energy: {self.energy}",
            f"Mode: {self.game_mode.value}",
            f"Tool: {self.selected_tool.name}"
        ]
        
        x_offset = 10
        for text in info_text:
            surface = self.font.render(text, True, (200, 200, 200))
            self.screen.blit(surface, (x_offset, ui_y + 10))
            x_offset += surface.get_width() + 20
        
        # Controls help
        controls = "SPACE: Pause | 1-6: Tools | R: Reset | ESC: Quit"
        control_surface = self.font.render(controls, True, (150, 150, 150))
        self.screen.blit(control_surface, (10, ui_y + 40))
        
        # Cell type legend
        legend_y = ui_y + 65
        legend_x = 10
        for cell_type in CellType:
            if cell_type != CellType.EMPTY:
                pygame.draw.rect(self.screen, self.colors[cell_type], 
                               (legend_x, legend_y, 15, 15))
                text = self.font.render(cell_type.name[:3], True, (200, 200, 200))
                self.screen.blit(text, (legend_x + 20, legend_y))
                legend_x += 80
    
    def handle_click(self, x, y):
        """Handle mouse clicks to place cells"""
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size
        
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            self.grid[grid_y, grid_x] = self.selected_tool.value
            
            # Add some energy cost for placing certain cells
            if self.selected_tool == CellType.FIREWALL:
                self.energy -= 2
            elif self.selected_tool == CellType.ANTIVIRUS:
                self.energy -= 1
    
    def reset(self):
        """Reset the game"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.generation = 0
        self.score = 0
        self.energy = 100
        self.initialize_patterns()
    
    def run(self):
        """Main game loop"""
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_6:
                        tool_index = event.key - pygame.K_1
                        if tool_index < len(CellType):
                            self.selected_tool = list(CellType)[tool_index]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(*event.pos)
            
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for visibility
        
        pygame.quit()

def main():
    """Main entry point"""
    print("=== HACKING GAME OF LIFE ===")
    print("\nGAMEPLAY RULES:")
    print("1. This is a modified Conway's Game of Life with hacking themes")
    print("2. Different cell types have unique behaviors and interactions")
    print("3. Your goal depends on the selected game mode")
    print("\nCELL TYPES:")
    print("- DATA (Green): Basic cells, follow standard Life rules")
    print("- VIRUS (Red): Aggressive cells that infect data")
    print("- FIREWALL (Orange): Defensive barriers against viruses")
    print("- ANTIVIRUS (Blue): Combat viruses and protect data")
    print("- ENCRYPTED (Yellow): Highly stable, protected cells")
    print("\nGAME MODES:")
    print("- HACKING: Spread viruses to maximize infection")
    print("- DEFENSE: Protect data and eliminate viruses")
    print("- CLASSIC: Traditional Game of Life gameplay")
    print("\nCONTROLS:")
    print("- Left Click: Place selected cell type")
    print("- 1-6 Keys: Select different cell types")
    print("- SPACE: Pause/Resume simulation")
    print("- R: Reset the game")
    print("- ESC: Quit")
    print("\nStarting game...")
    
    game = HackingGameOfLife()
    game.run()

if __name__ == "__main__":
    main()
