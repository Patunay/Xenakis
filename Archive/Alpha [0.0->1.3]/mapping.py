inq = 35000

rmax = 90000
rmin = 34

inq_range = rmax-rmin

OUTPUT = (inq-rmin)

OUTPUT = OUTPUT/inq_range

OUTPUT = OUTPUT * (10800-2100)

OUTPUT = OUTPUT + 2100

print(OUTPUT)



# OUTPUT = ((((inq-rmin)/inq_range)(10800-2100))+2100)