import numpy as np
import matplotlib.pyplot as plt
from SimpleCV import *

original = image = Image("P6070048.jpg")
image = image.sobel(doGray=True, xorder = 0, yorder = 1)
image = image.binarize(blocksize=3)

vproj = np.array([0] * image.height)

for i in range(image.width):
	for j in range(image.height):
		if image[i, j] == (255,255,255):
			vproj[j] += 1

avg = np.average(vproj)
std = np.std(vproj)
vproj[vproj < (avg+std)] = 0

candidates = []
nonzeros = 0

for i, value in np.ndenumerate(vproj):
	if value != 0:
		nonzeros += 1
	else:
		if nonzeros != 0:
			candidates.append([i[0]-nonzeros, i[0]-1])
			nonzeros = 0

#
# Fazendo Crop das Imagens
#
for i, candidate in enumerate(candidates):
	if (candidate[1]-candidate[0] > 1):
		cropheight = candidate[1]-candidate[0]
		crop = original.crop(0, candidate[0], image.width, cropheight)
		crop.save(str(candidate)+".jpg")

#
# Criacao do Grafico de Projecao Vertical
#
image.save("output.jpg")
fig, ax = plt.subplots()
ax.set_ylim([0, image.height])
ax.invert_yaxis()
ax.barh(range(image.height), vproj, ecolor='r')
plt.ylabel('Linha')
plt.xlabel('Quantidade')
plt.title('Quantidade de pixels brancos por linha')
plt.savefig('projecao.jpg')
plt.grid()
#plt.show()