(() => {
  const play = document.querySelector('.play');
  if (!play) return;
  const canSpeak = 'speechSynthesis' in window;
  const say = (text) => {
    if (!canSpeak || !text) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = document.documentElement.lang || 'es';
    window.speechSynthesis.speak(utterance);
  };
  document.querySelectorAll('[data-speak]').forEach((button) => {
    button.addEventListener('click', () => say(button.dataset.speak));
  });
  if (play.dataset.narration === 'true') say(play.dataset.question);
  if (play.dataset.sound === 'true' && play.dataset.outcome) {
    const audio = new AudioContext();
    const oscillator = audio.createOscillator();
    const gain = audio.createGain();
    oscillator.frequency.value = play.dataset.outcome === 'correct' ? 660 : 220;
    gain.gain.setValueAtTime(0.06, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audio.currentTime + 0.18);
    oscillator.connect(gain).connect(audio.destination);
    oscillator.start(); oscillator.stop(audio.currentTime + 0.18);
  }
})();
