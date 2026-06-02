from datetime import datetime
from flask import Blueprint, jsonify
from ..database import get_db
from ..models import Race

bp = Blueprint('races', __name__, url_prefix='/api/races')

@bp.route('/race_calendar/<year>', methods = ['GET'])
def get_calendar(year):
    db = get_db()

    try:
        race_list = db.query(Race).filter(Race.season == str(year)).all()

        if not race_list:
            return jsonify({'error': 'No races found for the specified year'}), 404

        return jsonify([{
            'id': race.id,
            'name': race.name,
            'location': race.location,
            'race_date': race.race_date,
            'deadline': race.deadline,
            'season': race.season,
            'round_number': race.round_number,
            'status': race.status
        } for race in race_list])
    
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500
    
@bp.route('/current', methods=['GET'])
def get_current_race():
    db = get_db()
    
    try:
        race = db.query(Race).filter(
            Race.race_date >= datetime.now()
        ).order_by(Race.race_date.asc()).first()
        
        if not race:
            return jsonify({'error': 'No upcoming races'}), 404
        
        return jsonify({
            'id': race.id,
            'name': race.name,
            'location': race.location,
            'race_date': race.race_date.isoformat(),
            'deadline': race.deadline.isoformat(),
            'season': race.season,
            'round_number': race.round_number,
            'status': race.status
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/all', methods=['GET'])
def get_all_races():
    db = get_db()
    
    try:
        races = db.query(Race).filter(
            Race.season == 2026
        ).order_by(Race.round_number.asc()).all()
        
        result = []
        for race in races:
            result.append({
                'id': race.id,
                'name': race.name,
                'location': race.location,
                'race_date': race.race_date.isoformat(),
                'deadline': race.deadline.isoformat(),
                'season': race.season,
                'round_number': race.round_number,
                'status': race.status
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500