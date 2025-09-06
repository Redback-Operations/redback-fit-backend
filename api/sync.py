from datetime import datetime, timezone
from models.user import UserProfile
from models import db
from flask import Blueprint, jsonify, request
from flask import current_app as app

sync_bp = Blueprint('sync', __name__)


@sync_bp.route('/update', methods=['POST'])
def update_sync_time():
    try: 
        user_id = request.json.get('user_id')
        if not user_id:
            app.logger.warning(f"[sync/update] missing user_id in payload")
            return jsonify({'error' : 'Missing user_id'}), 400
        
        user = db.session.get(UserProfile, user_id)
        if not user:
            app.logger.warning(f"[sync/update] user not found: {user_id}")
            return jsonify({'error' : 'User not found'}), 404
        
        user.last_synced = datetime.now(timezone.utc)
        db.session.commit()
        ts = user.last_synced.strftime('%Y-%m-%dT%H:%M:%SZ')
        app.logger.info(f"[sync/update] updated last_synced for user {user_id}: {ts}")
        return jsonify({'message' : 'Last sync time updated', 
                        'user_id' : str(user_id),
                        'last_synced' : ts
        }), 200
    except Exception as e:
        app.logger.error(f"[sync/update] error for user {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500



@sync_bp.route('/last', methods=['GET'])
def get_last_sync_time():
    try: 
        user_id = request.args.get('user_id')
        if not user_id:
            app.logger.warning(f"[sync/last] missing user_id in query")
            return jsonify({'error': 'Missing user_id'}), 400
        
        user = db.session.get(UserProfile, user_id)
        if not user:
            app.logger.warning(f"[sync/last] user not found: {user_id}")
            return jsonify({'error' : 'User not found'}), 404
        ts = user.last_synced.strftime('%Y-%m-%dT%H:%M:%SZ') if user.last_synced else None
        app.logger.info(f"[sync/last] fetched last_synced for user {user_id}: {ts}")
        return jsonify({
            'user_id' : str(user.id),
            'last_synced' : ts
        }), 200
    except Exception as e:
        app.logger.error(f"Error fetching sync status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


