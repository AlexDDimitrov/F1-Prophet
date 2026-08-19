from flask import Blueprint, jsonify
from app.services.f1_data import F1DriverData
import requests

bp = Blueprint('drivers', __name__, url_prefix='/api')
f1_service = F1DriverData()

def substitute_driver(driver_to_replace_id, replacement_driver_id, driver_list):
    existing_ids = {driver['driver_id'] for driver in driver_list}
    
    if driver_to_replace_id == replacement_driver_id:
        return driver_list
    if driver_to_replace_id not in existing_ids:
        return driver_list
    if replacement_driver_id in existing_ids:
        return driver_list
        
    try:
        res = requests.get(f"{f1_service.JOLPICA}/drivers/{replacement_driver_id}.json", timeout=10)
        res.raise_for_status() 
        data = res.json()
        
        drivers_list = data.get('MRData', {}).get('DriverTable', {}).get('Drivers', [])
        if not drivers_list:
            print(f"Driver {replacement_driver_id} not found in API response.")
            return driver_list
            
        driver_data = drivers_list[0]
        
        for driver in driver_list:

            team = 'missing'
            if replacement_driver_id == 'tsunoda':
                team = 'Red Bull Racing'

            if driver['driver_id'] == driver_to_replace_id:
                driver.update({
                    'driver_id': driver_data.get('driverId'),
                    'code': driver_data.get('code'),
                    'number': f"#{driver_data.get('permanentNumber')}",
                    'full_name': f"{driver_data.get('givenName', '')} {driver_data.get('familyName', '')}".strip(),
                    'given_name': driver_data.get('givenName'),
                    'family_name': driver_data.get('familyName'),
                    'nationality': driver_data.get('nationality'),
                    'date_of_birth': driver_data.get('dateOfBirth', 'Unknown'),
                    'team': team,
                    'position': None,
                    'points': 0,
                    'wins': 0
                })
                break
                
        return driver_list
        
    except Exception as e:
        print(f"Error fetching replacement driver details: {e}")
        return driver_list



@bp.route('/drivers-for-gp', methods=['GET'])
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

            #only for the dutch gp
            result = substitute_driver("hadjar", "tsunoda", result)

        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error in get_drivers: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

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

@bp.route('/drivers-all-time', methods=['GET'])
def get_drivers():
    try:
        drivers = f1_service.get_all_drivers(season=2026)
        standings = f1_service.get_current_standings(season=2026)

        drivers2025 = f1_service.get_all_drivers(season=2025)
        standings2025 = f1_service.get_current_standings(season=2025)

        standings_dict = {s['driver_id']: s for s in standings}
        standings2025_dict = {s['driver_id']: s for s in standings2025}

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


        for driver in drivers2025:
            if driver in result:
                continue

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