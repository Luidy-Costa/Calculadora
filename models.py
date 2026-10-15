from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    patrimonio = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False) # Notebook, Monitor, Teclado, etc.
    marca_modelo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='disponivel') # 'disponivel', 'emprestado', 'manutencao'
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    emprestimos = db.relationship('Emprestimo', backref='equipamento', lazy=True, cascade="all, delete-orphan", order_by="desc(Emprestimo.data_emprestimo)")
    
    def __repr__(self):
        return f'<Equipamento {self.patrimonio} - {self.tipo} ({self.status})>'
    
    @property
    def emprestimo_ativo(self):
        for emp in self.emprestimos:
            if emp.status == 'ativo':
                return emp
        return None

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    
    id = db.Column(db.Integer, primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)
    responsavel_nome = db.Column(db.String(100), nullable=False)
    responsavel_contato = db.Column(db.String(100), nullable=True) # Email, telefone ou setor
    data_emprestimo = db.Column(db.DateTime, default=datetime.utcnow)
    data_prevista_devolucao = db.Column(db.Date, nullable=True)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='ativo') # 'ativo', 'devolvido'
    observacoes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Emprestimo #{self.id} - Equipamento {self.equipamento_id} para {self.responsavel_nome}>'
