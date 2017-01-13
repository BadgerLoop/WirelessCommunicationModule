import socket, sys, yaml, riffle

# Get configuration variables from config.yml
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
print(cfg)

class CANSocket(object):
  FORMAT = "<IB3x8s"
  FD_FORMAT = "<IB3x64s"
  CAN_RAW_FD_FRAMES = 5

  def __init__(self, interface=None):
    self.sock = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    if interface is not None:
      self.bind(interface)

  def bind(self, interface):
    self.sock.bind((interface,))
    self.sock.setsockopt(socket.SOL_CAN_RAW, self.CAN_RAW_FD_FRAMES, 1)

  def send(self, cob_id, data, flags=0):
    cob_id = cob_id | flags
    can_pkt = struct.pack(self.FORMAT, cob_id, len(data), data)
    self.sock.send(can_pkt)

  def recv(self, flags=0):
    can_pkt = self.sock.recv(72)

    if len(can_pkt) == 16:
      cob_id, length, data = struct.unpack(self.FORMAT, can_pkt)
    else:
      cob_id, length, data = struct.unpack(self.FD_FORMAT, can_pkt)

    cob_id &= socket.CAN_EFF_MASK
    return (cob_id, data[:length])


def format_data(data):
    return ''.join([hex(byte)[2:] for byte in data])


def generate_bytes(hex_string):
    if len(hex_string) % 2 != 0:
      hex_string = "0" + hex_string

    int_array = []
    for i in range(0, len(hex_string), 2):
        int_array.append(int(hex_string[i:i+2], 16))

    return bytes(int_array)


def send_cmd(args):
    try:
      s = CANSocket(args.interface)
    except OSError as e:
      sys.stderr.write('Could not send on interface {0}\n'.format(args.interface))
      sys.exit(e.errno)

    try:
      cob_id = int(args.cob_id, 16)
    except ValueError:
      sys.stderr.write('Invalid cob-id {0}\n'.format(args.cob_id))
      sys.exit(errno.EINVAL)

    s.send(cob_id, generate_bytes(args.body), socket.CAN_EFF_FLAG if args.extended_id else 0)


def listen_cmd(cfg):
    try:
      s = CANSocket(cfg['can']['interface'])
    except OSError as e:
      sys.stderr.write('Could not listen on interface %s' % (cfg['interface'], ))
      sys.exit(e.errno)

    #print 'Listening on %s' % (cfg['interface'], )

    while True:
        cob_id, data = s.recv()
        #print('%s %03x#%s' % (cfg['can']['interface'], cob_id, format_data(data)))


class Send(riffle.Domain):

    def onJoin(self):
        print("Connected to Exis Node")
        self.subscribe(cmd, self.subscription)

    def subscription(self, command):
        print("Received message %s\n" %(command,))

class DataProvider(riffle.Domain):

    def onJoin(self):
        print("Successfully joined")

        while True:
            sender.publish(ep, data)
            switch[data[0]]('data', backend)
    
def main():
	#riffle.SetLogLevelDebug()
    # riffle.SetFabric(cfg['fabric'])
    # domain = cfg['domain']
    # Send(domain).join()
    listen_cmd(cfg)

if __name__ == '__main__':
    main()



