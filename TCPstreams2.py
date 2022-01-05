#!/usr/bin/env python3
import socket

defaultport = 5000
buf=4096

class client:
  def __init__(self,Host,Port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host, Port))
    self.s = s
    
  def getdat(self):
    return self.s.recv(buf)
  def getstdat(self):
    return self.getdat().decode('utf-8')

  def senddat(self,bindat):
    try:
      self.s.send(bindat)
      return True
    except socket.error:
      #print('Client Connection Closed')
      return False
    
  def sendstdat(self,strdat):
    try:
      self.s.send(bytes(strdat,'utf-8'))
      return True
    except socket.error:
      #print('Client Connection Closed')
      return False

  def close(self):
    self.s.close()

OBJS = []
class server:
  def __init__(self,Host,Port):
    global OBJS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((Host, Port))
    s.listen(1)
    self.s = s
    self.id = len(OBJS)
    OBJS.append(self.s)
    
    
  class accept:
      def __init__(main,self):
        conn, addr = self.s.accept()
        main.conn = conn
        

      def senddat(main,bindat):
        try:
          main.conn.send(bindat)
          return True
        except socket.error:
          #print('Client Connection Closed')
          return False
      def sendstdat(main,strdat):
        try:
          main.conn.send(bytes(strdat,'utf-8'))
          return True
        except socket.error:
          #print('Client Connection Closed')
          return False
      def getdat(main):
       return main.conn.recv(buf)
      def getstdat(main):
       return main.getdat().decode('utf-8')
        
      def close(main):
        main.conn.close()
    
  
