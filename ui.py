import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtCore import Qt
from database import Database
from edit_window import EditWindow

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Layout para centralizar os botões
        button_layout = QHBoxLayout()

        self.cadastro_btn = QPushButton("Cadastrar Imóvel")
        self.cadastro_btn.clicked.connect(self.abrir_cadastro)
        self.cadastro_btn.setFixedWidth(self.width() // 3)
        button_layout.addWidget(self.cadastro_btn, alignment=Qt.AlignCenter)

        self.listar_btn = QPushButton("Listar Imóveis")
        self.listar_btn.clicked.connect(self.abrir_listagem)
        self.listar_btn.setFixedWidth(self.width() // 3)
        button_layout.addWidget(self.listar_btn, alignment=Qt.AlignCenter)

        self.fechar_btn = QPushButton("Fechar Aplicação")
        self.fechar_btn.clicked.connect(self.fechar_aplicacao)
        self.fechar_btn.setFixedWidth(self.width() // 3)
        button_layout.addWidget(self.fechar_btn, alignment=Qt.AlignCenter)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Sistema de Imóveis')
        
        # Configurar tamanho da tela inicial
        self.resize(800, 600)
        
        # Centralizar a janela na tela
        self.center()

        self.show()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def abrir_cadastro(self):
        self.cadastro_window = CadastroWindow()
        self.cadastro_window.show()

    def abrir_listagem(self):
        self.listagem_window = ListagemWindow()
        self.listagem_window.show()

    def fechar_aplicacao(self):
        QApplication.instance().quit()

class CadastroWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Tipo de negociação
        self.tipo_negociacao = QComboBox()
        self.tipo_negociacao.addItems(["Venda", "Locação", "Venda/Locação"])
        layout.addWidget(QLabel("Tipo de Negociação:"))
        layout.addWidget(self.tipo_negociacao)

        # Status
        self.status = QComboBox()
        self.status.addItems(["Disponível", "Locado", "Vendido", "À liberar"])
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status)

        # Endereço
        self.endereco = QLineEdit()
        layout.addWidget(QLabel("Endereço:"))
        layout.addWidget(self.endereco)

        # Descrição curta
        self.descricao_curta = QLineEdit()
        layout.addWidget(QLabel("Descrição Curta:"))
        layout.addWidget(self.descricao_curta)

        # Tipo de imóvel
        self.tipo_imovel = QComboBox()
        self.tipo_imovel.addItems(["Apartamento", "Casa", "Terreno"])
        layout.addWidget(QLabel("Tipo de Imóvel:"))
        layout.addWidget(self.tipo_imovel)

        # Características
        self.caracteristicas = QTextEdit()
        layout.addWidget(QLabel("Características:"))
        layout.addWidget(self.caracteristicas)

        # Preço
        self.preco = QLineEdit()
        layout.addWidget(QLabel("Preço:"))
        layout.addWidget(self.preco)

        # Condições
        self.condicoes = QTextEdit()
        layout.addWidget(QLabel("Condições:"))
        layout.addWidget(self.condicoes)

        # Observações
        self.observacoes = QTextEdit()
        layout.addWidget(QLabel("Observações:"))
        layout.addWidget(self.observacoes)

        # Botão de salvar
        self.salvar_btn = QPushButton("Salvar")
        self.salvar_btn.clicked.connect(self.salvar_dados)
        layout.addWidget(self.salvar_btn)

        self.setLayout(layout)
        self.setWindowTitle('Cadastro de Imóveis')

    def salvar_dados(self):
        try:
            self.db.inserir_imovel(
                self.tipo_negociacao.currentText(),
                self.status.currentText(),
                self.endereco.text(),
                self.descricao_curta.text(),
                self.tipo_imovel.currentText(),
                self.caracteristicas.toPlainText(),
                float(self.preco.text()),
                self.condicoes.toPlainText(),
                self.observacoes.toPlainText()
            )
            QMessageBox.information(self, "Sucesso", "Dados salvos com sucesso!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar dados: {e}")

class ListagemWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["ID", "Tipo Negociação", "Status", "Endereço", "Descrição Curta", "Tipo Imóvel", "Características", "Preço", "Condições", "Observações"])
        self.load_data()

        self.table.cellClicked.connect(self.habilitar_edicao)
        layout.addWidget(self.table)

        self.editar_btn = QPushButton("Editar Imóvel")
        self.editar_btn.setEnabled(False)
        self.editar_btn.clicked.connect(self.editar_imovel)
        layout.addWidget(self.editar_btn)

        self.setLayout(layout)
        self.setWindowTitle('Lista de Imóveis')
        
        # Configurar tamanho da tela de listagem
        self.resize(800, 600)
        
        # Centralizar a janela na tela
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_data(self):
        imoveis = self.db.obter_imoveis()
        self.table.setRowCount(len(imoveis))
        for row_idx, imovel in enumerate(imoveis):
            for col_idx, data in enumerate(imovel):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def habilitar_edicao(self, row, column):
        self.selected_row = row
        self.editar_btn.setEnabled(True)

    def editar_imovel(self):
        imovel_id = int(self.table.item(self.selected_row, 0).text())
        self.edit_window = EditWindow(self.db, imovel_id)
        self.edit_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(app.exec_())
