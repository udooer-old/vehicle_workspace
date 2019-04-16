import smbus
import math
import time

def start():
    
    alonzo = smbus.SMBus(1)
    X=[]
    Y=[]
    Z=[]
    #x = alonzo.read_byte_data(0x1e,3)
    
    alonzo.write_byte_data(0x1c,0x20,0x7c) #ultra mode odr 80hz    
    alonzo.write_byte_data(0x1c,0x21,0x20) #fullscale 8g    
    alonzo.write_byte_data(0x1c,0x22,0x00) #continous conversion mode
    
    print("Loading...")
    time.sleep(0.5)
    for i in range(1,200):
    
        block =  alonzo.read_i2c_block_data( 0x1c,0x028,6)
    
        XGUS = block[1]*256+block[0]
        if XGUS > 32767:
            XGUS -= 65536
        YGUS = block[3]*256+block[2]
        if YGUS > 32767:
            YGUS -= 65536
        ZGUS = block[5]*256+block[4]
        if ZGUS > 32767:
            ZGUS -= 65536
    
        X.append(XGUS)
        Y.append(YGUS)
        Z.append(ZGUS)
        print(XGUS,YGUS,ZGUS)
    
        time.sleep(0.1)
    
    
    Xoffset=0.5*(max(X)+min(X))#multiply by ten, cuz register store int only
    Yoffset=0.5*(max(Y)+min(Y))
    Zoffset=0.5*(max(Z)+min(Z))
    
    f = open("../calibration.txt",'w')
    Xoff=str(Xoffset)
    Yoff=str(Yoffset)
    Zoff=str(Zoffset)
    f.writelines(Xoff+"\n"+Yoff+"\n"+Zoff+"\n")
    f.close()
    
    alonzo.close()
