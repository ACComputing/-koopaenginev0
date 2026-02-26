#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  Clickteam Fusion #  —  Koopa Engine (Fusion 3–style IDE)        ║
║  Menu Bar · Workspace · Properties · Frame Editor · Output        ║
║  Export: .exe  .app  .html  .py                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, sys, subprocess, threading, copy, time, random

# ═══════════════════════════════════════════════════════════════════
#  THEMES — Dark / Blue (CT default) / Light
# ═══════════════════════════════════════════════════════════════════
THEMES = {
    "dark": dict(
        bg="#1e1f22", panel="#27282c", ribbon="#2b2d30",
        tabbar="#2b2d30", tab_act="#1e1f22", tab_in="#2b2d30",
        fg="#dde1e7", fg2="#7a8088", fg3="#4a4e54",
        accent="#4b8ef1", gold="#f0a732", sel="#2d4a7a",
        border="#3d3f45", input="#35373d", hover="#3a3c42",
        green="#4ec9b0", red="#f44747", blue="#569cd6",
        status="#111214", sfg="#9ba3b0", term="#111214",
        lime="#4ec9b0", grip="#3d3f45", wspace="#1a1b1e",
        prop="#1e1f22", tree="#27282c", mario_r="#f04040",
        toolbar="#2b2d30", name="dark",
    ),
    "blue": dict(
        bg="#1c2740", panel="#1e2e50", ribbon="#16243a",
        tabbar="#1a2840", tab_act="#1c2740", tab_in="#1a2840",
        fg="#c0d4f0", fg2="#6080b0", fg3="#3a5070",
        accent="#3a88e8", gold="#f0c040", sel="#1e4480",
        border="#283858", input="#1e2e50", hover="#243060",
        green="#40c890", red="#e84040", blue="#5090d8",
        status="#101828", sfg="#80a0d0", term="#0c1622",
        lime="#40e890", grip="#283858", wspace="#141c34",
        prop="#1c2740", tree="#1e2e50", mario_r="#f04848",
        toolbar="#16243a", name="blue",
    ),
    "light": dict(
        bg="#f4f4f4", panel="#ececec", ribbon="#dcdcdc",
        tabbar="#e0e0e0", tab_act="#f4f4f4", tab_in="#e0e0e0",
        fg="#1a1a1a", fg2="#555555", fg3="#999999",
        accent="#0070c0", gold="#b86800", sel="#c0d8f8",
        border="#c0c0c0", input="#ffffff", hover="#e8e8e8",
        green="#007850", red="#c00000", blue="#0050a0",
        status="#d0d0d0", sfg="#303030", term="#1e1e1e",
        lime="#008844", grip="#b8b8b8", wspace="#e8e8e8",
        prop="#f8f8f8", tree="#ececec", mario_r="#c02020",
        toolbar="#dcdcdc", name="light",
    ),
}
CUR_THEME = ["dark"]
T = dict(THEMES["dark"])

FUI   = ("Segoe UI", 9)
FMONO = ("Consolas", 10)
FBOLD = ("Segoe UI", 9, "bold")
FSM   = ("Segoe UI", 8)
FSMB  = ("Segoe UI", 8, "bold")
FTAB  = ("Segoe UI", 9)
TILE_PX = 32

# ═══════════════════════════════════════════════════════════════════
#  TILE DEFINITIONS  (color, symbol, solid, hazard)
# ═══════════════════════════════════════════════════════════════════
TILES = {
    "empty":          ("#1e1f22"," ",   False,False),
    "ground":         ("#7a4f2c","▓",   True, False),
    "grass_top":      ("#5aad3c","▀",   True, False),
    "brick":          ("#c0603a","▦",   True, False),
    "hard_block":     ("#9b6b3c","■",   True, False),
    "?_block":        ("#e8ab4f","?",   True, False),
    "used_block":     ("#888060","□",   True, False),
    "invisible_blk":  ("#2a2a3a","·",   True, False),
    "note_block":     ("#c87832","♪",   True, False),
    "bounce_block":   ("#ee8800","↑",   True, False),
    "pipe_top_l":     ("#3cb03c","╔",   True, False),
    "pipe_top_r":     ("#2d9a2d","╗",   True, False),
    "pipe_body_l":    ("#2e8b2e","║",   True, False),
    "pipe_body_r":    ("#267826","║",   True, False),
    "platform":       ("#8b6914","═",   True, False),
    "moving_plat":    ("#aa7722","▬",   True, False),
    "cloud_solid":    ("#d8f0ff","▓",   True, False),
    "sky_platform":   ("#a8c0e8","═",   True, False),
    "cloud_l":        ("#c0d8f8","☁",   False,False),
    "cloud_m":        ("#d0e8f8","☁",   False,False),
    "cloud_r":        ("#b0c8e8","☁",   False,False),
    "bush_l":         ("#3a9a3a","(",   False,False),
    "bush_m":         ("#4aaa4a","━",   False,False),
    "bush_r":         ("#3a9a3a",")",   False,False),
    "coin_tile":      ("#ffd700","o",   False,False),
    "vine":           ("#3a8a3a","§",   False,False),
    "flagpole_top":   ("#e0e0e0","◉",   False,False),
    "flagpole":       ("#cccccc","|",   False,False),
    "underground":    ("#2a1a0a","▓",   True, False),
    "stone_block":    ("#888888","▓",   True, False),
    "water":          ("#2038ec","≋",   False,False),
    "sand":           ("#f0c060","░",   True, False),
    "coral":          ("#ff6060","⧖",   True, False),
    "ice":            ("#a8e0f8","▭",   True, False),
    "snow":           ("#e8f4fc","░",   False,False),
    "lava":           ("#e83800","≋",   False,True),
    "lava_rock":      ("#5a1800","▓",   True, False),
    "lava_pit":       ("#c82000","≋",   False,True),
    "castle_wall":    ("#555555","▓",   True, False),
    "castle_floor":   ("#444444","▓",   True, False),
    "castle_brick":   ("#666660","▦",   True, False),
    "spike":          ("#cccccc","▲",   False,True),
    "warp_zone":      ("#3030c0","W",   False,False),
    "checkpoint":     ("#00bfff","✦",   False,False),
    "start_pos":      ("#00ff88","S",   False,False),
    "end_pos":        ("#ff8800","E",   False,False),
    "p_switch":       ("#4444ee","P",   True, False),
    "donut_block":    ("#ffaaaa","○",   True, False),
}

TILE_GROUPS = {
    "🌍 Terrain":   ["ground","grass_top","underground","stone_block","castle_wall","castle_floor","castle_brick"],
    "🧱 Blocks":    ["brick","hard_block","?_block","used_block","invisible_blk","note_block","bounce_block","donut_block","p_switch"],
    "🟢 Pipes":     ["pipe_top_l","pipe_top_r","pipe_body_l","pipe_body_r"],
    "🟫 Platforms": ["platform","moving_plat","cloud_solid","sky_platform"],
    "🎨 Deco":      ["cloud_l","cloud_m","cloud_r","bush_l","bush_m","bush_r","vine","snow","coin_tile"],
    "🔥 Hazards":   ["lava","lava_pit","lava_rock","spike"],
    "💧 Water/Ice": ["water","sand","coral","ice"],
    "⭐ Special":   ["flagpole_top","flagpole","warp_zone","checkpoint","start_pos","end_pos"],
}

ENTITIES = {
    "Player":        ("#ff4444","P"),  "Goomba":     ("#c08030","G"),
    "Koopa":         ("#38c038","K"),  "Para Koopa": ("#60c060","↑K"),
    "Shell":         ("#50aa50","S"),  "Piranha":    ("#e02820","⊛"),
    "Hammer Bro":    ("#4858c0","H"),  "Lakitu":     ("#b0a020","L"),
    "Spiny":         ("#cc4444","Sp"), "Boo":        ("#e0e0e0","☺"),
    "Thwomp":        ("#6060a0","▼"),  "Bullet Bill":("#333333","●"),
    "Bowser Jr":     ("#ff8c00","BJ"), "Bowser":     ("#884400","BO"),
    "Fire Bar":      ("#ff6000","⊝"),  "Mushroom":   ("#ff6060","M"),
    "1UP":           ("#38c038","1U"), "Fire Flower":("#ff6000","F"),
    "Super Leaf":    ("#88cc44","♣"),  "Star":       ("#ffd700","★"),
    "Coin (obj)":    ("#ffd700","¢"),  "Yoshi":      ("#44cc44","Y"),
    "Spring":        ("#ffb300","SP"), "Warp Pipe":  ("#2e8b2e","WP"),
    "Key":           ("#ffd700","⚷"), "Door":        ("#8b4513","D"),
    "Goal Tape":     ("#ffffff","=="), "Enemy Spawn": ("#aa0000","⊕"),
}

BG_COLORS = {
    "grass":"#5c94fc","underground":"#000000","water":"#080838",
    "sky":"#90c0f8","ice":"#c8e8f8","pipe":"#000000",
    "dark":"#101010","special":"#000000","final":"#000000",
}
MUSIC = ["overworld","underground","underwater","castle","boss",
         "star_power","athletic","airship","ghost_house","world10"]

LAYER_DEFS = [
    {"name":"Background","color":"#1a3a5c"},
    {"name":"Tiles",     "color":"#3a6a2c"},
    {"name":"Entities",  "color":"#8a2a2a"},
    {"name":"Foreground","color":"#3a3a8a"},
]

LEVEL_DEFAULTS = dict(
    name="1-1",world_type="grass",width=100,height=15,
    music="overworld",gravity=9.8,time=300,
    scroll="horizontal",background="grass",
    start_x=2,start_y=12,is_castle=False,is_underwater=False,
)

# ═══════════════════════════════════════════════════════════════════
#  HELPER WIDGETS
# ═══════════════════════════════════════════════════════════════════
def flatbtn(parent, text, cmd=None, bg=None, fg=None, font=FUI,
            padx=6, pady=3, w=None, tip=""):
    if bg is None: bg = T["input"]
    if fg is None: fg = "#000000"
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=font, relief="flat", bd=0,
                  activebackground=T["sel"], activeforeground="#000000",
                  cursor="hand2", padx=padx, pady=pady)
    if w: b.config(width=w)
    if tip: _Tip(b, tip)
    return b

class _Tip:
    def __init__(self, w, t):
        self.w=w; self.t=t; self.tw=None
        w.bind("<Enter>",self.show); w.bind("<Leave>",self.hide)
    def show(self,e=None):
        x=self.w.winfo_rootx()+18
        y=self.w.winfo_rooty()+self.w.winfo_height()+3
        self.tw=tw=tk.Toplevel(self.w)
        tw.wm_overrideredirect(True); tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw,text=self.t,bg=T["hover"],fg=T["fg"],
                 font=FSM,padx=7,pady=3,relief="flat").pack()
    def hide(self,e=None):
        if self.tw:
            try: self.tw.destroy()
            except: pass
            self.tw=None

class VSEntry(tk.Entry):
    def __init__(self,p,**kw):
        super().__init__(p,bg=T["input"],fg=T["fg"],font=FMONO,
            insertbackground=T["fg"],relief="flat",bd=0,
            highlightthickness=1,highlightcolor=T["accent"],
            highlightbackground=T["border"],**kw)

def scrolled(parent, bg=None):
    if bg is None: bg=T["panel"]
    f=tk.Frame(parent,bg=bg); f.pack(fill="both",expand=True)
    vsb=ttk.Scrollbar(f,orient="vertical"); vsb.pack(side="right",fill="y")
    c=tk.Canvas(f,bg=bg,highlightthickness=0,yscrollcommand=vsb.set)
    c.pack(fill="both",expand=True); vsb.config(command=c.yview)
    inner=tk.Frame(c,bg=bg); c.create_window((0,0),window=inner,anchor="nw")
    inner.bind("<Configure>",lambda e:c.configure(scrollregion=c.bbox("all")))
    c.bind("<MouseWheel>",lambda e:c.yview_scroll(-1*(e.delta//120),"units"))
    return f,inner,c

# ═══════════════════════════════════════════════════════════════════
#  LEVEL MODEL
# ═══════════════════════════════════════════════════════════════════
class Level:
    def __init__(self,props=None):
        self.props=dict(LEVEL_DEFAULTS)
        if props: self.props.update(props)
        self.layers=self._blank(); self.history=[]; self.filepath=None
    def _blank(self):
        w,h=self.props["width"],self.props["height"]
        return [
            [["empty"]*w for _ in range(h)],
            [["empty"]*w for _ in range(h)],
            [[None]*w    for _ in range(h)],
            [["empty"]*w for _ in range(h)],
        ]
    def get(self,l,r,c):
        try: return self.layers[l][r][c]
        except: return None
    def set(self,l,r,c,v):
        try: self.layers[l][r][c]=v
        except: pass
    def snapshot(self):
        if len(self.history)>60: self.history.pop(0)
        self.history.append(copy.deepcopy(self.layers))
    def undo(self):
        if self.history: self.layers=self.history.pop(); return True
        return False
    def flood_fill(self,layer,r,c,nv):
        ov=self.get(layer,r,c)
        if ov==nv: return
        w,h=self.props["width"],self.props["height"]
        stack=[(r,c)]
        while stack:
            rr,cc=stack.pop()
            if not(0<=rr<h and 0<=cc<w): continue
            if self.get(layer,rr,cc)!=ov: continue
            self.set(layer,rr,cc,nv)
            stack+=[(rr+1,cc),(rr-1,cc),(rr,cc+1),(rr,cc-1)]
    def to_dict(self): return {"props":self.props,"layers":self.layers}
    @classmethod
    def from_dict(cls,d):
        l=cls(d["props"]); l.layers=d["layers"]; return l

# ═══════════════════════════════════════════════════════════════════
#  CODE GENERATORS
# ═══════════════════════════════════════════════════════════════════
def _td(level): return [[t if t and t!="empty" else None for t in row] for row in level.layers[1]]
def _ed(level):
    e=[]
    for r,row in enumerate(level.layers[2]):
        for c,v in enumerate(row):
            if v: e.append({"type":v,"x":c,"y":r})
    return e

def gen_pygame(level):
    p=level.props
    td=json.dumps(_td(level)); ed=json.dumps(_ed(level))
    bg=BG_COLORS.get(p.get("background","grass"),"#5c94fc")
    bgr=tuple(int(bg.lstrip("#")[i:i+2],16) for i in(0,2,4))
    sx=p.get("start_x",2); sy=p.get("start_y",12)
    return f'''#!/usr/bin/env python3
# ============================================================
# Auto-generated by Koopa Engine  (Clickteam Fusion 3 Edition)
# Mario Forever / Buziol Games Engine — Pygame 600x400
# Level: {p["name"]}  World: {p.get("world_type","grass")}
# ============================================================
import pygame, sys, asyncio, random

SW,SH=600,400; TS=32
GRAVITY={p.get("gravity",9.8)}
BG_COLOR={bgr}
LEVEL_NAME="{p["name"]}"
LEVEL_TIME={p.get("time",300)}

TILE_COLORS={{
    "ground":(122,79,44),"grass_top":(90,173,60),"brick":(192,96,58),
    "hard_block":(155,107,60),"?_block":(232,171,79),"note_block":(200,120,50),
    "castle_wall":(85,85,85),"castle_floor":(68,68,68),"castle_brick":(102,102,96),
    "lava":(232,56,0),"lava_pit":(200,32,0),"lava_rock":(90,24,0),
    "water":(32,56,236),"ice":(168,224,248),"sand":(240,192,96),
    "spike":(204,204,204),"platform":(139,105,20),"cloud_solid":(216,240,255),
    "sky_platform":(168,192,232),"moving_plat":(170,119,34),
    "pipe_top_l":(60,176,60),"pipe_top_r":(45,154,45),
    "pipe_body_l":(46,139,46),"pipe_body_r":(38,120,38),
    "underground":(42,26,10),"stone_block":(136,136,136),
    "bounce_block":(238,136,0),"donut_block":(255,170,170),
    "p_switch":(68,68,238),"used_block":(136,128,96),
    "snow":(232,244,252),"coral":(255,96,96),"vine":(58,138,58),
    "invisible_blk":(42,42,58),
}}

SOLID={{
    "ground","grass_top","brick","hard_block","?_block","used_block",
    "invisible_blk","pipe_top_l","pipe_top_r","pipe_body_l","pipe_body_r",
    "platform","cloud_solid","sky_platform","ice","lava_rock","moving_plat",
    "castle_wall","castle_floor","castle_brick","note_block","bounce_block",
    "donut_block","p_switch","underground","stone_block","sand","coral",
}}
HAZARD={{"lava","lava_pit","spike"}}
BOUNCE_TILES={{"bounce_block","note_block"}}

TILE_MAP={td}
ENTITY_LIST={ed}

pygame.init()
screen=pygame.display.set_mode((SW,SH))
pygame.display.set_caption(f"Koopa Engine — {{LEVEL_NAME}}")
clock=pygame.time.Clock()
font_sm=pygame.font.SysFont("Arial",14,bold=True)
font_lg=pygame.font.SysFont("Arial",32,bold=True)
font_xs=pygame.font.SysFont("Arial",11)

class Particle:
    def __init__(self,x,y,vx,vy,col,life):
        self.x=x;self.y=y;self.vx=vx;self.vy=vy;self.col=col;self.life=life;self.ml=life
    def update(self): self.x+=self.vx;self.y+=self.vy;self.vy+=0.4;self.life-=1
    def draw(self,surf,cx):
        if self.life<=0: return
        s=max(2,int(5*(self.life/self.ml)))
        pygame.draw.rect(surf,self.col,pygame.Rect(int(self.x)-cx,int(self.y),s,s))

def spawn_pts(x,y,col=(255,215,0),n=10):
    return [Particle(x,y,random.uniform(-3,3),random.uniform(-5,-0.5),col,random.randint(20,45)) for _ in range(n)]

class Player:
    W,H=24,32
    def __init__(self,x,y):
        self.x=float(x*TS);self.y=float(y*TS-self.H)
        self.vx=self.vy=0.0;self.on_ground=False
        self.alive=True;self.score=0;self.coins=0
        self.facing=1;self.anim=0;self.invuln=0
    def update(self,tiles):
        keys=pygame.key.get_pressed()
        spd=4.5 if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 3.2
        self.vx=0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.vx=-spd; self.facing=-1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.vx= spd; self.facing= 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy=-11.5; self.on_ground=False
        self.vy=min(self.vy+GRAVITY*(1/60),18)
        self.x+=self.vx; self._cx(tiles)
        self.y+=self.vy; self.on_ground=False; self._cy(tiles)
        if self.x<0: self.x=0
        if self.y>SH+120: self.alive=False
        if self.invuln>0: self.invuln-=1
        self.anim=(self.anim+1)%32
    def _t(self,tx,ty,tiles):
        if ty<0 or ty>=len(tiles) or tx<0 or tx>=len(tiles[0]): return None
        return tiles[ty][tx]
    def _sol(self,tx,ty,tiles): t=self._t(tx,ty,tiles); return t in SOLID if t else False
    def _haz(self,tx,ty,tiles): t=self._t(tx,ty,tiles); return t in HAZARD if t else False
    def _cx(self,tiles):
        r=pygame.Rect(self.x,self.y,self.W,self.H)
        for tx in[r.left//TS,(r.right-1)//TS]:
            for ty in[r.top//TS,(r.bottom-1)//TS]:
                if self._sol(tx,ty,tiles):
                    if self.vx>0: self.x=tx*TS-self.W
                    elif self.vx<0: self.x=(tx+1)*TS
                    self.vx=0
    def _cy(self,tiles):
        r=pygame.Rect(self.x,self.y,self.W,self.H)
        for tx in[r.left//TS,(r.right-1)//TS]:
            for ty in[r.top//TS,(r.bottom-1)//TS]:
                if self._sol(tx,ty,tiles):
                    if self.vy>0: self.y=ty*TS-self.H; self.on_ground=True
                    elif self.vy<0: self.y=(ty+1)*TS
                    if self._t(tx,ty,tiles) in BOUNCE_TILES and self.vy<0: self.vy=abs(self.vy)*0.7
                    self.vy=0
                if self._haz(tx,ty,tiles) and self.invuln==0: self.alive=False
    def rect(self): return pygame.Rect(int(self.x),int(self.y),self.W,self.H)
    def draw(self,surf,cx):
        if self.invuln>0 and (self.invuln//4)%2==0: return
        r=self.rect(); sx=r.x-cx; sy=r.y
        # overalls/shoes
        pygame.draw.rect(surf,(0,80,180),pygame.Rect(sx,sy+18,self.W,14))
        pygame.draw.rect(surf,(80,40,20),pygame.Rect(sx,sy+28,10,6))
        pygame.draw.rect(surf,(80,40,20),pygame.Rect(sx+14,sy+28,10,6))
        # body
        pygame.draw.rect(surf,(220,60,50),pygame.Rect(sx,sy+8,self.W,12))
        # head
        pygame.draw.rect(surf,(220,160,110),pygame.Rect(sx+2,sy+2,self.W-4,12))
        # hat
        pygame.draw.rect(surf,(220,60,50),pygame.Rect(sx+2,sy-2,self.W-4,8))
        pygame.draw.rect(surf,(220,60,50),pygame.Rect(sx+8,sy-6,self.W-10,6))
        # eye + mustache
        ex=sx+16 if self.facing==1 else sx+4
        pygame.draw.circle(surf,(0,0,0),(ex,sy+6),2)
        pygame.draw.rect(surf,(80,40,20),pygame.Rect(sx+4,sy+10,self.W-8,4))
        # walk
        if abs(self.vx)>0.1 and self.on_ground:
            fr=(self.anim//8)%2
            pygame.draw.rect(surf,(0,60,160),pygame.Rect(sx+(0 if fr else 8),sy+28,10,8))

class Goomba:
    W,H=28,26
    def __init__(self,x,y):
        self.x=float(x*TS);self.y=float(y*TS-self.H)
        self.vx=-1.8;self.vy=0.0;self.alive=True;self.squish=0;self.anim=0
    def update(self,tiles):
        if self.squish>0: self.squish-=1; return
        self.vy=min(self.vy+GRAVITY*(1/60),18)
        self.x+=self.vx
        nx=int((self.x+(self.W if self.vx>0 else 0))//TS); ny=int((self.y+self.H)//TS)
        def sol(tx,ty):
            if ty<0 or ty>=len(tiles) or tx<0 or tx>=len(tiles[0]): return False
            return tiles[ty][tx] in SOLID
        if not sol(nx,ny): self.vx*=-1
        for wy in[int(self.y//TS),int((self.y+self.H-1)//TS)]:
            if sol(nx,wy): self.vx*=-1; break
        self.y+=self.vy
        r=pygame.Rect(self.x,self.y,self.W,self.H)
        for tx in[r.left//TS,(r.right-1)//TS]:
            ty=r.bottom//TS
            if sol(tx,ty): self.y=ty*TS-self.H; self.vy=0
        self.anim=(self.anim+1)%20
    def kill(self): self.squish=25
    def rect(self): return pygame.Rect(int(self.x),int(self.y),self.W,self.H)
    def draw(self,surf,cx):
        r=self.rect(); sx=r.x-cx; sy=r.y
        if self.squish>0:
            pygame.draw.ellipse(surf,(160,100,30),pygame.Rect(sx,sy+r.h-10,r.w,10))
            return
        pygame.draw.ellipse(surf,(172,112,36),r)
        pygame.draw.rect(surf,(80,40,10),pygame.Rect(sx+2,sy+r.h-8,r.w-4,8))
        frx=1 if (self.anim//10)%2==0 else -1
        pygame.draw.ellipse(surf,(230,180,120),pygame.Rect(sx+2,sy+4,10,10))
        pygame.draw.ellipse(surf,(230,180,120),pygame.Rect(sx+r.w-12,sy+4,10,10))
        pygame.draw.circle(surf,(0,0,0),(sx+6,sy+8),3)
        pygame.draw.circle(surf,(0,0,0),(sx+r.w-6,sy+8),3)
        pygame.draw.circle(surf,(255,255,255),(sx+7,sy+7),1)
        pygame.draw.circle(surf,(255,255,255),(sx+r.w-5,sy+7),1)
        pygame.draw.polygon(surf,(80,40,10),[(sx+4,sy+r.h-10),(sx+8,sy+r.h-16),(sx+12,sy+r.h-10)])
        pygame.draw.polygon(surf,(80,40,10),[(sx+r.w-12,sy+r.h-10),(sx+r.w-8,sy+r.h-16),(sx+r.w-4,sy+r.h-10)])

class CoinAnim:
    def __init__(self,x,y): self.x=x*TS+10;self.y=y*TS+4;self.alive=True;self.anim=0
    def update(self): self.anim=(self.anim+1)%40
    def draw(self,surf,cx):
        w=max(2,int(11*abs((self.anim-20)/20)))
        pygame.draw.ellipse(surf,(255,215,0),pygame.Rect(int(self.x)-w//2-cx,int(self.y),w,22))
        pygame.draw.ellipse(surf,(200,155,0),pygame.Rect(int(self.x)-w//2-cx,int(self.y),w,22),2)
        if w>4:
            pygame.draw.line(surf,(255,240,100),(int(self.x)-cx,int(self.y)+4),(int(self.x)-cx,int(self.y)+18),2)

def draw_hud(surf, player, timer):
    # CT / Mario Forever style HUD bar
    hud=pygame.Surface((SW,40),pygame.SRCALPHA)
    hud.fill((0,0,0,210))
    surf.blit(hud,(0,0))
    pygame.draw.line(surf,(80,80,80),(0,40),(SW,40),1)
    # Score
    surf.blit(font_xs.render("MARIO",True,(180,180,180)),(10,3))
    surf.blit(font_sm.render(f"{{player.score:06d}}",True,(255,255,255)),(8,16))
    # Coins
    pygame.draw.circle(surf,(255,215,0),(SW//2-60,20),7)
    pygame.draw.circle(surf,(200,155,0),(SW//2-60,20),7,1)
    surf.blit(font_sm.render(f"x{{player.coins:02d}}",True,(255,215,0)),(SW//2-48,12))
    # World
    surf.blit(font_xs.render("WORLD",True,(180,180,180)),(SW//2,3))
    surf.blit(font_sm.render(LEVEL_NAME,True,(255,215,0)),(SW//2+2,16))
    # Timer
    surf.blit(font_xs.render("TIME",True,(180,180,180)),(SW-66,3))
    tcol=(255,60,60) if timer<60 else (255,255,255)
    surf.blit(font_sm.render(str(timer),True,tcol),(SW-58,16))
    # Lives (static 3)
    for i in range(3):
        pygame.draw.rect(surf,(220,60,50),pygame.Rect(SW//2+80+i*18,14,12,12))
        pygame.draw.rect(surf,(220,60,50),pygame.Rect(SW//2+82+i*18,8,8,6))

async def main():
    tiles=TILE_MAP
    player=Player({sx},{sy})
    goombas=[]; coins=[]; particles=[]
    for e in ENTITY_LIST:
        t=e["type"]
        if t=="Player":     player=Player(e["x"],e["y"])
        elif t=="Goomba":   goombas.append(Goomba(e["x"],e["y"]))
        elif t=="Coin (obj)": coins.append(CoinAnim(e["x"],e["y"]))
    cam_x=0; timer=LEVEL_TIME; t_tick=0; running=True
    while running:
        dt=clock.tick(60)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: running=False
            if ev.type==pygame.KEYDOWN:
                if not player.alive and ev.key==pygame.K_r: return await main()
        if player.alive:
            player.update(tiles)
            for g in [g for g in goombas if g.alive and g.squish==0]: g.update(tiles)
            for c in [c for c in coins if c.alive]: c.update()
            for pt in particles: pt.update()
            particles=[pt for pt in particles if pt.life>0]
            tc=int(player.x-SW//3); mc=max(0,len(tiles[0])*TS-SW) if tiles else 0
            cam_x=max(0,min(tc,mc))
            t_tick+=dt
            if t_tick>=1000: timer-=1; t_tick=0
            if timer<=0: player.alive=False
            pr=player.rect()
            for g in [g for g in goombas if g.alive and g.squish==0]:
                if pr.colliderect(g.rect()):
                    if player.vy>0 and pr.bottom<g.rect().centery+10:
                        g.kill(); player.vy=-8.5; player.score+=100
                        particles+=spawn_pts(g.x,g.y,(180,120,40))
                    elif player.invuln==0: player.alive=False
            for c in [c for c in coins if c.alive]:
                if pr.inflate(-4,-4).colliderect(pygame.Rect(int(c.x),int(c.y),16,22)):
                    c.alive=False; player.coins+=1; player.score+=200
                    particles+=spawn_pts(c.x,c.y,(255,215,0),6)
        # ── DRAW ──────────────────────────────────────────────────
        screen.fill(BG_COLOR)
        vl=max(0,cam_x//TS); vr=min(vl+SW//TS+2,len(tiles[0]) if tiles else 0)
        for r,row in enumerate(tiles):
            for c in range(vl,min(vr,len(row))):
                t=row[c]
                if not t or t=="empty": continue
                col=TILE_COLORS.get(t,(100,100,100))
                rx=c*TS-cam_x; ry=r*TS
                pygame.draw.rect(screen,col,pygame.Rect(rx,ry,TS,TS))
                if t in("?_block","brick","hard_block","note_block","bounce_block"):
                    pygame.draw.rect(screen,(min(col[0]+50,255),min(col[1]+30,255),min(col[2]+10,255)),pygame.Rect(rx,ry,TS,4))
                    pygame.draw.rect(screen,(max(col[0]-40,0),max(col[1]-30,0),max(col[2]-10,0)),pygame.Rect(rx,ry+TS-4,TS,4))
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(rx,ry,TS,TS),1)
                if t=="?_block":
                    s=font_sm.render("?",True,(255,255,200)); screen.blit(s,(rx+TS//2-s.get_width()//2,ry+TS//2-s.get_height()//2))
                elif t=="coin_tile":
                    pygame.draw.circle(screen,(255,215,0),(rx+TS//2,ry+TS//2),8)
        for c in [c for c in coins if c.alive]: c.draw(screen,cam_x)
        for pt in particles: pt.draw(screen,cam_x)
        for g in [g for g in goombas if g.alive or g.squish>0]: g.draw(screen,cam_x)
        if player.alive: player.draw(screen,cam_x)
        draw_hud(screen,player,timer)
        if not player.alive:
            ov=pygame.Surface((SW,SH),pygame.SRCALPHA); ov.fill((0,0,0,150)); screen.blit(ov,(0,0))
            go=font_lg.render("GAME OVER",True,(255,60,60)); screen.blit(go,(SW//2-go.get_width()//2,SH//2-40))
            rr=font_sm.render("Press R to restart",True,(220,220,220)); screen.blit(rr,(SW//2-rr.get_width()//2,SH//2+20))
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit(); sys.exit()

if __name__=="__main__": asyncio.run(main())
'''

def gen_html(level):
    p=level.props
    bg=BG_COLORS.get(p.get("background","grass"),"#5c94fc")
    td=json.dumps(_td(level)); ed=json.dumps(_ed(level))
    sx=p.get("start_x",2)*32; sy=p.get("start_y",12)*32
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>Koopa Engine — {p["name"]}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#111;display:flex;flex-direction:column;align-items:center;
      justify-content:center;min-height:100vh;font-family:"Segoe UI",sans-serif}}
h1{{color:#f0a732;font-size:16px;margin-bottom:10px;letter-spacing:3px;text-transform:uppercase}}
#c{{border:2px solid #3d3f45;display:block;image-rendering:pixelated}}
#info{{margin-top:8px;color:#7a8088;font-size:11px}}
#ctrl{{margin-top:4px;color:#4b8ef1;font-size:11px}}
</style>
</head>
<body>
<h1>⬛ Koopa Engine  ·  {p["name"]}</h1>
<canvas id="c" width="600" height="400"></canvas>
<div id="info">World: {p.get("world_type","grass")} · {p.get("width",100)}×{p.get("height",15)} tiles · Buziol Games Engine</div>
<div id="ctrl">Arrow Keys / WASD = Move  |  Space / W / ↑ = Jump  |  R = Restart</div>
<script>
const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");
const SW=600,SH=400,TS=32;
const BG="{bg}";
const TILES={td};
const ENTS={ed};
const START_X={sx},START_Y={sy};
const LEVEL_NAME="{p["name"]}";
const LEVEL_TIME={p.get("time",300)};
const GRAVITY={p.get("gravity",9.8)};

const SOLID=new Set(["ground","grass_top","brick","hard_block","?_block","used_block",
  "invisible_blk","pipe_top_l","pipe_top_r","pipe_body_l","pipe_body_r","platform",
  "cloud_solid","sky_platform","ice","lava_rock","moving_plat","castle_wall",
  "castle_floor","castle_brick","note_block","bounce_block","donut_block",
  "p_switch","underground","stone_block","sand","coral"]);
const HAZARD=new Set(["lava","lava_pit","spike"]);
const TILE_COLORS={{
  ground:"#7a4f2c",grass_top:"#5aad3c",brick:"#c0603a",hard_block:"#9b6b3c",
  "?_block":"#e8ab4f",note_block:"#c87832",castle_wall:"#555555",
  castle_floor:"#444444",castle_brick:"#666660",lava:"#e83800",
  lava_pit:"#c82000",lava_rock:"#5a1800",water:"#2038ec",ice:"#a8e0f8",
  sand:"#f0c060",spike:"#cccccc",platform:"#8b6914",cloud_solid:"#d8f0ff",
  sky_platform:"#a8c0e8",moving_plat:"#aa7722",pipe_top_l:"#3cb03c",
  pipe_top_r:"#2d9a2d",pipe_body_l:"#2e8b2e",pipe_body_r:"#267826",
  underground:"#2a1a0a",stone_block:"#888888",bounce_block:"#ee8800",
  donut_block:"#ffaaaa",p_switch:"#4444ee",used_block:"#888060",
  snow:"#e8f4fc",coin_tile:"#ffd700",vine:"#3a8a3a",
}};

let px=START_X,py=START_Y,vx=0,vy=0,onGround=false,alive=true,facing=1;
let score=0,coins=0,timer=LEVEL_TIME,tTick=0,camX=0,invuln=0,anim=0;
const PW=24,PH=32;
const keys={{}};
let coinObjs=ENTS.filter(e=>e.type==="Coin (obj)").map(e=>
  ({{x:e.x*TS+10,y:e.y*TS+4,alive:true,a:0}}));
let goombas=ENTS.filter(e=>e.type==="Goomba").map(e=>
  ({{x:e.x*TS,y:e.y*TS-26,vx:-1.8,vy:0,alive:true,squish:0,a:0}}));
let particles=[];

function sol(tx,ty){{
  if(ty<0||ty>=TILES.length||tx<0||tx>=TILES[0].length)return false;
  return TILES[ty][tx]&&SOLID.has(TILES[ty][tx]);
}}
function haz(tx,ty){{
  if(ty<0||ty>=TILES.length||tx<0||tx>=TILES[0].length)return false;
  return TILES[ty][tx]&&HAZARD.has(TILES[ty][tx]);
}}
function colX(){{
  for(let ty=~~(py/TS);ty<=~~((py+PH-1)/TS);ty++)
    for(let tx of[~~(px/TS),~~((px+PW-1)/TS)])
      if(sol(tx,ty)){{if(vx>0)px=tx*TS-PW;else px=(tx+1)*TS;vx=0;}}
}}
function colY(){{
  for(let tx=~~(px/TS);tx<=~~((px+PW-1)/TS);tx++)
    for(let ty of[~~(py/TS),~~((py+PH-1)/TS)]){{
      if(sol(tx,ty)){{if(vy>0){{py=ty*TS-PH;onGround=true;}}else py=(ty+1)*TS;vy=0;}}
      if(haz(tx,ty)&&invuln===0)alive=false;
    }}
}}
function spawnPts(x,y,col,n=8){{
  for(let i=0;i<n;i++)particles.push({{
    x,y,vx:(Math.random()-0.5)*5,vy:Math.random()*-5-0.5,
    col,life:Math.random()*25+15,ml:40
  }});
}}

let last=0;
function loop(now){{
  const dt=(now-last)/1000||0.016;last=now;
  if(alive){{
    const spd=(keys.ShiftLeft||keys.ShiftRight)?4.5:3.2;
    vx=(keys.ArrowLeft||keys.KeyA)?-spd:(keys.ArrowRight||keys.KeyD)?spd:0;
    if(vx<0)facing=-1;if(vx>0)facing=1;
    if((keys.Space||keys.ArrowUp||keys.KeyW)&&onGround){{vy=-11.5;onGround=false;}}
    vy=Math.min(vy+GRAVITY*dt,18);
    px+=vx;colX();py+=vy;onGround=false;colY();
    if(px<0)px=0;if(py>SH+100)alive=false;
    if(invuln>0)invuln--;
    anim=(anim+1)%32;
    tTick+=dt;if(tTick>=1){{timer--;tTick=0;}}if(timer<=0)alive=false;
    let tCam=px-SW/3;
    camX=Math.max(0,Math.min(tCam,(TILES[0]||[]).length*TS-SW));
    // Goomba update
    goombas.forEach(g=>{{
      if(!g.alive||g.squish>0){{g.squish=Math.max(0,g.squish-1);return;}}
      g.vy=Math.min(g.vy+GRAVITY*dt,18);g.x+=g.vx;
      const nx=~~((g.x+(g.vx>0?28:0))/TS),ny=~~((g.y+26)/TS);
      if(!sol(nx,ny))g.vx*=-1;
      for(let wy of[~~(g.y/TS),~~((g.y+25)/TS)])if(sol(nx,wy)){{g.vx*=-1;break;}}
      g.y+=g.vy;
      const gr=~~((g.y+26)/TS);
      for(let tx of[~~(g.x/TS),~~((g.x+27)/TS)])if(sol(tx,gr)){{g.y=gr*TS-26;g.vy=0;}}
      g.a=(g.a+1)%20;
    }});
    coinObjs.forEach(c=>{{if(c.alive)c.a=(c.a+1)%40;}});
    particles.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.vy+=0.4;p.life--;p.ml=p.ml||40;}});
    particles=particles.filter(p=>p.life>0);
    // Collisions
    const pr={{x:px,y:py,w:PW,h:PH}};
    goombas.forEach(g=>{{
      if(!g.alive||g.squish>0)return;
      const gr={{x:g.x,y:g.y,w:28,h:26}};
      if(pr.x<gr.x+gr.w&&pr.x+pr.w>gr.x&&pr.y<gr.y+gr.h&&pr.y+pr.h>gr.y){{
        if(vy>0&&pr.y+pr.h<gr.y+gr.h/2+10){{
          g.squish=25;g.alive=false;vy=-8.5;score+=100;
          spawnPts(g.x+14,g.y,"#c87828");
        }}else if(invuln===0)alive=false;
      }}
    }});
    coinObjs.forEach(c=>{{
      if(!c.alive)return;
      if(Math.abs(px-c.x+12)<18&&Math.abs(py-c.y+11)<20){{
        c.alive=false;coins++;score+=200;spawnPts(c.x,c.y,"#ffd700",6);
      }}
    }});
  }}
  // DRAW
  ctx.fillStyle=BG;ctx.fillRect(0,0,SW,SH);
  const vl=Math.max(0,~~(camX/TS)),vr=Math.min(vl+SW/TS+2,(TILES[0]||[]).length);
  for(let r=0;r<TILES.length;r++)
    for(let c=vl;c<vr;c++){{
      const t=TILES[r][c];if(!t||t==="empty")continue;
      const col=TILE_COLORS[t]||"#888";
      ctx.fillStyle=col;ctx.fillRect(c*TS-camX,r*TS,TS,TS);
      ctx.strokeStyle="rgba(0,0,0,0.35)";ctx.lineWidth=1;
      ctx.strokeRect(c*TS-camX,r*TS,TS,TS);
      if(t==="?_block"){{
        ctx.fillStyle="#fff8d0";ctx.font="bold 18px Arial";
        ctx.textAlign="center";ctx.fillText("?",c*TS-camX+TS/2,r*TS+TS/2+7);
      }}
      if(t==="coin_tile"){{
        ctx.fillStyle="#ffd700";ctx.beginPath();
        ctx.arc(c*TS-camX+TS/2,r*TS+TS/2,8,0,Math.PI*2);ctx.fill();
      }}
    }}
  // Coins
  coinObjs.filter(c=>c.alive).forEach(c=>{{
    const w=Math.max(2,~~(11*Math.abs((c.a-20)/20)));
    ctx.fillStyle="#ffd700";ctx.beginPath();
    ctx.ellipse(c.x-camX,c.y+11,w,11,0,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle="#c8a000";ctx.lineWidth=1.5;ctx.stroke();
  }});
  // Particles
  particles.forEach(p=>{{
    if(p.life<=0)return;
    const a=p.life/(p.ml||40);ctx.fillStyle=p.col||"#ff0";
    ctx.globalAlpha=a;ctx.fillRect(~~p.x-camX,~~p.y,~~(4*a)+1,~~(4*a)+1);
  }});
  ctx.globalAlpha=1;
  // Goombas
  goombas.forEach(g=>{{
    const sx=~~g.x-camX,sy=~~g.y;
    if(g.squish>0){{
      ctx.fillStyle="#b06820";ctx.beginPath();
      ctx.ellipse(sx+14,sy+26,14,6,0,0,Math.PI*2);ctx.fill();return;
    }}
    ctx.fillStyle="#ac7024";ctx.beginPath();
    ctx.ellipse(sx+14,sy+13,14,13,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="#502808";ctx.fillRect(sx+2,sy+18,24,8);
    // eyes
    ctx.fillStyle="#f0c880";
    ctx.beginPath();ctx.arc(sx+7,sy+8,5,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(sx+21,sy+8,5,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="#000";
    ctx.beginPath();ctx.arc(sx+7,sy+9,3,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(sx+21,sy+9,3,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="#fff";
    ctx.beginPath();ctx.arc(sx+8,sy+8,1,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(sx+22,sy+8,1,0,Math.PI*2);ctx.fill();
  }});
  // Player
  if(alive&&(invuln===0||(~~(invuln/4))%2===0)){{
    const sx=~~px-camX,sy=~~py;
    // shoes
    ctx.fillStyle="#502808";ctx.fillRect(sx,sy+PH-4,12,5);ctx.fillRect(sx+12,sy+PH-4,12,5);
    // overalls
    ctx.fillStyle="#0050b4";ctx.fillRect(sx,sy+PH-18,PW,14);
    ctx.fillStyle="#1060c8";ctx.fillRect(sx+2,sy+PH-22,PW-4,6);
    // body
    ctx.fillStyle="#dc3c32";ctx.fillRect(sx,sy+8,PW,14);
    // skin face
    ctx.fillStyle="#dca060";ctx.fillRect(sx+2,sy+2,PW-4,12);
    // hat
    ctx.fillStyle="#dc3c32";ctx.fillRect(sx+2,sy-2,PW-4,8);ctx.fillRect(sx+6,sy-6,PW-8,5);
    // mustache
    ctx.fillStyle="#502808";ctx.fillRect(sx+4,sy+10,PW-8,4);
    // eye
    const ex=facing>0?sx+PW-10:sx+4;
    ctx.fillStyle="#000";ctx.beginPath();ctx.arc(ex+3,sy+6,2,0,Math.PI*2);ctx.fill();
  }}
  // CT-style HUD
  ctx.fillStyle="rgba(0,0,0,0.82)";ctx.fillRect(0,0,SW,40);
  ctx.strokeStyle="#2a2a2a";ctx.lineWidth=1;ctx.strokeRect(0,0,SW,40);
  ctx.fillStyle="#aaa";ctx.font="10px Segoe UI";ctx.textAlign="left";
  ctx.fillText("MARIO",10,13);
  ctx.fillStyle="#fff";ctx.font="bold 14px Consolas";
  ctx.fillText(String(score).padStart(6,"0"),8,30);
  ctx.fillStyle="#ffd700";ctx.beginPath();ctx.arc(SW/2-60,20,7,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="#c8a000";ctx.lineWidth=1;ctx.stroke();
  ctx.fillStyle="#ffd700";ctx.font="bold 14px Consolas";ctx.textAlign="left";
  ctx.fillText("x"+String(coins).padStart(2,"0"),SW/2-48,28);
  ctx.fillStyle="#aaa";ctx.font="10px Segoe UI";ctx.textAlign="center";
  ctx.fillText("WORLD",SW/2,13);
  ctx.fillStyle="#f0a732";ctx.font="bold 14px Consolas";
  ctx.fillText(LEVEL_NAME,SW/2,30);
  ctx.fillStyle="#aaa";ctx.font="10px Segoe UI";ctx.textAlign="right";
  ctx.fillText("TIME",SW-10,13);
  ctx.fillStyle=timer<60?"#ff4040":"#ffffff";ctx.font="bold 14px Consolas";
  ctx.fillText(timer,SW-8,30);
  // Lives
  for(let i=0;i<3;i++){{
    const lx=SW/2+80+i*18,ly=12;
    ctx.fillStyle="#dc3c32";ctx.fillRect(lx,ly+6,12,10);ctx.fillRect(lx+4,ly,8,7);
  }}
  if(!alive){{
    ctx.fillStyle="rgba(0,0,0,0.65)";ctx.fillRect(0,0,SW,SH);
    ctx.fillStyle="#ff4040";ctx.font="bold 34px Arial";ctx.textAlign="center";
    ctx.fillText("GAME OVER",SW/2,SH/2-20);
    ctx.fillStyle="#ddd";ctx.font="16px Segoe UI";
    ctx.fillText("Press R to restart",SW/2,SH/2+20);
  }}
  ctx.textAlign="left";
  requestAnimationFrame(loop);
}}
document.addEventListener("keydown",e=>{{keys[e.code]=true;if(e.code==="KeyR"&&!alive)location.reload();}});
document.addEventListener("keyup",  e=>keys[e.code]=false);
requestAnimationFrame(t=>{{last=t;requestAnimationFrame(loop);}});
</script>
</body>
</html>'''

# ═══════════════════════════════════════════════════════════════════
#  MAIN IDE  — Clickteam Fusion # (exact layout)
# ═══════════════════════════════════════════════════════════════════
class KoopaEngineCT:
    def __init__(self, root):
        self.root = root
        self.root.title("Application1 - Koopa Engine  [Clickteam Fusion #]")
        self.root.geometry("1440x900")
        self.root.minsize(1024,680)
        self.root.configure(bg=T["bg"])

        self.level       = Level()
        self.active_layer= 1
        self.active_tile = "ground"
        self.active_ent  = "Player"
        self.tool        = "paint"
        self.zoom        = 1.0
        self.show_grid   = True
        self.layer_vis   = [True,True,True,True]
        self.layer_lock  = [False,False,False,False]
        self._drag       = False
        self._erase_drag_active = False
        self._tile_inner = None
        self._ent_inner  = None
        self._layer_panel= None
        self._set_vars   = {}
        self._tool_btns  = {}
        self._tbar_btns  = {}
        self._tab_frames = {}
        self._active_tab = None
        self.status_l    = tk.StringVar(value="  Ready  |  Left=paint  Right-click=delete  |  Clickteam Fusion #")
        self.status_r    = tk.StringVar(value="Row 0, Col 0  |  Tiles")

        self._ttk_theme()
        self._build_all()
        self._redraw()
        self._log("Clickteam Fusion #  —  Koopa Engine  ·  Ready","mario")
        self._log(f"Frame '{self.level.props['name']}'  {self.level.props['width']}×{self.level.props['height']}  ready","success")
        self._log("P=Paint  E=Erase  F=Fill  T=Entity  G=Grid  Right-click=delete  Ctrl+Z=Undo  F5=Run","info")

    # ── MENU BAR (Clickteam Fusion # exact) ───────────────────────────
    def _build_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # File
        file_m = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_m)
        file_m.add_command(label="New", command=self._new_level, accelerator="Ctrl+N")
        file_m.add_command(label="Open...", command=self._open_level, accelerator="Ctrl+O")
        file_m.add_command(label="Save", command=self._save_level, accelerator="Ctrl+S")
        file_m.add_command(label="Save As...", command=self._save_as)
        file_m.add_separator()
        file_m.add_command(label="Export", command=lambda: None)
        file_m.add_separator()
        file_m.add_command(label="Exit", command=self.root.quit, accelerator="Alt+F4")
        # Edit
        edit_m = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_m)
        edit_m.add_command(label="Undo", command=self._undo, accelerator="Ctrl+Z")
        edit_m.add_command(label="Clear", command=self._clear_all)
        edit_m.add_separator()
        edit_m.add_command(label="Level Properties...", command=self._props_dlg)
        # View
        self._menu_grid_var = tk.BooleanVar(value=self.show_grid)
        view_m = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_m)
        view_m.add_checkbutton(label="Grid", variable=self._menu_grid_var, command=self._menu_toggle_grid)
        view_m.add_command(label="Zoom In", command=lambda: self._set_zoom(self.zoom*1.25))
        view_m.add_command(label="Zoom Out", command=lambda: self._set_zoom(self.zoom/1.25))
        view_m.add_command(label="Zoom 100%", command=lambda: self._set_zoom(1.0))
        # Insert (Clickteam-style)
        insert_m = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Insert", menu=insert_m)
        insert_m.add_command(label="New Frame", command=self._new_level)
        insert_m.add_command(label="Object...", command=lambda: self._set_tool("entity"))
        # Run
        run_m = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_m)
        run_m.add_command(label="Run Application", command=self._run_preview, accelerator="F5")
        run_m.add_command(label="Build", command=lambda: self._export("pygame"))
        # Tools
        tools_m = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_m)
        tools_m.add_command(label="Install Dependencies...", command=self._dep_wizard)
        tools_m.add_command(label="Options...", command=lambda: None)
        # Help
        help_m = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_m)
        help_m.add_command(label="About Clickteam Fusion #", command=lambda: messagebox.showinfo("About", "Clickteam Fusion #\nKoopa Engine — Fusion 3–style IDE\nMario Forever / Buziol Engine"))

    # ── TTK ──────────────────────────────────────────────────────────
    def _ttk_theme(self):
        s=ttk.Style(); s.theme_use("clam")
        s.configure(".",background=T["bg"],foreground=T["fg"],
                    fieldbackground=T["input"],troughcolor=T["panel"],
                    bordercolor=T["border"],selectbackground=T["sel"],
                    selectforeground=T["fg"],relief="flat",font=FUI)
        s.configure("TFrame",background=T["bg"])
        s.configure("TLabel",background=T["bg"],foreground=T["fg"])
        for sc in("Vertical.TScrollbar","Horizontal.TScrollbar"):
            s.configure(sc,background=T["input"],troughcolor=T["panel"],
                        arrowcolor=T["fg2"],borderwidth=0)
        s.configure("TCombobox",fieldbackground=T["input"],background=T["input"],
                    foreground=T["fg"],selectbackground=T["sel"],arrowcolor=T["fg"])
        s.configure("TCheckbutton",background=T["panel"],foreground=T["fg"])
        s.map("TCheckbutton",background=[("active",T["hover"])])
        s.configure("Treeview",background=T["tree"],foreground=T["fg"],
                    fieldbackground=T["tree"],rowheight=22,borderwidth=0)
        s.configure("Treeview.Heading",background=T["ribbon"],
                    foreground=T["fg2"],relief="flat",font=FSM)
        s.map("Treeview",background=[("selected",T["sel"])],
                         foreground=[("selected","#fff")])

    # ── FULL BUILD ────────────────────────────────────────────────────
    def _build_all(self):
        self._build_menubar()
        self._build_ribbon()
        body = tk.Frame(self.root, bg=T["bg"])
        body.pack(fill="both", expand=True)
        self._build_left_panels(body)
        self._build_center(body)
        self._build_right_panels(body)
        self._build_statusbar()

    # ── RIBBON (CT style top toolbar) ────────────────────────────────
    def _build_ribbon(self):
        ribbon = tk.Frame(self.root, bg=T["ribbon"], height=80)
        ribbon.pack(fill="x"); ribbon.pack_propagate(False)

        # App branding (Clickteam Fusion #)
        brand = tk.Frame(ribbon, bg=T["ribbon"], width=180)
        brand.pack(side="left", fill="y"); brand.pack_propagate(False)
        tk.Label(brand, text="Clickteam Fusion", bg=T["ribbon"], fg=T["accent"],
                 font=("Segoe UI",11,"bold"), pady=4).pack()
        tk.Label(brand, text="#  ·  Koopa Engine", bg=T["ribbon"], fg=T["gold"],
                 font=("Segoe UI",8,"bold")).pack()
        tk.Frame(ribbon, bg=T["border"], width=1).pack(side="left", fill="y", padx=4)

        # Ribbon sections (Clickteam Fusion # — File, Edit, View, Insert, Run, Tools)
        for grp_name, items in [
            ("File", [
                ("New",        self._new_level,  "New Frame (Ctrl+N)"),
                ("Open",       self._open_level, "Open... (Ctrl+O)"),
                ("Save",       self._save_level, "Save (Ctrl+S)"),
            ]),
            ("Edit", [
                ("Undo",       self._undo,       "Undo (Ctrl+Z)"),
                ("Clear",      self._clear_all,  "Clear All"),
                ("Properties",  self._props_dlg,  "Level Properties"),
            ]),
            ("View", [
                ("Grid",       self._toggle_grid, "Toggle Grid (G)"),
                ("Zoom +",     lambda: self._set_zoom(self.zoom*1.25), "Zoom In"),
                ("Zoom −",     lambda: self._set_zoom(self.zoom/1.25), "Zoom Out"),
            ]),
            ("Insert", [
                ("Frame",      self._new_level,   "New Frame"),
                ("Paint",      lambda: self._set_tool("paint"),  "Paint (P)"),
                ("Erase",      lambda: self._set_tool("erase"), "Erase (E)"),
                ("Fill",       lambda: self._set_tool("fill"),   "Fill (F)"),
                ("Entity",     lambda: self._set_tool("entity"), "Entity (T)"),
            ]),
            ("Run", [
                ("Run",        self._run_preview, "Run Application (F5)"),
                ("Export .py", lambda: self._export("pygame"),  "Export Pygame"),
                ("Export .html", lambda: self._export("html"),   "Export HTML5"),
                (".exe / .app", lambda: self._export("exe"),    "Build Executable"),
            ]),
            ("Tools", [
                ("Dependencies", self._dep_wizard, "Install Dependencies"),
            ]),
        ]:
            grp = tk.Frame(ribbon, bg=T["ribbon"])
            grp.pack(side="left", padx=4, pady=4)
            tk.Label(grp, text=grp_name, bg=T["ribbon"], fg=T["fg2"],
                     font=("Segoe UI",7,"bold")).pack(anchor="w")
            btn_row = tk.Frame(grp, bg=T["ribbon"])
            btn_row.pack()
            for txt, cmd, tip in items:
                b = tk.Button(btn_row, text=txt, command=cmd,
                              bg=T["toolbar"], fg="#000000", font=FSM,
                              relief="flat", bd=0, cursor="hand2",
                              activebackground=T["sel"], activeforeground="#000000",
                              padx=6, pady=4)
                b.pack(side="left", padx=1)
                _Tip(b, tip)
            tk.Frame(ribbon, bg=T["grip"], width=1).pack(side="left", fill="y", pady=8)

        # Theme toggles — right side (Clickteam Fusion #)
        theme_f = tk.Frame(ribbon, bg=T["ribbon"])
        theme_f.pack(side="right", padx=12)
        tk.Label(theme_f, text="Theme", bg=T["ribbon"], fg=T["fg2"],
                 font=("Segoe UI",7,"bold")).pack()
        tf_row = tk.Frame(theme_f, bg=T["ribbon"])
        tf_row.pack()
        for name, col, tip in [
            ("dark", "#1e1f22", "Dark Mode"),
            ("blue", "#1c2740", "Blue Mode"),
            ("light","#f4f4f4","Light Mode"),
        ]:
            b = tk.Button(tf_row, text=name.capitalize(),
                          command=lambda n=name: self._set_theme(n),
                          bg=col, fg="#000000",
                          font=("Segoe UI",8,"bold"), relief="flat", bd=0,
                          cursor="hand2", padx=6, pady=4,
                          activebackground=T["sel"], activeforeground="#000000")
            b.pack(side="left", padx=2)
            _Tip(b, tip)

        self._bind_keys()

    def _bind_keys(self):
        self.root.bind("<Control-z>", lambda e: self._undo())
        self.root.bind("<Control-s>", lambda e: self._save_level())
        self.root.bind("<Control-n>", lambda e: self._new_level())
        self.root.bind("<Control-o>", lambda e: self._open_level())
        self.root.bind("<F5>",        lambda e: self._run_preview())
        self.root.bind("p", lambda e: self._set_tool("paint"))
        self.root.bind("e", lambda e: self._set_tool("erase"))
        self.root.bind("f", lambda e: self._set_tool("fill"))
        self.root.bind("t", lambda e: self._set_tool("entity"))
        self.root.bind("g", lambda e: self._toggle_grid())
        self.root.bind("<plus>",      lambda e: self._set_zoom(self.zoom*1.25))
        self.root.bind("<minus>",     lambda e: self._set_zoom(self.zoom/1.25))
        self.root.bind("<Control-0>", lambda e: self._set_zoom(1.0))

    # ── LEFT PANELS (Workspace tree + Object Inspector) ───────────────
    def _build_left_panels(self, parent):
        left = tk.Frame(parent, bg=T["panel"], width=210)
        left.pack(side="left", fill="y"); left.pack_propagate(False)

        # Workspace (Clickteam Fusion # — exact name)
        self._ct_section(left, "Workspace")
        ws_f = tk.Frame(left, bg=T["tree"])
        ws_f.pack(fill="x", padx=2)
        self._ws_tree = ttk.Treeview(ws_f, show="tree", height=8)
        self._ws_tree.pack(fill="x", padx=2, pady=2)
        app_n = self._ws_tree.insert("","end",text="Application 1",open=True)
        self._ws_frame_n = self._ws_tree.insert(app_n,"end",
                           text=f"Frame 1 — {self.level.props['name']}",open=True)
        for ld in LAYER_DEFS:
            self._ws_tree.insert(self._ws_frame_n,"end",text=f"  {ld['name']}")

        tk.Frame(left, bg=T["border"], height=1).pack(fill="x", padx=4, pady=3)

        # Properties (Clickteam Fusion # — exact name)
        self._ct_section(left, "Properties")
        prop_f = tk.Frame(left, bg=T["prop"])
        prop_f.pack(fill="both", expand=True, padx=2, pady=2)
        cols=("Property","Value")
        self._prop_tree = ttk.Treeview(prop_f, columns=cols,
                                       show="headings", height=12)
        for c in cols:
            self._prop_tree.heading(c, text=c)
            self._prop_tree.column(c, width=95)
        psb = ttk.Scrollbar(prop_f, orient="vertical",
                            command=self._prop_tree.yview)
        psb.pack(side="right", fill="y")
        self._prop_tree.config(yscrollcommand=psb.set)
        self._prop_tree.pack(fill="both", expand=True)
        self._refresh_inspector()

    def _ct_section(self, parent, title):
        hdr = tk.Frame(parent, bg=T["ribbon"])
        hdr.pack(fill="x")
        tk.Label(hdr, text=title, bg=T["ribbon"], fg=T["fg2"],
                 font=FSMB, padx=8, pady=3).pack(side="left")

    def _refresh_inspector(self):
        for r in self._prop_tree.get_children():
            self._prop_tree.delete(r)
        p = self.level.props
        for k,v in [("Name",p["name"]),("World",p.get("world_type","grass")),
                    ("Width",p["width"]),("Height",p["height"]),
                    ("Music",p.get("music","overworld")),
                    ("Gravity",p.get("gravity",9.8)),
                    ("Time",p.get("time",300)),
                    ("Layer",LAYER_DEFS[self.active_layer]["name"]),
                    ("Tool",self.tool),
                    ("Tile",self.active_tile)]:
            self._prop_tree.insert("","end",values=(k,v))

    # ── CENTER (Tab bar + editor canvas + terminal) ───────────────────
    def _build_center(self, parent):
        center = tk.Frame(parent, bg=T["bg"])
        center.pack(side="left", fill="both", expand=True)

        # Tab bar (Clickteam Fusion # — Frame Editor tabs)
        self._tabbar_f = tk.Frame(center, bg=T["tabbar"], height=32)
        self._tabbar_f.pack(fill="x"); self._tabbar_f.pack_propagate(False)
        self._tab_frames = {}; self._active_tab = None
        self._add_tab(self.level.props["name"], "Frame")

        # Toolbar strip under tabs
        self._build_tbar(center)

        # Frame Editor (Clickteam Fusion # — main editing area)
        ed_hdr = tk.Frame(center, bg=T["ribbon"], height=22)
        ed_hdr.pack(fill="x"); ed_hdr.pack_propagate(False)
        tk.Label(ed_hdr, text="Frame Editor", bg=T["ribbon"], fg=T["fg2"],
                 font=FSMB, padx=8, pady=2).pack(side="left")
        cv_area = tk.Frame(center, bg=T["bg"])
        cv_area.pack(fill="both", expand=True)
        self._build_canvas(cv_area)

        # Terminal / output
        self._build_terminal(center)
        self._build_statusbar_inline(center)

    def _add_tab(self, name, icon="🎮"):
        if name in self._tab_frames: return
        tab = tk.Frame(self._tabbar_f, bg=T["tab_in"], cursor="hand2")
        tab.pack(side="left")
        lbl = tk.Label(tab, text=f"  {icon} {name}  ",
                       bg=T["tab_in"], fg=T["fg2"], font=FTAB, pady=6)
        lbl.pack(side="left")
        x = tk.Label(tab, text=" × ", bg=T["tab_in"],
                     fg=T["fg3"], font=FUI, cursor="hand2")
        x.pack(side="left")
        x.bind("<Button-1>", lambda e, n=name: self._close_tab(n))
        for w in (tab, lbl):
            w.bind("<Button-1>", lambda e, n=name: self._activate_tab(n))
        self._tab_frames[name] = {"f":tab,"l":lbl,"x":x}
        self._activate_tab(name)

    def _activate_tab(self, name):
        if self._active_tab and self._active_tab in self._tab_frames:
            d = self._tab_frames[self._active_tab]
            d["f"].config(bg=T["tab_in"]); d["l"].config(bg=T["tab_in"],fg=T["fg2"])
            d["x"].config(bg=T["tab_in"])
            for c in d["f"].winfo_children():
                if isinstance(c,tk.Frame) and c.cget("height")==2: c.destroy()
        self._active_tab = name
        d = self._tab_frames[name]
        d["f"].config(bg=T["tab_act"]); d["l"].config(bg=T["tab_act"],fg=T["fg"])
        d["x"].config(bg=T["tab_act"])
        tk.Frame(d["f"], bg=T["accent"], height=2).pack(fill="x", side="bottom")

    def _close_tab(self, name):
        if name in self._tab_frames:
            self._tab_frames[name]["f"].destroy()
            del self._tab_frames[name]
            if self._tab_frames:
                self._activate_tab(list(self._tab_frames.keys())[-1])

    def _build_tbar(self, parent):
        bar = tk.Frame(parent, bg=T["toolbar"], height=30)
        bar.pack(fill="x"); bar.pack_propagate(False)
        tk.Frame(bar, bg=T["border"], width=1).pack(side="left", fill="y", padx=3)
        self._tbar_btns = {}
        for icon, key, tip in [("✏","paint","Paint (P)"),("⌫","erase","Erase (E)"),
                                ("▣","fill","Fill (F)"),("♟","entity","Entity (T)")]:
            bg = T["accent"] if key==self.tool else T["toolbar"]
            b = tk.Label(bar, text=icon, bg=bg, fg="#000000",
                         font=("Segoe UI Symbol",12), cursor="hand2",
                         width=3, pady=2)
            b.pack(side="left", padx=1)
            b.bind("<Button-1>", lambda e, k=key: self._set_tool(k))
            _Tip(b, tip); self._tbar_btns[key] = b
        tk.Frame(bar, bg=T["border"], width=1).pack(side="left", fill="y", padx=3)
        tk.Label(bar, text="Zoom:", bg=T["toolbar"], fg=T["fg2"], font=FSM).pack(side="left")
        self._zoom_lbl = tk.Label(bar, text="100%", bg=T["toolbar"],
                                  fg=T["gold"], font=FSMB, width=5)
        self._zoom_lbl.pack(side="left")
        flatbtn(bar, "+", lambda: self._set_zoom(self.zoom*1.25), bg=T["input"],
                padx=4, pady=1).pack(side="left", padx=1)
        flatbtn(bar, "−", lambda: self._set_zoom(self.zoom/1.25), bg=T["input"],
                padx=4, pady=1).pack(side="left", padx=1)
        flatbtn(bar, "1:1", lambda: self._set_zoom(1.0), bg=T["input"],
                padx=4, pady=1).pack(side="left", padx=1)
        tk.Frame(bar, bg=T["border"], width=1).pack(side="left", fill="y", padx=3)
        tk.Label(bar, text="Layer:", bg=T["toolbar"], fg=T["fg2"], font=FSM).pack(side="left")
        self._layer_var = tk.StringVar(value=LAYER_DEFS[self.active_layer]["name"])
        lcb = ttk.Combobox(bar, textvariable=self._layer_var,
                           values=[l["name"] for l in LAYER_DEFS],
                           width=10, state="readonly", font=FUI)
        lcb.pack(side="left", padx=4)
        lcb.bind("<<ComboboxSelected>>", self._on_layer_combo)
        tk.Frame(bar, bg=T["border"], width=1).pack(side="left", fill="y", padx=3)
        tk.Label(bar, text="Tile:", bg=T["toolbar"], fg=T["fg2"], font=FSM).pack(side="left")
        self._tile_prev = tk.Canvas(bar, width=20, height=20,
                                    bg=TILES.get(self.active_tile,("#888"," ",False,False))[0],
                                    highlightthickness=1, highlightbackground=T["border"])
        self._tile_prev.pack(side="left", padx=4)
        self._tile_name_lbl = tk.Label(bar, text=self.active_tile,
                                       bg=T["toolbar"], fg=T["gold"], font=FSM)
        self._tile_name_lbl.pack(side="left", padx=2)
        # Grid toggle
        gv = tk.BooleanVar(value=self.show_grid)
        ttk.Checkbutton(bar, text="Grid (G)", variable=gv,
                        command=self._toggle_grid).pack(side="left", padx=8)
        flatbtn(bar, "▶ Run F5", self._run_preview,
                bg=T["green"], fg="#000", padx=8, pady=2).pack(side="right", padx=8)

    def _on_layer_combo(self, e=None):
        n = self._layer_var.get()
        for i,ld in enumerate(LAYER_DEFS):
            if ld["name"]==n: self.active_layer=i; break
        self._refresh_inspector(); self._update_status(0,0)

    def _build_canvas(self, parent):
        frame = tk.Frame(parent, bg=T["wspace"])
        frame.pack(fill="both", expand=True)
        hbar = ttk.Scrollbar(frame, orient="horizontal")
        hbar.pack(side="bottom", fill="x")
        vbar = ttk.Scrollbar(frame, orient="vertical")
        vbar.pack(side="right", fill="y")
        self.canvas = tk.Canvas(frame, bg=T["wspace"], cursor="crosshair",
                                xscrollcommand=hbar.set,
                                yscrollcommand=vbar.set,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        hbar.config(command=self.canvas.xview)
        vbar.config(command=self.canvas.yview)
        self.canvas.bind("<ButtonPress-1>",   self._cv_press)
        self.canvas.bind("<B1-Motion>",        self._cv_drag)
        self.canvas.bind("<ButtonRelease-1>",  self._cv_release)
        # Right-click to delete: Button-3 (Windows/Linux), Button-2 (macOS), Control+Click
        for btn in (2, 3):
            self.canvas.bind(f"<ButtonPress-{btn}>",    self._cv_erase_press)
            self.canvas.bind(f"<B{btn}-Motion>",         self._cv_erase_drag)
            self.canvas.bind(f"<ButtonRelease-{btn}>",  self._cv_erase_release)
        self.canvas.bind("<Control-Button-1>", self._cv_erase_press)
        self.canvas.bind("<Control-B1-Motion>", self._cv_erase_drag)
        self.canvas.bind("<Control-ButtonRelease-1>", self._cv_erase_release)
        self.canvas.bind("<Motion>",           self._cv_hover)
        self.canvas.bind("<MouseWheel>",       self._cv_scroll)
        self.canvas.bind("<Control-MouseWheel>",self._cv_zoom_scroll)

    def _build_terminal(self, parent):
        rsz = tk.Frame(parent, bg=T["border"], height=2, cursor="sb_v_double_arrow")
        rsz.pack(fill="x"); rsz.bind("<B1-Motion>", self._resize_term)
        self._term_frame = tk.Frame(parent, bg=T["term"], height=140)
        self._term_frame.pack(fill="x"); self._term_frame.pack_propagate(False)
        pnl_hdr = tk.Frame(self._term_frame, bg=T["ribbon"], height=24)
        pnl_hdr.pack(fill="x"); pnl_hdr.pack_propagate(False)
        for lbl in ["Output", "Messages", "Errors"]:
            tk.Label(pnl_hdr, text=lbl, bg=T["ribbon"], fg=T["fg2"],
                     font=FSM, padx=10, pady=3).pack(side="left")
        flatbtn(pnl_hdr, "×", lambda: self._term_frame.pack_forget(),
                bg=T["ribbon"], fg=T["fg2"], padx=5, pady=1).pack(side="right")
        self.term = tk.Text(self._term_frame, bg=T["term"], fg=T["lime"],
                            font=("Consolas",9), bd=0, relief="flat",
                            state="disabled", wrap="word")
        tsb = ttk.Scrollbar(self._term_frame, orient="vertical",
                            command=self.term.yview)
        tsb.pack(side="right", fill="y")
        self.term.config(yscrollcommand=tsb.set)
        self.term.pack(fill="both", expand=True, padx=8, pady=2)
        self.term.tag_config("mario",   foreground="#f04040")
        self.term.tag_config("success", foreground=T["green"])
        self.term.tag_config("warn",    foreground=T["gold"])
        self.term.tag_config("error",   foreground=T["red"])
        self.term.tag_config("info",    foreground=T["fg"])
        self.term.tag_config("cmd",     foreground=T["blue"])

    def _build_statusbar_inline(self, parent):
        bar = tk.Frame(parent, bg=T["status"], height=20)
        bar.pack(fill="x"); bar.pack_propagate(False)
        tk.Label(bar, textvariable=self.status_l, bg=T["status"],
                 fg=T["sfg"], font=FSM, padx=8).pack(side="left")
        for txt in ["Clickteam Fusion #","Koopa Engine","Buziol","Pygame 600×400"]:
            tk.Label(bar, text=txt, bg=T["status"], fg=T["sfg"],
                     font=FSM, padx=6).pack(side="right")
        tk.Label(bar, textvariable=self.status_r, bg=T["status"],
                 fg=T["sfg"], font=FSM, padx=8).pack(side="right")

    def _build_statusbar(self):
        pass  # inline above

    # ── RIGHT PANELS (Tile Palette + Entity + Layers) ─────────────────
    def _build_right_panels(self, parent):
        right = tk.Frame(parent, bg=T["panel"], width=240)
        right.pack(side="right", fill="y"); right.pack_propagate(False)

        nb = ttk.Notebook(right)
        nb.pack(fill="both", expand=True)

        # Tile palette tab
        tp = tk.Frame(nb, bg=T["panel"])
        nb.add(tp, text=" Tiles ")
        self._build_tile_panel(tp)

        # Entity palette tab
        ep = tk.Frame(nb, bg=T["panel"])
        nb.add(ep, text=" Entities ")
        self._build_entity_panel(ep)

        # Layers tab
        lp = tk.Frame(nb, bg=T["panel"])
        nb.add(lp, text=" Layers ")
        self._build_layer_panel(lp)

        # Properties tab
        pp = tk.Frame(nb, bg=T["panel"])
        nb.add(pp, text=" Settings ")
        self._build_settings_panel(pp)

        # Minimap
        mm_f = tk.Frame(right, bg=T["panel"])
        mm_f.pack(fill="x", side="bottom")
        self._ct_section(mm_f, "Frame Overview")
        self.minimap = tk.Canvas(mm_f, bg=T["wspace"], width=226, height=68,
                                 highlightthickness=1,
                                 highlightbackground=T["border"])
        self.minimap.pack(padx=6, pady=4)

    def _build_tile_panel(self, parent):
        sf = tk.Frame(parent, bg=T["panel"]); sf.pack(fill="x", padx=6, pady=4)
        tk.Label(sf, text="🔍", bg=T["panel"], fg=T["fg2"]).pack(side="left")
        sv = tk.StringVar()
        VSEntry(sf, textvariable=sv).pack(side="left", fill="x", expand=True, padx=4)
        _, inner, _ = scrolled(parent, T["panel"])
        self._tile_inner = inner
        sv.trace_add("write", lambda *a: self._fill_tiles(sv.get()))
        self._fill_tiles("")

    def _fill_tiles(self, filt=""):
        g = self._tile_inner
        if not g: return
        for w in g.winfo_children(): w.destroy()
        row_f = None; col = 0
        for grp, names in TILE_GROUPS.items():
            # Group header
            hdr = tk.Frame(g, bg=T["ribbon"])
            hdr.grid(row=col//4*2 if col%4==0 else (col//4)*2,
                     column=0, columnspan=4, sticky="ew", pady=(4,1))
            tk.Label(hdr, text=grp, bg=T["ribbon"], fg=T["fg2"],
                     font=FSMB, padx=6, pady=1).pack(anchor="w")
            col = (col//4+1)*4
            for name in names:
                if filt and filt.lower() not in name.lower(): continue
                if name not in TILES: continue
                color,sym,solid,hazard=TILES[name]
                r_idx = col//4
                c_idx = col%4
                cell = tk.Frame(g, bg=T["panel"], padx=1, pady=1)
                cell.grid(row=r_idx*2+1, column=c_idx, padx=1, pady=1)
                sel = name==self.active_tile
                tc = tk.Canvas(cell, width=42, height=42, bg=color,
                               highlightthickness=2,
                               highlightbackground=T["accent"] if sel else T["border"],
                               cursor="hand2")
                tc.pack()
                tc.create_text(21,21,text=sym,fill="#fff",font=("Consolas",13,"bold"))
                if hazard: tc.create_text(38,4,text="⚠",fill="#ff4",font=("Symbol",7))
                tc.bind("<Button-1>", lambda e,n=name: self._pick_tile(n))
                _Tip(tc, f"{name}{'  SOLID' if solid else ''}{'  ⚠HAZARD' if hazard else ''}")
                tk.Label(cell, text=name[:7], bg=T["panel"], fg=T["fg2"],
                         font=FSM, width=6, anchor="center").pack()
                col += 1

    def _pick_tile(self, n):
        self.active_tile=n; self.tool="paint"
        self._fill_tiles(""); self._set_tool("paint")
        if hasattr(self,"_tile_prev"): self._tile_prev.config(bg=TILES[n][0])
        if hasattr(self,"_tile_name_lbl"): self._tile_name_lbl.config(text=n)
        self._log(f"Tile: {n}","info")

    def _build_entity_panel(self, parent):
        _, inner, _ = scrolled(parent, T["panel"])
        self._ent_inner = inner
        col = 0
        for name,(color,sym) in ENTITIES.items():
            cell = tk.Frame(inner, bg=T["panel"], padx=1, pady=1)
            cell.grid(row=col//3, column=col%3, padx=2, pady=2)
            sel = name==self.active_ent
            ec = tk.Canvas(cell, width=52, height=52, bg=color,
                           highlightthickness=2,
                           highlightbackground=T["accent"] if sel else T["border"],
                           cursor="hand2")
            ec.pack()
            ec.create_text(26,26,text=sym,fill="#fff",font=("Consolas",10,"bold"))
            ec.bind("<Button-1>", lambda e,n=name: self._pick_ent(n))
            _Tip(ec, name)
            tk.Label(cell, text=name[:9], bg=T["panel"], fg=T["fg2"],
                     font=FSM, width=9, anchor="center").pack()
            col += 1

    def _pick_ent(self, n):
        self.active_ent=n; self.tool="entity"
        self._set_tool("entity"); self._log(f"Entity: {n}","info")

    def _build_layer_panel(self, parent):
        hdr = tk.Frame(parent, bg=T["panel"]); hdr.pack(fill="x", padx=8, pady=6)
        tk.Label(hdr, text="Frame Layers", bg=T["panel"], fg=T["fg"],
                 font=FBOLD).pack(side="left")
        self._layer_panel = tk.Frame(parent, bg=T["panel"])
        self._layer_panel.pack(fill="both", expand=True)
        self._draw_layers()

    def _draw_layers(self):
        if not self._layer_panel: return
        for w in self._layer_panel.winfo_children(): w.destroy()
        for i,ld in enumerate(reversed(LAYER_DEFS)):
            ri = len(LAYER_DEFS)-1-i
            is_a = ri==self.active_layer
            bg = T["sel"] if is_a else T["hover"]
            row = tk.Frame(self._layer_panel, bg=bg, cursor="hand2")
            row.pack(fill="x", padx=4, pady=1)
            tk.Frame(row, bg=ld["color"], width=5).pack(side="left", fill="y")
            vis = tk.Label(row, text="👁" if self.layer_vis[ri] else "◌",
                           bg=bg, fg="#000000", font=FSM, width=2, cursor="hand2")
            vis.pack(side="right", padx=2)
            vis.bind("<Button-1>", lambda e,idx=ri: self._tog_vis(idx))
            lk = tk.Label(row, text="🔒" if self.layer_lock[ri] else "  ",
                          bg=bg, fg="#000000", font=FSM, width=2, cursor="hand2")
            lk.pack(side="right", padx=2)
            lk.bind("<Button-1>", lambda e,idx=ri: self._tog_lock(idx))
            nl = tk.Label(row, text=ld["name"], bg=bg,
                          fg="#000000",
                          font=FBOLD if is_a else FUI,
                          anchor="w", padx=8, pady=8)
            nl.pack(side="left", fill="x", expand=True)
            nl.bind("<Button-1>", lambda e,idx=ri: self._set_layer(idx))
            row.bind("<Button-1>",  lambda e,idx=ri: self._set_layer(idx))
        tk.Frame(self._layer_panel, bg=T["border"], height=1).pack(fill="x", padx=8, pady=4)
        tk.Label(self._layer_panel,
                 text=f"Active: {LAYER_DEFS[self.active_layer]['name']}",
                 bg=T["panel"], fg=T["accent"], font=FBOLD).pack(anchor="w", padx=12)

    def _tog_vis(self,i): self.layer_vis[i]=not self.layer_vis[i]; self._draw_layers(); self._redraw()
    def _tog_lock(self,i): self.layer_lock[i]=not self.layer_lock[i]; self._draw_layers()
    def _set_layer(self,i):
        self.active_layer=i; self._draw_layers()
        if hasattr(self,"_layer_var"): self._layer_var.set(LAYER_DEFS[i]["name"])
        self._refresh_inspector(); self._update_status(0,0)

    def _build_settings_panel(self, parent):
        _, inner, _ = scrolled(parent, T["panel"])
        p=self.level.props; self._set_vars={}

        def section(t):
            tk.Frame(inner, bg=T["border"], height=1).pack(fill="x", padx=4, pady=4)
            tk.Label(inner, text=t, bg=T["panel"], fg=T["fg2"],
                     font=FSMB, padx=8, anchor="w").pack(fill="x")

        def field(key, lbl, kind="entry", opts=None):
            row=tk.Frame(inner, bg=T["panel"]); row.pack(fill="x", padx=8, pady=2)
            tk.Label(row, text=lbl, bg=T["panel"], fg=T["fg2"],
                     font=FSM, width=14, anchor="w").pack(side="left")
            if kind=="entry":
                v=tk.StringVar(value=str(p.get(key,"")))
                VSEntry(row, textvariable=v, width=10).pack(side="left")
            elif kind=="combo":
                v=tk.StringVar(value=str(p.get(key,"")))
                ttk.Combobox(row, textvariable=v, values=opts,
                             width=10, state="readonly").pack(side="left")
            elif kind=="check":
                v=tk.BooleanVar(value=bool(p.get(key,False)))
                ttk.Checkbutton(row, variable=v).pack(side="left")
            self._set_vars[key]=v

        section("IDENTITY")
        field("name","Name"); field("world_type","World","combo",list(BG_COLORS.keys()))
        section("SIZE")
        field("width","Width (tiles)"); field("height","Height (tiles)")
        section("TIME & AUDIO")
        field("time","Time Limit"); field("music","Music","combo",MUSIC)
        section("PHYSICS")
        field("gravity","Gravity")
        field("scroll","Scroll","combo",["horizontal","vertical","free"])
        section("FLAGS")
        field("is_castle","Castle","check"); field("is_underwater","Underwater","check")
        section("PLAYER START")
        field("start_x","Start X"); field("start_y","Start Y")

        flatbtn(inner,"  ✓ Apply  ",self._apply_settings,
                bg=T["accent"],fg="#000000",padx=10,pady=5).pack(pady=10)

    def _apply_settings(self):
        for k,v in self._set_vars.items():
            val=v.get()
            if k in("width","height","time","start_x","start_y"):
                try: val=int(val)
                except: pass
            elif k=="gravity":
                try: val=float(val)
                except: pass
            self.level.props[k]=val
        self._log(f"Settings: {self.level.props['name']}","success")
        self._refresh_inspector(); self._redraw()

    # ── THEME SWITCH ─────────────────────────────────────────────────
    def _set_theme(self, name):
        global T
        CUR_THEME[0] = name
        T.clear(); T.update(THEMES[name])
        self._ttk_theme()
        # Rebuild everything
        for widget in self.root.winfo_children():
            widget.destroy()
        self._tab_frames = {}; self._active_tab = None
        self._tile_inner = None; self._ent_inner = None
        self._layer_panel = None; self._set_vars = {}
        self._tool_btns = {}; self._tbar_btns = {}
        self.root.configure(bg=T["bg"])
        self._build_all()
        self._redraw()
        self._log(f"Theme: {name}","success")

    # ── CANVAS DRAWING ───────────────────────────────────────────────
    def _redraw(self):
        self.canvas.delete("all")
        lvl=self.level; w=lvl.props["width"]; h=lvl.props["height"]
        px=max(4,int(TILE_PX*self.zoom))
        bg_key=lvl.props.get("background",lvl.props.get("world_type","grass"))
        bg_hex=BG_COLORS.get(bg_key,"#5c94fc")
        self.canvas.configure(bg=bg_hex,
                              scrollregion=(0,0,w*px+80,h*px+80))
        for li in range(4):
            if not self.layer_vis[li]: continue
            for r in range(h):
                for c in range(w):
                    cell=lvl.get(li,r,c)
                    if not cell or cell=="empty": continue
                    x1=c*px; y1=r*px; x2=x1+px; y2=y1+px
                    if li==2:
                        ed=ENTITIES.get(cell)
                        if ed:
                            col,sym=ed
                            self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2,
                                                    fill=col,outline="#fff",width=1)
                            fs=max(5,px//3)
                            self.canvas.create_text((x1+x2)//2,(y1+y2)//2,
                                                    text=sym,fill="#fff",
                                                    font=("Consolas",fs,"bold"))
                    else:
                        td=TILES.get(cell)
                        if not td: continue
                        color,sym,solid,hazard=td
                        self.canvas.create_rectangle(x1,y1,x2,y2,fill=color,outline="",width=0)
                        if px>=14:
                            fs=max(5,px//3)
                            self.canvas.create_text((x1+x2)//2,(y1+y2)//2,
                                                    text=sym,fill="#fff",
                                                    font=("Consolas",fs))
                        if hazard:
                            self.canvas.create_text(x2-4,y1+4,text="⚠",
                                                    fill="#ff4",font=("Symbol",max(6,px//5)))
        if self.show_grid:
            gc="#444466" if bg_hex in("#000000","#101010","#1a1a2e","#000","#0c1622") else "#aaaacc"
            for c in range(w+1):
                self.canvas.create_line(c*px,0,c*px,h*px,fill=gc,width=1)
            for r in range(h+1):
                self.canvas.create_line(0,r*px,w*px,r*px,fill=gc,width=1)
        for c in range(0,w,5):
            self.canvas.create_text(c*px+2,2,text=str(c),fill=T["fg3"],
                                    font=("Consolas",max(6,px//4)),anchor="nw")
        for r in range(0,h,2):
            self.canvas.create_text(2,r*px+2,text=str(r),fill=T["fg3"],
                                    font=("Consolas",max(6,px//4)),anchor="nw")
        self._draw_minimap()

    def _draw_minimap(self):
        mm=self.minimap; mm.delete("all")
        lvl=self.level; w=lvl.props["width"]; h=lvl.props["height"]
        if w==0 or h==0: return
        mw,mh=226,68; tw=mw/w; th=mh/h
        bg_hex=BG_COLORS.get(lvl.props.get("background","grass"),"#5c94fc")
        mm.config(bg=bg_hex)
        for r in range(h):
            for c in range(w):
                cell=lvl.get(1,r,c)
                if not cell or cell=="empty": continue
                td=TILES.get(cell)
                if not td: continue
                mm.create_rectangle(c*tw,r*th,(c+1)*tw+1,(r+1)*th+1,fill=td[0],outline="")
        for r in range(h):
            for c in range(w):
                cell=lvl.get(2,r,c)
                if not cell: continue
                ed=ENTITIES.get(cell)
                if not ed: continue
                mm.create_oval(c*tw,r*th,(c+1)*tw,(r+1)*th,fill=ed[0],outline="")

    # ── CANVAS EVENTS ────────────────────────────────────────────────
    def _xy(self,event):
        px_=max(4,int(TILE_PX*self.zoom))
        return int(self.canvas.canvasy(event.y)//px_),int(self.canvas.canvasx(event.x)//px_)

    def _paint(self,r,c):
        if self.layer_lock[self.active_layer]: return
        w_=self.level.props["width"]; h_=self.level.props["height"]
        if not(0<=r<h_ and 0<=c<w_): return
        if self.tool in("paint","entity"):
            v=self.active_ent if self.active_layer==2 else (self.active_ent if self.tool=="entity" else self.active_tile)
            if self.tool=="entity": v=self.active_ent
            elif self.tool=="paint": v=self.active_tile if self.active_layer!=2 else self.active_ent
            self.level.set(self.active_layer,r,c,v); self._redraw()
        elif self.tool=="erase":
            self.level.set(self.active_layer,r,c,None if self.active_layer==2 else "empty")
            self._redraw()

    def _cv_press(self,event):
        r,c=self._xy(event); self.level.snapshot()
        if self.tool=="fill":
            v=self.active_ent if self.active_layer==2 else self.active_tile
            self.level.flood_fill(self.active_layer,r,c,v); self._redraw()
        else: self._paint(r,c)
        self._update_status(r,c); self._drag=True

    def _cv_drag(self,event):
        if not self._drag: return
        r,c=self._xy(event); self._paint(r,c); self._update_status(r,c)

    def _cv_release(self,event): self._drag=False

    def _cv_erase_press(self, event):
        if self.layer_lock[self.active_layer]:
            return
        self.level.snapshot()
        self._erase_drag_active = True
        r, c = self._xy(event)
        w_, h_ = self.level.props["width"], self.level.props["height"]
        if 0 <= r < h_ and 0 <= c < w_:
            self.level.set(self.active_layer, r, c,
                           None if self.active_layer == 2 else "empty")
            self._redraw()
        self._update_status(r, c)
        return "break"

    def _cv_erase_drag(self, event):
        if not self._erase_drag_active or self.layer_lock[self.active_layer]:
            return
        r, c = self._xy(event)
        w_, h_ = self.level.props["width"], self.level.props["height"]
        if 0 <= r < h_ and 0 <= c < w_:
            self.level.set(self.active_layer, r, c,
                           None if self.active_layer == 2 else "empty")
            self._redraw()
        self._update_status(r, c)
        return "break"

    def _cv_erase_release(self, event):
        self._erase_drag_active = False
        return "break"

    def _cv_hover(self,event): r,c=self._xy(event); self._update_status(r,c)
    def _cv_scroll(self,event): self.canvas.yview_scroll(-1*(event.delta//120),"units")
    def _cv_zoom_scroll(self,event): self._set_zoom(self.zoom*(1.1 if event.delta>0 else 0.9))

    def _update_status(self,r,c):
        self.status_r.set(f"Row {r}, Col {c}  |  {LAYER_DEFS[self.active_layer]['name']}")

    def _set_zoom(self,z):
        self.zoom=max(0.25,min(4.0,z))
        if hasattr(self,"_zoom_lbl"): self._zoom_lbl.config(text=f"{int(self.zoom*100)}%")
        self._redraw()

    def _set_tool(self,key):
        self.tool=key
        for k,b in self._tbar_btns.items():
            b.config(bg=T["accent"] if k==key else T["toolbar"], fg="#000000")
        self._refresh_inspector()

    def _toggle_grid(self):
        self.show_grid=not self.show_grid
        if hasattr(self,"_menu_grid_var"): self._menu_grid_var.set(self.show_grid)
        self._redraw()
    def _menu_toggle_grid(self): self.show_grid=self._menu_grid_var.get(); self._redraw()
    def _resize_term(self,event):
        new_h=max(60,self._term_frame.winfo_height()-event.y)
        self._term_frame.config(height=new_h)

    # ── LEVEL OPS ────────────────────────────────────────────────────
    def _new_level(self):
        self.level=Level(); self._add_tab(self.level.props["name"],"Frame")
        self._redraw(); self._log("New level.","success")

    def _open_level(self):
        path=filedialog.askopenfilename(title="Open",
            filetypes=[("Koopa Level","*.klvl"),("JSON","*.json"),("All","*.*")])
        if not path: return
        try:
            with open(path) as fp: d=json.load(fp)
            self.level=Level.from_dict(d); self.level.filepath=path
            self._add_tab(self.level.props["name"],"Frame")
            self._redraw(); self._log(f"Opened: {path}","success")
        except Exception as ex: messagebox.showerror("Error",str(ex))

    def _save_level(self):
        if self.level.filepath: self._do_save(self.level.filepath)
        else: self._save_as()

    def _save_as(self):
        path=filedialog.asksaveasfilename(title="Save",defaultextension=".klvl",
            filetypes=[("Koopa Level","*.klvl"),("JSON","*.json")])
        if not path: return
        self.level.filepath=path; self._do_save(path)

    def _do_save(self,path):
        try:
            with open(path,"w") as fp: json.dump(self.level.to_dict(),fp,indent=2)
            self._log(f"Saved: {path}","success")
        except Exception as ex: messagebox.showerror("Error",str(ex))

    def _undo(self):
        if self.level.undo(): self._redraw(); self._log("Undo","warn")
        else: self._log("Nothing to undo","warn")

    def _clear_all(self):
        if messagebox.askyesno("Clear","Clear ALL layers?"):
            self.level.snapshot(); self.level.layers=self.level._blank()
            self._redraw(); self._log("Cleared.","warn")

    def _props_dlg(self): pass  # Settings in right panel

    # ── EXPORT ───────────────────────────────────────────────────────
    def _export(self, target):
        out=filedialog.askdirectory(title="Select Output Folder")
        if not out: return
        if target=="pygame":
            code=gen_pygame(self.level)
            path=os.path.join(out,"main.py")
            with open(path,"w") as fp: fp.write(code)
            self._log(f"Exported → {path}","success")
            messagebox.showinfo("Done",f"Pygame source:\n{path}\n\npython main.py")
            return
        if target=="html":
            code=gen_html(self.level)
            path=os.path.join(out,"index.html")
            with open(path,"w") as fp: fp.write(code)
            self._log(f"Exported → {path}","success")
            messagebox.showinfo("Done",f"HTML5 game:\n{path}\n\nOpen in browser.")
            return
        # exe / mac via PyInstaller
        py_path=os.path.join(out,"main.py")
        with open(py_path,"w") as fp: fp.write(gen_pygame(self.level))
        messagebox.showinfo("Build",
            "PyInstaller build starting.\nCheck the terminal panel for output.")
        def build():
            try:
                cmd=["pyinstaller","--onefile","--windowed","main.py"]
                proc=subprocess.Popen(cmd,cwd=out,stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,text=True)
                for line in proc.stdout:
                    self.root.after(0,lambda l=line:self._log(l.rstrip(),"cmd"))
                proc.wait()
                if proc.returncode==0:
                    dist=os.path.join(out,"dist")
                    self.root.after(0,lambda:self._log(f"Build OK → {dist}","success"))
                    self.root.after(0,lambda:messagebox.showinfo("Build OK",f"Executable in:\n{dist}"))
                else:
                    self.root.after(0,lambda:self._log("Build FAILED","error"))
                    self.root.after(0,lambda:messagebox.showerror("Failed","PyInstaller failed.\nRun Install Dependencies."))
            except FileNotFoundError:
                self.root.after(0,lambda:messagebox.showerror("Missing","pyinstaller not found.\nUse Install Deps."))
            except Exception as ex:
                self.root.after(0,lambda:messagebox.showerror("Error",str(ex)))
        threading.Thread(target=build,daemon=True).start()

    def _dep_wizard(self):
        w=tk.Toplevel(self.root); w.title("Install Dependencies")
        w.geometry("520x340"); w.configure(bg=T["bg"])
        tk.Label(w,text="Koopa Engine — Dependency Installer",
                 bg=T["bg"],fg=T["gold"],font=FBOLD).pack(pady=8)
        tk.Label(w,text="Installs: pygame  pyinstaller  pygbag",
                 bg=T["bg"],fg=T["fg2"],font=FUI).pack()
        log=tk.Text(w,bg=T["term"],fg=T["lime"],font=("Consolas",9),height=13,relief="flat")
        log.pack(fill="both",expand=True,padx=10,pady=6)
        close=flatbtn(w,"Close",w.destroy,bg=T["input"]); close.pack(pady=4)
        close.config(state="disabled")
        def append(t): self.root.after(0,lambda:(log.insert("end",t),log.see("end")))
        def task():
            append("Installing...\n")
            cmd=[sys.executable,"-m","pip","install","pygame","pyinstaller","pygbag"]
            proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            for line in proc.stdout: append(line)
            proc.wait()
            append("\n✓ Done!\n" if proc.returncode==0 else "\n✗ Error.\n")
            self.root.after(0,lambda:close.config(state="normal"))
        threading.Thread(target=task,daemon=True).start()

    def _run_preview(self):
        import tempfile
        code=gen_pygame(self.level)
        tmp=tempfile.NamedTemporaryFile(mode="w",suffix=".py",delete=False,prefix="koopa_")
        tmp.write(code); tmp.close()
        self._log(f"Run: {tmp.name}","success")
        def run():
            try:
                proc=subprocess.Popen([sys.executable,tmp.name],
                                      stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                for line in proc.stdout:
                    self.root.after(0,lambda l=line:self._log(l.rstrip(),"cmd"))
                proc.wait()
            except Exception as ex: self.root.after(0,lambda:self._log(str(ex),"error"))
        threading.Thread(target=run,daemon=True).start()

    def _log(self,msg,tag="info"):
        ts=time.strftime("%H:%M:%S")
        self.term.config(state="normal")
        self.term.insert("end",f"[{ts}] ","info")
        self.term.insert("end",msg+"\n",tag)
        self.term.see("end"); self.term.config(state="disabled")

# ═══════════════════════════════════════════════════════════════════
#  ENTRY
# ═══════════════════════════════════════════════════════════════════
if __name__=="__main__":
    root=tk.Tk()
    try: root.tk.call("tk","scaling",1.0)
    except: pass
    app=KoopaEngineCT(root)
    root.mainloop()
