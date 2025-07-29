import pygame
import paho.mqtt.client as mqtt
from collections import deque
import json
import threading

# ---------- 配置 ----------
MQTT_BROKER = "192.168.3.51"   # 改成你的 ESP32/MQTT 服务器地址
MQTT_TOPIC  = "sensor/data"

W, H = 240, 320
BUF        = 60            # 60 点 ≈ 5 分钟

PAGE_EVT   = pygame.USEREVENT + 1
SAMPLE_EVT = pygame.USEREVENT + 2

# 5个通道：T H P UV LUX
CHANNELS = ["Temperature", "Humidity", "AirPressure", "UVLight", "illuminance"]
# CHANNELS = ["温度", "湿度", "气压", "紫外线", "光照度"]
UNITS    = ["°C", "%", "hPa", "UV", "lux"]
COLORS   = [(255,50,50),(50,255,50),(50,50,255),(255,255,0),(255,255,255)]

# 缓存：每个通道一个 deque
data   = [deque([0]*BUF, maxlen=BUF) for _ in range(len(CHANNELS))]

pygame.init()
screen = pygame.display.set_mode((W, H))
clock  = pygame.time.Clock()
font   = pygame.font.SysFont('arial', 16)

# ---------- MQTT ----------
latest = [0.0] * len(CHANNELS)
lock   = threading.Lock()

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print("RAW:", msg.payload)
    try:
        j = json.loads(msg.payload.decode())
        with lock:
            for i, key in enumerate(CHANNELS):
                if key in j:
                    latest[i] = float(j[key])
    except Exception as e:
        print("JSON error:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect_async(MQTT_BROKER, 1884, 60)
mqtt_client.loop_start()     # 后台线程不断收数据

# ---------- 布局 ----------
LEFT   = 40
RIGHT  = 5
BOTTOM = 25
TOP    = 35
PLOT_W = W - LEFT - RIGHT
PLOT_H = H - TOP - BOTTOM

def draw_page(ch):
    """绘制第 ch 通道"""
    with lock:
        vals = list(data[ch])
        cur  = latest[ch]

    y_min = min(vals) if vals else 0
    y_max = max(vals) if vals else 1
    span  = max(y_max - y_min, 1e-6)

    # 清绘制区
    plot_rect = pygame.Rect(LEFT, TOP, PLOT_W, PLOT_H)
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (0,0,0), plot_rect)

    # 坐标轴
    axis = (200,200,200)
    pygame.draw.line(screen, axis, (LEFT,TOP),(LEFT,TOP+PLOT_H),1)
    pygame.draw.line(screen, axis, (LEFT,TOP+PLOT_H),
                     (LEFT+PLOT_W,TOP+PLOT_H),1)

    # Y 轴刻度
    for ratio in (0,0.5,1):
        val = y_min + span*ratio
        y   = TOP+PLOT_H-int(ratio*PLOT_H)
        pygame.draw.line(screen,axis,(LEFT-3,y),(LEFT,y))
        txt=font.render(f"{val:.1f}",True,axis)
        screen.blit(txt,(2,y-6))

    # X 轴时间
    for i in range(0,BUF,20):
        x = LEFT+int(i/(BUF-1)*PLOT_W)
        pygame.draw.line(screen,axis,(x,TOP+PLOT_H),(x,TOP+PLOT_H+3))
        sec=i*5
        txt=font.render(f"{sec}s",True,axis)
        screen.blit(txt,(x-8,TOP+PLOT_H+5))

    # 折线
    if len(vals)>=2:
        pts=[]
        for j,v in enumerate(vals):
            x=LEFT+int(j/(BUF-1)*PLOT_W)
            y=TOP+PLOT_H-int((v-y_min)/span*PLOT_H)
            pts.append((x,y))
        pygame.draw.lines(screen,COLORS[ch],False,pts,2)

    # 标题 + 当前值
    title=font.render(f"{CHANNELS[ch]}  {cur:.2f}{UNITS[ch]}",True,(255,255,0))
    screen.blit(title,(LEFT,5))

# ---------- 主循环 ----------
pygame.time.set_timer(PAGE_EVT, 5000)
pygame.time.set_timer(SAMPLE_EVT, 5000)
page = 0

running=True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        elif e.type==PAGE_EVT:
            page=(page+1)%len(CHANNELS)
        elif e.type==SAMPLE_EVT:
            with lock:
                for i in range(len(CHANNELS)):
                    data[i].append(latest[i])
    draw_page(page)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
mqtt_client.loop_stop()

