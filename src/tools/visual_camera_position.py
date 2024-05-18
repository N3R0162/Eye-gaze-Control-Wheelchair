import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
camera_position =  [[-323.781122  ],
 [  35.05458151],
 [   3.98082982]]
pattern_size = (7,10)
# Plot the camera position
ax.scatter(camera_position[0], camera_position[1], camera_position[2], c='r', marker='o', label='Camera Position')

# Optionally, plot the checkerboard corners
# (For simplicity, this example assumes a single checkerboard at the origin)
checkerboard_corners = np.zeros((pattern_size[0] * pattern_size[1], 3))
ax.scatter(checkerboard_corners[:,0], checkerboard_corners[:,1], checkerboard_corners[:,2], c='b', marker='x', label='Checkerboard Corners')

# Set labels and title
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Camera Position and Checkerboard Corners')
ax.legend()

plt.show()
