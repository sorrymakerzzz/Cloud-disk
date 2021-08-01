import numpy as np

#双线性插值
def bli(i,j,p,q):
    Y_00=d[i][j]
    Y_10=d[i][j+1]
    Y_11=d[i+1][j+1]
    Y_01=d[i+1][j]
    t=q*4/24
    u=p*6/24
    s=(1-t)*(1-u)*Y_00+t*(1-u)*Y_10+t*u*Y_11+(1-t)*u*Y_01
    return s

#二维3次卷积插值
def cci(i,j,p,q):
    dx=(q*4)/24
    dz=(p*6)/24
    C=np.array([[d[i-1][j-1],d[i-1][j],d[i-1][j+1],d[i-1][j+2]],
       [d[i][j-1],d[i][j],d[i][j+1],d[i][j+2]],
       [d[i+1][j-1],d[i+1][j],d[i+1][j+1],d[i+1][j+2]],
       [d[i+2][j-1],d[i+2][j],d[i+2][j+1],d[i+2][j+2]]])    
    a_x=-1*pow(dx,3)+2*pow(dx,2)-dx
    b_x=3*pow(dx,3)-5*pow(dx,2)+2
    c_x=-3*pow(dx,3)+4*pow(dx,2)+dx
    d_x=pow(dx,3)-pow(dx,2)
    
    a_z=-1*pow(dz,3)+2*pow(dz,2)-dz
    b_z=3*pow(dz,3)-5*pow(dz,2)+2
    c_z=-3*pow(dz,3)+4*pow(dz,2)+dz
    d_z=pow(dz,3)-pow(dz,2)

    A=np.array([a_z,b_z,c_z,d_z])
    B=np.array([[a_x],[b_x],[c_x],[d_x]])
    s=1/4*A@C@B
    return s
#读取数据
d=np.loadtxt('md.txt')

#创建插值后的数组
d1=np.zeros([485,2299])

#双线性插值
#对数据进行处理
for i in range(122):
    for j in range(384):
        for p in range(5):
            for q in range(7):
                if (p in [0,4])&(q in [0,6]):
                    d1[i*4][j*6]=d[i][j]
                else:
                    if i==121 or j==383:
                        break
                    d1[i*4+p][j*6+q]=bli(i,j,p,q)

#将处理后的数据保存到另一文本中
np.savetxt('双线性插值.txt',d1,delimiter="  ")

#二维三次卷积插值
#对数据进行处理
for i in range(1,121):
    for j in range(1,383):
        for p in range(5):
            for q in range(7):
                if (p in [0,4])&(q in [0,6]):
                    d1[i*4][j*6]=d[i][j]
                else:
                    if i==120 or j==382:
                        break
                    d1[i*4+p][j*6+q]=cci(i,j,p,q)

#将处理后的数据保存到另一文本中
np.savetxt('二维三次卷积插值.txt',d1,delimiter="  ")

