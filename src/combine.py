import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

import image_interpreter as ii
import drill_solver as ds

# image interpreter 
output1 = ii.interpret_image("test_images/basic-circle-outline-small-issue.jpg", 30)
output2 = ii.interpret_image("test_images/basic-circle-outline-issue.jpg", 30)

# drill solver 
print("CALCULATING ROUGH TRANSITION")
roughSet, candidates = ds.getRoughTransition([], output1, output2)
print("ALLOCATING SPOTS");
allocatedSet  = ds.alocateTransition(output1, roughSet, candidates);
print("RESOLVING COLLISIONS")
fixedSet = ds.fixTransitions(output1,allocatedSet,8)

# Display PLOT
x, y = map(list,zip(*output1))
categories = np.arange(0, len(x), 1, dtype=int)
colormap = cm.rainbow(np.linspace(0, 1, len(y)))

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
ax1.set_title("start")
ax1.scatter(x, y, color=colormap[categories])
ax1.invert_yaxis()

ax2.set_title("rough");
x, y = map(list,zip(*output2));
ax2.scatter(x, y, marker="x");
x, y = map(list,zip(*[roughSet[x] for x in roughSet.keys()]));
ax2.scatter(x, y, color=colormap[categories]);
ax2.invert_yaxis();

x, y = map(list,zip(*allocatedSet))
ax3.set_title("allocated")
ax3.scatter(x, y, color=colormap[categories])
ax3.invert_yaxis()

x, y = map(list,zip(*fixedSet))
ax4.set_title("end")
ax4.scatter(x, y, color=colormap[categories])
ax4.invert_yaxis()
plt.show()