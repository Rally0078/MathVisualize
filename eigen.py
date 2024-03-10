import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import matplotlib.gridspec as gridspec
import numpy as np

transform = np.array([[0.0,1.0],[1.0,0.0]])
vec = np.array([1,3])
fig, ax = plt.subplots(figsize=(20,20))
def helper():
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    eigenvals, eigenvecs = np.linalg.eig(transform)
    if not np.iscomplex(eigenvecs[0,0]) and not np.iscomplex(eigenvecs[0,1]) and not np.iscomplex(eigenvecs[1,0]) and not np.iscomplex(eigenvecs[1,1]):
        ax.axline((eigenvecs[0]), slope=eigenvecs[0,1]/eigenvecs[0,0],color="black", linestyle="--")
        ax.axline((eigenvecs[1]),slope=eigenvecs[1,1]/eigenvecs[1,0], color="black", linestyle="--")
helper()
def onclick(event):
    ax.plot(event.xdata, event.ydata, 'o', markersize=4, color='green')
    fig.canvas.draw()
    vec = np.array([event.xdata, event.ydata])
    newVec = transform@vec
    ax.plot(newVec[0], newVec[1],'o', markersize=4, color='red')
    print(transform)
    print(newVec)
    fig.canvas.draw()
def clearFigure(event):
    if event.key == 'c':
        ax.cla()
        helper()
        fig.canvas.draw()

fig.subplots_adjust(bottom=0.4)
gs = gridspec.GridSpec(2,2)
gs.update(left=0.4, right=0.7, bottom=0.05, top=0.12, hspace=0.1)

axes = [fig.add_subplot(gs[i,j]) for i,j in [[0,0],[0,1],[1,0],[1,1]]]
# create the textboxes

tb_a00= TextBox(axes[0],'a00', initial = str(transform[0,0]), hovercolor='0.975', label_pad=0.1)
tb_a01 = TextBox(axes[1],'a01',  initial = str(transform[0,1]), hovercolor='0.975', label_pad=0.1)
tb_a10 = TextBox(axes[2],'a10', initial = str(transform[1,0]), hovercolor='0.975', label_pad=0.1)
tb_a11 = TextBox(axes[3],'a11',  initial = str(transform[1,1]), hovercolor='0.975', label_pad=0.1)

def submit(val):
    lim = [float(tb.text) for tb in [tb_a00, tb_a01, tb_a10, tb_a11]]
    transform[0,0] = lim[0]
    transform[0,1] = lim[1]
    transform[1,0] = lim[2]
    transform[1,1] = lim[3]
    ax.cla()
    helper()
    fig.canvas.draw()

for tb in [tb_a00, tb_a01, tb_a10, tb_a11]:
    tb.on_submit(submit)


clear = fig.canvas.mpl_connect('key_press_event', clearFigure)
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()