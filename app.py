from flask import Flask, jsonify, request, render_template

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = '1234567'  # Puedes cambiarlo si quieres

# Configura la conexión a PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/DispensarioMedicoApec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Modelo de ejemplo
class TipoFarmaco(db.Model):
    __tablename__ = 'tipos_farmacos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)
# Modelo: Marca
class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    estado = db.Column(db.Boolean, default=True)

# Modelo: Ubicacion
class Ubicacion(db.Model):
    __tablename__ = 'ubicaciones'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    estante = db.Column(db.String(20))
    tramo = db.Column(db.String(20))
    celda = db.Column(db.String(20))
    estado = db.Column(db.Boolean, default=True)

# Modelo: Medicamento
class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    tipo_farmaco_id = db.Column(db.Integer, db.ForeignKey('tipos_farmacos.id'))
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'))
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'))
    dosis = db.Column(db.String(50))
    estado = db.Column(db.Boolean, default=True)

# Modelo: Paciente
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cedula = db.Column(db.String(20))
    carnet = db.Column(db.String(20))
    tipo_paciente = db.Column(db.String(20))  # Estudiante, Empleado, etc.
    estado = db.Column(db.Boolean, default=True)

# Modelo: Medico
class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    cedula = db.Column(db.String(20))
    tanda = db.Column(db.String(20))  # Matutina, Vespertina, etc.
    especialidad = db.Column(db.String(50))
    estado = db.Column(db.Boolean, default=True)

# Modelo: Visita
class Visita(db.Model):
    __tablename__ = 'visitas'
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'))
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'))
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    sintomas = db.Column(db.Text)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'))
    recomendaciones = db.Column(db.Text)
    estado = db.Column(db.Boolean, default=True)


# Modelo: Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    #password_hash = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tipos_farmacos')
def api_tipos_farmacos():
    tipos = TipoFarmaco.query.all()
    return jsonify([{"id": t.id, "descripcion": t.descripcion, "estado": t.estado} for t in tipos])


# MARCAS

@app.route('/marcas')
def marcas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    marcas = Marca.query.all()
    return render_template('marcas.html', marcas=marcas)

@app.route('/marcas/crear', methods=['POST'])
def crear_marca():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    descripcion = request.form['descripcion']
    nueva = Marca(descripcion=descripcion, estado=True)
    db.session.add(nueva)
    db.session.commit()
    flash('Marca creada correctamente.')
    return redirect(url_for('marcas'))

@app.route('/marcas/eliminar/<int:id>')
def eliminar_marca(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    marca = Marca.query.get_or_404(id)
    marca.estado = False
    db.session.commit()
    flash('Marca eliminada.')
    return redirect(url_for('marcas'))

@app.route('/marcas/editar/<int:id>')
def editar_marca(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    marca = Marca.query.get_or_404(id)
    return render_template('editar_marca.html', marca=marca)

@app.route('/marcas/actualizar/<int:id>', methods=['POST'])
def actualizar_marca(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    marca = Marca.query.get_or_404(id)
    marca.descripcion = request.form['descripcion']
    db.session.commit()
    flash('Marca actualizada correctamente.')
    return redirect(url_for('marcas'))



# UBICACIONES
@app.route('/ubicaciones')
def listar_ubicaciones():
    ubicaciones = Ubicacion.query.all()
    return jsonify([{
        "id": u.id,
        "descripcion": u.descripcion,
        "estante": u.estante,
        "tramo": u.tramo,
        "celda": u.celda,
        "estado": u.estado
    } for u in ubicaciones])


# UBICACIONES - GESTIÓN COMPLETA
@app.route('/ubicaciones')
def ubicaciones():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    ubicaciones = Ubicacion.query.all()
    return render_template('ubicaciones.html', ubicaciones=ubicaciones)

@app.route('/ubicaciones/crear', methods=['POST'])
def crear_ubicacion():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    descripcion = request.form['descripcion']
    estante = request.form['estante']
    tramo = request.form['tramo']
    celda = request.form['celda']
    nueva = Ubicacion(descripcion=descripcion, estante=estante, tramo=tramo, celda=celda, estado=True)
    db.session.add(nueva)
    db.session.commit()
    flash('Ubicación creada correctamente.')
    return redirect(url_for('ubicaciones'))

@app.route('/ubicaciones/eliminar/<int:id>')
def eliminar_ubicacion(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    ubicacion = Ubicacion.query.get_or_404(id)
    ubicacion.estado = False
    db.session.commit()
    flash('Ubicación eliminada.')
    return redirect(url_for('ubicaciones'))

@app.route('/ubicaciones/editar/<int:id>')
def editar_ubicacion(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    ubicacion = Ubicacion.query.get_or_404(id)
    return render_template('editar_ubicacion.html', ubicacion=ubicacion)

@app.route('/ubicaciones/actualizar/<int:id>', methods=['POST'])
def actualizar_ubicacion(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    ubicacion = Ubicacion.query.get_or_404(id)
    ubicacion.descripcion = request.form['descripcion']
    ubicacion.estante = request.form['estante']
    ubicacion.tramo = request.form['tramo']
    ubicacion.celda = request.form['celda']
    db.session.commit()
    flash('Ubicación actualizada correctamente.')
    return redirect(url_for('ubicaciones'))


# MEDICAMENTOS
@app.route('/medicamentos')
def listar_medicamentos():
    medicamentos = Medicamento.query.all()
    return jsonify([{
        "id": m.id,
        "descripcion": m.descripcion,
        "tipo_farmaco_id": m.tipo_farmaco_id,
        "marca_id": m.marca_id,
        "ubicacion_id": m.ubicacion_id,
        "dosis": m.dosis,
        "estado": m.estado
    } for m in medicamentos])

# PACIENTES
@app.route('/pacientes')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([{
        "id": p.id,
        "nombre": p.nombre,
        "cedula": p.cedula,
        "carnet": p.carnet,
        "tipo_paciente": p.tipo_paciente,
        "estado": p.estado
    } for p in pacientes])

@app.route('/form_paciente', methods=['GET'])
def form_paciente():
    return render_template('crear_paciente.html')


# MÉDICOS
@app.route('/medicos')
def listar_medicos():
    medicos = Medico.query.all()
    return jsonify([{
        "id": m.id,
        "nombre": m.nombre,
        "cedula": m.cedula,
        "tanda": m.tanda,
        "especialidad": m.especialidad,
        "estado": m.estado
    } for m in medicos])

# VISITAS
@app.route('/visitas')
def listar_visitas():
    visitas = Visita.query.all()
    return jsonify([{
        "id": v.id,
        "medico_id": v.medico_id,
        "paciente_id": v.paciente_id,
        "fecha": v.fecha.strftime('%Y-%m-%d'),
        "hora": v.hora.strftime('%H:%M'),
        "sintomas": v.sintomas,
        "medicamento_id": v.medicamento_id,
        "recomendaciones": v.recomendaciones,
        "estado": v.estado
    } for v in visitas])





@app.route('/crear_admin')
def crear_admin():
    if Usuario.query.filter_by(username='admin').first():
        return "Ya existe un usuario admin."

    nuevo = Usuario(username='admin')
    nuevo.set_password('admin123')  # Puedes cambiar esta contraseña
    db.session.add(nuevo)
    db.session.commit()
    return "Usuario admin creado correctamente."







@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    nuevo_paciente = Paciente(
        nombre=data['nombre'],
        cedula=data['cedula'],
        carnet=data['carnet'],
        tipo_paciente=data['tipo_paciente'],
        estado=True
    )
    db.session.add(nuevo_paciente)
    db.session.commit()

    if request.is_json:
        return jsonify({"mensaje": "Paciente creado exitosamente"}), 201
    else:
        return "Paciente registrado correctamente desde el formulario"

#login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['usuario'] = user.username
            return redirect(url_for('dashboard'))  # Redirige al panel
        else:
            return "Credenciales incorrectas. Intenta de nuevo."

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')  # o crea dashboard.html que extienda de base_dashboard





@app.route('/registro', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if Usuario.query.filter_by(username=username).first():
            return "Ese usuario ya existe."

        nuevo = Usuario(username=username)
        nuevo.set_password(password)
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registro_usuario.html')

from flask import flash

# Ver todos los tipos de fármacos
@app.route('/tipos_farmacos')
def tipos_farmacos():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    tipos = TipoFarmaco.query.all()
    return render_template('tipos_farmacos.html', tipos=tipos)
# Crear un nuevo tipo
@app.route('/tipos_farmacos/crear', methods=['POST'])
def crear_tipo_farmaco():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    descripcion = request.form['descripcion']
    nuevo_tipo = TipoFarmaco(descripcion=descripcion, estado=True)
    db.session.add(nuevo_tipo)
    db.session.commit()
    flash('Tipo de fármaco creado correctamente.')
    return redirect(url_for('tipos_farmacos'))

# Eliminar tipo (baja lógica)
@app.route('/tipos_farmacos/eliminar/<int:id>')
def eliminar_tipo_farmaco(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    tipo = TipoFarmaco.query.get_or_404(id)
    tipo.estado = False
    db.session.commit()
    flash('Tipo de fármaco eliminado.')
    return redirect(url_for('tipos_farmacos'))

# Editar tipo (mostrar form)
@app.route('/tipos_farmacos/editar/<int:id>')
def editar_tipo_farmaco(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    tipo = TipoFarmaco.query.get_or_404(id)
    return render_template('editar_tipo_farmaco.html', tipo=tipo)

# Guardar edición
@app.route('/tipos_farmacos/actualizar/<int:id>', methods=['POST'])
def actualizar_tipo_farmaco(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    tipo = TipoFarmaco.query.get_or_404(id)
    tipo.descripcion = request.form['descripcion']
    db.session.commit()
    flash('Tipo de fármaco actualizado.')
    return redirect(url_for('tipos_farmacos'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




