from flask import Blueprint, jsonify
from app.services.f1_data import F1DriverData

bp = Blueprint('drivers', __name__, url_prefix='/api')
f1_service = F1DriverData()

@bp.route('/drivers', methods=['GET'])
def get_drivers():
    try:
        drivers = f1_service.get_all_drivers(season=2026)
        standings = f1_service.get_current_standings(season=2026)

        standings_dict = {s['driver_id']: s for s in standings}

        result = []

        for driver in drivers:
            driver_id = driver['driver_id']
            standing = standings_dict.get(driver_id, {})

            team = standing.get('team', 'Unknown')
            if team == 'Unknown':
                continue

            result.append({
                'driver_id': driver_id,
                'code': driver['code'],
                'number': driver['number'],
                'full_name': driver['full_name'],
                'given_name': driver['given_name'],
                'family_name': driver['family_name'],
                'nationality': driver['nationality'],
                'date_of_birth': driver.get('date_of_birth', 'Unknown'),
                'team': standing.get('team', 'Unknown'),
                'position': standing.get('position'),
                'points': standing.get('points', 0),
                'wins': standing.get('wins', 0)
            })

        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error in get_drivers: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@bp.route('/drivers/<driver_id>', methods=['GET'])
def get_driver_detail(driver_id):
    try:
        drivers = f1_service.get_all_drivers(season=2026)
        driver = next((d for d in drivers if d['driver_id'] == driver_id), None)
        
        if not driver:
            return jsonify({'error': 'Driver not found'}), 404

        standings = f1_service.get_current_standings(season=2026)
        standing = next((s for s in standings if s['driver_id'] == driver_id), {})

        career_stats = f1_service.get_driver_career_stats(driver_id)

        result = {
            'driver_id': driver_id,
            'code': driver['code'],
            'number': driver['number'],
            'full_name': driver['full_name'],
            'given_name': driver['given_name'],
            'family_name': driver['family_name'],
            'nationality': driver['nationality'],
            'date_of_birth': driver['date_of_birth'],
            'team': standing.get('team', 'Unknown'),
            'position': standing.get('position'),
            'points': standing.get('points', 0),
            'wins': standing.get('wins', 0),
            'career_wins': career_stats['wins'],
            'career_podiums': career_stats['podiums'],
            'career_poles': career_stats['poles'],
            'career_championships': career_stats['championships']
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in get_driver_detail: {e}")
        return jsonify({'error': str(e)}), 500