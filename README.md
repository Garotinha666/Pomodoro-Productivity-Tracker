# 🍅 Pomodoro Productivity Tracker

Timer Pomodoro completo com estatísticas e gráficos em Python!

## 🌟 Funcionalidades

- ⏱️ **Timer Pomodoro** com modos:
  - Pomodoro: 25 minutos de foco
  - Pausa Curta: 5 minutos de descanso
  - Pausa Longa: 15 minutos de descanso

- 📊 **Estatísticas Detalhadas**:
  - Total de pomodoros completados
  - Tempo total de foco
  - Sessões realizadas hoje
  - Média diária de pomodoros
  - Gráfico de histórico dos últimos 7 dias

- 📝 **Gerenciador de Tarefas**:
  - Adicione tarefas do que precisa fazer
  - Marque tarefas como completas
  - Remova tarefas concluídas

- 💾 **Persistência de Dados**:
  - Todas as estatísticas são salvas automaticamente
  - Histórico completo de sessões
  - Dados salvos em formato JSON

## 📦 Instalação

### 1. Certifique-se de ter Python 3.11 instalado

```bash
python --version
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install matplotlib
```

## 🚀 Como Executar

### No terminal:

```bash
python pomodoro_tracker.py
```

### No Windows (duplo clique):
- Simplesmente dê duplo clique no arquivo `pomodoro_tracker.py`

## 📖 Como Usar

### Timer
1. Escolha o modo (Pomodoro, Pausa Curta ou Pausa Longa)
2. Clique em "▶️ Iniciar" para começar
3. Use "⏸️ Pausar" para pausar
4. Use "🔄 Resetar" para reiniciar o timer

### Estatísticas
- Visualize suas estatísticas na aba "📊 Estatísticas"
- Veja o gráfico de progresso dos últimos 7 dias
- Acompanhe seu desempenho diário

### Tarefas
1. Digite a tarefa no campo de texto
2. Pressione Enter ou clique em "➕ Adicionar Tarefa"
3. Selecione uma tarefa e clique em "✓ Completar" para marcá-la
4. Clique em "🗑️ Remover" para deletar tarefas

## 🎯 Técnica Pomodoro

A técnica Pomodoro consiste em:

1. **25 minutos de foco** (1 Pomodoro)
2. **5 minutos de pausa curta**
3. Após 4 Pomodoros: **15 minutos de pausa longa**

### Benefícios:
- ✅ Melhora o foco e concentração
- ✅ Reduz o cansaço mental
- ✅ Aumenta a produtividade
- ✅ Ajuda a gerenciar o tempo

## 📂 Arquivos Gerados

O aplicativo cria automaticamente:

- `pomodoro_stats.json` - Arquivo com todas as estatísticas e dados

## 🎨 Recursos

- Interface gráfica moderna e intuitiva
- Notificações quando o timer termina
- Sugestão automática do próximo modo
- Barra de progresso visual
- Gráficos interativos de progresso

## 🔧 Requisitos do Sistema

- Python 3.11
- Tkinter (geralmente vem com Python)
- Matplotlib

## 💡 Dicas

1. **Foco total**: Durante o Pomodoro, evite todas as distrações
2. **Pausas reais**: Use as pausas para se afastar do trabalho
3. **Planeje**: Use a lista de tarefas para organizar o que fazer
4. **Consistência**: Tente fazer pelo menos 4 Pomodoros por dia
5. **Acompanhe**: Use as estatísticas para melhorar sua produtividade

## 🐛 Solução de Problemas

### Erro ao importar matplotlib:
```bash
pip install --upgrade matplotlib
```

### Erro ao importar tkinter (Linux):
```bash
sudo apt-get install python3-tk
```

### Erro ao importar tkinter (Mac):
```bash
brew install python-tk
```

## 📝 Licença

Este projeto é de código aberto e está disponível para uso livre.

## 🤝 Contribuições

Sugestões e melhorias são sempre bem-vindas!

---

**Desenvolvido com ❤️ para aumentar sua produtividade!** 🚀
