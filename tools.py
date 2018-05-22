import tgt 
import operator
import praatio.tgio as tgio
from pydub import AudioSegment
import subprocess

def child_speech_detector(mom_puzzle_textgrid,v):
	""" Detects child speech segments by:
		filter out manually annotated mom speech segments
		compute child speech band energy per frame, set threhold of being voiced or not
		apply median filter to the results of being voiced or not per frame
		if two voiced frames are seperated by only 1 min, merge 
		return time intervals of detected child speech 

	Args:
		mom_puzzle_textgrid: manually annotated mom speech textgrids 
		v: VoiceActivityDetector object 
	
	Returns:
		speech_time: the time intervals of detected child speech segments 
		mom_tier: manually annotated mom speech textgrid tier 
	"""
	speech_time = {}
	data = v.data
	tg = tgt.read_textgrid(mom_puzzle_textgrid)
	mom_tier = tg.get_tier_by_name('Mother') 
	child_tier = tg.get_tier_by_name('Child') 
	for i in range(len(mom_tier)):
		end_sample = int(round(mom_tier[i].end_time*v.rate))
		if i==len(mom_tier)-1:
			start_sample = len(data)
		else:
			start_sample = int(round(mom_tier[i+1].start_time*v.rate))

		v.data = data[end_sample:start_sample]
		detected_windows = v.detect_speech()
		for sample_start,speech in detected_windows:
			sample_start,speech = int(sample_start),int(speech)
			sample_start+=end_sample
			if speech:
				# extend if two intervals speperate by only 1min 
				region_start_time = sample_start*1.0/v.rate
				region_start_time = float("{0:.2f}".format(region_start_time)) # round to 2 floats 

				if len(speech_time):
					largest_time_prev = max(speech_time.keys())
					if region_start_time-1<=largest_time_prev:
						speech_time[region_start_time] = speech_time[largest_time_prev]
						del speech_time[largest_time_prev]
					else:
						speech_time[region_start_time]=region_start_time
				else:
					speech_time[region_start_time]=region_start_time					 

	speech_time = sorted(speech_time.items(), key=operator.itemgetter(1))

	return speech_time, mom_tier

def export_child_audio_segments(total_time,child_puzzle_wav,add_seconds_at_boundary,child_segment_wav_outdir,speech_time):
	""" export the detected child speech segments into child_segment_wav_outdir directory, and
		manually add seconds at child speech boundary 

	Args:
		total_time: total time of the audio recording
		child_puzzle_wav: audio recorded by mic on child
		add_seconds_at_boundary: seconds to be added at boundary of detected child segments 
		child_segment_wav_outdir: dir to store the child speech segments 
		speech_time: detected speech intervals of child (returned from child_speech_detector)

	Returns:
		turns: detected child speech segments [(start_time,end_time,label)] to be written to the textgrid 

	"""

	turns=[]
	Audio = AudioSegment.from_wav(child_puzzle_wav)
	Audio = Audio.set_frame_rate(8000)
	for i in range(len(speech_time)):
		start=speech_time[i][1]
		end=speech_time[i][0]
		label='CS'
		if end-start>=0.1:
			# manually add seconds at boundary 
			if start<add_seconds_at_boundary:
				start=0
			else:
				start-=add_seconds_at_boundary
			if end>=total_time-add_seconds_at_boundary:
				end=total_time
			else:
				end+=add_seconds_at_boundary
			turns.append((start,end,label))

			# extract the corresponding audio segments at meanwhile 
			t1 = start * 1000 # in milliseconds 
			t2 = end * 1000
	  		newAudio = Audio[t1:t2]
	  		filename = child_puzzle_wav.split('/')[-1].split('.wav')[0]
	  		newAudio.export(child_segment_wav_outdir+"/"+filename+'-'+str(start)+'-'+str(end)+'.wav', format="wav")
	print("Done export detected child segments to '"+child_segment_wav_outdir+"/'")
	return turns

def write_to_txtgrids(annotation,turns):
	tier = tgio.IntervalTier(annotation, turns)
	return tier 


def export_mom_audio_segments(mom_puzzle_wav,mom_tier,mom_segment_wav_outdir):
	""" modify manually annotated mom segments, by merging intervals if two are seperated by only 1 sec
		export the detected mom speech segments into mom_segment_wav_outdir directory

	Args:
		mom_puzzle_wav: audio recorded by mic on mom
		mom_tier: manually annotated mom segments
		mom_segment_wav_outdir: dir to store the mom speech segments 

	Returns:
		mom_turns: modified mom speech segments [(start_time,end_time,label)] to be written to the textgrid 

	"""

	mom_turns = [(0,0,'MS')] 
	Audio = AudioSegment.from_wav(mom_puzzle_wav)
	Audio = Audio.set_frame_rate(8000)

	for i in mom_tier:
		if str(i.text) == 'MS':
			# merge interval within 1 sec
			if i.start_time-1<=mom_turns[-1][1]:
				tup = mom_turns[-1]
				del mom_turns[-1]
				start = tup[0]
				end = i.end_time
			else:
				start = i.start_time
				end = i.end_time

			if end-start<=0.1:
				continue # or move to the end, do another loop 

			mom_turns.append((start,end,i.text))

			# extract the corresponding audio segments at meanwhile 
			t1 = start * 1000 # in milliseconds 
			t2 = end * 1000
		  	newAudio = Audio[t1:t2]
		  	filename = mom_puzzle_wav.split('/')[-1].split('.wav')[0]
		  	newAudio.export(mom_segment_wav_outdir+"/"+filename+'-'+str(start)+'-'+str(end)+'.wav', format="wav")
	print("Done export detected mom segments to '"+mom_segment_wav_outdir+"/'")
	return mom_turns

def transcription(total_turns,mom_puzzle_wav,child_puzzle_wav,mom_segment_wav_outdir,child_segment_wav_outdir,json_file_name):
	"""  transcrie both mom and child speech segments (returned from turns in export_child_audio_segments and mom_turns in export_mom_audio_segments)
	transcription scripts of kaldi in ./transcribe.sh

	Args:
		total_turns: child turns + mom turns returned from export_child_audio_segments and export_mom_audio_segments
		mom_puzzle_wav: audio recorded by mic on mom 
		child_puzzle_wav:  audio recorded by mic on child
		mom_segment_wav_outdir: dir stored the mom speech segments 
		child_segment_wav_outdir: dir stored the child speech segments 
		json_file_name: path to write the transcription results to json file 

	Returns:
		outputs the json_file_name, which records the start, end time and transcription of mom and child speech

	"""

	data=[]
	total_turns = sorted(total_turns, key=lambda x: x[0])
	for s,e,l in total_turns:
		if str(l)=='MS':
			filename = mom_puzzle_wav.split('/')[-1].split('.wav')[0]
			filename = mom_segment_wav_outdir+'/'+filename+'-'+str(s)+'-'+str(e)+'.wav'
			idu = 'Mom:'
		if str(l)=='CS':
			filename = child_puzzle_wav.split('/')[-1].split('.wav')[0]
			filename = child_segment_wav_outdir+'/'+filename+'-'+str(s)+'-'+str(e)+'.wav'	
			idu = 'Child:'	
		transcription_filename = 'text'
		cmd = "./transcribe.sh {0} {1} {2}".format(filename,transcription_filename,idu)
		transcription = subprocess.check_output(cmd,shell=True)
		item = {"id":transcription.split(':')[0],"start_time":s,"end_time":e,"transcription":transcription.split(':')[1].split('\n')[0]}
		data.append(item)
		# os.system(cmd)
	jsonData=json.dumps(data,indent=4,separators=(',',':')) #json object 
	with open(json_file_name, 'w') as f: f.write(jsonData)
