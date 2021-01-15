

from timeit import Timer

setup = """
from dplython import X, mutate, group_by, diamonds
diamonds = diamonds >> mutate(bin=X["Unnamed: 0"] % 5000)
gbinp = diamonds.groupby("bin")
gbind = diamonds >> group_by(X.bin)
"""

setup2 = """
import pandas as pd
from dplython import X, mutate, group_by, diamonds
gbinp = pd.DataFrame(diamonds).groupby("carat")
"""
# diamonds = diamonds >> mutate(bin=X["Unnamed: 0"] % 5000)
# gbind = diamonds >> group_by(X.bin)

test_stmt = "7 + 7"

Timer(stmt=test_stmt,
      setup=setup).timeit()

Timer(stmt="gbinp.x.transform('mean') + gbinp.y.transform('mean')",
      setup=setup).timeit()
Timer(stmt="gbind >> mutate(foo=X.x.mean() + X.y.mean())",
      setup=setup).timeit()