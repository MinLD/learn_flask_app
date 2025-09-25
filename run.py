# run.py

from app import create_app
import os
import click
from app.extensions import db
from app.models.auth_model import Role,User
app = create_app()


# run `flask seed --with-admin` to create an admin user and roles
@app.cli.command("seed")
@click.option('--with-admin', is_flag=True, help='Create an admin user.')
def seed(with_admin):
    """
    Gieo mầm dữ liệu ban đầu cho database: tạo roles và tài khoản admin (tùy chọn).
    """
    # --- 1. TẠO ROLES ---
    roles_to_create = {
        'admin': 'Administrator with all permissions',
        'user': 'Regular user with limited permissions'
    }
    roles_created_count = 0
    for role_name, role_desc in roles_to_create.items():
        if not Role.query.filter_by(name=role_name).first():
            new_role = Role(name=role_name, description=role_desc)
            db.session.add(new_role)
            roles_created_count += 1
    
    if roles_created_count > 0:
        db.session.commit()
        click.echo(f'{roles_created_count} role(s) đã được tạo.')
    else:
        click.echo('Tất cả các role mặc định đã tồn tại.')

    # --- 2. TẠO ADMIN (NẾU CÓ CỜ --with-admin) ---
    if with_admin:
        click.echo('Đang tiến hành tạo tài khoản admin...')
        admin_username = os.getenv('ADMIN_USERNAME')
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if not all([admin_username, admin_email, admin_password]):
            click.echo('Lỗi: Cần thiết lập ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD trong file .env.')
            return

        if User.get_user_by_username(admin_username):
            click.echo(f'Tài khoản admin "{admin_username}" đã tồn tại.')
            return

        try:
            admin_user = User(username=admin_username, email=admin_email)
            admin_user.set_password(admin_password)
            
            admin_role = Role.get_role_by_name('admin')
            if admin_role:
                admin_user.roles.append(admin_role)
            
            db.session.add(admin_user)
            db.session.commit()
            click.echo(f'Tài khoản admin "{admin_username}" đã được tạo thành công.')
        except Exception as e:
            db.session.rollback()
            click.echo(f'Lỗi khi tạo tài khoản admin: {e}')

if __name__ == '__main__':
    app.run(debug=True, reloader_type='watchdog')
