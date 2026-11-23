"""Render the invitation's music-box melody to a WAV (same synth as index.html), starting at the tap.
usage: music_render.py RECDIR OUT.wav"""
import base64
import json
import pathlib
import sys
from playwright.sync_api import sync_playwright

rec, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
meta = json.loads((rec / 'times.json').read_text())
dur = meta['times'][-1] + .5
tap = meta['tap']
JS = r"""
async ([dur, tap]) => {
  const SR = 44100, ac = new OfflineAudioContext(2, Math.ceil(SR * dur), SR);
  const mtof = m => 440 * Math.pow(2, (m - 69) / 12);
  const EIGHTH = .56;
  const CHORDS = [
    { bass: 52, pad: [56, 59, 63, 66], tones: [64, 66, 68, 71, 75, 78] },
    { bass: 49, pad: [56, 59, 63, 64], tones: [61, 64, 68, 71, 73, 76] },
    { bass: 45, pad: [57, 61, 64, 68], tones: [61, 64, 68, 69, 71, 76] },
    { bass: 47, pad: [54, 59, 63, 66], tones: [59, 63, 66, 68, 71, 75] }
  ];
  const PATTERNS = [[0, 3, 5, 4, 2, 4, 3, 1], [1, 4, 5, 3, 2, 3, 4, 0], [0, 2, 4, 5, 4, 3, 1, 2], [5, 3, 4, 2, 3, 1, 2, 0]];
  const out = ac.createGain();
  const comp = ac.createDynamicsCompressor(); comp.threshold.value = -18; comp.ratio.value = 3;
  out.connect(comp).connect(ac.destination);
  const len = SR * 4.2, ir = ac.createBuffer(2, len, SR);
  for (let ch = 0; ch < 2; ch++) { const d = ir.getChannelData(ch); for (let i = 0, e = 1, k = Math.pow(.001, 1 / len); i < len; i++, e *= k) d[i] = (Math.random() * 2 - 1) * e; }
  const verb = ac.createConvolver(); verb.buffer = ir;
  const wet = ac.createGain(); wet.gain.value = .75; verb.connect(wet).connect(out);
  const bus = ac.createGain(); bus.gain.value = .75; bus.connect(out); bus.connect(verb);
  const lp = ac.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 1300; lp.Q.value = .4;
  const padBus = ac.createGain(); padBus.connect(lp).connect(bus);
  function bell(t, f, v) {
    const g = ac.createGain(); g.gain.setValueAtTime(.0001, t); g.gain.exponentialRampToValueAtTime(v, t + .005); g.gain.exponentialRampToValueAtTime(.0001, t + 3);
    const o = ac.createOscillator(); o.type = 'sine'; o.frequency.value = f;
    const o2 = ac.createOscillator(); o2.type = 'sine'; o2.frequency.value = f * 3.01;
    const g2 = ac.createGain(); g2.gain.setValueAtTime(v * .18, t); g2.gain.exponentialRampToValueAtTime(.0001, t + .6);
    o.connect(g).connect(bus); o2.connect(g2).connect(bus);
    o.start(t); o2.start(t); o.stop(t + 3.1); o2.stop(t + .7);
  }
  function pad(t, notes, d, type, level) {
    notes.forEach(m => [-7, 7].forEach(det => {
      const o = ac.createOscillator(); o.type = type; o.frequency.value = mtof(m); o.detune.value = det;
      const g = ac.createGain(); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(level, t + 2);
      g.gain.setValueAtTime(level, t + d - .3); g.gain.linearRampToValueAtTime(0, t + d + 2);
      o.connect(g).connect(padBus); o.start(t); o.stop(t + d + 2.2);
    }));
  }
  // As on the page: the music starts with the tap and fades in over 2.5 s; here it also fades out at the end.
  const t0 = tap + .12;
  out.gain.setValueAtTime(0, 0); out.gain.setValueAtTime(0, tap); out.gain.linearRampToValueAtTime(.85, tap + 2.5);
  out.gain.setValueAtTime(.85, dur - 3); out.gain.linearRampToValueAtTime(0, dur - .2);
  for (let step = 0, t = t0; t < dur; step++, t += EIGHTH) {
    const bar = Math.floor(step / 8), i = step % 8, ch = CHORDS[bar % 4];
    if (i === 0) { pad(t, ch.pad, EIGHTH * 8, 'sine', .02); pad(t, [ch.bass], EIGHTH * 8, 'triangle', .03); }
    const pat = PATTERNS[Math.floor(bar / 4) % PATTERNS.length];
    if (i === 0 || Math.random() > .2) bell(t + Math.random() * .015, mtof(ch.tones[pat[i]] + 12 + (i === 5 && bar % 2 ? 12 : 0)), i % 4 === 0 ? .09 : .055);
  }
  const buf = await ac.startRendering();
  // 16-bit WAV, normalised so the loudest moment sits at -1 dBFS (phones play videos quieter than pages)
  const L = buf.getChannelData(0), R = buf.getChannelData(1), n = L.length;
  let peak = 0; for (let i = 0; i < n; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
  const gain = peak > 0 ? .89 / peak : 1;
  const ab = new ArrayBuffer(44 + n * 4), v = new DataView(ab);
  const w = (o, s) => [...s].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
  w(0, 'RIFF'); v.setUint32(4, 36 + n * 4, true); w(8, 'WAVE'); w(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true);
  v.setUint32(24, SR, true); v.setUint32(28, SR * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); w(36, 'data'); v.setUint32(40, n * 4, true);
  for (let i = 0, o = 44; i < n; i++, o += 4) { v.setInt16(o, Math.max(-1, Math.min(1, L[i] * gain)) * 32767, true); v.setInt16(o + 2, Math.max(-1, Math.min(1, R[i] * gain)) * 32767, true); }
  const bytes = new Uint8Array(ab); let s = ''; for (let i = 0; i < bytes.length; i += 32768) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 32768));
  return [btoa(s), peak];
}
"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page()
    p.set_content('<html></html>')
    data, peak = p.evaluate(JS, [dur, tap])
    b.close()
out.write_bytes(base64.b64decode(data))
print(f'{out.name}: {dur:.1f}s, raw peak {peak:.3f}, {out.stat().st_size / 1e6:.1f} MB')
