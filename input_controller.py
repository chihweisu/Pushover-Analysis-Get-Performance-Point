from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import  QFileDialog
from input import Ui_PushoverCurve
from datetime import datetime
import numpy as np
import math
from data_function import Interpolate_data,find_api,get_k

class input_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.input = Ui_PushoverCurve()
        self.input.setupUi(self)
        self.setup_control()

    def setup_control(self):
        # TODO
        self.input.Browse.clicked.connect(self.BrowseClicked)
        self.input.savebutton.clicked.connect(self.SavebuttonClicked)
        self.input.iterationbutton.clicked.connect(self.IterationbuttonClicked)

    def BrowseClicked(self):
        fname=QFileDialog.getOpenFileName(self)
        self.input.filename.setText(fname[0])

    def SavebuttonClicked(self):
        self.input.plotwidget.canvas.figure.savefig('Capacity vs Demand.png',dpi=300)

    def IterationbuttonClicked(self):
        try:
            #檔案讀取
            with open(self.input.filename.text(),'r') as file :
                Sa_capacity=[]
                Sd_capacity=[]
                for line in file.readlines():
                    data=line.split("\t")
                    Sd_capacity.append(float(data[0]))
                    Sa_capacity.append(float(data[1]))
            Ca=float(self.input.Ca.text())
            Cv=float(self.input.Cv.text())
            type=self.input.type.currentText()

            [Sd_capacity,Sa_capacity]=Interpolate_data(Sd_capacity,Sa_capacity,200)
            T_M=Cv/(2.5*Ca)
            T=np.arange(0,6.5,0.05)
            Sa_demand=[round(2.5*Ca,3) if t<T_M else round(Cv/t,3) for t in T]
            Sd_demand=[round((T/(2*math.pi))**2*Sa*9.81,3) for (T,Sa) in zip(T,Sa_demand)]
            
            #//////初始勁度斜線與需求譜交點///
            self.input.textBrowser.setText("Iteration Start")
            self.input.plotwidget.canvas.axes.clear()
            self.input.plotwidget.canvas.axes.plot(Sd_capacity,Sa_capacity,color='DodgerBlue',label='Capacity Spectrum')
            self.input.plotwidget.canvas.axes.plot(Sd_demand,Sa_demand,color='tomato',label='Deamand Spectrum')
            self.input.plotwidget.canvas.draw()
            m=(Sa_capacity[1]-Sa_capacity[0])/(Sd_capacity[1]-Sd_capacity[0])  #初始勁度斜率
            for i in range(len(Sd_demand)) :
                if m*Sd_demand[i]>Sa_demand[i]:
                    x_first=Sd_demand[i]
                    break

            #////找出初始試誤點////////
            dpi=x_first
            line_color=["DarkSeaGreen","DimGray","Khaki","LightPink","MediumPurple"]
            #/////開始迴圈/////////////////
            for trial in range(int(Sd_demand[-1]*100)):
                [api,x_cal,y_cal]=find_api(dpi,Sa_capacity,Sd_capacity)
                #/////計算雙線性面積以求的降伏點 dy ay////
                area_0=np.trapz(y_cal,x_cal,dx=0.001)
                math_b=dpi*m-api
                math_c=2*area_0-dpi*api
                dy=round(math_c/math_b,4)
                ay=round(m*dy,4)
                #///求折減後的需求反應譜
                dmp_0=63.7*(ay*dpi-dy*api)/(dpi*api)
                k=get_k(type,dmp_0,dy,ay,dpi,api)

                dmp_eff=round(k*dmp_0+5,2)
                SRA=round((3.21-0.68*np.log(dmp_eff))/2.12,3)
                SRV=round((2.31-0.411*np.log(dmp_eff))/1.65,3)
                T_Mnew=SRV/SRA*T_M
                Sa_new=[round(2.5*Ca*SRA,3) if t<T_Mnew else round(SRV*Cv/t,3) for t in T]
                Sd_new=[round((x/(2*math.pi))**2*y*9.81,3) for (x,y) in zip(T,Sa_new)]
                self.input.plotwidget.canvas.axes.plot(Sd_new,Sa_new,color=line_color[trial%len(line_color)])
                #/////找折減後的需求反應譜與容量譜的交點///////////////////
                for j in range(len(Sd_capacity)):
                    delta=np.array([Sd-Sd_capacity[j] for Sd in Sd_new])
                    result=np.argwhere(delta>0)
                    demand_index=result[0][0]
                    if Sa_capacity[j]-Sa_new[demand_index]>0:
                        x_intersection=round(Sd_capacity[j],3)
                        y_intersection=round(Sa_capacity[j],3)
                        break
                error=(((x_intersection-dpi)/dpi)**2+((y_intersection-api)/api)**2)**0.5*100
                output="第{}次疊代，試誤點為({},{})，等效阻尼比為{}%，誤差為{}%" \
                    .format(str(trial+1),str(dpi),str(api),str(dmp_eff),str(round(error,2)))
                self.input.textBrowser.append(output)
                if error<5:
                    self.input.plotwidget.canvas.axes.plot(dpi,api,marker='o',color='red',markersize=6,\
                        label='Performance Point\n({},{})'.format(str(round(dpi,3)),str(round(api,3))))
                    self.input.plotwidget.canvas.axes.plot(Sd_new,Sa_new,color='tomato')
                    self.input.plotwidget.canvas.axes.plot([0,dy,dpi],[0,ay,api],color='black',linestyle='--')
                    break
                dpi=round(max(dpi-0.005,x_intersection),3)
                
            self.input.plotwidget.canvas.axes.set_xlabel('Spectral Displacement (m)')
            self.input.plotwidget.canvas.axes.set_ylabel('Spectral Acceleration/g ')
            self.input.plotwidget.canvas.axes.grid(True,linestyle='--', color='black',alpha=0.3)
            self.input.plotwidget.canvas.axes.legend(fontsize=8.5)
            self.input.plotwidget.canvas.axes.set_xlim(left=0)
            self.input.plotwidget.canvas.axes.set_ylim(bottom=0)
            self.input.plotwidget.canvas.draw()
            self.input.textBrowser.append('Iteration finished  '+ datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        except (FileNotFoundError, ValueError):
            self.input.textBrowser.setText("Input Error")
        except (UnboundLocalError, NameError,IndexError):
            self.input.textBrowser.append("Peformance point not found")

        




    

  




    




   

       
 

    # set the layout
    #   layout = QtGui.QVBoxLayout()
    #   layout.addWidget(self.toolbar)
    #   layout.addWidget(self.canvas)
    #   layout.addWidget(self.button)
    #   self.setLayout(layout)


      
    
    # windowList= []
    # def FlexCalClicked(self):
    #   thewindow = QtWidgets.QMainWindow()
    #   self.ui = FlexCal_controller()
    #   self.windowList.append(thewindow)
    #   thewindow.show()
