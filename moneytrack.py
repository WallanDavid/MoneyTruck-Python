import tkinter as tk
from tkinter import messagebox

class Despesa:
    def __init__(self, categoria, valor, data, nota=""):
        self.categoria = categoria
        self.valor = valor
        self.data = data
        self.nota = nota

class FinancasAppGUI:
    def __init__(self, master):
        self.master = master
        master.title("MoneyTrack - Rastreamento de Despesas")

        # Criando a lista de despesas
        self.lista_despesas = tk.Listbox(master, width=70)
        self.lista_despesas.pack(padx=10, pady=10)

        # Criando os botões
        self.adicionar_despesa_button = self.create_button("Adicionar Despesa", self.adicionar_despesa)
        self.mostrar_despesas_button = self.create_button("Mostrar Despesas", self.mostrar_despesas)
        self.calcular_total_button = self.create_button("Calcular Total de Despesas", self.calcular_total_despesas)
        self.sair_button = self.create_button("Sair", master.quit)

        # Instanciando a aplicação
        self.app = FinancasApp()

    def create_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command)
        button.pack(side=tk.LEFT, padx=5, pady=5)
        return button

    def adicionar_despesa(self):
        adicionar_despesa_window = tk.Toplevel(self.master)
        adicionar_despesa_window.title("Adicionar Despesa")

        # Criando os campos de entrada
        fields = ["Categoria", "Valor (R$)", "Data (DD/MM/AAAA)", "Nota"]
        self.entries = self.create_entry_fields(adicionar_despesa_window, fields)

        # Criando o botão de adicionar
        adicionar_button = self.create_button("Adicionar", self.adicionar_despesa_ao_app)

    def create_entry_fields(self, master, fields):
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(master, text=field + ":").grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(master)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field] = entry
        return entries

    def adicionar_despesa_ao_app(self):
        despesa_info = {key: entry.get() for key, entry in self.entries.items()}
        self.app.adicionar_despesa(**despesa_info)
        self.update_despesa_list()
        self.clear_entry_fields()

    def update_despesa_list(self):
        self.lista_despesas.delete(0, tk.END)
        for despesa in self.app.despesas:
            self.lista_despesas.insert(tk.END, f"{despesa.categoria}: R${despesa.valor} ({despesa.data}) - {despesa.nota}")

    def clear_entry_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def mostrar_despesas(self):
        mostrar_despesas_window = tk.Toplevel(self.master)
        mostrar_despesas_window.title("Despesas Registradas")

        # Adicionando barra de rolagem
        scrollbar = tk.Scrollbar(mostrar_despesas_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Criando área de texto para exibir despesas
        text_area = tk.Text(mostrar_despesas_window, yscrollcommand=scrollbar.set)
        text_area.pack(expand=True, fill=tk.BOTH)

        # Adicionando as despesas à área de texto
        for despesa in self.app.despesas:
            text_area.insert(tk.END, f"{despesa.categoria}: R${despesa.valor} ({despesa.data}) - {despesa.nota}\n")

        # Configurando a barra de rolagem para a área de texto
        scrollbar.config(command=text_area.yview)

    def calcular_total_despesas(self):
        total = sum(despesa.valor for despesa in self.app.despesas)
        messagebox.showinfo("Total de Despesas", f"O total de despesas é R${total:.2f}")

class FinancasApp:
    def __init__(self):
        self.despesas = []

    def adicionar_despesa(self, categoria, valor, data, nota=""):
        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "Valor da despesa inválido. Por favor, insira um número.")
            return

        self.despesas.append(Despesa(categoria, valor, data, nota))

def main():
    root = tk.Tk()
    app = FinancasAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
