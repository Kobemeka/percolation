import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def boundCheck(v,b):
    if 0 <= v <= b-1:  return True
    return False

def tBoundCheck(vs,bs):
    return all(list(map(lambda x: boundCheck(*x),zip(vs,bs))))

def edge_probs(nx,ny,seed=None):
    np.random.seed(seed)
    row_probs = np.random.random(size=(nx-1,ny))
    column_probs = np.random.random(size=(nx,ny-1))
    return row_probs,column_probs

def rowControl(nx,ny,probability,row_probs):

    # row_opens = []

    # for px in range(nx-1):
    #     for py in range(ny):
    #         prob = row_probs[px,py]
    #         if prob <= probability:
    #             row_opens.append([(px,py),(px+1,py)])
    # return row_opens
    return [[(px,py),(px+1,py)] for py in range(ny) for px in range(nx-1) if row_probs[px,py] <= probability]

def columnControl(nx,ny,probability,column_probs):

    # column_opens = []
    # for px in range(nx):
    #     for py in range(ny-1):
    #         prob = column_probs[px,py]
    #         if prob <= probability:
    #             column_opens.append([(px,py),(px,py+1)])
    # return column_opens
    return [[(px,py),(px,py+1)] for py in range(ny-1) for px in range(nx) if column_probs[px,py] <= probability]

def edgeControl(nx,ny,probability,row_probs,column_probs):
    return rowControl(nx,ny,probability,row_probs),columnControl(nx,ny,probability,column_probs)

def seenMatrix(nx,ny):

    return np.zeros((nx,ny))

def connect(x,y,nx,ny,row_opens,column_opens,seen):
    this = (x,y)
    right = (x+1,y)
    left = (x-1,y)
    top = (x,y-1)
    bottom = (x,y+1)

    rrow = [this,right] 
    lrow = [this,left]
    tcol = [this,top]
    bcol = [this,bottom]
    connections = [this]

    seen[this] = 1

    if tBoundCheck(right,(nx,ny)):
        if not seen[right] and rrow in row_opens:
            seen[right] = 1
            conn = connect(*right,nx,ny,row_opens,column_opens,seen)
            connections = connections + conn[0]
            seen = conn[1]

    if tBoundCheck(left,(nx,ny)):
        if not seen[left] and lrow in row_opens:
            seen[left] = 1
            conn = connect(*left,nx,ny,row_opens,column_opens,seen)
            connections = connections + conn[0]
            seen = conn[1]

    if tBoundCheck(top,(nx,ny)):
        if not seen[top] and tcol in column_opens:
            seen[top] = 1
            conn = connect(*top,nx,ny,row_opens,column_opens,seen)
            connections = connections + conn[0]
            seen = conn[1]

    if tBoundCheck(bottom,(nx,ny)):
        if not seen[bottom] and bcol in column_opens:
            seen[bottom] = 1
            conn = connect(*bottom,nx,ny,row_opens,column_opens,seen)
            connections = connections + conn[0]
            seen = conn[1]

    return connections,seen

def clusters(nx,ny,ro,co,seen):

    clusters_ = []
    while not all(seen.flatten()):
        notSeen = np.where(seen == 0)
        start = notSeen[0][0],notSeen[1][0]
        conn = connect(*start,nx,ny,ro,co,seen)
        clusters_.append(conn[0])
        seen = conn[1]
    return clusters_

def getClusters(nx,ny,probability,seed=None):
    rp,cp = edge_probs(nx,ny,seed)
    ro,co = edgeControl(nx,ny,probability,rp,cp)
    seen = seenMatrix(nx,ny)
    return clusters(nx,ny,ro,co,seen)

def draw(nx,ny,prob,anim=False,draw_type="plot",seed=None):
    clusters = getClusters(nx,ny,prob,seed)
    fig,ax = plt.subplots(figsize=(5*nx,5*ny))
    ax.set_aspect(1)
    ax.set_xlim([-1,nx])
    ax.set_ylim([-1,ny])
    np.random.seed(seed)
    colors = [np.array(np.random.random((1,3)))*0.85 for _ in range(len(clusters))]
    if anim:
        if draw_type == "plot":
            for i,cluster in enumerate(clusters):
                for px,py in zip(*zip(*cluster)):
                    ax.set_xlim([-1,nx])
                    ax.set_ylim([-1,ny])
                    ax.scatter(
                        px,
                        py,
                        color = tuple(colors[i]),
                        marker="s",
                        )
                    plt.pause(0.00000001)
        elif draw_type == "rectangle":
            for i,cluster in enumerate(clusters):
                for px,py in zip(*zip(*cluster)):
                    
                    ax.add_patch(
                        Rectangle((px-0.5,py-0.5),1,1,facecolor=colors[i],edgecolor="k")
                    )
                    plt.pause(0.000000001)
    else:
        if draw_type == "plot":

            for i,cluster in enumerate(clusters):
                ax.plot(*list(zip(*cluster)), marker="s", linestyle='None')

        elif draw_type == "rectangle":
            for i,cluster in enumerate(clusters):
                for px,py in zip(*zip(*cluster)):
                    ax.add_patch(
                        Rectangle((px-0.5,py-0.5),1,1,facecolor=colors[i],edgecolor="k")
                    )

    
    plt.show()