
import os
import sys
if os.name != 'posix':
    sys.exit('platform not supported')
import psutil
import netifaces
from datetime import datetime
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont
from pythonwifi.iwlibs import Wireless

# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "LA:%.1f %.1f %.1f Up: %s" \
            % (av1, av2, av3, str(uptime).split('.')[0])

def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
            % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
            % (bytes2human(usage.used), usage.percent)

def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))
def wifi():
    wifi = Wireless('wlan0')
    name_essid= wifi.getEssid()
    return "ESSID: %s" \
	  %  (name_essid)

def ipadr():
    ip=netifaces.ifaddresses('wlan0')[2][0]['addr']
    return"IP: %s" \
          %  (ip)
def stats(oled):
    font = ImageFont.load_default()
    #font2 = ImageFont.truetype('../fonts/C&C Red Alert [INET].ttf', 12)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
    #font = ImageFont.truetype('fonts/Minecraftia-Regular.ttf', 8)
    with canvas(oled) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill=255)
        draw.text((0, 14), mem_usage(), font=font2, fill=255)
        draw.text((0, 26), disk_usage('/'), font=font2, fill=255)
        draw.text((0, 38), wifi(), font=font2, fill=255)
        draw.text((0, 50), ipadr(), font=font2, fill=255)

def main():
    oled = ssd1306(port=0, address=0x3D)
    stats(oled)

if __name__ == "__main__":
    main()
