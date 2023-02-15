import numpy as np
import math
from scipy.interpolate import interp1d # 導入 scipy 中的一維插值工具 interp1d

def interpolate_data(x,y,n):
    # 由給定數據點集 (x,y) 求插值函數 fx
    fx = interp1d(x, y,kind='linear') # 由已知數據 (x,y) 求出插值函數 fx
    # 由插值函數 fx 計算插值點的函數值
    xInterp = np.linspace(min(x),max(x),n) # 指定需插值的數據點集 xInterp
    yInterp = fx(xInterp) # 調用插值函數 fx，計算 xInterp 的函數值
    return list(xInterp),list(yInterp)

def math_quadratic_equation(matha,mathb,mathc):
        q=mathb**2-4*matha*mathc
        if q<0:
            output="Your equation has no root."
        elif q==0:
            output=-mathb/2*matha
        else:
            q1=(-mathb+q**0.5)/(2*matha)
            q2=(-mathb-q**0.5)/(2*matha)
            output=[q1, q2]
        return output 

def find_api(dpi,Sa_capacity,Sd_capacity):
    result=np.argwhere(Sd_capacity>dpi)
    i=result[0][0]
    api=round(Sa_capacity[i-1]+(Sa_capacity[i]-Sa_capacity[i-1])*(dpi-Sd_capacity[i-1]) \
        /(Sd_capacity[i]-Sd_capacity[i-1]),3)
    x_cal=Sd_capacity[:i]
    x_cal.append(dpi)
    y_cal=Sa_capacity[:i]
    y_cal.append(api)
    return api,x_cal,y_cal

def get_k(type,dmp_0,dy,ay,dpi,api):
    if type=="A":
        k=1 if dmp_0<16.2 else 1.13-0.51*(ay*dpi-dy*api)/(dpi*api)
    elif type=="B":
        k=0.67 if dmp_0<25 else 0.845-0.446*(ay*dpi-dy*api)/(dpi*api)
    elif type=="C":
        k=0.33
    return k