from ..services.organized_events_service import create_organized_event, join_organized_event, get_all_organized_events_approved
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from ..controller.auth_controller import Role_required
from ..utils.response import success_response, error_response
from ..schemas.users_schemas import Organized_EventsSchema

organization_events_bp = Blueprint('organization_events', __name__)
@organization_events_bp.route('/', methods=['POST'])
@jwt_required()
@Role_required(role='organization_owner')
def controller_create_organized_event():
    data = request.get_json()
    organized_event, error = create_organized_event(data)
    if error:
        return error_response(error, 400)
    return success_response(data=Organized_EventsSchema().dump(organized_event), code=201)

@organization_events_bp.route('/join/<string:organized_event_id>', methods=['PATCH'])
@jwt_required()
def controller_join_organized_event(organized_event_id):
    user_id = get_jwt().get('sub')
    data, error = join_organized_event(organized_event_id, user_id)
    if error:
        return error_response(error, 400)
    return success_response(data=data, code=200)

@organization_events_bp.route('/approved', methods=['GET'])
def controller_get_all_approved():
    data = get_all_organized_events_approved()
    return success_response(data=Organized_EventsSchema(many=True).dump(data), code=200)

