# Machine Spirit Solver

## Introduction

This project decouples the algorithmic logic for tree exploration from the Problem Definition (the specific rules of a "given world")

## System Architecture

* **State** `Data Container`: Immutable dataclass that represent a snapshot of the system at any given moment
* **Problem** `Logic Layer`: An abstract base class that defines the rules of the "World",
  generating possible actions, transitioning between states, and verifying goal conditions.
* **Solver** `Engine`: A pure search engine agnostic to the problem domain. It explores the state-tree
  to find the sequence of actions with less weight.

## How to Implement a New Problem

To implement a new challenge (game, maze, etc), you only need to create a class that inherits from Problem:

```python
class MyNewProblem(Problem):
    def get_actions(self, state):
        # Define possible actions

    def apply_action(self, state, action):
        # Define state evolution

    def is_goal(self, state):
        # Define win condition

```

# Problems Implemented

## Warhammer Problem

### Introduction

You are a Devastator Space Marine and your objetive is to purge every xenos in the map.

[Preview](https://github.com/user-attachments/assets/7b6d6d9c-1668-4cf7-bbfd-174503f6e86e)

Your movements are *orthogonal* (90 angles only), you can *set and unset your gun*,
*shoot* in a distance of 2 and *pray* to the Emperor to restore faith.


### Objective

The objective of this problem is to find the minimum number of actions required to purge all xenos in the map.
This is just for learning and fun, testing trees algorithms and heuristics.


### Actions
- **Move**: You can move to an adjacent cell (up, down, left, right) if it's not occupied by a wall or a xeno.
- **Set Gun**: You can set your gun to prepare for shooting.
- **Unset Gun**: You can unset your gun if you no longer want to shoot.
- **Shoot**: You can shoot in a straight line (up, down, left, right) if your gun is set and there are xenos within a distance of 2 cells.
- **Pray**: You can pray to the Emperor to restore your faith, which allows you to continue fighting. This action can be used when you have no more faith left.


# Performance limits

As this is a tree problem, performance limits the creation of situations where the
number of actions required to solve a problem and the different possible options for each node are high. 


# Installation

```bash
# Clone the repo
git clone https://github.com/SifonFelipe/warhammer-tree.git
cd warhammer-tree

# Sync venv
uv sync

# Run the solver with the Warhammer problem (for default)
uv run main.py
```
