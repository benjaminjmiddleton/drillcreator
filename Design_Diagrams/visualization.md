## Algorithm Visualization
The algorithm first finds a rough transition by estimating the marcher’s final location based on their original
location relative to the center. Then, the algorithm allocates the marchers, who prefer sets closest to this estimate.
This gives us the ”Rough Transition and Allocation” set below. Finally, the algorithm attempts to solve collisions,
giving us the “Final Transition.” Notice that the rough transition has switched the position of the red and green x’s,
causing a collision, and that this is fixed in the Final Transition.

### Input Set
![Input Set](../assets/input_set.png "Input Set")
### Rough Transition and Allocation
![Rough Transition and Allocation](../assets/rough_transition_set.png "Rough Transition and Allocation")
### Final Transition
![Final Transition](../assets/final_transition_set.png "Final Transition")
