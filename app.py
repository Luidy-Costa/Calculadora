from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import sentry_sdk

from config import Config
from models import db, Equipamento, Emprestimo

# Inicialização do Sentry
if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        send_default_pii=True,
    )

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa o banco de dados com a aplicação
db.init_app(app)

with app.app_context():
    db.create_all()

# --- Rotas do Sistema ---

@app.route('/')
def index():
    """Painel principal com indicadores e últimos registros."""
    total_equipamentos = Equipamento.query.count()
    disponiveis = Equipamento.query.filter_by(status='disponivel').count()
    emprestados = Equipamento.query.filter_by(status='emprestado').count()
    manutencao = Equipamento.query.filter_by(status='manutencao').count()
    
    ultimos_emprestimos = Emprestimo.query.order_by(Emprestimo.data_emprestimo.desc()).limit(5).all()
    equipamentos_recentes = Equipamento.query.order_by(Equipamento.criado_em.desc()).limit(5).all()
    
    return render_template('index.html',
                           total=total_equipamentos,
                           disponiveis=disponiveis,
                           emprestados=emprestados,
                           manutencao=manutencao,
                           ultimos_emprestimos=ultimos_emprestimos,
                           equipamentos_recentes=equipamentos_recentes)

@app.route('/equipamentos')
def listar_equipamentos():
    """Listagem de equipamentos com filtro por status e tipo."""
    status_filter = request.args.get('status')
    tipo_filter = request.args.get('tipo')
    query = Equipamento.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if tipo_filter:
        query = query.filter_by(tipo=tipo_filter)
        
    equipamentos = query.order_by(Equipamento.patrimonio.asc()).all()
    tipos_existentes = [t[0] for t in db.session.query(Equipamento.tipo).distinct().all()]
    
    return render_template('equipamentos.html', 
                           equipamentos=equipamentos, 
                           status_filter=status_filter,
                           tipo_filter=tipo_filter,
                           tipos_existentes=tipos_existentes)

@app.route('/equipamentos/novo', methods=['GET', 'POST'])
def novo_equipamento():
    """Cadastra um novo equipamento."""
    if request.method == 'POST':
        patrimonio = request.form.get('patrimonio', '').strip().upper()
        tipo = request.form.get('tipo', '').strip()
        marca_modelo = request.form.get('marca_modelo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        
        if not patrimonio or not tipo or not marca_modelo:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('novo_equipamento.html')
            
        # Verifica se já existe equipamento com esse patrimônio
        existente = Equipamento.query.filter_by(patrimonio=patrimonio).first()
        if existente:
            flash(f'Já existe um equipamento cadastrado com o patrimônio {patrimonio}!', 'warning')
            return render_template('novo_equipamento.html')
            
        novo = Equipamento(
            patrimonio=patrimonio,
            tipo=tipo,
            marca_modelo=marca_modelo,
            descricao=descricao,
            status='disponivel'
        )
        db.session.add(novo)
        db.session.commit()
        
        flash(f'Equipamento {patrimonio} cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_equipamentos'))
        
    return render_template('novo_equipamento.html')

@app.route('/equipamentos/<int:id>')
def detalhe_equipamento(id):
    """Consulta detalhada do estado de um equipamento e seu histórico."""
    equipamento = Equipamento.query.get_or_404(id)
    return render_template('detalhe_equipamento.html', equipamento=equipamento)

@app.route('/equipamentos/<int:id>/status', methods=['POST'])
def alterar_status_equipamento(id):
    """Permite alterar o status para manutenção ou disponível (caso não esteja emprestado)."""
    equipamento = Equipamento.query.get_or_404(id)
    novo_status = request.form.get('status')
    
    if equipamento.status == 'emprestado':
        flash('Não é possível alterar o status de um equipamento que está atualmente emprestado. Registre a devolução primeiro.', 'warning')
        return redirect(url_for('detalhe_equipamento', id=id))
        
    if novo_status in ['disponivel', 'manutencao']:
        equipamento.status = novo_status
        db.session.commit()
        flash(f'Status do equipamento atualizado para "{novo_status}".', 'info')
        
    return redirect(url_for('detalhe_equipamento', id=id))

@app.route('/emprestimos')
def listar_emprestimos():
    """Lista todos os empréstimos registrados (ativos e devolvidos)."""
    status_filter = request.args.get('status', 'ativo')
    query = Emprestimo.query
    
    if status_filter in ['ativo', 'devolvido']:
        query = query.filter_by(status=status_filter)
        
    emprestimos = query.order_by(Emprestimo.data_emprestimo.desc()).all()
    return render_template('emprestimos.html', emprestimos=emprestimos, status_filter=status_filter)

@app.route('/emprestimos/novo', methods=['GET', 'POST'])
def novo_emprestimo():
    """Registra um novo empréstimo."""
    equipamento_id_param = request.args.get('equipamento_id', type=int)
    equipamentos_disponiveis = Equipamento.query.filter_by(status='disponivel').all()
    
    if request.method == 'POST':
        equipamento_id = request.form.get('equipamento_id', type=int)
        responsavel_nome = request.form.get('responsavel_nome', '').strip()
        responsavel_contato = request.form.get('responsavel_contato', '').strip()
        data_prevista_str = request.form.get('data_prevista_devolucao')
        observacoes = request.form.get('observacoes', '').strip()
        
        if not equipamento_id or not responsavel_nome:
            flash('Selecione o equipamento e informe o nome do responsável.', 'danger')
            return render_template('novo_emprestimo.html', 
                                   equipamentos=equipamentos_disponiveis, 
                                   equipamento_selecionado=equipamento_id_param)
                                   
        equipamento = Equipamento.query.get(equipamento_id)
        if not equipamento or equipamento.status != 'disponivel':
            flash('O equipamento selecionado não está disponível para empréstimo.', 'danger')
            return redirect(url_for('novo_emprestimo'))
            
        data_prevista = None
        if data_prevista_str:
            try:
                data_prevista = datetime.strptime(data_prevista_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        emprestimo = Emprestimo(
            equipamento_id=equipamento.id,
            responsavel_nome=responsavel_nome,
            responsavel_contato=responsavel_contato,
            data_prevista_devolucao=data_prevista,
            observacoes=observacoes,
            status='ativo'
        )
        
        equipamento.status = 'emprestado'
        
        db.session.add(emprestimo)
        db.session.commit()
        
        flash(f'Empréstimo do equipamento {equipamento.patrimonio} registrado para {responsavel_nome}!', 'success')
        return redirect(url_for('listar_emprestimos'))
        
    return render_template('novo_emprestimo.html', 
                           equipamentos=equipamentos_disponiveis, 
                           equipamento_selecionado=equipamento_id_param)

@app.route('/emprestimos/<int:id>/devolver', methods=['POST'])
def devolver_emprestimo(id):
    """Registra a devolução de um empréstimo."""
    emprestimo = Emprestimo.query.get_or_404(id)
    if emprestimo.status == 'devolvido':
        flash('Este empréstimo já foi finalizado anteriormente.', 'info')
        return redirect(url_for('listar_emprestimos'))
        
    emprestimo.status = 'devolvido'
    emprestimo.data_devolucao = datetime.utcnow()
    
    if emprestimo.equipamento:
        emprestimo.equipamento.status = 'disponivel'
        
    db.session.commit()
    flash(f'Devolução do equipamento {emprestimo.equipamento.patrimonio} concluída com sucesso!', 'success')
    return redirect(url_for('listar_emprestimos'))

# --- Captura de Erros Personalizada (404 e Exceções Gerais para o Sentry) ---

@app.errorhandler(404)
def not_found_error(error):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with sentry_sdk.push_scope() as scope:
        scope.fingerprint = [f"404-{request.path}-{agora}"]
        sentry_sdk.capture_exception(error)
    return render_template('404.html', error=error), 404

@app.errorhandler(Exception)
def handle_exception(error):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with sentry_sdk.push_scope() as scope:
        scope.fingerprint = [f"erro-{agora}-{type(error).__name__}"]
        sentry_sdk.capture_exception(error)
    status_code = getattr(error, 'code', 500)
    return render_template('erro.html', error=error, status_code=status_code), status_code

# --- Requisito Prático: Geração de Erro Proativo (Teste Sentry) ---
@app.route('/debug-sentry')
def trigger_error():
    """Endpoint dedicado exigido na Prática 02 para validação da telemetria no Sentry."""
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with sentry_sdk.push_scope() as scope:
        # Evita agrupamento no Sentry utilizando a data e hora atual no fingerprint
        scope.fingerprint = [f"debug-sentry-{agora}"]
        raise RuntimeError(f"Erro Proativo [{agora}]: Monitoramento Sentry e ChatOps validado com sucesso!")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
