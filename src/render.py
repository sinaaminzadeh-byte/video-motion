import math, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import imageio_ffmpeg

W,H=540,960
F='assets/Vazirmatn-Bold.ttf'
fonts={s:ImageFont.truetype(F,s) for s in [12,14,16,18,20,22,24,26,28,30,34,38,42,48,54,62]}
blue='#146EF5'; green='#00B86B'; dark='#0A1428'; red='#E94D4F'
scenes=[(0,4,'مشتریات فقط توی اینستاگرام','دنبالت نمی‌گردن'),(4,7,'آدم‌ها قیمت محصولات رو','توی ترب مقایسه می‌کنن'),(7,10,'اگه اونجا نباشی،','رقیبت ممکنه باشه'),(10,13,'ترب مثل ویترین','یه پاساژ بزرگه'),(13,17,'مشتری مقایسه می‌کنه','و فروشگاهش رو انتخاب می‌کنه'),(17,20.5,'برای بخش خرید اینترنتی ترب','سایت فروشگاهی و اینماد لازمه'),(20.5,25,'با فروشگاه اینترنتی حرفه‌ای','مسیرهای جدید فروش باز می‌شن'),(25,30,'نواک وب','فروشگاه اینترنتیت رو بساز')]
def fa(t): return get_display(arabic_reshaper.reshape(t))
def text(d,xy,t,size,color,anchor='mm'):
 d.text(xy,fa(t),font=fonts[size],fill=color,anchor=anchor)
def rr(d,box,r,fill,outline=None,width=1): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=width)
def clamp(x): return max(0,min(1,x))
def ease(x): x=clamp(x); return 1-(1-x)**3
def product(d,x,y,col):
 rr(d,(x,y,x+76,y+78),18,col); d.arc((x+23,y+17,x+53,y+54),180,360,fill='white',width=3); rr(d,(x+22,y+35,x+54,y+61),5,'white')
def modern(t,i,p):
 im=Image.new('RGB',(W,H),'#081428'); d=ImageDraw.Draw(im)
 d.ellipse((-170,-190,390,370),fill='#10284A'); d.ellipse((350,700,800,1150),fill='#0D2544')
 text(d,(72,100),'نواک',18,'#7DAEFF'); d.line((32,135,508,135),fill='#29405F',width=2)
 # central floating UI panel, changes with narrative
 slide=int((1-ease(p*2))*60); y=270+slide
 if i==0:
  rr(d,(68,y,472,y+320),30,'#F7FAFF'); rr(d,(97,y+36,443,y+91),14,'#E5EDF9'); text(d,(270,y+63),'فقط اینستاگرام؟',26,dark)
  for n in range(3): product(d,103+n*119,y+140,['#146EF5','#00B86B','#9AAFD1'][n])
  d.line((113,y+250,428,y+250),fill='#D2DFF0',width=5)
 elif i in (1,3,4):
  rr(d,(54,y-20,486,y+350),30,'#F7FAFF'); text(d,(404,y+17),'ترب',28,red); rr(d,(82,y+44,458,y+95),12,'#ECF0F5'); text(d,(265,y+69),'جست‌وجوی محصول',16,'#637387')
  for n in range(3):
   yy=y+111+n*69; rr(d,(82,yy,458,yy+58),10,'white', '#DEE5EE'); rr(d,(96,yy+8,138,yy+50),8,['#DFEBFF','#E2F5ED','#FFE8E8'][n]); text(d,(330,yy+19),'فروشگاه '+['اول','دوم','سوم'][n],16,dark); text(d,(330,yy+42),['۱٬۲۵۰٬۰۰۰','۱٬۳۰۰٬۰۰۰','۱٬۳۸۰٬۰۰۰'][n]+' تومان',12,'#73829A')
  text(d,(270,y+328),'نمای مفهومی · قیمت‌ها فرضی',12,'#73829A')
 elif i==2:
  rr(d,(64,y+20,476,y+285),28,'#132C4C', '#36577C',2)
  for n in range(3):
   x=100+n*120; product(d,x,y+75,['#146EF5','#00B86B','#E94D4F'][n]); text(d,(x+38,y+190),['تو','رقیب','رقیب'][n],20,'white')
 elif i in (5,6):
  rr(d,(66,y,474,y+310),26,'#F6F9FF'); rr(d,(66,y,474,y+54),20,blue); text(d,(270,y+27),'فروشگاه اینترنتی',18,'white')
  for n in range(3): product(d,102+n*119,y+95,['#146EF5','#00B86B','#7894C1'][n])
  rr(d,(120,y+217,420,y+264),14,'#DDF6EB'); text(d,(270,y+240),'مسیرهای بیشتر برای دیده‌شدن',16,'#008C53')
 else:
  d.ellipse((160,y,380,y+220),fill=blue); text(d,(270,y+110),'ن',62,'white'); text(d,(270,y+290),'NOVAK WEB',22,'#86B6FF')
 # large readable message and lower caption
 text(d,(270,171),['۰۱ / فرصت','۰۲ / مقایسه','۰۳ / رقابت','۰۴ / ویترین','۰۵ / انتخاب','۰۶ / زیرساخت','۰۷ / مسیرها','۰۸ / شروع'][i],14,'#8DAED5')
 text(d,(270,690),scenes[i][2],28,'white'); text(d,(270,742),scenes[i][3],26,'#75E2B4' if i>4 else '#91BCFF')
 if i==5: text(d,(270,800),'ثبت‌نام و تأیید ترب نیز ضروری است',14,'#A9BCD5')
 if i==7: rr(d,(126,805,414,860),27,blue); text(d,(270,832),'سفارش طراحی فروشگاه',18,'white')
 d.line((45,910,495,910),fill='#243B5B',width=3); d.line((45,910,45+int(450*t/30),910),fill=green,width=4)
 return im

def editorial(t,i,p):
 bg=['#F5F1E9','#146EF5','#101B30','#F5F1E9','#00A760','#F5F1E9','#101B30','#146EF5'][i]; im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im); light=bg in ['#F5F1E9']; ink=dark if light else 'white'; accent=blue if light else '#C2FFDF'
 d.rectangle((28,52,512,56),fill=ink); text(d,(465,84),'نواک وب',16,ink); text(d,(74,84),f'0{i+1}',18,ink)
 off=int((1-ease(p*2))*100)
 # editorial typography and strong graphic device
 if i==0:
  text(d,(270+off,240),'مشتری کجاست؟',42,dark); d.rectangle((35,315,505,475),fill=blue); text(d,(270,393),'فقط اینستاگرام؟',34,'white'); d.line((75,515,465,515),fill=dark,width=5); text(d,(270,580),'نه لزوماً.',38,blue)
 elif i==1:
  text(d,(270,225),'جست‌وجو',48,'white'); rr(d,(42,315+off,498,390+off),36,'white'); text(d,(260,352+off),'محصول + مقایسه قیمت',22,dark)
  for n in range(3): rr(d,(55+n*150,465,185+n*150,615),15,['#D3E4FF','#D6FAE6','#FFD8D8'][n]); text(d,(120+n*150,540),['۱','۲','۳'][n],42,dark)
 elif i==2:
  text(d,(270,240),'جای خالی',48,'white'); d.rectangle((45,335,250,560),outline='#6D809B',width=4); text(d,(148,445),'تو؟',42,'#8193AD'); d.rectangle((285,335,495,560),fill=green); text(d,(390,445),'رقیب',38,'white')
 elif i==3:
  text(d,(270,205),'یک پاساژ',48,dark); text(d,(270,265),'بی‌انتها',38,blue)
  for n in range(3):
   x=40+n*160; rr(d,(x,360,x+140,570),12,'white', '#C9D3E1',2); d.rectangle((x,360,x+140,405),fill=[red,blue,green][n]); text(d,(x+70,480),'ویترین',18,dark)
 elif i==4:
  text(d,(270,220),'مقایسه کن',48,'white'); d.line((270,330,270,600),fill='#C2FFDF',width=5)
  for n in range(2): rr(d,(45+n*245,365,245+n*245,550),20,'white'); text(d,(145+n*245,435),'پیشنهاد',24,dark); text(d,(145+n*245,490),['الف','ب'][n],34,blue)
 elif i==5:
  text(d,(270,220),'زیرساخت',48,dark); rr(d,(55,325,485,570),24,'white','#CCD8E7',3); text(d,(270,400),'فروشگاه اینترنتی',28,blue); text(d,(270,490),'+ اینماد',38,green)
 elif i==6:
  text(d,(270,210),'یک فروشگاه',42,'white'); text(d,(270,275),'چند مسیر',42,'#8DFFCA'); d.line((270,350,270,450),fill='white',width=5); d.line((100,450,440,450),fill='white',width=5)
  for n in range(3):
   x=100+n*170; d.line((x,450,x,500),fill='white',width=5); d.ellipse((x-48,500,x+48,596),fill=[blue,green,'#F1BD5C'][n]); text(d,(x,548),['وب','ترب','جست‌وجو'][n],16,dark if n==2 else 'white')
 else:
  d.ellipse((175,200,365,390),fill='white'); text(d,(270,290),'ن',62,blue); text(d,(270,465),'نواک وب',48,'white'); rr(d,(80,570,460,635),32,'#C2FFDF'); text(d,(270,602),'وقت ساخت فروشگاهته',24,dark)
 text(d,(270,745),scenes[i][2],26,ink); text(d,(270,795),scenes[i][3],24,accent)
 if i==5: text(d,(270,850),'ثبت‌نام و تأیید ترب نیز ضروری است',14,dark)
 d.rectangle((28,914,512,917),fill=ink); d.rectangle((28,914,28+int(484*t/30),917),fill=green if light else '#C2FFDF')
 return im

def audio(path):
 sr=44100; a=np.zeros(sr*30,dtype=np.float32); rng=np.random.default_rng(30)
 for n,(start,end,*_) in enumerate(scenes):
  start+=.12; length=.24; tt=np.arange(int(sr*length))/sr; env=np.exp(-tt*22); chirp=np.sin(2*np.pi*(440+70*n)*tt+2*np.pi*500*tt*tt); noise=rng.normal(0,1,len(tt)); sig=(.13*chirp+.015*noise)*env; k=int(start*sr); a[k:k+len(sig)]+=sig
  if n in [1,3,4,6]:
   for k2 in [0.8,1.35]:
    k=int((start+k2)*sr); tt=np.arange(int(sr*.07))/sr; a[k:k+len(tt)]+=.06*np.sin(2*np.pi*950*tt)*np.exp(-tt*60)
 pcm=(np.clip(a,-1,1)*32767).astype('<i2')
 with wave.open(path,'wb') as f: f.setparams((1,2,sr,len(pcm),'NONE','not compressed')); f.writeframes(pcm.tobytes())

def render(v):
 out=f'output/video-0{v}'; os.makedirs(out,exist_ok=True); audio(out+'/sfx.wav'); ff=imageio_ffmpeg.get_ffmpeg_exe()
 cmd=[ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r','30','-i','-','-i',out+'/sfx.wav','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t','30',out+'/final.mp4']
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for frame in range(900):
  t=frame/30; i=next(k for k,(s,e,*_) in enumerate(scenes) if s<=t<e); s,e,*_=scenes[i]; p=t-s; im=(modern if v==1 else editorial)(t,i,p)
  if frame==30: im.resize((1080,1920),Image.Resampling.LANCZOS).save(out+'/cover.png')
  proc.stdin.write(im.tobytes())
 proc.stdin.close(); rc=proc.wait(); assert rc==0
 os.remove(out+'/sfx.wav')
if __name__=='__main__':
 import sys
 render(int(sys.argv[1]))
