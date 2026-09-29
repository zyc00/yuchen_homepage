// Keep preview videos still when the visitor prefers reduced motion.
// Each publication's Video link opens the recording in the browser's full player.
const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
const demoVideos = document.querySelectorAll(".publication-video video");

function respectMotionPreference() {
  for (const video of demoVideos) {
    video.autoplay = !motionPreference.matches;
    if (motionPreference.matches) video.pause();
  }
}

respectMotionPreference();
motionPreference.addEventListener("change", respectMotionPreference);
