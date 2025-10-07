from ..models.models_model import Organization
from ..services.role_service import get_role_by_name
from ..services.users_service import get_user_by_id
from ..extensions import db
from ..schemas.users_schemas import OrganizationSchema
from ..services.upload_service import upload_file


def get_organization_by_id(organization_id):
    return Organization.query.filter_by(id=organization_id).first()

def user_get_organization_by_id(organization_id, current_user_id):
    organization = get_organization_by_id(organization_id)
    if not organization:
        return None, "Không tìm thấy doanh nghiệp"
    if organization.owner_id != current_user_id:
        return None, "Không có quyền lấy thông tin doanh nghiệp này"
    return organization, None

def create_organization(data, user_id):
    user = get_user_by_id(user_id)
    if not user:
        return None, "Không tìm thấy người dùng"
    if user.organization:
        return None, "Mỗi người dùng chỉ được đăng ký một doanh nghiệp"

    if not data:
        return None, "Thiếu thông tin bắt buộc"
    name = data.get('name')
    description = data.get('description')
    tax_code = data.get('tax_code')
    website = data.get('website')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')

    logo_url = None
    if 'logo_url' in data:
        logo_url = upload_file(data['logo_url'], user_id)

    new_organization = Organization(
        name=name, 
        description=description, 
        logo_url=logo_url, 
        tax_code=tax_code, 
        website=website, 
        email=email, 
        phone=phone, 
        address=address, 
        owner=user)
    user.organization = new_organization
    db.session.add(new_organization)
    db.session.commit()
    return new_organization, None

def update_organization(data, organization_id, current_user_id):
    organization = get_organization_by_id(organization_id)
    if not organization:
        return None, "Không tìm thấy doanh nghiệp"
    print(organization.owner_id, current_user_id)
    if organization.owner_id != current_user_id:
        return None, "Không có quyền cập nhật doanh nghiệp này"
    if not data:
        return None, "Thiếu thông tin bắt buộc"
    updatable_fields = [
        'name', 'description', 'tax_code',
        'website', 'contact_email', 'phone_number', 'address'
    ]
    for field in updatable_fields:
        if field in data and data[field] is not None:
            setattr(organization, field, data.get(field))
    if 'logo_url' in data:
        avatar_media = upload_file(data['logo_url'], current_user_id)
        organization.logo_url = avatar_media

    db.session.commit()

    return organization, None
# admin
def admin_approve_organization(organization_id):
    organization = get_organization_by_id(organization_id)
    if not organization:
        return "Không tìm thấy doanh nghiệp"
    role = get_role_by_name(name='organization_owner')
    if not role:
        return "Không tìm thấy quyền người dùng"
    if organization.status != 'pending':
        return f"Doanh nghiệp này đang ở trạng thái '{organization.status}', không thể duyệt."
    organization.owner.roles.append(role)
    organization.status = "approved"
    db.session.commit()
    return None
def admin_reject_organization(organization_id):
    organization = get_organization_by_id(organization_id)
    if not organization:
        return "Không tìm thấy doanh nghiệp"
    
    if organization.status != 'pending':
        return f"Doanh nghiệp này đang ở trạng thái '{organization.status}', không thể duyệt."
    organization.status = "rejected"
    db.session.commit()
    return None
def admin_get_all_organizations(page, per_page):
    organization = Organization.query.paginate(page=page, per_page=per_page)
    return OrganizationSchema().dump(organization, many=True)
    

  