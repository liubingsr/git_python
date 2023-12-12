import numpy as np
import matplotlib.pyplot as plt
import time

def function(x, y):
    m = 30
    if x < m and y < m:
        return 30*x - y
    elif x < m <= y:
        return 30*y - x
    elif x >= m > y:
        return x**2 - y/2
    elif x >= m and y >= m:
        return 20*(y**2) - 500*x

x_min = 0
x_max = 60
y_min = 0
y_max = 60

#速度上下限必须互为相反数，保证方向的随机性
v_min = -1
v_max = 1
#c2越大越容易收敛
w = 0.4
c1 = 0.2
c2 = 3

t = np.arange(x_min,x_max,0.5)
import numpy as np
import matplotlib.pyplot as plt
import time

def function(x, y):
    m = 30
    if x < m and y < m:
        return 30*x - y
    elif x < m <= y:
        return 30*y - x
    elif x >= m > y:
        return x**2 - y/2
    elif x >= m and y >= m:
        return 20*(y**2) - 500*x

x_min = 0
x_max = 60
y_min = 0
y_max = 60

#速度上下限必须互为相反数，保证方向的随机性
v_min = -1
v_max = 1
#c2越大越容易收敛
w = 0.4
c1 = 0.2
c2 = 3

t = np.arange(x_min,x_max,0.5)
#print(t)
#print(len(t))
X, Y = np.meshgrid(t, t)    #需要弄明白
#print(X, Y)
Z = np.zeros(shape = X.shape)    #需要弄明白
for i in range(len(t)):
    for j in range(len(t)):
        Z[i][j] = function(X[i][j], Y[i][j])

class Particle:
    def __init__(self):
        #当前点的坐标
        self.x = np.random.uniform(x_min, x_max)
        self.y = np.random.uniform(y_min, y_max)

        #记录局部最优点和最优值
        self.x_local_best = self.x
        self.y_local_best = self.y
        self.f_local_best = function(self.x, self.y)

        #当前点的前进速度
        self.vx = np.random.uniform(v_min, v_max)
        self.vy = np.random.uniform(v_min, v_max)

class PSO:
    def __init__(self, iter_num, size):
    
        #size个点
        self.particles = [Particle() for _ in range(size)]      #需要弄明白

        #记录全局最优点和最优值
        self.x_global_best = 20
        self.y_global_best = 20
        self.f_global_best = function(self.x_global_best, self.y_global_best)

        #迭代次数
        self.iter_num = iter_num

        #用来作图
        self.f_global_best_records = []

    def update_v(self, particle):
        vx_new = w*particle.vx + c1*np.random.rand()*(particle.x_local_best - particle.x) + c2*np.random.rand()*(self.x_global_best - particle.x)
        vy_new = w*particle.vy + c1*np.random.rand()*(particle.y_local_best - particle.y) + c2*np.random.rand()*(self.y_global_best - particle.y)
        particle.vx = max(min(vx_new, v_max), v_min)
        particle.vy = max(min(vy_new, v_max), v_min)

    def update_xy(self, particle):
        x_new = particle.x + particle.vx
        y_new = particle.y + particle.vy
        x_new = max(min(x_new, x_max), x_min)
        y_new = max(min(y_new, y_max), y_min)
        f_new = function(x_new, y_new)
        particle.x = x_new
        particle.y = y_new

        if f_new < particle.f_local_best:
            particle.x_local_best = particle.x
            particle.y_local_best = particle.y
            particle.f_local_best = f_new

        if f_new < self.f_global_best:
            self.x_global_best = particle.x
            self.y_global_best = particle.y
            self.f_global_best = f_new

    def update(self):
        for _ in range(self.iter_num):
            x = []
            y = []
            f = []
            for particle in self.particles:
                self.update_v(particle)
                self.update_xy(particle)
                x.append(particle.x)
                y.append(particle.y)
                f.append(function(particle.x, particle.y))
            yield x, y, f #需要弄明白
            self.f_global_best_records.append(self.f_global_best)

def main():
    iter_num = 100
    size = 30
    pso = PSO(iter_num, size)
    fig = plt.figure(figsize = (8, 6))
    ax = fig.add_subplot(111, projection = '3d')
    for x, y, f in pso.update():
        ax.clear()
        ax.plot_surface(X, Y, Z, cmap = 'rainbow', alpha = 0.4, rstride = 1, cstride = 1)
        ax.scatter(x, y, f, s = 10, c = 'r', label = '顺序点')
        plt.ion()
        plt.pause(0.1)
        plt.ioff()
    print('result coordinate:', pso.x_global_best, ' ', pso.y_global_best,' ',pso.f_global_best)
    plt.show
    plt.plot(range(len(pso.f_global_best_records)), pso.f_global_best_records, alpha = 1)
    plt.show

if __name__ == '__main__':
    main()