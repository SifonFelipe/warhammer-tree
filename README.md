# Warhammer 40,000 Tree


## Introduction

You are a Devastator Space Marine and your objetive is to purge every xenos in the map.


Your movements are *orthogonal* (90 angles only), you can *set and unset your gun*,
*shoot* in a distance of 2 and *pray* to the Emperor to restore faith.


## Objective

The objective of this problem is to find the minimum number of actions required to purge all xenos in the map.
This is just for learning and fun, testing trees algorithms and heuristics.


## Actions
- **Move**: You can move to an adjacent cell (up, down, left, right) if it's not occupied by a wall or a xeno.
- **Set Gun**: You can set your gun to prepare for shooting.
- **Unset Gun**: You can unset your gun if you no longer want to shoot.
- **Shoot**: You can shoot in a straight line (up, down, left, right) if your gun is set and there are xenos within a distance of 2 cells.
- **Pray**: You can pray to the Emperor to restore your faith, which allows you to continue fighting. This action can be used when you have no more faith left.


## Performance limits

As this is a tree problem, performance limits the creation of situations where the number of actions required to purge all xenos is very high. The map size and the number of xenos should be limited to ensure that the problem can be solved within a reasonable time frame.
