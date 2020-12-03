#!/usr/bin/env python
# coding: utf-8

# In[209]:


#Импорт библиотек
import scipy as sci
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation


# In[210]:


#Задаем константы
G=6.67408e-11 

#Задаем переменные
MassND = 1.989e+30 #Масса солнца [кг]
DistanceND = 5.326e+12 #Растояние до Звезд1 [м]
VecolotyND = 30000 #относительная скорость Земли вокруг Солнца [м/с]
TimeND = 79.91 * 365 * 24 * 3600 * 0.51 #орбитальный период Звеззды №1

#Чистые константы
K1=G * TimeND * MassND / (DistanceND ** 2 * VecolotyND)
K2=VecolotyND * TimeND / DistanceND


# In[211]:


#Определение масс
Mass1 = 1.1 #Звезда №1
Mass2 = 0.907 #Звезда №2

#Определение векторов начальной позиции
Distance1 = [-0.5, 0, 0] #м
Distance2 = [0.5, 0, 0] #м

#Преобразование Радиус векторов в массивы
Distance1 = sci.array(Distance1, dtype = "float64")
Distance2 = sci.array(Distance2, dtype = "float64")

#Поиск Центра Масс
DistanceCom=(Mass1 * Distance1 + Mass2 * Distance2) / (Mass1 + Mass2)

#Инициализация векторов скорости
Vecoloty1 = [0.01, 0.01, 0] #м/с
Vecoloty2 = [-0.05, 0, -0.1] #м/с

#Преобразование векторов скорости в массивы
Vecoloty1 = sci.array(Vecoloty1,dtype="float64")
Vecoloty2 = sci.array(Vecoloty2,dtype="float64")

#Нахождение скорости Центра Масс
VecolotyCom = (Mass1 * Vecoloty1 + Mass2 * Vecoloty2) / (Mass1 + Mass2)


# In[212]:


#Функция, определяющая уравнения движения
def TwoBodyEquations(w, Time, G, Mass1, Mass2):
    Distance1 = w[:3]
    Distance2 = w[3:6]
    Vecoloty1 = w[6:9]
    Vecoloty2 = w[9:12]
    
    Distance = sci.linalg.norm(Distance2 - Distance1) #Вычисление величины или норму вектора
    dv1bydt = K1 * Mass2 * (Distance2 - Distance1) / Distance ** 3
    dv2bydt = K1 * Mass1 * (Distance1 - Distance2) / Distance ** 3
    dr1bydt = K2 * Vecoloty1
    dr2bydt = K2 * Vecoloty2
    
    DistanceDerivs = sci.concatenate((dr1bydt, dr2bydt))
    Derivs=sci.concatenate((DistanceDerivs, dv1bydt, dv2bydt))
    
    return Derivs


# In[213]:


#Первоначальные параметры
InitParams = sci.array([Distance1, Distance2, Vecoloty1, Vecoloty2]) #
InitParams = InitParams.flatten() #flatten делает массив однамерным 
TimeSpan = sci.linspace(0,8,500) #8 орбитальных периодов 50 точек


import scipy.integrate

TwoBodySol = sci.integrate.odeint(TwoBodyEquations, InitParams, TimeSpan, args = (G,m1,m2))


# In[214]:


Distance1Sol = TwoBodySol[:,:3]
Distance2Sol = TwoBodySol[:,3:6]


# In[215]:


#Поиск местоположения Центра Масс
DistanceComSol = (Mass1 * Distance1Sol + Mass2 * Distance2Sol) / (Mass1 + Mass2)

#Нахождения местоположения Звезды №1
Distance1ComSol = Distance1Sol - DistanceComSol

#Нахождения местоположения Звезды №2
Distance2comSol = Distance2Sol - DistanceComSol


# In[216]:


#Cоздаем график
fig = plt.figure(figsize = (15,15))

#Задаем 3 оси пространства
ax = fig.add_subplot(111,projection="3d")

#Plot the orbits
ax.plot(Distance1ComSol[:,0], Distance1ComSol[:,1], Distance1ComSol[:,2], color = "darkblue")
ax.plot(Distance2comSol[:,0], Distance2comSol[:,1], Distance2comSol[:,2], color = "tab:red")

#строим финальные позиции звезд
ax.scatter(Distance1ComSol[-1,0], Distance1ComSol[-1,1], Distance1ComSol[-1,2], color="darkblue", marker="o", s=100, label="Звезда №1")
ax.scatter(r2com_sol[-1,0],r2com_sol[-1,1],r2com_sol[-1,2],color="tab:red",marker="o",s=100,label="Звезда №2")
#небольшие дети
ax.set_xlabel("по иксу",fontsize=14)
ax.set_ylabel("по игреку",fontsize=14)
ax.set_zlabel("по зэду",fontsize=14)
ax.set_title("Визуализация Орбит двойной звездной системы\n",fontsize=14)
ax.legend(loc="upper left",fontsize=14)


# In[ ]:




