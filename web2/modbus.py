from .models import Log
from .enums import LogStatusEnum
from .utils import word_to_int
from django.http import request
from authentication.repo import ProfileRepo
from pyModbusTCP.client import ModbusClient
import time
import random


RETRY_TO_CONNECT_DELAY=0.3
RETRY_TO_CONNECT_TIME=2
test=True
DO_LOG=False
class LeoModbus(ModbusClient):
    def __init__(self,*args, **kwargs):
        self.user=kwargs['user'] if 'user' in kwargs else None
        if 'request' in kwargs:
            self.request=kwargs['request'] 
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user'] 
        if self.user is None:
            return
        self.profile=ProfileRepo(request=self.request).me
        super(LeoModbus, self).__init__()
    def connect(self,host,port):
        self.host(host)
        self.port(port)
        retry=0
        # open or reconnect TCP to server
        while not self.is_open() and retry<RETRY_TO_CONNECT_TIME:
            if self.open():
                print(self.host() +" is Open")
            retry+=1
            if not self.open():
                print("unable to connect to "+host+":"+str(port))
                if DO_LOG:
                    title=f"unable to connect to {self.host_address}:{self.port_no} "
                    print(title)
                    log=Log(title=title,profile=self.profile,status=LogStatusEnum.UNABLE_TO_CONNECT)
                    log.save()

            time.sleep(RETRY_TO_CONNECT_DELAY)

    def write_single_coil(self,address,value):
        is_ok=False
        if self.is_open():           
            is_ok = super(LeoModbus,self).write_single_coil(address, value)
        return is_ok
    def read_holding_registers(self,address,count):
        if self.is_open():
            self.regs=[]
            # read 10 registers at address 0, store result in regs list
            regs = super(LeoModbus,self).read_holding_registers(address, count)
            # regs = super(LeoModbus,self).read_holding_registers(1000, 2)
            if not regs:
                return
            for reg in regs:
                reg=word_to_int(str(reg),16)
                self.regs.append(reg)
            
            # print("reg ad #0 to 9: "+str(self.regs))
            # if success display registers
            if self.regs:
                # print(f"registers [{address}-{address+count}] : "+str(self.regs))
                return self.regs
    def disconnect(self):
        self.close()
    def read_coils(self,address,count):
        print(f"read_coils")
        print(f"address:{address}")
        print(f"count:{count}")
        if self.is_open():
            # address=1
            # read 10 registers at address 0, store result in regs list
            self.regs = super(LeoModbus,self).read_coils(address, count)
            # if success display registers
            if self.regs:
                print(f"coils[{address}-{address+count}] : "+str(self.regs))
                return self.regs
        else:
            if DO_LOG:
                from .models import Log
                from .enums import LogStatusEnum
                title=f"cannot connect to {self.host_address}:{self.port_no} "
                print(title)
                log=Log(title=title,profile=self.profile,status=LogStatusEnum.CAN_NOT_CONNECT)
                log.save()
            # print('is not open!')
            pass

def main():
    modbus=LeoModbus()
    port=502
    host="192.168.0.193"
    modbus.connect(host=host,port=port)
    modbus.write_single_coil(address=31,value=False)


if __name__=="__main__":
    main()