#  Game of Life (pygame learning project)

A simple implementation of **Conway’s Game of Life** written in Python using **pygame**.
Inspired by this amazing video where people have built entire computers with this logic: https://www.youtube.com/watch?v=Kk2MH9O4pXY

This project is a **learning exercise** focused on understanding pygame fundamentals such as the game loop, timing, rendering a grid, and separating simulation logic from display code.  
It is intentionally kept simple and readable while exploring how a cellular automaton behaves in real time.

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
- Configurable grid size and cell size  
- Adjustable simulation speed using a pygame clock  
- Randomly generated starting state  
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

## Nota bene
The man himself, John Conway who created the algorithm, about The game of Life: https://www.youtube.com/watch?v=R9Plq-D1gEk
