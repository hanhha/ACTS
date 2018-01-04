#!/usr/bin/env python3

#TODO: analysis_agent

def get_base_volumes (all_24hsum):
	base_volumes = dict()
	for mar in all_24hsum:
		base = mar ['MarketName'].split ('-')[0]
		if base in base_volumes.keys():
			base_volumes [base] += mar ['BaseVolume']
		else:
			base_volumes [base] = mar ['BaseVolume']
	return base_volumes
		



