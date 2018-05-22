# speech-segmentation-transcription

  Detect the child speech segments based on the manually annotated mom speech segments,
  modify mom speech segment intervals, and output both to textgrids. 
  Export both detected mom and child wav segments, and transcribe them using kaldi ASPIRE model. 
  Write the transcription results to json file. 

# Usage:
  $ python run.py --child_puzzle_wav=\
  					--mom_puzzle_wav=\
  					--mom_puzzle_textgrid=\
  					--child_outfile_textgrid=\
  					--child_segment_wav_outdir=\
  					--mom_segment_wav_outdir=\
  					--add_seconds_at_boundary=
            
            
# Example result:
  (example input: MCRP_ID#3001_G1.wav and MCRP_ID#3001_G1.TextGrid, apply extract_session.py first to get the puzzle session audios) \
  \
  egs.TextGrid: output textgrid of child and mom speech segments detedcted by the program \
  JSONData.json: json file of transcriptions by the program \
  text_whole: easy visualization of dialog between child and mom, transcribed by the program \
  child_audio_trans_by_eesen: transcription on audio recorded by mic on child using speech kitchen EESEN \
  mom_audio_trans_by_eesen: transcription on audio recorded by mic on mom using speech kitchen EESEN \
  
  
