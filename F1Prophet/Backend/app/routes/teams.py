from flask import Blueprint, jsonify
from app.services.f1_data import F1DriverData

bp = Blueprint('teams', __name__, url_prefix='/api')
f1_service = F1DriverData()

@bp.route('/teams', methods=['GET'])
def get_teams():
    try:
        teams = f1_service.get_all_teams(season=2026)
        standings = f1_service.get_team_standings(season=2026)

        standings_dict = {s['team_id']: s for s in standings}

        result = []
        for team in teams:
            team_id = team['team_id']
            standing = standings_dict.get(team_id, {})

            if not standings:
                continue

            result.append({
                'team_id': team_id,
                'name': team['name'],
                'nationality': team['nationality'],
                'position': standing.get('position'),
                'points': standing.get('points', 0),
                'wins': standing.get('wins', 0)
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error in get_teams: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

