

import os
import esptool
from flashtool.version import VERSION

class Flasher():
    def getVersion(self):
        return ("Version %s, esptool %s"%(VERSION,str(esptool.__version__)))
    FULLOFFSET=61440
    HDROFFSET = 288
    VERSIONOFFSET = 16
    NAMEOFFSET = 48
    MINSIZE = HDROFFSET + NAMEOFFSET + 32
    CHECKBYTES = {
        0: 0xe9,  # image magic
        288: 0x32,  # app header magic
        289: 0x54,
        290: 0xcd,
        291: 0xab
    }

    def getString(self,buffer, offset, len):
        return buffer[offset:offset + len].rstrip(b'\0').decode('utf-8')

    def getFirmwareInfo(self,ih,imageFile,offset):
        buffer = ih.read(self.MINSIZE)
        if len(buffer) != self.MINSIZE:
            return self.setErr("invalid image file %s, to short"%imageFile)
        for k, v in self.CHECKBYTES.items():
            if buffer[k] != v:
                return self.setErr("invalid magic at %d, expected %d got %d"
                                % (k+offset, v, buffer[k]))
        name = self.getString(buffer, self.HDROFFSET + self.NAMEOFFSET, 32)
        version = self.getString(buffer, self.HDROFFSET + self.VERSIONOFFSET, 32)
        return {'error':False,'info':"%s:%s"%(name,version)}

    def setErr(self,err):
        return {'error':True,'info':err}
    def checkImageFile(self,filename,isFull):
        if not os.path.exists(filename):
            return self.setErr("file %s not found"%filename)
        with open(filename,"rb") as fh:
            offset=0
            if isFull:
                b=fh.read(1)
                if len(b) != 1:
                    return self.setErr("unable to read header")
                if b[0] != 0xe9:
                    return self.setErr("invalid magic in file, expected 0xe9 got 0x%02x"%b[0])
                st=fh.seek(self.FULLOFFSET)
                offset=self.FULLOFFSET
            return self.getFirmwareInfo(fh,filename,offset)


    def checkSettings(self,port,fileName,isFull):
        if port is None:
            print("ERROR: no com port selected")
            return
        if fileName is None or fileName == '':
            print("ERROR: no filename selected")
            return
        info = self.checkImageFile(fileName, isFull)
        if info['error']:
            print("ERROR: %s" % info['info'])
            return
        return {'port':port,'isFull':isFull}

    def runEspTool(self,command):
        print("run esptool: %s" % " ".join(command))
        try:
            esptool.main(command)
            print("esptool done")
        except Exception as e:
            print("Exception in esptool %s" % e)
            raise

    def runCheck(self,port,fileName,isFull):
        param = self.checkSettings(port,fileName,isFull)
        if not param:
            return
        print("Settings OK")
        command = ['--chip', 'ESP32', '--port', param['port'], 'chip_id']
        self.runEspTool(command)

    def runFlash(self,port,fileName,isFull):
        param=self.checkSettings(port,fileName,isFull)
        if not param:
            return
        if param['isFull']:
            command=['--chip','ESP32','--port',param['port'],'write_flash','0x1000',fileName]
            self.runEspTool(command)
        else:
            command=['--chip','ESP32','--port',param['port'],'erase_region','0xe000','0x2000']
            self.runEspTool(command)
            command = ['--chip', 'ESP32', '--port', param['port'], 'write_flash', '0x10000', fileName]
            self.runEspTool(command)
