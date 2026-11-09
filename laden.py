import fastf1
fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2026, 'Monza', 'R')
session.load()

print(session.results[['Abbreviation', 'TeamName', 'Position']])