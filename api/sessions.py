<<<<<<< HEAD
from flask import Blueprint, request, jsonify
from models.session import db, Session, WeatherObservation
from datetime import datetime
import requests

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')

def fetch_weather_for_session(session: Session):
    # Round to hour, pad handled by API via range we request
    start_iso = session.start_time.replace(minute=0, second=0, microsecond=0).isoformat()
    end_iso = session.end_time.replace(minute=0, second=0, microsecond=0).isoformat()

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={session.lat}&longitude={session.lon}"
        "&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m"
        f"&start_hour={start_iso}&end_hour={end_iso}"
        "&timezone=UTC"
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json().get("hourly", {})

    times = data.get("time", [])
    temps = data.get("temperature_2m", [])
    appt  = data.get("apparent_temperature", [])
    hums  = data.get("relative_humidity_2m", [])
    prec  = data.get("precipitation", [])
    wind  = data.get("wind_speed_10m", [])

    obs = []
    for i, t in enumerate(times):
        ts = datetime.fromisoformat(t.replace("Z","+00:00"))
        o = WeatherObservation(
            session_id=session.id, timestamp=ts,
            temperature_c=(temps[i] if i < len(temps) else None),
            apparent_temp_c=(appt[i] if i < len(appt) else None),
            humidity_pct=(hums[i] if i < len(hums) else None),
            precipitation_mm=(prec[i] if i < len(prec) else None),
            wind_speed_ms=(wind[i] if i < len(wind) else None),
        )
        obs.append(o)
    if obs:
        db.session.bulk_save_objects(obs)
        db.session.commit()

@sessions_bp.route('/', methods=['POST'])
def create_session():
    data = request.get_json() or {}
    required = ["user_id","start_time","end_time","lat","lon"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    s = Session(
        user_id=int(data["user_id"]),
        start_time=datetime.fromisoformat(data["start_time"]),
        end_time=datetime.fromisoformat(data["end_time"]),
        sport=data.get("sport"),
        distance_km=float(data.get("distance_km", 0.0)),
        avg_hr=data.get("avg_hr"),
        calories=data.get("calories"),
        steps=data.get("steps"),
        lat=float(data["lat"]), lon=float(data["lon"]),
    )
    db.session.add(s); db.session.commit()

    fetch_weather_for_session(s)
    return jsonify(s.as_dict()), 201

@sessions_bp.route('/', methods=['GET'])
def list_sessions():
    sessions = Session.query.order_by(Session.start_time.desc()).all()
    return jsonify([s.as_dict() for s in sessions])

@sessions_bp.route('/<int:session_id>/weather', methods=['GET'])
def get_session_weather(session_id):
    obs = WeatherObservation.query.filter_by(session_id=session_id)\
        .order_by(WeatherObservation.timestamp.asc()).all()
    if not obs:
        s = Session.query.get_or_404(session_id)
        fetch_weather_for_session(s)
        obs = WeatherObservation.query.filter_by(session_id=session_id)\
            .order_by(WeatherObservation.timestamp.asc()).all()
    return jsonify([o.as_dict() for o in obs])
=======
from flask import Blueprint, jsonify
from models.activity import Activity
from models import db
from datetime import datetime

sessions_bp = Blueprint('sessions_api', __name__)

@sessions_bp.route('', methods=['GET'])
def get_sessions():
    # replace with authenticated user ID from session/token
    user_id = 1  

    activities = Activity.query.filter_by(user_id=user_id).order_by(Activity.begin_time.desc()).all()
    
    sessions = []
    for a in activities:
        sessions.append({
            'session_id': a.id,
            'coach': a.coach if a.coach else 'N/A',
            'duration': a.duration,
            'date': a.begin_time.strftime("%Y/%m/%d"),
            'training': a.activity_type
        })
    
    return jsonify(sessions), 200
>>>>>>> upstream/main
