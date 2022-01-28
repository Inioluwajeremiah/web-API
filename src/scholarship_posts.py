from flask import Blueprint, app, jsonify, request
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from src.constants.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from src.Models import ScholarshipPost, db

scholarships_blueprint = Blueprint(
    'scholarships', __name__, url_prefix="/api/v1/scholarships")


@scholarships_blueprint.route('/', methods=['POST', 'GET'])
@jwt_required()
def get_all():

    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        ga = request.get_json().get('ga', '')
        title = request.get_json().get('title', '')
        subtitle = request.get_json().get('subtitle', '')
        institution = request.get_json().get('institution', '')
        faculty = request.get_json().get('faculty', '')
        department = request.get_json().get('department', '')
        course = request.get_json().get('course', '')
        level = request.get_json().get('level', '')
        description = request.get_json().get('description', '')
        duration = request.get_json().get('duration', '')
        appfee = request.get_json().get('appfee', '')
        fund_type = request.get_json().get('fund_type', '')
        url = request.get_json().get('app_url', '')
        visits = request.get_json().get('visits', '')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }), HTTP_400_BAD_REQUEST

        if ScholarshipPost.query.filter_by(app_url=url).first():
            return jsonify({
                'error': 'Url already exists'
            }), HTTP_409_CONFLICT

        scholarshipPost = ScholarshipPost(user_id=current_user_id, ga=ga, title=title, subtitle=subtitle,
                                          institution=institution, faculty=faculty, department=department,
                                          course=course, level=level, description=description, duration=duration,
                                          appfee=appfee, fund_type=fund_type, app_url=url, visits=visits)

        db.session.add(scholarshipPost)
        db.session.commit()

        return jsonify({
            'id': scholarshipPost.id,
            'ga': scholarshipPost.ga,
            'title': scholarshipPost.title,
            'subtitle': scholarshipPost.subtitle,
            'institution': scholarshipPost.institution,
            'faculty': scholarshipPost.faculty,
            'department': scholarshipPost.department,
            'course': scholarshipPost.course,
            'level': scholarshipPost.level,
            'description': scholarshipPost.description,
            'duration': scholarshipPost.duration,
            'appfee': scholarshipPost.appfee,
            'fund_type': scholarshipPost.fund_type,
            'app_url': scholarshipPost.app_url,
            'app_short_url': scholarshipPost.app_short_url,
            'visits': scholarshipPost.visits,
            'date_created': scholarshipPost.date_created,
            'date_updated': scholarshipPost.date_updated
        }), HTTP_201_CREATED
    else:

        page = request.args.get('page', 1, type=int)
        perPage = request.args.get('perPage', 5, type=int)

        scholarshipPost = ScholarshipPost.query.filter_by(
            user_id=current_user_id).paginate(page=page, per_page=perPage)
        data = []

        for post in scholarshipPost.items:
            data.append({
                'id': post.id,
                'ga': post.ga,
                'title': post.title,
                'subtitle': post.subtitle,
                'institution': post.institution,
                'faculty': post.faculty,
                'department': post.department,
                'course': post.course,
                'level': post.level,
                'description': post.description,
                'duration': post.duration,
                'appfee': post.appfee,
                'fund_type': post.fund_type,
                'app_url': post.app_url,
                'app_short_url': post.app_short_url,
                'visits': post.visits,
                'date_created': post.date_created,
                'date_updated': post.date_updated
            })

        meta = {
            "page": scholarshipPost.page,
            "pages": scholarshipPost.pages,
            "total_pages": scholarshipPost.total,
            "prev_page": scholarshipPost.prev_num,
            "next_page": scholarshipPost.next_num,
            "has_next": scholarshipPost.has_next,
            "next_prev": scholarshipPost.has_prev

        }

        return jsonify({
            'data': data,
            'meta': meta
        }), HTTP_200_OK


@scholarships_blueprint.get("/<int:id>")
@jwt_required()
def getSchPage(id):
    current_user = get_jwt_identity()

    scholarshipPost = ScholarshipPost.query.filter_by(
        user_id=current_user, id=id).first()

    if not scholarshipPost:
        return jsonify({
            'message': 'Item not found'
        }), HTTP_404_NOT_FOUND

    return jsonify({
        'id': scholarshipPost.id,
        'ga': scholarshipPost.ga,
        'title': scholarshipPost.title,
        'subtitle': scholarshipPost.subtitle,
        'institution': scholarshipPost.institution,
        'faculty': scholarshipPost.faculty,
        'department': scholarshipPost.department,
        'course': scholarshipPost.course,
        'level': scholarshipPost.level,
        'description': scholarshipPost.description,
        'duration': scholarshipPost.duration,
        'appfee': scholarshipPost.appfee,
        'fund_type': scholarshipPost.fund_type,
        'app_url': scholarshipPost.app_url,
        'app_short_url': scholarshipPost.app_short_url,
        'visits': scholarshipPost.visits,
        'date_created': scholarshipPost.date_created,
        'date_updated': scholarshipPost.date_updated
    }), HTTP_201_CREATED


# E D I T    P O S T
@scholarships_blueprint.put('/<int:id>')
@scholarships_blueprint.patch('/<int:id>')
@jwt_required()
def editPost(id):

    current_user = get_jwt_identity()

    scholarshipPost = ScholarshipPost.query.filter_by(
        user_id=current_user, id=id).first()

    if not scholarshipPost:
        return jsonify({
            'message': 'Item not found'
        }), HTTP_404_NOT_FOUND

    ga = request.get_json().get('ga', '')
    title = request.get_json().get('title', '')
    subtitle = request.get_json().get('subtitle', '')
    institution = request.get_json().get('institution', '')
    faculty = request.get_json().get('faculty', '')
    department = request.get_json().get('department', '')
    course = request.get_json().get('course', '')
    level = request.get_json().get('level', '')
    description = request.get_json().get('description', '')
    duration = request.get_json().get('duration', '')
    appfee = request.get_json().get('appfee', '')
    fund_type = request.get_json().get('fund_type', '')
    url = request.get_json().get('app_url', '')
    visits = request.get_json().get('visits', '')

    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
        }), HTTP_400_BAD_REQUEST

    scholarshipPost.ga = ga
    scholarshipPost.title = title
    scholarshipPost.subtitle = subtitle
    scholarshipPost.institution = institution
    scholarshipPost.faculty = faculty
    scholarshipPost.department = department
    scholarshipPost.course = course
    scholarshipPost.level = level
    scholarshipPost.description = description
    scholarshipPost.duration = duration
    scholarshipPost.appfee = appfee
    scholarshipPost.fund_type = fund_type
    scholarshipPost.app_url = url
    scholarshipPost.visits - visits

    db.session.commit()

    return jsonify({
        'id': scholarshipPost.id,
        'ga': scholarshipPost.ga,
        'title': scholarshipPost.title,
        'subtitle': scholarshipPost.subtitle,
        'institution': scholarshipPost.institution,
        'faculty': scholarshipPost.faculty,
        'department': scholarshipPost.department,
        'course': scholarshipPost.course,
        'level': scholarshipPost.level,
        'description': scholarshipPost.description,
        'duration': scholarshipPost.duration,
        'appfee': scholarshipPost.appfee,
        'fund_type': scholarshipPost.fund_type,
        'app_url': scholarshipPost.app_url,
        'app_short_url': scholarshipPost.app_short_url,
        'visits': scholarshipPost.visits,
        'date_created': scholarshipPost.date_created,
        'date_updated': scholarshipPost.date_updated
    }), HTTP_200_OK


# DELETE ITEM
@scholarships_blueprint.delete('/<int:id>')
@jwt_required()
def deletePost(id):

    current_user = get_jwt_identity()

    scholarshipPost = ScholarshipPost.query.filter_by(
        user_id=current_user, id=id).first()

    if not scholarshipPost:
        return jsonify({
            'message': 'Item not found'
        }), HTTP_404_NOT_FOUND

    db.session.delete(scholarshipPost)
    db.session.commit()

    return jsonify({

    }), HTTP_204_NO_CONTENT


@scholarships_blueprint.get('/stats')
@jwt_required()
@swag_from('./docs/sch_post/stats.yaml')
def getStats():
    current_user = get_jwt_identity()

    data = []

    posts = ScholarshipPost.query.filter_by(user_id=current_user).all()

    for post in posts:
        newLink = {
            'id': post.id,
            'visits': post.visits,
            'app_url': post.app_url,
            'short_url': post.app_short_url
        }

        data.append(newLink)
    return jsonify({
        'data': data
    }), HTTP_200_OK
