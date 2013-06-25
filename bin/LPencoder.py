import os
import sys
from datetime import datetime

def volPerc(per):
	return str((100.0 + int(per))/100.0)
	
	
if __name__ == "__main__":
	startTime = datetime.now()
	#Code Time!
	if len(sys.argv) < 6:
		print "Not enough arguments\n LPencoder.py [input] [GameVolumeBoost] [VoiceVolumeBoost] [VoiceAudioPadding] [crop Height:Width:X:Y or no] [TransformHD= std,lossless, no]"
		sys.exit(1)
	
	fileName        = sys.argv[1]
	gameAudioBoost  = sys.argv[2]
	voiceAudioBoost = sys.argv[3]
	voicePadding    = sys.argv[4]
	crop            = sys.argv[5]
	hdEncode        = (sys.argv[6]).lower() 
	fileNoExt, ext  = os.path.splitext(fileName)
	logFile         = fileNoExt+'log'+str(datetime.now())+'.txt'
	toLogFile       = ' >> '+logFile
		
	#Processing de video and mixing the audio
	print 'Extracting game audio from video'
	os.system('mplayer -vo null -vc dump -ao pcm:file="'+fileNoExt+'-gamesound.wav" '+fileName+toLogFile)
	print 'Adjusting Video Game Audio Volume'
	os.system('sox -G -v '+volPerc(gameAudioBoost)+' '+fileNoExt+'-gamesound.wav testa.wav')
	print 'Adjusting Commentary Audio Volume'
	os.system('sox -G -v '+volPerc(voiceAudioBoost)+' '+fileNoExt+'-commentary.wav testa2.wav')
	print 'Mixing the Video Game and Commentary audio'
	os.system('sox -m testa.wav "|sox testa2.wav -p pad '+voicePadding+'" mixed.wav channels 1')
	print 'Deleting temporal audio files'
	os.system('del testa.wav testa2.wav')
	print 'Replacing Original Audio with Mixed Audio Track in Video'
	os.system('mencoder -ovc copy -audiofile mixed.wav -oac copy -mc 0 '+fileName+' -o '+fileNoExt+'-new'+ext+toLogFile)
	print 'Deleting video and audio mix temporal files'
	os.system('del '+fileNoExt+'-nosound'+ext+' '+fileNoExt+'-gamesound.wav mixed.wav'+toLogFile)
	#Optional Cropping
	if crop != 'no':
		print 'Cropping the video'
		os.system('rename '+fileNoExt+'-new'+ext+' '+fileNoExt+'-uncrop'+ext)
		os.system('ffmpeg -i '+fileNoExt+'-uncrop'+ext+' -qscale 0 -filter:v "crop='+crop+'" '+fileNoExt+'-new'+ext)
		os.system('del '+fileNoExt+'-uncrop'+ext)
	#Optional HD encoding
	if hdEncode == 'std':
		print'Encoding video to x264 HD - 1920x1080'
		os.system('ffmpeg -i '+fileNoExt+'-new'+ext+' -s 1920x1080 -aspect 16:9 -c:v libx264 -preset ultrafast '+fileNoExt+'-HD.mp4')
	elif hdEncode == 'lossless':
		print'Encoding video to Lossless H.264/x264 HD - 1920x1080'
		os.system('ffmpeg -i '+fileNoExt+'-new'+ext+' -s 1920x1080 -aspect 16:9 -c:v libx264 -preset veryslow  -qp 0 '+fileNoExt+'-HD.mp4')
	print('COMPLETE!!')
	print(datetime.now() - startTime)