from operator import or_
from ..models.models_model import Category
from ..services.upload_service import upload_file
from ..extensions import db
from ..utils.response import paginated_response
from ..schemas.users_schemas import CategorySchema
def get_category_by_id(category_id):
    return Category.query.filter_by(id=category_id).first()

def modal_create_category(data, user_id):
    name = data.get('name')
    description = data.get('description')
    image = data.get('image')
    try:
        image, error = upload_file(image, user_id)
        if error:
            return None, error
        new_category = Category(name=name, description=description, image=image)
        db.session.add(new_category)
        db.session.commit()
        return new_category, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def modal_update_category(category_id, data, user_id):
    category = get_category_by_id(category_id)
    if not category:
        return None, "Không tìm thấy danh mục"
    update_file = ['name', 'description']
    for file in update_file:
        if file in data:
            setattr(category, file, data[file])
    if data.get('image'):
        image, error = upload_file(data.get('image'), user_id)
        if error:
            return None, error
        category.image = image
    try:
        db.session.commit()
        return category, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)
    
def modal_get_all_categories(page, per_page):
    try:
        paginated_result = Category.query.paginate(page=page, per_page=per_page)
        category_data = CategorySchema(many=True).dump(paginated_result)
        return paginated_response(category_data, paginated_result), None
    except Exception as e:
        return None, str(e)
    
def modal_delete_category(category_id):
    category = get_category_by_id(category_id=category_id)
    if not category:
        return None, "Không tìm thấy danh mục"
    try:
        db.session.delete(category)
        db.session.commit()
        return "Xóa danh mục thành công", None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def modal_search_categories(data, page, per_page):
        search_query = data.get('keyword')
        if not search_query:
            return None, "Thiếu từ khóa tìm kiếm"
        search_pattern = f"%{search_query}%"
        try: 
            paginated_result = Category.query.filter(
            or_(
                Category.name.ilike(search_pattern),
                Category.description.ilike(search_pattern)
            )).paginate(page=page, per_page=per_page, error_out=False)
            category_data = CategorySchema().dump(paginated_result.items, many=True)
            return paginated_response(category_data, paginated_result), None
        except Exception as e:
            db.session.rollback()
            return None, str(e)