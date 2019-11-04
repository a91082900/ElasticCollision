from vpython import *
import numpy as np

ground = box(pos = vec(0, -0.005, 0), size = vec(10, 0.01, 10), color = color.cyan)

small = sphere(radius = 0.04, v = vec(0, 0, 0), m = 1)
big = sphere(radius = 0.157, v = vec(0, 0, 0), m = 10)
e1 = 0.64
e2 = 0.67
eps = -1e-8


t = 0
dt = 0.001
interval = 0
g = vec(0, -9.8, 0)
flag = False
gd = graph(width=300, height=200,
    xtitle='t', ytitle='h',align='left')
gd2 = graph(width=300, height=200,
    xtitle='t', ytitle='v', align='right')


fx1 = gcurve(graph=gd, color=color.red)
fx2 = gcurve(graph=gd, color=color.blue)
fv1 = gcurve(graph=gd2, color=color.red)
fv2 = gcurve(graph=gd2, color=color.blue)

def bounce(a, e = 1):
    if a.pos.y - a.radius < eps:
        #print("HI", a.pos.y - a.radius)
        a.v = e * (-a.v)
def collision(a, b, e = 1):
    global flag, interval
    #print(a.pos.y - a.radius - b.pos.y - b.radius)
    if interval <= 0:
        if a.pos.y - a.radius - b.pos.y - b.radius < eps:
            
            #print("HEY", a.pos.y - a.radius - b.pos.y - b.radius))
            flag = True
            tmp = a.v
            a.v = a.v * (a.m-e*b.m) / (a.m+b.m) + b.v * (1+e)*b.m / (a.m+b.m)
            b.v = tmp * (1+e)*a.m / (a.m+b.m) + b.v * (b.m-e*a.m) / (a.m+b.m)
            #print("Hi", a.v.y, b.v.y)

        interval = 10
    else:
        interval -= 1
    
        
def set_height(h): # 小球底部高度
    global small, big
    small.v = vec(0, 0, 0)
    big.v = vec(0, 0, 0)
    small.pos = vec(0, h+small.radius, 0)
    big.pos = vec(0, h-big.radius, 0)
max_h = 0
max_hs = []
if __name__ == "__main__":
    scene.camera.follow(small)
    for i in range(1, 2):
        set_height(10)
        big.m = 100
        while t < 10:
            rate(1/dt)
            t += dt
            big.v += g*dt
            big.pos += big.v*dt
            small.v += g*dt
            small.pos += small.v*dt
            collision(small, big, e2)
            bounce(big, e1)
            scene.caption = "<br>"+str(round(t, 3))+"<br>m.height = "+str(small.pos.y)
            max_h = max(max_h, small.pos.y)
            
            #print(small.v.y, " ", big.v.y)

            """if small.pos.y > max:
                    max = small.pos.y
                elif flag and max > 2000:
                    print(max)
                    flag = False"""

            fx1.plot(t, small.pos.y)
            fx2.plot(t, big.pos.y)
            fv1.plot(t, small.v.y)
            fv2.plot(t, big.v.y)

        t = 0
        
        fx1 = gcurve(graph=gd, color=color.red)
        fx2 = gcurve(graph=gd, color=color.blue)
        fv1 = gcurve(graph=gd2, color=color.red)
        fv2 = gcurve(graph=gd2, color=color.blue)
        max_hs.append((e2, max_h))
        print(i, max_h)
        max_h = 0


    scene.caption = "<br>max height = "+str(max_h)
    
