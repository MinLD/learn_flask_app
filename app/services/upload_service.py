from ..utils.response import  error_response
from ..models.models_model import Media
import cloudinary.uploader 
from ..extensions import db

def upload_file(file, current_user_id):
    from ..services.users_service import get_user_by_id
    if not file:
        return error_response("Không có file nào được gửi lên", 400)    
    try:
        upload_result = cloudinary.uploader.upload(file)
    except Exception as e:
        return error_response(f"Lỗi khi upload ảnh: {e}", 500)
        
    public_id = upload_result.get('public_id')
    secure_url = upload_result.get('secure_url')
    resource_type = upload_result.get('resource_type')
    
    if not all([public_id, secure_url, resource_type]):
        return error_response("Upload thất bại, kết quả trả về không đầy đủ", 500)
        
    # TẠO MỘT BẢN GHI MEDIA MỚI
    new_media = Media(
        public_id=public_id,
        secure_url=secure_url,
        resource_type=resource_type,
        uploaded_by_user_id=current_user_id
    )
    user = get_user_by_id(current_user_id)
    if not user or not user.profile:
        return error_response("Không tìm thấy người dùng", 404)
    db.session.add(new_media)
    db.session.commit()
               

    return new_media