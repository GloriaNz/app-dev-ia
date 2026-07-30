import os
from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Module, Lesson, UserProgress

def register_routes(app):

    @app.route('/')
    def index():
        modules = Module.query.order_by(Module.order).all()
        return render_template('index.html', modules=modules)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')

            if not username or not email or not password:
                flash("Veuillez remplir tous les champs du formulaire.", "danger")
                return render_template('register.html')

            if User.query.filter((User.username == username) | (User.email == email)).first():
                flash("Cet nom d'utilisateur ou cette adresse email est déjà utilisé.", "warning")
                return render_template('register.html')

            user = User(username=username, email=email, role='student', has_premium_access=False)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash("Bienvenue ! Votre compte a été créé avec succès. Vous avez accès au Module 1 (Gratuit).", "success")
            return redirect(url_for('dashboard'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')

            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash(f"Ravi de vous revoir, {user.username} !", "info")
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash("Identifiants incorrects. Veuillez vérifier votre email et mot de passe.", "danger")

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("Vous avez été déconnecté avec succès.", "success")
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        modules = Module.query.order_by(Module.order).all()
        overall_progress = current_user.get_progress_percentage()

        # Construire les données de progression par module
        module_data = []
        for m in modules:
            progress_pct = current_user.get_module_progress(m.id)
            is_accessible = m.is_free or current_user.has_premium_access
            module_data.append({
                'module': m,
                'progress_pct': progress_pct,
                'is_accessible': is_accessible,
                'lessons_count': len(m.lessons)
            })

        return render_template('dashboard.html', 
                               overall_progress=overall_progress, 
                               module_data=module_data)

    @app.route('/lessons/<int:lesson_id>')
    @login_required
    def view_lesson(lesson_id):
        lesson = Lesson.query.get_or_404(lesson_id)
        module = lesson.module

        # Restrict Access Paywall Verification
        if not module.is_free and not current_user.has_premium_access:
            flash("Cette leçon appartient à un module Premium. Réservez votre accès complet pour débloquer cette leçon !", "warning")
            return redirect(url_for('paywall', required_lesson_id=lesson.id))

        # Navigations (Précédente / Suivante)
        all_lessons = Lesson.query.join(Module).order_by(Module.order, Lesson.order).all()
        current_index = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), None)
        
        prev_lesson = all_lessons[current_index - 1] if current_index is not None and current_index > 0 else None
        next_lesson = all_lessons[current_index + 1] if current_index is not None and current_index < len(all_lessons) - 1 else None

        is_completed = current_user.has_completed_lesson(lesson.id)
        all_modules = Module.query.order_by(Module.order).all()

        return render_template('lesson.html', 
                               lesson=lesson, 
                               module=module, 
                               is_completed=is_completed,
                               prev_lesson=prev_lesson,
                               next_lesson=next_lesson,
                               all_modules=all_modules)

    @app.route('/api/lessons/<int:lesson_id>/toggle-complete', methods=['POST'])
    @login_required
    def toggle_lesson_complete(lesson_id):
        lesson = Lesson.query.get_or_404(lesson_id)
        
        # Sécurité : Vérification de l'accès paywall
        if not lesson.module.is_free and not current_user.has_premium_access:
            return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403

        progress = UserProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()

        if progress:
            progress.completed = not progress.completed
        else:
            progress = UserProgress(user_id=current_user.id, lesson_id=lesson.id, completed=True)
            db.session.add(progress)

        db.session.commit()

        overall_pct = current_user.get_progress_percentage()
        module_pct = current_user.get_module_progress(lesson.module_id)

        return jsonify({
            'success': True,
            'completed': progress.completed,
            'overall_progress': overall_pct,
            'module_progress': module_pct,
            'message': 'Statut de la leçon mis à jour !'
        })

    @app.route('/paywall')
    @login_required
    def paywall():
        if current_user.has_premium_access:
            flash("Vous bénéficiez déjà de l'accès Premium Illimité !", "info")
            return redirect(url_for('dashboard'))

        required_lesson_id = request.args.get('required_lesson_id')
        modules = Module.query.order_by(Module.order).all()
        return render_template('paywall.html', modules=modules, required_lesson_id=required_lesson_id)

    @app.route('/api/pay-mock', methods=['POST'])
    @login_required
    def pay_mock():
        """Endpoint de simulation de paiement Stripe / Webhook de validation de commande."""
        current_user.has_premium_access = True
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Paiement simulé avec succès ! Votre compte dispose maintenant de l\'accès Premium complet.',
            'redirect_url': url_for('dashboard')
        })

    @app.route('/download/<filename>')
    @login_required
    def download_file(filename):
        uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
        file_path = os.path.join(uploads_dir, filename)
        
        # Générer un PDF factice s'il n'existe pas encore pour les tests
        if not os.path.exists(file_path):
            os.makedirs(uploads_dir, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Support de cours - Formation Développeur IA & Data\nDocument : {filename}\nContenu d'apprentissage certifié.")

        return send_from_directory(uploads_dir, filename, as_attachment=True)
