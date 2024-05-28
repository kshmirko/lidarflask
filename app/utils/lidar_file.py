from math import log2, floor
from datetime import datetime

def filter_data(inp):
    filtered = []
    i = 0
    while i < len(inp)-1:
        if (inp[i]==0x0d) and (inp[i+1]==0x0a):
            filtered.append(inp[i+1])
            i+=1
        else:
            filtered.append(inp[i])        
        i+=1

    filtered.append(inp[i])

    return filtered

class LidarFile:

    def __init__(self, fname)->None:
        if type(fname)==str:
            with open(fname, 'rb') as fin:
                self.read(fin)
        else:
            self.read(fname)

    def read(self, fin)->None:
        
        
        inp = fin.read(-1)
        fileLen = len(inp)-18
        log2filelen = log2(fileLen)
        if log2filelen!=floor(log2filelen):
            inp = filter_data(inp)
        
        data16 = []
        for i in range(len(inp)//2):
            data16.append((inp[i*2+1]<<8)|(inp[i*2]))
        
        self.start_time = datetime(data16[0], data16[1]+1, data16[2], data16[3], data16[4], data16[5])
        self.prof_len = data16[6]
        self.count = data16[7]
        self.rep_rate = data16[8]
        recorded_size = self.prof_len*self.count
        profile = data16[9:9+recorded_size]
        self.data = [0]*self.prof_len
        
        offset = 0

        for i in range(self.count):
            for j in range(self.prof_len):
                self.data[j] = self.data[j]+ profile[j+offset]
            offset+=self.prof_len
        
            


        pass

    