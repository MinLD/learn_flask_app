from ..services.challenges_service import get_challenge_by_id,create_challenge, active_challenge, get_all_challenges_pending,reject_challenge,get_all_challenges_idea
from flask import Blueprint, request
from ..utils.response import success_response, error_response
from flask_jwt_extended import jwt_required, get_jwt
from ..schemas.users_schemas import ChallengeSchema
from ..controller.auth_controller import Role_required

challenges_bp = Blueprint('challenges', __name__)
@challenges_bp.route('/', methods=['POST'])
@jwt_required()
def create_challenge_controller():
    data = request.form.to_dict()
    if 'images' in request.files:
        data['images'] = request.files.getlist('images')
    curent_user_id = get_jwt().get('sub')
    user_id = data.get('user_id')
    organization_id = data.get('organization_id')
    challenge, error = create_challenge(data, curent_user_id, organization_id, user_id)
    if error:
        return error_response(error, 400)
    return success_response(data=ChallengeSchema().dump(challenge), code=201)

@challenges_bp.route('/idea', methods=['GET'])
def get_all_challenges_idea_controller():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return success_response(data=ChallengeSchema().dump(get_all_challenges_idea(page, per_page), many=True), code=200)

@challenges_bp.route('/<string:challenge_id>', methods=['GET'])
def get_challenge_by_id_controller(challenge_id):
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        return error_response("Không tìm thấy thử thách", 400)
    return success_response(data=ChallengeSchema().dump(challenge), code=200)


#admin
@challenges_bp.route('active/<string:challenge_id>', methods=['PATCH'])
@jwt_required()
@Role_required(role='admin')
def controller_active_challenge(challenge_id):
    challenge, error = active_challenge(challenge_id)
    if error:
        return error_response(error, 400)
    return success_response(data=challenge, code=200)

@challenges_bp.route('reject/<string:challenge_id>', methods=['PATCH'])
@jwt_required()
@Role_required(role='admin')
def controller_reject_challenge(challenge_id):
    challenge, error = reject_challenge(challenge_id)
    if error:
        return error_response(error, 400)
    return success_response(data=challenge, code=200)

@challenges_bp.route('/pending', methods=['GET'])
@jwt_required()
@Role_required(role='admin')
def get_all_challenges_pending_controller():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return success_response(data=ChallengeSchema().dump(get_all_challenges_pending(page, per_page), many=True), code=200)