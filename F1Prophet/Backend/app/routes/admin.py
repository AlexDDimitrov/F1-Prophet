from flask import Blueprint, request, jsonify
from ..database import get_db
from ..models import User, Race, Prediction, RaceResult
from ..services.points_service import PointsCalculationService
from ..middleware.auth_guard import admin_required

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/calculate-points/<int:race_id>', methods=['OPTIONS', 'POST'])
@admin_required
def calculate_race_points(race_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400
    
    actual_results = data.get('actual_results', [])
    actual_fastest_lap = data.get('fastest_lap')
    
    if not actual_results:
        return jsonify({'error': 'actual_results is required'}), 400
    
    db = get_db()
    
    try:
        db.query(RaceResult).filter(RaceResult.race_id == race_id).delete()
        db.commit()

        for result in actual_results:
            is_fastest_lap = result['driver_id'] == actual_fastest_lap
            
            race_result = RaceResult(
                race_id=race_id,
                driver_id=result['driver_id'],
                position=result.get('position'),
                is_dnf=result.get('is_dnf', False),
                fastest_lap=is_fastest_lap
            )
            db.add(race_result)
        
        db.commit()
        
        predictions = db.query(Prediction).filter(
            Prediction.race_id == race_id
        ).all()
        
        if not predictions:
            return jsonify({'error': 'No predictions found for this race'}), 404
        
        points_calculated = 0
        user_points_updates = {}
        
        for prediction in predictions:
            predicted_positions = []
            for pos in prediction.positions:
                predicted_positions.append({
                    'driver_id': pos.driver_id,
                    'position': pos.position,
                    'is_dnf': pos.is_dnf
                })
            
            points_breakdown = PointsCalculationService.calculate_points(
                predicted_positions=predicted_positions,
                actual_results=actual_results,
                predicted_fastest_lap=prediction.fastest_lap,
                actual_fastest_lap=actual_fastest_lap
            )
            
            prediction.points_earned = points_breakdown['total_points']
            
            user_id = prediction.user_id
            if user_id not in user_points_updates:
                user_points_updates[user_id] = 0
            user_points_updates[user_id] += points_breakdown['total_points']
            
            points_calculated += 1
        
        db.commit()
    
        for user_id, points_earned in user_points_updates.items():
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.total_points += points_earned
        
        db.commit()
        
        race = db.query(Race).filter(Race.id == race_id).first()
        if race:
            race.status = 'completed'
        
        db.commit()
        
        return jsonify({
            'message': f'Points calculated for {points_calculated} predictions',
            'predictions_processed': points_calculated,
            'users_updated': len(user_points_updates)
        }), 200
        
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500

@bp.route('/race-results/<int:race_id>', methods=['GET'])
def get_race_results(race_id):
    db = get_db()
    
    try:
        results = db.query(RaceResult).filter(
            RaceResult.race_id == race_id
        ).order_by(
            RaceResult.position.asc()
        ).all()
        
        result_list = []
        fastest_lap_driver = None
        
        for result in results:
            result_list.append({
                'driver_id': result.driver_id,
                'position': result.position,
                'is_dnf': result.is_dnf,
                'fastest_lap': result.fastest_lap
            })
            
            if result.fastest_lap:
                fastest_lap_driver = result.driver_id
        
        return jsonify({
            'race_id': race_id,
            'results': result_list,
            'fastest_lap': fastest_lap_driver
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'detail': str(e)}), 500