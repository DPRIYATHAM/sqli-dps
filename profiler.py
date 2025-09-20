import cProfile

from sqlidps import PotentialSQLiPayload, SQLi

profiler = cProfile.Profile()
try:
    profiler.enable()
    SQLi.check("'OR 1=1 UNION SELECT null, version(), database(), user() -- -")
except PotentialSQLiPayload:
    profiler.disable()
    profiler.dump_stats("prof.out")

