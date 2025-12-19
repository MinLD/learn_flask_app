from flask import Blueprint, request
from ..utils.response import success_response, error_response,paginated_response
from flask_jwt_extended import jwt_required, get_jwt
from ..schemas.users_schemas import CategorySchema, ChallengeSchema
from ..controller.auth_controller import Role_required
from marshmallow import ValidationError
from ..services.category_service import modal_search_categories,modal_create_category, modal_update_category, modal_get_all_categories, modal_delete_category
from ..models.models_model import Challenge, Category
category_bp = Blueprint('api/categories', __name__)
@category_bp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
@Role_required(role='admin')
def controller_create_category():
    data = request.form.to_dict()
    schema = CategorySchema()
    user_id = get_jwt()['sub']
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    
    validated_data['image'] = request.files.get('image')
    if not validated_data['image'] :
        return error_response({
            'image': ['Vui lòng thêm hình ảnh danh mục']
        }, 400)
    new_category, error = modal_create_category(validated_data, user_id)
    if error:
        return error_response(str(error), 500)
    return success_response(data=CategorySchema().dump(new_category), code=201)

@category_bp.route('/<int:category_id>', methods=['PATCH'])
@jwt_required()
@Role_required(role='admin')
def controller_update_category(category_id):
    user_id = get_jwt()['sub']
    data = request.form.to_dict()
    if 'image' in request.files:
        data['image'] = request.files['image']
    category, error = modal_update_category(category_id, data, user_id)
    if error:
        return error_response(str(error), 500)
    return success_response(data=CategorySchema().dump(category), code=200)

@category_bp.route('/<int:category_id>/challenges', methods=['GET']) 
def controller_get_challenges_by_category(category_id):
    challenges = Challenge.query.filter_by(category_id=category_id).all()
    result = ChallengeSchema(many=True).dump(challenges)
    return success_response(data=result, code=200)

@category_bp.route('/', methods=['GET'])
def controller_get_all_categories():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    categories, error = modal_get_all_categories(page, per_page)
    if error:
        return error_response(str(error), 500)
    return success_response(data=categories, code=200)

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
@Role_required(role='admin')
def controller_delete_category(category_id):
    message, error = modal_delete_category(category_id)
    if error:
        return error_response(str(error), 500)
    return success_response(data={"message": message}, code=200)

@category_bp.route('/search', methods=['GET'])
def controller_search_categories():
    keyword = request.args.get('keyword', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    response_data, error = modal_search_categories({'keyword': keyword}, page, per_page)
    if error:
        return error_response(str(error), 500)
    return success_response(data=response_data, code=200)
