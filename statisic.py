import pstats

p = pstats.Stats('outputfile.prof')
p.sort_stats('cumulative').print_stats(10)