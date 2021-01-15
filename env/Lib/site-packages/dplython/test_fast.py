
from dplython import X, mutate, group_by, diamonds
diamonds = diamonds >> mutate(bin=X["Unnamed: 0"] % 5000)
gbinp = diamonds.groupby("bin")
gbind = diamonds >> group_by(X.bin)

# Test 1
gbinp["foo"] = gbinp.x.transform('mean')
gbind = gbind >> mutate(foo=X.x.mean())
print gbinp["foo"].equals(gbind["foo"])

# Test 2
gbinp["foo"] = gbinp.x.transform('mean') + gbinp.y.transform('mean')
gbind = gbind >> mutate(foo=X.x.mean() + X.y.mean())
print gbinp["foo"].equals(gbind["foo"])

