import csv 
import pdb 
import os 
from pydub import AudioSegment
from datetime import datetime

csv_dir = '/Users/yijiaxu/Desktop/child_segment/time_info_files/'
child_wav_full_dir = '/Users/yijiaxu/Desktop/child_segment/child_wav_full_dir/'
session_dir = '/Users/yijiaxu/Desktop/child_segment/child_wav_files_textgrids_by_session/'

# csv_all = [each for each in os.listdir(csv_dir) if each.endswith('.csv')]
for csv_file in os.listdir(csv_dir): #'MCRP_ID#3001_11-03-14_timeinfo_DVtimes.csv'
	if not csv_file.endswith('csv'):
		continue 
	MCRP_ID = csv_file.split('_')[1] #ID#3001
	with open(csv_dir+csv_file) as csv_context:
		reader = csv.reader(csv_context, delimiter=' ', quotechar='|')
		rows = [row for row in reader]
		[p1s_hr,p1s_min,p1s_sec,p1s_msec,\
		p1e_hr,p1e_min,p1e_sec,p1e_msec]=[int(i) for i in rows[2][0].split(',')[3:]] 
		[p2s_hr,p2s_min,p2s_sec,p2s_msec,\
		p2e_hr,p2e_min,p2e_sec,p2e_msec]=[int(i) for i in rows[3][0].split(',')[3:]] 

		p1_start_time = 3.6e6*p1s_hr+6e4*p1s_min+1e3*p1s_sec+p1s_msec #in ms
		p1_end_time = 3.6e6*p1e_hr+6e4*p1e_min+1e3*p1e_sec+p1e_msec
		p2_start_time = 3.6e6*p2s_hr+6e4*p2s_min+1e3*p2s_sec+p2s_msec #in ms
		p2_end_time = 3.6e6*p2e_hr+6e4*p2e_min+1e3*p2e_sec+p2e_msec
	
		Audio = AudioSegment.from_wav(child_wav_full_dir+'MCRP_'+MCRP_ID+'_child.wav')
		# Audio = Audio.set_frame_rate(8000)
		newAudio = Audio[p1_start_time:p1_end_time]
		newAudio.export(session_dir+'child_puzzle_1_wav/'+'MCRP_'+MCRP_ID+'_G1'+'.wav', format="wav")
		newAudio = Audio[p2_start_time:p2_end_time]
		newAudio.export(session_dir+'child_puzzle_2_wav/'+'MCRP_'+MCRP_ID+'_G2'+'.wav', format="wav")

