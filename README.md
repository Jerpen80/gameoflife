# Game of Life (pygame learning project)

A simple implementation of **Conway’s Game of Life** written in Python using **pygame**.  
Inspired by this amazing video where people have built entire computers with this logic:  
https://www.youtube.com/watch?v=Kk2MH9O4pXY

This project is a **learning exercise** focused on understanding pygame fundamentals such as the game loop, timing, rendering a grid, and separating simulation logic from display code.  
It is intentionally kept simple and readable while exploring how a cellular automaton behaves in real time.

---

## Game rules 

The Game of Life is, briefly, a two-dimensional cellular automata universe governed by a simple set of birth, death and survival rules.

- survival: if a live cell has two or three live neighbors, it survives.
- death: if a live cell has less than two or more than three live neighbors, it dies.
- birth: if a dead cell has exactly three live neighbors, it is born. 

---

## Usage

### Manual editing mode (default)

When started **without** the `--random` flag, the program opens in **editing mode**:

- Click on cells to toggle them alive or dead
- Grid lines are shown to make placement easier
- Press **SPACE** to start the simulation
- Press **N** to advance **one generation** and enter pause mode

This mode is useful for manually constructing patterns and stepping through their evolution.

---

### Random start

If the `--random` flag is provided, the grid is filled randomly with the given density (a float between `0` and `1`) and the simulation starts in paused state (press SPACE to start):

```bash
python3 gameoflife.py --random 0.15
```
---

## Controls

### Keyboard

- **SPACE**  
  Toggle between:
  - Edit → Run  
  - Run → Pause  
  - Pause → Run

- **N**  
  Advance the simulation by **one generation**  
  - From **Edit mode**: enters Pause mode and advances once  
  - From **Pause mode**: advances one generation

- **Arrow keys**  
  Pan the view when the grid is larger than the window:
  - ← → move left / right  
  - ↑ ↓ move up / down

- **ESC**  
  Quit the application

---

### Mouse

- **Left click (Edit mode only)**  
  Toggle a cell alive or dead at the cursor position

---

## Display and layout

- The application opens in a **borderless fullscreen window**
- If the grid is larger than the visible area, you can **pan the camera** using the arrow keys
- The simulation continues to run for cells outside the visible area (only the view is moved)

---

## Purpose

The goal of this project is to **learn pygame by building a concrete, visual program**.

Conway’s Game of Life is well suited for this because it:
- Uses a discrete grid
- Evolves over time using simple rules
- Clearly demonstrates the need for a proper update loop
- Separates simulation logic from rendering

This repository reflects an incremental learning process rather than a polished or highly optimized implementation.

---

## Features

- Pygame-based window and render loop  
- Manual editing of the starting grid  
- Randomized starting state with configurable density  
- Fullscreen display with camera panning  
- Pause / resume and single-step execution  
- Adjustable simulation speed  
- Explicit and readable implementation of the Game of Life rules  
- No external dependencies beyond pygame  

---

## Requirements

- Python **3.8+**
- `pygame`

Install pygame with:

```bash
pip install pygame
```
or
```bash
apt install python3-pygame
```
---

## Nota bene

John Conway, the creator of the Game of Life, explaining the algorithm himself:  
https://www.youtube.com/watch?v=R9Plq-D1gEk
