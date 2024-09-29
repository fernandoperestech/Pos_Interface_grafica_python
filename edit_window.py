from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton, QMessageBox, QHBoxLayout

class EditWindow(QWidget):
    def __init__(self, db, imovel_id):
        super().__init__()
        self.db = db
        self.imovel_id = imovel_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        imovel = self.db.obter_imovel_por_id(self.imovel_id)

        # Tipo de negociação
        self.tipo_negociacao = QComboBox()
        self.tipo_negociacao.addItems(["Venda", "Locação", "Venda/Locação"])
        self.tipo_negociacao.setCurrentText(imovel[1])
        layout.addWidget(QLabel("Tipo de Negociação:"))
        layout.addWidget(self.tipo_negociacao)

        # Status
        self.status = QComboBox()
        self.status.addItems(["Disponível", "Locado", "Vendido", "À liberar"])
        self.status.setCurrentText(imovel[2])
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status)

        # Endereço
        self.endereco = QLineEdit(imovel[3])
        layout.addWidget(QLabel("Endereço:"))
        layout.addWidget(self.endereco)

        # Descrição curta
        self.descricao_curta = QLineEdit(imovel[4])
        layout.addWidget(QLabel("Descrição Curta:"))
        layout.addWidget(self.descricao_curta)

        # Tipo de imóvel
        self.tipo_imovel = QComboBox()
        self.tipo_imovel.addItems(["Apartamento", "Casa", "Terreno"])
        self.tipo_imovel.setCurrentText(imovel[5])
        layout.addWidget(QLabel("Tipo de Imóvel:"))
        layout.addWidget(self.tipo_imovel)

        # Características
        self.caracteristicas = QTextEdit(imovel[6])
        layout.addWidget(QLabel("Características:"))
        layout.addWidget(self.caracteristicas)

        # Preço
        self.preco = QLineEdit(str(imovel[7]))
        layout.addWidget(QLabel("Preço:"))
        layout.addWidget(self.preco)

        # Condições
        self.condicoes = QTextEdit(imovel[8])
        layout.addWidget(QLabel("Condições:"))
        layout.addWidget(self.condicoes)

        # Observações
        self.observacoes = QTextEdit(imovel[9])
        layout.addWidget(QLabel("Observações:"))
        layout.addWidget(self.observacoes)

        # Botões de salvar e cancelar
        button_layout = QHBoxLayout()
        self.salvar_btn = QPushButton("Salvar")
        self.salvar_btn.clicked.connect(self.salvar_dados)
        button_layout.addWidget(self.salvar_btn)

        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.clicked.connect(self.close)
        button_layout.addWidget(self.cancelar_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setWindowTitle('Editar Imóvel')

    def salvar_dados(self):
        try:
            self.db.atualizar_imovel(
                self.imovel_id,
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
            QMessageBox.information(self, "Sucesso", "Dados atualizados com sucesso!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar dados: {e}")
