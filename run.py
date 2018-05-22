"""
Author: Yijia Xu 
Usage:
  # Detect the child speech segments based on the manually annotated mom speech segments,
  # modify mom speech segment intervals, and output both to textgrids 
  # export both wav segments, and transcribe them using kaldi ASPIRE model 
  # write transcription results to json file 

  $ python run.py --child_puzzle_wav=\
  					--mom_puzzle_wav=\
  					--mom_puzzle_textgrid=\
  					--child_outfile_textgrid=\
  					--child_segment_wav_outdir=\
  					--mom_segment_wav_outdir=\
  					--add_seconds_at_boundary=\
"""

from scipy.io import wavfile
import pdb 
import matplotlib.pyplot as plt
from vad import VoiceActivityDetector
import numpy as np 
import tgt 
import praatio.tgio as tgio
import os 
import json
import tensorflow as tf
from tools import child_speech_detector
from tools import export_child_audio_segments
from tools import export_mom_audio_segments
from tools import write_to_txtgrids
from tools import transcription

flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string('child_puzzle_wav', '/Users/yijiaxu/Desktop/child_segment/child_wav_files_textgrids_by_session/child_puzzle_1_wav/MCRP_ID#3001_G1_child.wav', \
	'full path of the audio recorded by mic on child')
flags.DEFINE_string('mom_puzzle_wav', '/Users/yijiaxu/Desktop/child_segment/mom_wav_files_textgrids_by_session/mom_puzzle_1_wav/MCRP_ID#3001_G1.wav', \
	'full path of the audio recorded by mic on mom')
flags.DEFINE_string('mom_puzzle_textgrid', '/Users/yijiaxu/Desktop/child_segment/mom_wav_files_textgrids_by_session/mom_puzzle_1_textgrids/MCRP_ID#3001_G1.TextGrid', \
	'full path of the textgrids annotated manually for audio recorded by mic on mom')
flags.DEFINE_string('child_outfile_textgrid', 'egs.TextGrid', \
	'full path of the textgrids to be created by program for both child detected speech segments and modified mom speech segments')

flags.DEFINE_string('child_segment_wav_outdir', 'child_seg_wav', \
	'dir to store detected child audio segments')
flags.DEFINE_string('mom_segment_wav_outdir', 'mom_seg_wav', \
	'dir to store detected mom audio segments')

flags.DEFINE_float('add_seconds_at_boundary', 0.2, \
	'seconds to add at boundary of child speech detected')

# child_puzzle_wav = '/Users/yijiaxu/Desktop/child_segment/child_wav_files_textgrids_by_session/child_puzzle_1_wav/MCRP_ID#3001_G1_child.wav'
# mom_puzzle_wav = '/Users/yijiaxu/Desktop/child_segment/mom_wav_files_textgrids_by_session/mom_puzzle_1_wav/MCRP_ID#3001_G1.wav'
# mom_puzzle_textgrid = '/Users/yijiaxu/Desktop/child_segment/mom_wav_files_textgrids_by_session/mom_puzzle_1_textgrids/MCRP_ID#3001_G1.TextGrid'
# child_outfile_textgrid = 'egs.TextGrid'
# add_seconds_at_boundary = 0.2
# child_segment_wav_outdir = 'child_seg_wav/'
# mom_segment_wav_outdir = 'mom_seg_wav/'

child_puzzle_wav = FLAGS.child_puzzle_wav 
mom_puzzle_wav = FLAGS.mom_puzzle_wav 
mom_puzzle_textgrid = FLAGS.mom_puzzle_textgrid 
child_outfile_textgrid = FLAGS.child_outfile_textgrid 
add_seconds_at_boundary = FLAGS.add_seconds_at_boundary
child_segment_wav_outdir = FLAGS.child_segment_wav_outdir 
mom_segment_wav_outdir = FLAGS.mom_segment_wav_outdir 

if not os.path.exists(child_segment_wav_outdir):
	os.makedirs(child_segment_wav_outdir)

if not os.path.exists(mom_segment_wav_outdir):
	os.makedirs(mom_segment_wav_outdir)

# detects child speech parts
v = VoiceActivityDetector(child_puzzle_wav)
data = v.data
total_time = len(data)*1.0/v.rate
total_time = float("{0:.2f}".format(total_time))
speech_time,mom_tier = child_speech_detector(mom_puzzle_textgrid,v)

# export detected child speech segments wav 
turns = export_child_audio_segments(total_time,child_puzzle_wav,add_seconds_at_boundary,child_segment_wav_outdir,speech_time)
total_turns = turns
tier = write_to_txtgrids('Machine-Label-CS',turns)

# modify manually annotated mom speech segments, and export the wav segments 
mom_turns = export_mom_audio_segments(mom_puzzle_wav,mom_tier,mom_segment_wav_outdir)
total_turns+=mom_turns
mom_tier = write_to_txtgrids('Human-Label-MS(modified)', mom_turns)

# write child and mom speech segment results to the textgrids 
tg = tgio.Textgrid()
tg.addTier(mom_tier)
tg.addTier(tier)
tg.save(child_outfile_textgrid)

# do transcriptions of the detected segments 
transcription(total_turns,mom_puzzle_wav,child_puzzle_wav,mom_segment_wav_outdir,child_segment_wav_outdir,'JSONData.json')
