
var currentFrame = $('#currentFrame');
var video = VideoFrame({
    id : 'video',
    frameRate: 29.97,
    callback : function(frame) {
        currentFrame.html(frame);
    }
});

$('#play-pause').click(function(){
    if(video.paused){
        video.play();
        video.listen('frame');
        $(this).html('Pause');
    }else{
        video.pause();
        video.stopListen();
        $(this).html('Play');
    }
});

//      <script type="text/Javascript" src="showFrame.js"></script>
