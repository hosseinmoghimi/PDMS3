from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer
import time
import random


RETRY_TO_CONNECT_DELAY=0.3
RETRY_TO_CONNECT_TIME=1
test=True
DO_LOG=False
class LeoModbus(ModbusClient):
    def __init__(self,*args, **kwargs):
        self.user=kwargs['user'] if 'user' in kwargs else None
        if self.user is not None:
            from authentication.repo import ProfileRepo
            self.profile=ProfileRepo(self.user).me
        super(LeoModbus, self).__init__(*args, **kwargs)
    def connect(self,host,port):
        self.host(host)
        self.port(port)
        # self.host_address=host
        # self.port_no=port
        
        retry=0
        # open or reconnect TCP to server
        while not self.is_open() and retry<RETRY_TO_CONNECT_TIME:
            retry+=1
            if not self.open():
                print("unable to connect to "+host+":"+str(port))
                if DO_LOG:
                    from .models import Log
                    from .enums import LogStatusEnum
                    title=f"unable to connect to {self.host_address}:{self.port_no} "
                    print(title)
                    log=Log(title=title,profile=self.profile,status=LogStatusEnum.UNABLE_TO_CONNECT)
                    log.save()

            time.sleep(RETRY_TO_CONNECT_DELAY)

    def write_single_coil(self,address,value):
        if self.is_open():           
            is_ok = super(LeoModbus,self).write_single_coil(address, value)
    def read_holding_registers(self,address,count):
        if self.is_open():
            self.regs=[]
            # read 10 registers at address 0, store result in regs list
            regs = super(LeoModbus,self).read_holding_registers(address, count)
            if not regs:
                return
            for reg in regs:
                from .utils import word_to_int
                reg=word_to_int(str(reg),16)
                self.regs.append(reg)
            print("reg ad #0 to 9: "+str(self.regs))
            # if success display registers
            if self.regs:
                print("reg ad #0 to 9: "+str(self.regs))
                return self.regs

    def read_coils(self,address,count):
        if self.is_open():
            # address=1
            print("address: "+str(address))
            # read 10 registers at address 0, store result in regs list
            self.regs = super(LeoModbus,self).read_coils(address, count)
            # if success display registers
            if self.regs:
                print("regs: "+str(self.regs))
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