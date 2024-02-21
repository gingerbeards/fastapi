



amount_overdue = 20500  #after lumpsum

old_daily_remit = 2300

multiplier = 0.25

tranche_daily_remit = old_daily_remit * multiplier

new_daily_remit = tranche_daily_remit + old_daily_remit 

tranche_duration = amount_overdue/tranche_daily_remit

print(new_daily_remit)
print(tranche_daily_remit)
print(tranche_duration)