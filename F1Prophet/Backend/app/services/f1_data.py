import requests
import time

class F1DriverData:
    JOLPICA = "https://api.jolpi.ca/ergast/f1"
    _cache = {}
    _cache_ttl = 3600 
    """ 1 hour for now. Probably 1 week or a day better."""

    def _get(self, url):
        now = time.time()
        if url in self._cache:
            data, timestamp = self._cache[url]
            if now - timestamp < self._cache_ttl:
                return data

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        self._cache[url] = (data, now)
        return data

    def _get_all_pages(self, url):
        all_races = []
        offset = 0
        limit = 100

        while True:
            separator = '&' if '?' in url else '?'
            data = self._get(f"{url}{separator}limit={limit}&offset={offset}")
            races = data['MRData']['RaceTable']['Races']
            total = int(data['MRData']['total'])

            all_races.extend(races)

            if offset + limit >= total:
                break

            offset += limit
            time.sleep(0.5)

        return all_races

    def get_all_drivers(self, season=2026):
        url = f"{self.JOLPICA}/{season}/drivers.json"
        try:
            data = self._get(url)
            drivers = data['MRData']['DriverTable']['Drivers']
            formatted_drivers = []
            for driver in drivers:
                formatted_drivers.append({
                    'driver_id': driver['driverId'],
                    'code': driver.get('code', 'N/A'),
                    'number': driver.get('permanentNumber', 'N/A'),
                    'full_name': f"{driver['givenName']} {driver['familyName']}",
                    'given_name': driver['givenName'],
                    'family_name': driver['familyName'],
                    'nationality': driver.get('nationality', 'Unknown'),
                    'date_of_birth': driver.get('dateOfBirth', 'Unknown'),
                    'url': driver.get('url', '')
                })
            return formatted_drivers
        except Exception as e:
            print(f"Error fetching drivers: {e}")
            return []

    def get_current_standings(self, season=2026):
        url = f"{self.JOLPICA}/{season}/driverStandings.json"
        try:
            data = self._get(url)
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
                    'position': int(standing['position']) if standing.get('position') else None,
                    'points': float(standing['points']) if standing.get('points') else 0,
                    'wins': int(standing['wins']) if standing.get('wins') else 0,
                    'team': standing['Constructors'][0]['name'] if standing['Constructors'] else 'Unknown'
                })
            return formatted_standings
        except Exception as e:
            print(f"Error fetching standings: {e}")
            return []

    def get_driver_career_stats(self, driver_id):
        stats = {'wins': 0, 'podiums': 0, 'poles': 0, 'championships': 0}
        try:
            # Wins & podiums
            races = self._get_all_pages(f"{self.JOLPICA}/drivers/{driver_id}/results.json")
            for race in races:
                if race['Results']:
                    result = next((r for r in race['Results'] if r['Driver']['driverId'] == driver_id), None)
                    if result:
                        pos = result.get('position', '99')
                        if pos == '1': stats['wins'] += 1
                        if pos in ['1', '2', '3']: stats['podiums'] += 1

            # Poles
            races = self._get_all_pages(f"{self.JOLPICA}/drivers/{driver_id}/qualifying.json")
            for race in races:
                if race['QualifyingResults']:
                    qual = next((q for q in race['QualifyingResults'] if q['Driver']['driverId'] == driver_id), None)
                    if qual and qual.get('position') == '1':
                        stats['poles'] += 1

            # Championships
            seasons_data = self._get(f"{self.JOLPICA}/drivers/{driver_id}/seasons.json?limit=100")
            seasons = seasons_data['MRData']['SeasonTable']['Seasons']

            for season in seasons:
                year = season['season']
                
                if int(year) >= 2026:
                    continue
                
                try:
                    s_data = self._get(f"{self.JOLPICA}/{year}/drivers/{driver_id}/driverStandings.json")
                    standings_lists = s_data['MRData']['StandingsTable']['StandingsLists']
                    if standings_lists and standings_lists[0]['DriverStandings']:
                        if standings_lists[0]['DriverStandings'][0].get('position') == '1':
                            stats['championships'] += 1
                except Exception:
                    continue
            return stats
        except Exception as e:
            print(f"Error fetching career stats for {driver_id}: {e}")
            return stats