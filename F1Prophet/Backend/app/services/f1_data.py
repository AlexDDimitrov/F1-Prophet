import requests

class F1DriverData:
    JOLPICA = "https://api.jolpi.ca/ergast/f1"

    def get_all_drivers(self, season=2026):
        url = f"{self.JOLPICA}/{season}/drivers.json"

        try:
            responce = requests.get(url, timeout=10)
            responce.raise_for_status()
            data = responce.json()

            drivers = data['MRData']['DriverTable']['Drivers']

            formatted_drivers = []

            for driver in drivers:
                formatted_drivers.append({
                    'driver_id': driver['driverId'],
                    'code': driver.get('code', ''),
                    'number': driver.get('permanentNumber', ''),
                    'full_name': f"{driver['givenName']} {driver['familyName']}",
                    'given_name': driver['givenName'],
                    'family_name': driver['familyName'],
                    'date_of_birth': driver['dateOfBirth'],
                    'nationality': driver['nationality']
                })

            return formatted_drivers

        except Exception as e:
            print(f"Error fetching drivers: {e}")
            return[]
    
    def get_current_standings(self, season=2026):

        url = f"{self.JOLPICA}/{season}/driverStandings.json"

        try:
            responce = requests.get(url, timeout=10)
            responce.raise_for_status()
            data = responce.json()

            list_of_standing = data['MRData']['StandingsTable']['StandingsLists']
            if not list_of_standing:
                return []
            
            standings = list_of_standing[0]['DriverStandings']

            formatted_standings = []
            for standing in standings:
                driver = standing['Driver']
                formatted_standings.append({
                    'driver_id': driver['driverId'],
                    'code': driver.get('code', ''),
                    'position': int(standing['position']),
                    'points': float(standing['points']),
                    'wins': int(standing['wins']),
                    'team': standing['Constructors'][0]['name'] if standing['Constructors'] else 'Unknown'
                })
            return formatted_standings
        
        except Exception as e:
            print(f"Error fetching standings: {e}")
            return []
        
    """def get_driver_career_stats(self, driver_id):
    stats = {
        'wins': 0,
        'podiums': 0,
        'poles': 0,
        'championships': 0
    }

    try:
        url = f"{self.JOLPICA}/drivers/{driver_id}/results.json?limit=1000"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        races = data['MRData']['RaceTable']['Races']

        for race in races:
            if race['Results']:
                driver_result = next(
                    (r for r in race['Results'] if r['Driver']['driverId'] == driver_id), 
                    None
                )
                
                if driver_result:
                    position = driver_result.get('position', '99')
                    
                    if position == '1':
                        stats['wins'] += 1
                    if position in ['1', '2', '3']:
                        stats['podiums'] += 1

        url = f"{self.JOLPICA}/drivers/{driver_id}/qualifying.json?limit=1000"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        races = data['MRData']['RaceTable']['Races']
        
        for race in races:
            if race['QualifyingResults']:
                driver_qual = next(
                    (q for q in race['QualifyingResults'] if q['Driver']['driverId'] == driver_id),
                    None
                )
                
                if driver_qual and driver_qual.get('position') == '1':
                    stats['poles'] += 1

        url = f"{self.JOLPICA}/drivers/{driver_id}/driverStandings.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        standings_lists = data['MRData']['StandingsTable']['StandingsLists']
        for season_standings in standings_lists:
            if season_standings['DriverStandings']:
                driver_standing = next(
                    (s for s in season_standings['DriverStandings'] if s['Driver']['driverId'] == driver_id),
                    None
                )
                
                if driver_standing and driver_standing.get('position') == '1':
                    stats['championships'] += 1
        
        return stats
        
    except Exception as e:
        print(f"Error fetching career stats for {driver_id}: {e}")
        return stats"""