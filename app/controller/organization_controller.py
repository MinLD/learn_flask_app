from ..services.organization_service import admin_get_all_organizations,user_get_organization_by_id, create_organization,admin_approve_organization, get_organization_by_id, admin_reject_organization, update_organization

from flask import Blueprint, request
from ..utils.response import success_response, error_response
from flask_jwt_extended import jwt_required, get_jwt
from ..schemas.users_schemas import OrganizationSchema
from ..controller.auth_controller import Role_required   
organization_bp = Blueprint('organization', __name__)

@organization_bp.route('/', methods=['POST'])
@jwt_required()
def controller_create_organization():
    user_id = get_jwt().get('sub')
    data = request.form.to_dict()
    if 'logo_url' in request.files:
        data['logo_url'] = request.files['logo_url']
    organization, error = create_organization(data, user_id)
    if error:
        return error_response(error, 400)
    return success_response(OrganizationSchema().dump(organization), code=201)

@organization_bp.route('/<string:organization_id>', methods=['GET'])
@jwt_required()
def controller_get_organization(organization_id):
    current_user_id = get_jwt().get('sub')
    organization, error = user_get_organization_by_id(organization_id, current_user_id)
    if error:
        return error_response(error, 400)
    return success_response(OrganizationSchema().dump(organization), code=200)

@organization_bp.route('/<string:organization_id>', methods=['PATCH'])
@jwt_required()
def controller_update_organization(organization_id):
    data = request.form.to_dict()
    current_user_id = get_jwt().get('sub')
    if 'logo_url' in request.files:
        data['logo_url'] = request.files['logo_url']
    organization, error = update_organization(data, organization_id, current_user_id)
    if error:
        return error_response(error, 400)
    return success_response(OrganizationSchema().dump(organization), code=200)


# admin
@organization_bp.route('/all', methods=['GET'])
@Role_required(role='admin')
def controller_admin_get_all_organizations():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return success_response(admin_get_all_organizations(page, per_page), code=200)
@organization_bp.route('/approve/<string:organization_id>', methods=['PATCH'])
@jwt_required()
@Role_required(role='admin')
def controller_admin_approve_organization(organization_id):
    error = admin_approve_organization(organization_id)
    if error:
        return error_response(error, 400)
    return success_response("Duyệt doanh nghiệp thành công", code=200)

@organization_bp.route('/reject/<string:organization_id>', methods=['PATCH'])
@jwt_required()
@Role_required(role='admin')
def controller_admin_reject_organization(organization_id):
    error = admin_reject_organization(organization_id)
    if error:
        return error_response(error, 400)
    return success_response("Không xét duyệt doanh nghiệp thành công", code=200)

