class PointsCalculationService:
    EXACT_POSITION_POINTS = 10
    PLUS_ONE_POSITION_POINTS = 5
    PLUS_TWO_POSITION_POINTS = 3
    DNF_CORRECT_POINTS = 5
    FASTEST_LAP_POINTS = 5
    
    @staticmethod
    def calculate_points(predicted_positions, actual_results, predicted_fastest_lap, actual_fastest_lap):
        position_points = PointsCalculationService._calculate_position_points(
            predicted_positions, actual_results
        )
        
        dnf_points = PointsCalculationService._calculate_dnf_points(
            predicted_positions, actual_results
        )
        
        fastest_lap_points = PointsCalculationService._calculate_fastest_lap_points(
            predicted_fastest_lap, actual_fastest_lap
        )
        
        total_points = position_points + dnf_points + fastest_lap_points
        
        return {
            'position_points': position_points,
            'dnf_points': dnf_points,
            'fastest_lap_points': fastest_lap_points,
            'total_points': total_points
        }
    
    @staticmethod
    def _calculate_position_points(predictions, actual):
        actual_positions = {
            result['driver_id']: result['position']
            for result in actual
            if not result.get('is_dnf', False)
        }
        
        total_points = 0
        
        for prediction in predictions:
            if prediction.get('is_dnf', False):
                continue
            
            driver_id = prediction['driver_id']
            predicted_pos = prediction.get('position')
            
            if driver_id not in actual_positions or predicted_pos is None:
                continue
            
            actual_pos = actual_positions[driver_id]
            diff = abs(predicted_pos - actual_pos)
            
            if diff == 0:
                total_points += PointsCalculationService.EXACT_POSITION_POINTS
            elif diff == 1:
                total_points += PointsCalculationService.PLUS_ONE_POSITION_POINTS
            elif diff == 2:
                total_points += PointsCalculationService.PLUS_TWO_POSITION_POINTS
        
        return total_points
    
    @staticmethod
    def _calculate_dnf_points(predictions, actual):
        actual_dnf = {
            result['driver_id']
            for result in actual
            if result.get('is_dnf', False)
        }
        
        predicted_dnf = {
            prediction['driver_id']
            for prediction in predictions
            if prediction.get('is_dnf', False)
        }
        
        correct_dnf_count = len(actual_dnf & predicted_dnf)
        
        return correct_dnf_count * PointsCalculationService.DNF_CORRECT_POINTS
    
    @staticmethod
    def _calculate_fastest_lap_points(predicted_fastest_lap, actual_fastest_lap):
        if not predicted_fastest_lap or not actual_fastest_lap:
            return 0
        
        return (
            PointsCalculationService.FASTEST_LAP_POINTS
            if predicted_fastest_lap == actual_fastest_lap
            else 0
        )