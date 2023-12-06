import numpy as np
import time

month = 13
E_wind = [0, 31.9166, 37.275, 54.4235, 60.1538, 70.2272, 67.2692, 66.0489, 62.4701, 59.2639, 43.7702, 31.5043, 26.9326]
E_solar = [0, 278.708, 240.345, 244.664, 242.277, 240.498, 224.084, 211.331, 207.114, 207.163, 238.922, 267.632, 312.806]
E_load = [0, 296.008, 267.309, 256.26, 243.698, 296.177, 286.133, 265.504, 276.639, 256.512, 265.629, 276.764, 281.345]

deltE = np.zeros(month)
E_lps = np.zeros(month)
E_battery = np.zeros(month)
E_capacitance = np.zeros(month)



Coef_converter = 0.95
alpha = 0.7
beta = 0.65
f_lpsp_max = 0.005

DOD = 0.4
C_battery = 100 #蓄电池的容量，Ah
U_battery = 12 #蓄电池的额定电压，V
e_battery_n = 1000*C_battery*U_battery/1.0E6   #单个蓄电池额定储能量，MWh，×1000后，变kWh

eta_battery_charge = 0.75
eta_battery_discharge = 0.85

C_capacitance = 3000 #超级电容的电容值，F
U_capacitance_max = 2.7 #超级电容工作电压最大值，V
U_capacitance_min = 0.8 #超级电容工作电压最小值，V

eta_capacitance_charge = 0.98
eta_capacitance_discharge = 0.98

p_battery = 400
p_capacitance = 3.5

f_ob = 0.1
f_oc = 0.01

f_mb = 0.02
f_mc = 0

f_db = 0.08
f_dc = 0.04

x_min = 0
x_max = 1.0E+8
y_min = 0
y_max = 1.0E+8

#速度上下限必须互为相反数，保证方向的随机性
v_min = -100000
v_max = 100000

#c2越大越容易收敛
w = 1
c1 = 0.5
c2 = 0.9

def function(x, y):
    #print('x =',x,'y = ', y)
    E_battery_n = x*e_battery_n
    E_battery_min = E_battery_n*(1 - DOD)

    E_capacitance_max = 1000*0.5*y*C_capacitance*U_capacitance_max**2/3.6E9  #超级电容器的最大储能量，MWh
    E_capacitance_min = 1000*0.5*y*C_capacitance*U_capacitance_min**2/3.6E9  #超级电容器的最小储能量，MWh


    for i_month in range(0, month):
        deltE[i_month] = 0
        E_lps[i_month] = 0
        E_battery[i_month] = E_battery_min
        E_capacitance[i_month] = E_capacitance_min

    f_lpsp = 0



    #print(E_battery_min/x, E_battery_n/x)
    #print(E_battery_min, E_battery_n)
    #input()


    for i_month in range(1, month):
        deltE[i_month] = Coef_converter*(E_wind[i_month] + E_solar[i_month]) - E_load[i_month]
        E_lps[i_month] = 0
        #print(i_month, '月份的不平衡量为', deltE[i_month], 'kWh')

        #充电
        if deltE[i_month] >= 0:            
            E_battery[i_month] = E_battery[i_month - 1] + deltE[i_month]*alpha*Coef_converter*eta_battery_charge
            E_capacitance[i_month] = E_capacitance[i_month - 1] + deltE[i_month]*(1 - alpha)*Coef_converter*eta_capacitance_charge
            if E_battery[i_month] > E_battery_n:
                E_battery[i_month] = E_battery_n
            if E_capacitance[i_month] > E_capacitance_max:
                E_capacitance[i_month] = E_capacitance_max
            #print(i_month, '月份不缺电')
        #放电
        else:
            deltE[i_month] = -deltE[i_month]
            E_battery[i_month] = E_battery[i_month - 1] - deltE[i_month]*alpha/eta_battery_discharge/Coef_converter
            E_capacitance[i_month] = E_capacitance[i_month - 1] - deltE[i_month]*(1 - alpha)/eta_capacitance_discharge/Coef_converter
            #print(i_month, '月份电池按需放电')
            if E_battery[i_month] < E_battery_min:
                E_lps[i_month] = E_battery_min - E_battery[i_month] #计算缺电率
                E_battery[i_month] = E_battery_min
            if E_capacitance[i_month] < E_capacitance_min:
                E_lps[i_month] += E_capacitance_min - E_capacitance[i_month] #计算缺电率
                E_capacitance[i_month] = E_capacitance_min

    #print(E_lps)
    #input()

    #计算缺电率flpsp
    sum_E_lps = 0
    sum_E_load = 0
    for i_month in range(1, month):
        sum_E_lps += E_lps[i_month]
        sum_E_load += E_load[i_month]
    
    f_lpsp = sum_E_lps/sum_E_load

    #print(sum_E_lps, sum_E_load, f_lpsp)
    #input()
    
    if f_lpsp > f_lpsp_max:
       LCC = float('inf')
    else:
       LCC = 1.0*((1 + f_ob + f_mb + f_db)*x*p_battery + (1 + f_oc + f_mc + f_dc)*y*p_capacitance) 
    
    #print(x, y, f_lpsp, LCC)
    #input()
    return LCC
    #return 1.0*((1 + f_ob + f_mb + f_db)*x*p_battery + (1 + f_oc + f_mc + f_dc)*y*p_capacitance)
    #return x + y
class Particle:
    def __init__(self):
        #当前点的坐标
        self.x = np.random.uniform(x_min, x_max)#********************大修改
        self.y = np.random.uniform(y_min, y_max)#********************大修改

        #self.x = 1.0E8
        #self.y = 1.0E8

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
        self.x_global_best = 1.0E8
        self.y_global_best = 1.0E8
        self.f_global_best = function(self.x_global_best, self.y_global_best)

        #迭代次数
        self.iter_num = iter_num
        #print(self.iter_num)
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
        #print(self.iter_num)
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
            #print(self.f_global_best)

def main():

    iter_num = 500
    size  = 1000
    pso = PSO(iter_num, size)
    for x,y,f in pso.update():
        print(pso.x_global_best, '\t', pso.y_global_best,'\t',pso.f_global_best)
    print('result coordinate:', pso.x_global_best, '\t', pso.y_global_best,'\t',pso.f_global_best)

    #print(E_battery)

if __name__ == '__main__':
    main()