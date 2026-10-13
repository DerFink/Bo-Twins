import socket,base64,sys
s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind(('127.0.0.1',2525)); s.listen(5); s.settimeout(40); out=open('smtp.log','w')
try:
    while True:
        c,_=s.accept(); f=c.makefile('rwb'); w=lambda t:(f.write((t+'\r\n').encode()),f.flush()); w('220 fake ESMTP'); data=False; buf=[]; st=0
        while True:
            l=f.readline()
            if not l: break
            t=l.decode('utf-8','replace').rstrip('\r\n')
            if data:
                if t=='.': data=False; out.write('MAIL\n'+'\n'.join(buf)+'\n----\n'); out.flush(); buf=[]; w('250 ok queued')
                else: buf.append(t)
                continue
            u=t.upper()
            if st==1: st=2; out.write('user '+base64.b64decode(t).decode()+'\n'); w('334 UGFzc3dvcmQ6'); continue
            if st==2: st=0; out.write('pass ok\n'); w('235 ok'); continue
            if u.startswith('EHLO'): f.write(b'250-fake\r\n250 AUTH LOGIN\r\n'); f.flush()
            elif u.startswith('AUTH LOGIN'): st=1; w('334 VXNlcm5hbWU6')
            elif u.startswith('MAIL FROM') or u.startswith('RCPT TO'): out.write(t+'\n'); w('250 ok')
            elif u=='DATA': data=True; w('354 go')
            elif u=='QUIT': w('221 bye'); break
            else: w('250 ok')
        c.close()
except socket.timeout: pass
