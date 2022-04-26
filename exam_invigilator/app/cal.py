def format_mon(month):

	try:
		months={'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08','september':'09','october':'10','november':'11','december':'12'}
		year=day=month=month.split()
		month=months.get(month[0].lower())
		day=day[1][0:2]
		print(day)
		if ',' in day:
			day='0'+day[0]
		year=year[2]
		print(day)
		print(year+'-'+month+'-'+day)
		return year+'-'+month+'-'+day
	except:
	 	return month

#print(format_mon('April 10, 2022'))
