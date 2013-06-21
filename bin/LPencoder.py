import os
import sys
from datetime import datetime

def volPerc(per):
	return str((100 + int(per))/100)
	
	
if __name__ == "__main__":
	startTime = datetime.now()
	#Code Time!
	if len(sys.argv) < 6:
		print "Not enough arguments\n LPencoder.py [input] [GameVolumeBoost] [VoiceVolumeBoost] [VoiceAudioPadding] [TransformHD= std,lossless, no]"
		sys.exit(1)
	fileName        = sys.argv[1]
	gameAudioBoost  = sys.argv[2]
	voiceAudioBoost = sys.argv[3]
	voicePadding    = sys.argv[4]
	hdEncode        = (sys.argv[5]).lower() 
	fileNoExt, ext  = os.path.splitext(fileName)
	logFile         = fileNoExt+'log'+str(datetime.now())+'.txt'
	toLogFile       = ' >> '+logFile
	#Processing de video and mixing the audio
	print 'Stripping sound from video file'
	os.system('mencoder -ovc copy -nosound '+fileName+' -o '+fileNoExt+'-nosound'+ext+toLogFile)
	print 'Saving game audio from video'
	os.system('mplayer -vo null -vc dump -ao pcm:file="'+fileNoExt+'-gamesound.wav" '+fileName+toLogFile)
	
	print 'Adjusting Video Game Audio Volume'
	#os.system('mplayer -vo null -vc dump -af volume='+gameAudioBoost+' -ao pcm:file=testa.wav '+fileNoExt+'-gamesound.wav'+toLogFile)
	os.system('sox -v '+volPerc(gameAudioBoost)+' '+fileNoExt+'-gamesound.wav testa.wav')
	print 'Adjusting Commentary Audio Volume'
	#os.system('mplayer -vo null -vc dump -af volume='+voiceAudioBoost+' -ao pcm:file=testa2.wav '+fileNoExt+'-commentary.wav'+toLogFile)
	os.system('sox -v '+volPerc(voiceAudioBoost)+' '+fileNoExt+'-commentary.wav testa.wav')
	print 'Mixing the Video Game and Commentary audio'
	os.system('sox -m testa.wav "|sox testa2.wav -p pad '+voicePadding+'" mixed.wav')
	print 'Deleting temporal audio files'
	os.system('del testa.wav testa2.wav')
	print 'Adding Mixed Audio Track to Soundless Video'
	os.system('mencoder -ovc copy -audiofile mixed.wav -oac copy '+fileNoExt+'-nosound'+ext+' -o '+fileNoExt+'-new'+ext+toLogFile)
	print 'Deleting video and audio mix temporal files'
	os.system('del '+fileNoExt+'-nosound'+ext+' '+fileNoExt+'-gamesound.wav mixed.wav'+toLogFile)
	#Optional HD encoding
	if hdEncode == 'std':
		print'Encoding video to x264 HD - 1920x1080'
		os.system('ffmpeg -i '+fileNoExt+'-new'+ext+' -s 1920x1080 -aspect 16:9 -c:v libx264 -preset ultrafast '+fileNoExt+'-HD.mp4')
	elif hdEncode == 'lossless':
		print'Encoding video to Lossless H.264/x264 HD - 1920x1080'
		os.system('ffmpeg -i '+fileNoExt+'-new'+ext+' -s 1920x1080 -aspect 16:9 -c:v libx264 -preset veryslow  -qp 0 '+fileNoExt+'-HD.mp4')
	print('COMPLETE!!')
	print(datetime.now() - startTime)