// Keep preview videos still when the visitor prefers reduced motion.
// Each publication's Video link opens the recording in the browser's full player.
const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
const demoVideos = document.querySelectorAll(".publication-video video");

// Only DexFLEX uses a faster preview; other videos keep their original speed.
const dexflexVideo = document.querySelector('[aria-labelledby="dexflex-title"] video');
if (dexflexVideo) {
  dexflexVideo.defaultPlaybackRate = 3;
  dexflexVideo.playbackRate = 3;
}

function respectMotionPreference() {
  for (const video of demoVideos) {
    video.autoplay = !motionPreference.matches;
    if (motionPreference.matches) video.pause();
  }
}

respectMotionPreference();
motionPreference.addEventListener("change", respectMotionPreference);
