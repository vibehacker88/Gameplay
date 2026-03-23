# Hacking Game of Life

A cyberpunk-themed variant of Conway's Game of Life where different cell types represent various elements of digital warfare and network security.

## 🎮 Gameplay Overview

The Hacking Game of Life combines the classic cellular automaton rules with strategic hacking mechanics. Players interact with a digital ecosystem where different cell types battle for dominance, following modified rules that simulate cyber warfare scenarios.

## 🎯 Game Objectives

### Game Modes

1. **HACKING Mode**
   - **Goal**: Spread viruses and compromise as much data as possible
   - **Win Condition**: Achieve maximum virus dominance
   - **Strategy**: Place viruses strategically to overwhelm defenses

2. **DEFENSE Mode**
   - **Goal**: Protect data and eliminate all viruses
   - **Win Condition**: Eradicate all viruses while maintaining data integrity
   - **Strategy**: Build firewalls and deploy antivirus programs

3. **CLASSIC Mode**
   - **Goal**: Traditional Life gameplay with data cells
   - **Win Condition**: Create stable patterns and maximize population
   - **Strategy**: Experiment with different patterns and configurations

## 🦠 Cell Types and Behaviors

### Data Cells (Green)
- **Behavior**: Follow standard Conway's Game of Life rules
- **Survival**: Lives with 2-3 neighbors
- **Birth**: Created with 3 data neighbors
- **Vulnerability**: Can be infected by adjacent viruses

### Virus Cells (Red)
- **Behavior**: Aggressive infection vectors
- **Survival**: Lives with 1-4 neighbors (highly adaptable)
- **Birth**: Created with 2+ virus neighbors
- **Special**: Infects adjacent data cells
- **Visual**: Pulsing red effect

### Firewall Cells (Orange)
- **Behavior**: Defensive barriers
- **Survival**: Stable with 2+ firewall neighbors
- **Weakness**: Overwhelmed by 4+ total neighbors
- **Special**: Blocks virus spread
- **Cost**: 2 energy units to place

### Antivirus Cells (Blue)
- **Behavior**: Virus hunters
- **Survival**: Lives with 2-3 neighbors
- **Combat**: Eliminates adjacent viruses
- **Weakness**: Overwhelmed by 3+ virus neighbors
- **Cost**: 1 energy unit to place

### Encrypted Cells (Yellow)
- **Behavior**: Highly secure, immutable data
- **Survival**: Never dies (permanent structure)
- **Special**: Immune to all effects
- **Visual**: Rainbow shifting effect

## 🎲 Game Rules

### Core Mechanics

1. **Turn-based Evolution**: The grid evolves in discrete generations
2. **Neighbor Counting**: Each cell considers its 8 adjacent neighbors
3. **Type-specific Rules**: Each cell type follows unique survival/birth rules
4. **Energy System**: Placing defensive cells costs energy
5. **Score Calculation**: Points based on cell dominance and game mode

### Interaction Rules

- **Virus Infection**: Data cells with 2+ virus neighbors become viruses
- **Antivirus Combat**: Antivirus cells eliminate nearby viruses
- **Firewall Blocking**: Firewalls prevent virus spread through their area
- **Energy Depletion**: Running out of energy in defense mode ends the game

## 🕹️ Controls

### Mouse Controls
- **Left Click**: Place selected cell type at cursor position
- **Cursor Position**: Shows grid coordinates in real-time

### Keyboard Controls
- **1-6 Keys**: Select different cell types for placement
- **SPACE**: Pause/Resume the simulation
- **R**: Reset the game to initial state
- **ESC**: Quit the application

### Cell Type Selection
- **1**: Empty (clear cells)
- **2**: Data cells
- **3**: Firewall cells
- **4**: Virus cells
- **5**: Antivirus cells
- **6**: Encrypted cells

## 📊 Scoring System

### HACKING Mode
- Virus cells: +10 points each
- Data cells: +5 points each
- Antivirus cells: -3 points each

### DEFENSE Mode
- Antivirus cells: +10 points each
- Firewall cells: +5 points each
- Virus cells: -3 points each
- Energy penalty: -1 point per virus present

### CLASSIC Mode
- Data cells: +1 point each
- Bonus points for stable patterns

## 🎨 Visual Features

### Cell Effects
- **Viruses**: Pulsing red animation
- **Encrypted**: Rainbow color shifting
- **Firewalls**: Solid orange barriers
- **Antivirus**: Steady blue glow
- **Data**: Standard green coloring

### UI Elements
- **Generation Counter**: Shows current evolution step
- **Score Display**: Real-time score updates
- **Energy Bar**: Remaining energy in defense mode
- **Tool Indicator**: Currently selected cell type
- **Legend**: Color-coded cell type reference

## 🔧 Technical Details

### Grid Specifications
- **Default Size**: 80x60 cells
- **Cell Size**: 10x10 pixels
- **Update Rate**: 10 generations per second
- **Maximum Population**: 4,800 cells

### Performance Features
- **Efficient numpy arrays** for grid calculations
- **Optimized neighbor counting** algorithms
- **Smooth visual effects** with minimal performance impact

## 🧩 Strategy Tips

### HACKING Mode Strategy
1. Start viruses near data clusters
2. Use multiple virus cells to overwhelm defenses
3. Target isolated data patches first
4. Avoid antivirus concentrations

### DEFENSE Mode Strategy
1. Build firewall rings around valuable data
2. Place antivirus cells at virus entry points
3. Maintain energy reserves for emergencies
4. Create layered defense systems

### Pattern Recognition
- **Gliders**: Moving patterns that can transport cells
- **Oscillators**: Repeating patterns for stable populations
- **Still Lifes**: Static patterns for permanent structures
- **Spaceships**: Complex moving patterns

## 🚀 Getting Started

### Installation
```bash
# Install required dependencies
pip install pygame numpy

# Run the game
python hacking_game_of_life.py
```

### System Requirements
- Python 3.7+
- Pygame library
- NumPy library
- 800x700 minimum screen resolution

## 🎓 Educational Value

This game demonstrates:
- **Cellular Automata**: Complex emergent behavior from simple rules
- **Game Theory**: Strategic interactions between different agents
- **Network Security**: Concepts of defense, offense, and resource management
- **Pattern Recognition**: Understanding stable and dynamic systems

## 🔮 Future Features

- **Multiplayer Mode**: Competitive network battles
- **Level Editor**: Create custom scenarios
- **AI Opponents**: Computer-controlled strategies
- **Power-ups**: Special abilities and boosts
- **Campaign Mode**: Progressive challenges with story elements

## 📝 License

MIT License - Feel free to modify and distribute for educational purposes.

---

**Enjoy the cyber warfare evolution!** 🚀💻🔐
