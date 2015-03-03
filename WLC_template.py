
class WLC_SSH(object):

    def __init__(self,device,port,user,passwd):
        self.device=device
        self.port=port
        self.user=user
        self.passwd=passwd
        self.temp=paramiko.SSHClient()
        self.temp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.temp.connect(device, username= user, password=passwd)
        self.session=self.temp.invoke_shell()
        
        #Log into the WLC
        self.session.send(user)
        self.session.send("\n")
        self.session.send(passwd)
        self.session.send("\n")
        print 'You have logged in '
    
    def disable_paging(self):
        self.session.send('\n')
        self.session.send('config paging disable')
        self.session.send('\n')
        time.sleep(2)
        print 'disabled paging'

    def clean_buffer(self):
        loop=0
        while loop < 30:
            if self.session.recv_ready():
                rubbish=self.session.recv(65535)
                time.sleep(3)
            loop+=1

        print 'buffer cleaned'


    def Hostname(self):
        self.session.send('\n')
        time.sleep(0.5)
        host=self.session.recv(8000).decode('ascii')
        return host


    def run_commamd(self,command,host,delay,max_loops=15):
        print 'retrieving data please wait'
        self.session.send('\n')
        self.session.send(command)
        self.session.send('\n')
        time.sleep(delay)
        DEBUG=False
        output=''
    
        MAX_BUFFER=65535
        not_done = True
        i = 1
        while (not_done) and (i <= max_loops):
            print '!'
            if DEBUG: print ("In while loop")
            time.sleep(2*delay)
            i += 1
            # Keep reading data as long as available (up to max_loops)
            if self.session.recv_ready():
                if DEBUG: print ("recv_ready = True")
                DataToStr=self.session.recv(MAX_BUFFER).decode('ascii')
                output += DataToStr
            else:
                if DEBUG: print ("recv_ready = False")
                not_done = False
        output=output.strip(host)
        output=output.strip(command)
        return output

    def close_conn(self):
         self.session.close() #Close the SSH connection
