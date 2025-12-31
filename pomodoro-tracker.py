#!/usr/bin/env python3
"""
🍅 Pomodoro Productivity Tracker
Timer Pomodoro com estatísticas e gráficos
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time

class PomodoroTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("🍅 Pomodoro Productivity Tracker")
        self.root.geometry("900x700")
        self.root.configure(bg="#667eea")
        
        # Configurações do timer
        self.pomodoro_time = 25 * 60  # 25 minutos
        self.short_break = 5 * 60     # 5 minutos
        self.long_break = 15 * 60     # 15 minutos
        
        # Estado do aplicativo
        self.time_left = self.pomodoro_time
        self.is_running = False
        self.current_mode = "Pomodoro"
        self.timer_thread = None
        
        # Estatísticas
        self.stats_file = "pomodoro_stats.json"
        self.load_stats()
        
        # Configurar interface
        self.setup_ui()
        self.update_display()
        
    def load_stats(self):
        """Carrega estatísticas do arquivo"""
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        else:
            self.stats = {
                'total_pomodoros': 0,
                'total_time': 0,
                'sessions_today': 0,
                'daily_history': {},
                'tasks': []
            }
    
    def save_stats(self):
        """Salva estatísticas no arquivo"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=4)
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#667eea")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🍅 Pomodoro Productivity Tracker",
            font=("Helvetica", 24, "bold"),
            bg="#667eea",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Aba Timer
        self.timer_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.timer_tab, text="⏱️ Timer")
        self.setup_timer_tab()
        
        # Aba Estatísticas
        self.stats_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.stats_tab, text="📊 Estatísticas")
        self.setup_stats_tab()
        
        # Aba Tarefas
        self.tasks_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.tasks_tab, text="📝 Tarefas")
        self.setup_tasks_tab()
    
    def setup_timer_tab(self):
        """Configura a aba do timer"""
        # Frame do timer
        timer_frame = tk.Frame(self.timer_tab, bg="white")
        timer_frame.pack(expand=True)
        
        # Label do modo
        self.mode_label = tk.Label(
            timer_frame,
            text=self.current_mode,
            font=("Helvetica", 18),
            bg="white",
            fg="#666"
        )
        self.mode_label.pack(pady=20)
        
        # Display do timer
        self.timer_label = tk.Label(
            timer_frame,
            text="25:00",
            font=("Courier", 72, "bold"),
            bg="white",
            fg="#667eea"
        )
        self.timer_label.pack(pady=30)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(
            timer_frame,
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=20)
        
        # Botões de controle
        button_frame = tk.Frame(timer_frame, bg="white")
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶️ Iniciar",
            command=self.start_timer,
            font=("Helvetica", 14, "bold"),
            bg="#10b981",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = tk.Button(
            button_frame,
            text="⏸️ Pausar",
            command=self.pause_timer,
            font=("Helvetica", 14, "bold"),
            bg="#f59e0b",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="🔄 Resetar",
            command=self.reset_timer,
            font=("Helvetica", 14, "bold"),
            bg="#ef4444",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.reset_button.grid(row=0, column=2, padx=5)
        
        # Botões de modo
        mode_frame = tk.Frame(timer_frame, bg="white")
        mode_frame.pack(pady=20)
        
        tk.Button(
            mode_frame,
            text="Pomodoro (25min)",
            command=lambda: self.set_mode("Pomodoro"),
            font=("Helvetica", 11),
            bg="#8b5cf6",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).grid(row=0, column=0, padx=5)
        
        tk.Button(
            mode_frame,
            text="Pausa Curta (5min)",
            command=lambda: self.set_mode("Pausa Curta"),
            font=("Helvetica", 11),
            bg="#8b5cf6",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).grid(row=0, column=1, padx=5)
        
        tk.Button(
            mode_frame,
            text="Pausa Longa (15min)",
            command=lambda: self.set_mode("Pausa Longa"),
            font=("Helvetica", 11),
            bg="#8b5cf6",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        ).grid(row=0, column=2, padx=5)
    
    def setup_stats_tab(self):
        """Configura a aba de estatísticas"""
        # Frame de estatísticas
        stats_frame = tk.Frame(self.stats_tab, bg="white")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            stats_frame,
            text="📊 Suas Estatísticas",
            font=("Helvetica", 20, "bold"),
            bg="white"
        ).pack(pady=10)
        
        # Grid de estatísticas
        stats_grid = tk.Frame(stats_frame, bg="white")
        stats_grid.pack(pady=20)
        
        # Cards de estatísticas
        self.create_stat_card(stats_grid, "Total de Pomodoros", 
                            str(self.stats['total_pomodoros']), 0, 0)
        self.create_stat_card(stats_grid, "Tempo Total (min)", 
                            str(self.stats['total_time'] // 60), 0, 1)
        self.create_stat_card(stats_grid, "Sessões Hoje", 
                            str(self.stats['sessions_today']), 1, 0)
        self.create_stat_card(stats_grid, "Média Diária", 
                            self.calculate_daily_average(), 1, 1)
        
        # Frame do gráfico
        graph_frame = tk.Frame(stats_frame, bg="white")
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Criar gráfico
        self.create_chart(graph_frame)
    
    def create_stat_card(self, parent, label, value, row, col):
        """Cria um card de estatística"""
        card = tk.Frame(parent, bg="#667eea", relief=tk.RAISED, borderwidth=2)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        tk.Label(
            card,
            text=value,
            font=("Helvetica", 36, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(pady=10)
        
        tk.Label(
            card,
            text=label,
            font=("Helvetica", 12),
            bg="#667eea",
            fg="white"
        ).pack(pady=5)
        
        # Configurar peso das colunas
        parent.grid_columnconfigure(col, weight=1)
    
    def create_chart(self, parent):
        """Cria o gráfico de histórico"""
        # Preparar dados
        dates = []
        pomodoros = []
        
        # Últimos 7 dias
        for i in range(6, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            dates.append((datetime.now() - timedelta(days=i)).strftime("%d/%m"))
            pomodoros.append(self.stats['daily_history'].get(date, 0))
        
        # Criar figura
        fig = Figure(figsize=(7, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plotar gráfico de barras
        bars = ax.bar(dates, pomodoros, color='#667eea', alpha=0.8)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Data', fontsize=10)
        ax.set_ylabel('Pomodoros', fontsize=10)
        ax.set_title('Histórico dos Últimos 7 Dias', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Integrar com tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_tasks_tab(self):
        """Configura a aba de tarefas"""
        tasks_frame = tk.Frame(self.tasks_tab, bg="white")
        tasks_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            tasks_frame,
            text="📝 Gerenciar Tarefas",
            font=("Helvetica", 20, "bold"),
            bg="white"
        ).pack(pady=10)
        
        # Frame de entrada
        input_frame = tk.Frame(tasks_frame, bg="white")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.task_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            relief=tk.SOLID,
            borderwidth=1
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        tk.Button(
            input_frame,
            text="➕ Adicionar Tarefa",
            command=self.add_task,
            font=("Helvetica", 11, "bold"),
            bg="#667eea",
            fg="white",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.RIGHT)
        
        # Frame da lista de tarefas
        list_frame = tk.Frame(tasks_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.tasks_listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 12),
            yscrollcommand=scrollbar.set,
            relief=tk.SOLID,
            borderwidth=1,
            selectmode=tk.SINGLE
        )
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)
        
        # Botões de ação
        action_frame = tk.Frame(tasks_frame, bg="white")
        action_frame.pack(pady=10)
        
        tk.Button(
            action_frame,
            text="✓ Completar",
            command=self.complete_task,
            font=("Helvetica", 11),
            bg="#10b981",
            fg="white",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            action_frame,
            text="🗑️ Remover",
            command=self.remove_task,
            font=("Helvetica", 11),
            bg="#ef4444",
            fg="white",
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Carregar tarefas
        self.load_tasks()
    
    def add_task(self):
        """Adiciona uma nova tarefa"""
        task = self.task_entry.get().strip()
        if task:
            self.stats['tasks'].append({
                'text': task,
                'completed': False,
                'created_at': datetime.now().isoformat()
            })
            self.save_stats()
            self.load_tasks()
            self.task_entry.delete(0, tk.END)
    
    def complete_task(self):
        """Marca uma tarefa como completa"""
        selection = self.tasks_listbox.curselection()
        if selection:
            idx = selection[0]
            self.stats['tasks'][idx]['completed'] = True
            self.save_stats()
            self.load_tasks()
    
    def remove_task(self):
        """Remove uma tarefa"""
        selection = self.tasks_listbox.curselection()
        if selection:
            idx = selection[0]
            del self.stats['tasks'][idx]
            self.save_stats()
            self.load_tasks()
    
    def load_tasks(self):
        """Carrega as tarefas na listbox"""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.stats['tasks']:
            status = "✓" if task['completed'] else "○"
            text = task['text']
            if task['completed']:
                text = f"[COMPLETA] {text}"
            self.tasks_listbox.insert(tk.END, f"{status} {text}")
            
            if task['completed']:
                self.tasks_listbox.itemconfig(tk.END, fg='gray')
    
    def set_mode(self, mode):
        """Define o modo do timer"""
        if not self.is_running:
            self.current_mode = mode
            if mode == "Pomodoro":
                self.time_left = self.pomodoro_time
            elif mode == "Pausa Curta":
                self.time_left = self.short_break
            else:  # Pausa Longa
                self.time_left = self.long_break
            self.update_display()
    
    def start_timer(self):
        """Inicia o timer"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def pause_timer(self):
        """Pausa o timer"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
    
    def reset_timer(self):
        """Reseta o timer"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.set_mode(self.current_mode)
    
    def run_timer(self):
        """Executa o timer em thread separada"""
        while self.is_running and self.time_left > 0:
            time.sleep(1)
            self.time_left -= 1
            self.root.after(0, self.update_display)
        
        if self.time_left == 0:
            self.root.after(0, self.timer_finished)
    
    def timer_finished(self):
        """Chamado quando o timer termina"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        
        # Atualizar estatísticas se foi um Pomodoro
        if self.current_mode == "Pomodoro":
            self.stats['total_pomodoros'] += 1
            self.stats['total_time'] += 25
            self.stats['sessions_today'] += 1
            
            # Atualizar histórico diário
            today = datetime.now().strftime("%Y-%m-%d")
            if today not in self.stats['daily_history']:
                self.stats['daily_history'][today] = 0
            self.stats['daily_history'][today] += 1
            
            self.save_stats()
            
            # Atualizar aba de estatísticas
            if hasattr(self, 'stats_tab'):
                self.setup_stats_tab()
        
        # Notificação
        messagebox.showinfo(
            "🍅 Pomodoro Timer",
            f"{self.current_mode} concluído!\n\nBom trabalho! 🎉"
        )
        
        # Sugerir próximo modo
        if self.current_mode == "Pomodoro":
            if self.stats['total_pomodoros'] % 4 == 0:
                self.set_mode("Pausa Longa")
            else:
                self.set_mode("Pausa Curta")
        else:
            self.set_mode("Pomodoro")
    
    def update_display(self):
        """Atualiza o display do timer"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)
        self.mode_label.config(text=self.current_mode)
        
        # Atualizar barra de progresso
        if self.current_mode == "Pomodoro":
            total = self.pomodoro_time
        elif self.current_mode == "Pausa Curta":
            total = self.short_break
        else:
            total = self.long_break
        
        progress = ((total - self.time_left) / total) * 100
        self.progress['value'] = progress
        
        # Atualizar título da janela
        self.root.title(f"🍅 Pomodoro - {time_str}")
    
    def calculate_daily_average(self):
        """Calcula a média diária de pomodoros"""
        if not self.stats['daily_history']:
            return "0"
        
        total = sum(self.stats['daily_history'].values())
        days = len(self.stats['daily_history'])
        avg = total / days if days > 0 else 0
        return f"{avg:.1f}"
    
    def on_closing(self):
        """Chamado ao fechar a aplicação"""
        # Resetar sessões do dia à meia-noite
        today = datetime.now().strftime("%Y-%m-%d")
        if hasattr(self, 'last_reset_date') and self.last_reset_date != today:
            self.stats['sessions_today'] = 0
        
        self.save_stats()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = PomodoroTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
