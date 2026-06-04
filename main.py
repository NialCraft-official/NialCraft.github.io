import tkinter as tk, random as r, socket, threading

class NialcraftApp:
    def __init__(self, s):
        self.s = s; s.title("Nialcraft 2D"); s.geometry("800x600"); self.p, self.b, self.f, self.expl_running, self.ie, self.net_sock, self.my_id, self.players = [], [], False, False, None, None, None, {}
        self.c = tk.Canvas(s, bg="#222222", highlightthickness=0); self.c.pack(fill=tk.BOTH, expand=True); s.bind("<F11>", self.tg_f); self.init_m()
    
    def tg_f(self, e=None): 
        self.f = not self.f; self.s.attributes("-fullscreen", self.f)
    
    def init_m(self, e=None):
        if self.net_sock:
            try: self.net_sock.close()
            except: pass
            self.net_sock = None
        for k in ["w","s","a","d","W","S","A","D"]: self.s.unbind(f"<{k}>")
        if self.ie and self.ie.winfo_exists(): self.ie.destroy(); self.ie = None
        self.c.delete("all"); self.p, self.b, self.expl_running = [], [], False
        
        # Восстановленная матрица логотипа NIALCRAFT
        m = [
            [0,1,0,0,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
            [1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,0,1,0],
            [1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,1,0,0,1,0],
            [1,0,0,1,1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,1,0],
            [1,0,0,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,0,0,0,1,0]
        ]
        sz, cl, sx, sy = 8, ["#4CAF50", "#8BC34A", "#795548", "#9E9E9E"], 400 - (len(m[0]) * 8) // 2, 40
        for ri, row in enumerate(m):
            for ci, v in enumerate(row):
                if v:
                    x, y = sx + ci * sz, sy + ri * sz; pid = self.c.create_rectangle(x, y, x + sz, y + sz, fill=r.choice(cl), outline="")
                    self.p.append({"id": pid, "x": x, "y": y, "vx": r.uniform(-4, 4), "vy": r.uniform(-6, 2), "life": 100})
        for p in self.p: self.c.tag_bind(p["id"], "<Button-1>", lambda e: self.start_expl())
        self.cr_b("Одиночная игра", 240, self.st_s); self.cr_b("Мультиплеер", 310, self.op_m); self.cr_b("Выход из игры", 380, self.s.quit); self.an_b()
    
    def cr_b(self, t, ty, cmd):
        bid = self.c.create_rectangle(-250, ty, -50, ty + 45, fill="#444444", outline="#666666", width=2); tid = self.c.create_text(-150, ty + 22, text=t, fill="white", font=("Courier", 14, "bold"))
        self.c.tag_bind(bid, "<Enter>", lambda e: self.c.itemconfig(bid, fill="#555555", outline="#888888")); self.c.tag_bind(tid, "<Enter>", lambda e: self.c.itemconfig(bid, fill="#555555", outline="#888888"))
        self.c.tag_bind(bid, "<Leave>", lambda e: self.c.itemconfig(bid, fill="#444444", outline="#666666")); self.c.tag_bind(tid, "<Leave>", lambda e: self.c.itemconfig(bid, fill="#444444", outline="#666666"))
        for i in (bid, tid): self.c.tag_bind(i, "<Button-1>", lambda e: cmd())
        self.b.append({"b": bid, "t": tid, "cx": -250, "tx": 275, "y": ty})
    
    def an_b(self):
        mv = False
        for b in self.b:
            if b["cx"] < b["tx"]: b["cx"] += 25; self.c.coords(b["b"], b["cx"], b["y"], b["cx"] + 250, b["y"] + 45); self.c.coords(b["t"], b["cx"] + 125, b["y"] + 22); mv = True
        if mv: self.s.after(20, self.an_b)
    
    def start_expl(self):
        if not self.expl_running: self.expl_running = True; self.expl()
    
    def expl(self):
        if not self.expl_running: return
        act = False
        for p in self.p:
            if p["life"] > 0: p["x"] += p["vx"]; p["y"] += p["vy"]; p["vy"] += 0.4; p["life"] -= 2; self.c.coords(p["id"], p["x"], p["y"], p["x"] + 8, p["y"] + 8); act = True
        if act: self.s.after(16, self.expl)
    
    def st_s(self):
        self.wo = self.c.create_rectangle(150, 150, 650, 450, fill="#111111", outline="#FF9800", width=3); self.wt = self.c.create_text(400, 280, text="ОДИНОЧНАЯ ИГРА\nW.I.P. (Work In Progress)\n\n[Будет добавлена загрузка .mnc JSON файлов]\n\nКликните в любое место, чтобы скрыть окно", fill="#FF9800", font=("Courier", 14, "bold"), justify=tk.CENTER)
        for i in (self.wo, self.wt): self.c.tag_bind(i, "<Button-1>", self.hd_w)
    
    def hd_w(self, e=None):
        if hasattr(self, 'wo'): self.c.delete(self.wo); self.c.delete(self.wt)
    
    def op_m(self):
        self.c.delete("all"); self.c.create_text(400, 120, text="ПОДКЛЮЧЕНИЕ К СЕРВЕРУ", fill="white", font=("Courier", 20, "bold")); self.c.create_text(400, 160, text="(Запустите server через отдельный .bat перед коннектом)", fill="#888888", font=("Courier", 10)); self.c.create_text(400, 230, text="Введите IP-адрес сервера:", fill="#AAAAAA", font=("Courier", 12))
        self.ie = tk.Entry(self.s, font=("Courier", 14), bg="#333333", fg="white", insertbackground="white", justify="center"); self.ie.insert(0, "127.0.0.1:25565"); self.iw = self.c.create_window(400, 270, window=self.ie, width=280, height=35)
        for t, y, c in [("ПОДКЛЮЧИТЬСЯ", 340, self.cn_s), ("НАЗАД В МЕНЮ", 410, self.init_m)]:
            b = self.c.create_rectangle(275, y, 525, y + 45, fill="#4CAF50" if y==340 else "#f44336", outline=""); tx = self.c.create_text(400, y + 22, text=t, fill="white", font=("Courier", 12, "bold"))
            for i in (b, tx): self.c.tag_bind(i, "<Button-1>", lambda e, cmd=c: cmd())
    
    def cn_s(self):
        ip_p = self.ie.get() if (self.ie and self.ie.winfo_exists()) else "127.0.0.1:25565"
        try: self.ie.destroy()
        except: pass
        self.c.delete("all"); ip, port = ip_p.split(":") if ":" in ip_p else (ip_p, 25565); port = int(port)
        self.c.create_text(400, 300, text=f"Установка соединения с {ip}:{port}...", fill="white", font=("Courier", 14)); self.s.update()
        try:
            self.net_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                resolved_ip = socket.gethostbyname(ip)
                self.net_sock.connect((resolved_ip, port))
            except:
                if ip == "127.0.0.1": self.net_sock.connect(("localhost", port))
                else: raise Exception()
            self.players = {}; threading.Thread(target=self.listen_server, daemon=True).start()
        except Exception as e:
            self.c.delete("all"); self.c.create_text(400, 220, text=f"КРИТИЧЕСКАЯ ОШИБКА ПОДКЛЮЧЕНИЯ:\n{e}", fill="#f44336", font=("Courier", 12), justify=tk.CENTER); self.cr_b("НАЗАД В МЕНЮ", 360, self.init_m); return
        self.g, self.bs, self.px, self.py = 9, 45, 4, 4; self.rx, self.ry = 400 - 405 // 2, 300 - 405 // 2; self.dr_w()
        for k in ["w","s","a","d","W","S","A","D"]: self.s.bind(f"<{k}>", lambda e, key=k: self.mv_p(key))
    
    def listen_server(self):
        while True:
            try:
                t_byte = self.net_sock.recv(1)
                if not t_byte: break
                t = int(t_byte[0])
                if t == 1:
                    d = self.net_sock.recv(2); self.my_id = (int(d[0]) << 8) + int(d[1])
                elif t in [2, 3]:
                    d = self.net_sock.recv(4); pid = (int(d[0]) << 8) + int(d[1])
                    if pid != self.my_id: self.players[pid] = {"x": int(d[2]), "y": int(d[3])}; self.s.after(0, self.dr_w)
                elif t == 4:
                    d = self.net_sock.recv(2); pid = (int(d[0]) << 8) + int(d[1])
                    if pid in self.players: del self.players[pid]; self.s.after(0, self.dr_w)
            except: break
    
    def dr_w(self):
        self.c.delete("all"); self.c.create_text(400, 20, text=f"Nialcraft Мультиплеер (Ваш ID: {self.my_id})", fill="#888888", font=("Courier", 12))
        for gx in range(9):
            for gy in range(9):
                x1, y1 = self.rx + gx * 45, self.ry + gy * 45; cl, oc = ("#333333", "#2a2a2a") if gy < 3 else ("#4CAF50", "#388E3C") if gy == 3 else ("#795548", "#5D4037") if gy < 7 else ("#9E9E9E", "#616161")
                self.c.create_rectangle(x1, y1, x1 + 45, y1 + 45, fill=cl, outline=oc)
        for pid, pi in self.players.items():
            ex, ey = self.rx + pi["x"] * 45 + 8, self.ry + pi["y"] * 45 + 14; self.c.create_rectangle(ex, ey, ex + 29, ey + 27, fill="#E91E63", outline="#C2185B", width=2); self.c.create_rectangle(ex + 6, ey - 10, ex + 23, ey, fill="#FFC107", outline="#FFA000"); self.c.create_text(ex + 14, ey - 18, text=f"P_{pid}", fill="white", font=("Courier", 8))
        x, y = self.rx + self.px * 45 + 8, self.ry + self.py * 45 + 14; self.c.create_rectangle(x, y, x + 29, y + 27, fill="#00BCD4", outline="#0097A7", width=2); self.c.create_rectangle(x + 6, y - 10, x + 23, y, fill="#FFC107", outline="#FFA000")
    
    def mv_p(self, k):
        dx, dy = (0, -1) if k in "wW" else (0, 1) if k in "sS" else (-1, 0) if k in "aA" else (1, 0)
        if 0 <= self.px + dx < 9 and 0 <= self.py + dy < 9:
            self.px += dx; self.py += dy; self.dr_w()
            if self.net_sock and self.my_id:
                try: self.net_sock.sendall(bytes([3, self.my_id >> 8, self.my_id & 255, self.px, self.py]))
                except: pass

if __name__ == "__main__": 
    r_t = tk.Tk(); app = NialcraftApp(r_t); r_t.mainloop()