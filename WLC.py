# WLC_SSH
import paramiko
import time


def WLC_SSH_Login(remote,user,passwd):

    #Log into the WLC
    remote.send(user)
    remote.send("\n")
    remote.send(passwd)
    remote.send("\n")

    print 'You have logged in '

def disable_paging(remote):
    remote.send('\n')
    remote.send('config paging disable')
    remote.send('\n')
    time.sleep(2)
    print 'disabled paging'

def clean_buffer(remote):
    loop=0
    while loop < 30:
        if remote.recv_ready():
            rubbish=remote.recv(65535)
            time.sleep(3)
        loop+=1

    print 'buffer cleaned'


def Hostname(remote):
    remote.send('\n')
    time.sleep(0.5)
    host=remote.recv(8000).decode('ascii')

    return host


def run_commamd(remote, command,host,delay,max_loops=15):
    print 'retrieving data please wait'
    remote.send('\n')
    remote.send(command)
    remote.send('\n')
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
        if remote.recv_ready():
            if DEBUG: print ("recv_ready = True")
            DataToStr=remote.recv(MAX_BUFFER).decode('ascii')
            output += DataToStr
        else:
            if DEBUG: print ("recv_ready = False")
            not_done = False
    output=output.strip(host)
    output=output.strip(command)
    return output






if __name__ == "__main__":
    user='x'
    passwd='x'
    device='x.x.x.x'




    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(device, username= user, password=passwd)
    remote_conn = remote_conn_pre.invoke_shell()


    WLC_SSH_Login(remote_conn,user,passwd)



    disable_paging(remote_conn)

    clean_buffer(remote_conn)

    host=Hostname(remote_conn)

    out=run_commamd(remote_conn,'show ap summary',host,3)

    print out



    remote_conn.close() #Close the SSH connection
