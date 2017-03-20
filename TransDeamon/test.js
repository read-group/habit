var ffmpeg = require('fluent-ffmpeg');
ffmpeg('./a.amr').output('./a.mp3').audioFilters('volume=5').on('end', function(stdout, stderr) {
    console.log('Transcoding succeeded !');
  }).run();
