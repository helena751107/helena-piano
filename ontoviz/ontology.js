/* HELENA PIANO — studio ontology.
 *
 * One knowledge base behind the landing page: every glow on screen is a node
 * with a class, a weight, and a source (chapter + line from the webzine). The
 * graph, the dashboard, the inspector and the Web MCP tools all read this one
 * object. Text is taken from index.html; nothing here invents a claim.
 */

export const COL = ['#f4efe6', '#8b7cf0', '#d4a84b', '#3db8a8', '#e85d4c', '#a99cff', '#8fb3c9', '#f0c75e'];
export const CLASS = ['Hub', 'Pillar', 'Map', 'Step', 'Channel', 'Session', 'Rhythm', 'Install'];
export const SECTIONS = ['cover', 'pillars', 'map', 'method', 'channels', 'session', 'rhythm', 'install'];
export const HUB = 'piano';

/* Brand strings that panels.js and onto.js paint into the 3D scene. Keeping
   them here means the engine stays generic and the copy stays one place per
   site. */
export const BRAND = {
  kicker: 'Piano ontology',
  kickerDash: 'Piano ontology · WebGPU knowledge graph',
  kickerIntro: 'Piano ontology · interactive 3D · WebGPU',
  nameA: 'Helena ',
  nameB: 'Piano',
  lede: 'An interactive 3D knowledge base for a one-phone classical webzine. Every glow is an entity — practice, repertoire, take, broadcast — every line a relation, and each one traces back to a chapter.',
  introA: 'Keys to air.',
  introB: 'Render lane. Magazine lane.',
  introSub: 'A classical music webzine made on a single phone. Piano music rendered on an S21, with listening notes, reviews and interviews beside it.',
  note: 'PRACTICE · REPERTOIRE · RECORD · BROADCAST — ONE PHONE',
  noteShort: 'PRACTICE · RECORD · BROADCAST',
  noteWrap: ['PRACTICE · REPERTOIRE · RECORD', 'BROADCAST — ONE PHONE, ONE LILAC P'],
  coverTitle: 'Keys to air.<br><em>Render lane. Magazine lane.</em>',
  coverDeck: 'Piano music rendered on an S21 in the IT lane, listening notes and reviews in the magazine lane. This page is also the knowledge base: every glow is an entity with a source.'
};

const N = [];
const L = [];
const add = (id, label, cls, s, val, ref, quote, desc, extra = {}) => {
  N.push({ id, label, cls, s, val, ref, quote, desc, ...extra });
};
const link = (source, target, rel) => L.push({ source, target, rel });

/* ── hub + chapters ─────────────────────────────────────────────── */
add(HUB, 'HELENA PIANO', 'Hub', 0, 14, 'Cover', 'Keys to air. Render lane, magazine lane.',
  'The mini studio where practice room and broadcast desk share one roof. Every public account leaves under big sister’s name.', { chapter: 'cover', big: 1 });
add('ch.pillars', '01 · Studio', 'Hub', 0, 7, '01 · Studio pillars', 'Four zones · mini studio',
  'Practice, repertoire, record, broadcast. Tap a card and that zone’s meter fills in.', { chapter: 'pillars' });
add('ch.map', '02 · Map', 'Hub', 0, 7, '02 · Infographic', 'From keys to airwaves',
  'The dotted paths from the keyboard to the broadcast tower. Hover or tap a node to open its description.', { chapter: 'map' });
add('ch.method', '03 · Pipeline', 'Hub', 0, 7, '03 · Pipeline', 'Broadcast pipeline, 5 stages',
  'Warm → Work → Take → Shape → Air. The designer’s draft and the foreman’s build keep the same rhythm.', { chapter: 'method' });
add('ch.channels', '04 · Channels', 'Hub', 0, 7, '04 · Channels', 'Doors out',
  'Same keyboard, different doors. Practice records and broadcasts do not mix purposes.', { chapter: 'channels' });
add('ch.session', '05 · Session', 'Hub', 0, 7, '05 · Session card', 'Practice card template',
  'One session, four boxes: piece, minutes, sticking point, next. Reused for logs and broadcast planning.', { chapter: 'session' });
add('ch.rhythm', '06 · Rhythm', 'Hub', 0, 7, '06 · Rhythm', 'Weekly practice breath',
  'A sketch of target weighting — a filling bar is a direction, not a target.', { chapter: 'rhythm' });
add('ch.install', '07 · Install', 'Hub', 0, 7, '07 · Install', 'Pin it to your home screen',
  'No service worker — manifest plus a lilac P monogram, so it opens fast and current.', { chapter: 'install' });
['ch.pillars', 'ch.map', 'ch.method', 'ch.channels', 'ch.session', 'ch.rhythm', 'ch.install']
  .forEach((c) => link(HUB, c, 'chapter'));

/* ── 01 · the four zones ────────────────────────────────────────── */
add('z.practice', 'Practice', 'Pillar', 1, 9, '01 · Studio pillars', 'The zone that keeps hands, ears and time. A log of repetition, not perfection.',
  'Session time and tempo notes, marking the sticking bars, running alongside the S21 timer and metronome. Focus weight 90%.', { chapter: 'pillars', weight: 90 });
add('z.rep', 'Repertoire', 'Pillar', 1, 8, '01 · Studio pillars', 'What’s going up now, what’s coming next. The list is the broadcast plan.',
  'Piece cards with difficulty, a public versus practice-only split, and a crossing point with the Faith axis. Focus weight 82%.', { chapter: 'pillars', weight: 82 });
add('z.record', 'Record', 'Pillar', 1, 8, '01 · Studio pillars', 'Capturing clips. One phone is enough for a mini-session take.',
  'Audio and video takes, file naming rules, the termux-setup and youtube/ folders. Focus weight 86%.', { chapter: 'pillars', weight: 86 });
add('z.air', 'Broadcast', 'Pillar', 1, 9, '01 · Studio pillars', 'The last door out, onto YouTube. Short or long.',
  'Shorts or full-length performances, title and thumbnail drafts from _Grok, funnel back to the hub. Focus weight 88%.', { chapter: 'pillars', weight: 88 });
['z.practice', 'z.rep', 'z.record', 'z.air'].forEach((c) => link('ch.pillars', c, 'contains'));

/* ── 02 · the map ───────────────────────────────────────────────── */
add('m.practice', 'Practice · Floor', 'Map', 2, 6, '02 · Infographic', 'Session log · tempo · sticking bars. The studio’s floor.',
  'Where every path starts: the take is only as good as the week of logs under it.', { chapter: 'map' });
add('m.rep', 'Repertoire · List', 'Map', 2, 6, '02 · Infographic', 'The list of pieces to upload. The seed of the broadcast calendar.',
  'Public pieces and practice-only pieces stay on separate shelves.', { chapter: 'map' });
add('m.record', 'Record · Take', 'Map', 2, 6, '02 · Infographic', 'Capturing takes. Phone mic and external input.',
  'Clip capture on the phone; the file name carries the date and the piece.', { chapter: 'map' });
add('m.youtube', 'YouTube', 'Channel', 4, 5, '02 · Infographic', 'Broadcast. Shorts and full performance videos.',
  'The ecosystem’s broadcast tower — the slow, deep door.', { chapter: 'map', href: 'https://www.youtube.com/@helena_phone' });
add('m.pages', 'Pages · Hub', 'Channel', 4, 5, '02 · Infographic', 'This webzine, install icons, docs.',
  'An SSOT satellite: the webzine, the manifest, the documents that ship as HTML.', { chapter: 'map', href: 'https://github.com/helena751107/helena-piano' });
add('m.archive', 'Archive', 'Channel', 4, 4, '02 · Infographic', 'Takes and notes preserved. youtube/ · logs.',
  'Nothing thrown away: old takes and session notes stay as the raw material for the next piece.', { chapter: 'map' });
['m.practice', 'm.rep', 'm.record', 'm.youtube', 'm.pages', 'm.archive'].forEach((c) => link('ch.map', c, 'contains'));
link('ch.map', 'z.practice', 'contains');

/* ── 03 · the 5-stage pipeline ──────────────────────────────────── */
add('s.warm', 'Warm', 'Step', 3, 5, '03 · Pipeline', 'Open the hands with scales, arpeggios and easy phrases.',
  'It is fine if the log just says “warm-up minutes”. The point is that the hands were opened on purpose.', { chapter: 'method' });
add('s.work', 'Work', 'Step', 3, 5, '03 · Pipeline', 'Attack the sticking bars. One passage at a time.',
  'Slow, metronome-marked, hands separate if needed. Name the cause in one line.', { chapter: 'method' });
add('s.take', 'Take', 'Step', 3, 5, '03 · Pipeline', 'Capture it in one go. A usable take beats a perfect one.',
  'Phone on the music stand, one pass, no comping marathon.', { chapter: 'method' });
add('s.shape', 'Shape', 'Step', 3, 5, '03 · Pipeline', 'Cuts, title, thumbnail.',
  'The designer’s draft from _Grok meets the foreman’s build rhythm here.', { chapter: 'method' });
add('s.air', 'Air', 'Step', 3, 5, '03 · Pipeline', 'Out to YouTube. Shorts or a full performance.',
  'Decide the door before exporting: the length rule belongs to the door, not to the take.', { chapter: 'method' });
['s.warm', 's.work', 's.take', 's.shape', 's.air'].forEach((c) => link('ch.method', c, 'contains'));
['s.warm', 's.work', 's.take', 's.shape'].forEach((c, i) => link(c, ['s.work', 's.take', 's.shape', 's.air'][i], 'flow'));
link('s.air', 's.warm', 'flow');

/* ── 04 · the doors out ─────────────────────────────────────────── */
add('g.youtube', 'YouTube', 'Channel', 4, 6, '04 · Channels', 'Performances, practice vlogs, shorts. The broadcast tower.',
  'Connected to the ecosystem tower; the slowest and deepest door.', { chapter: 'channels', href: 'https://www.youtube.com/@helena_phone' });
add('g.s21', 'S21 · Termux', 'Channel', 4, 6, '04 · Channels', 'termux-setup.sh, phone health, the upload-script lane.',
  'The workstation door: the same phone that records is the one that uploads.', { chapter: 'channels', href: 'https://helena751107.github.io/helena_phone/' });
add('g.pages', 'GitHub · Pages', 'Channel', 4, 5, '04 · Channels', 'This webzine, icons, the youtube/ folder. An SSOT satellite.',
  'Source of truth for the page itself, and the install entry.', { chapter: 'channels', href: 'https://github.com/helena751107/helena-piano' });
['g.youtube', 'g.s21', 'g.pages'].forEach((c) => link('ch.channels', c, 'contains'));

/* ── 05 · session card + studio etiquette ───────────────────────── */
add('c.piece', 'Piece · movement', 'Session', 5, 7, '05 · Session card', 'Piece · (title / movement).',
  'One piece per card. A card that holds two pieces is two sessions confused.', { chapter: 'session' });
add('c.minutes', 'Minutes', 'Session', 5, 7, '05 · Session card', 'Minutes · warm-up __ / focus __ / take __.',
  'Three numbers, no essay. The split shows where the time actually went.', { chapter: 'session' });
add('c.block', 'Sticking point', 'Session', 5, 7, '05 · Session card', 'Sticking point · bar · cause in one line.',
  'A bar number and a cause: the next session starts here.', { chapter: 'session' });
add('c.next', 'Next · 48 hours', 'Session', 5, 6, '05 · Session card', 'One thing within 48 hours.',
  'One thing only. Two days is long enough to forget the hands, short enough to keep them.', { chapter: 'session' });
add('c.etiquette', 'Studio etiquette', 'Session', 5, 7, '05 · Session card', 'Practice failures aren’t mocked as content. Honesty of the hands over showing off.',
  'When there is a care-track (Track 1) commitment, it comes before the broadcast schedule.', { chapter: 'session' });
add('c.name', 'Big sister’s name', 'Session', 5, 6, '05 · Session card', 'Every public account here is under big sister’s name.',
  'No face in front; one name carries the studio.', { chapter: 'session' });
add('c.craft', '_Grok design', 'Session', 5, 5, '05 · Session card', 'Design drafts from _Grok, built by the foreman.',
  'Thumbnails and titles are drafts until they pass the studio’s own eye.', { chapter: 'session' });
['c.piece', 'c.minutes', 'c.block', 'c.next', 'c.etiquette', 'c.name', 'c.craft'].forEach((c) => link('ch.session', c, 'contains'));

/* ── 06 · weekly rhythm ─────────────────────────────────────────── */
add('r.practice', 'Practice 40', 'Rhythm', 6, 6, '06 · Rhythm', 'Target weighting of the week: 40%.',
  'The largest share goes to the room where the hands are made.', { chapter: 'rhythm' });
add('r.rep', 'Repertoire 15', 'Rhythm', 6, 5, '06 · Rhythm', 'Target weighting of the week: 15%.',
  'Enough to keep the list honest, not enough to replace practice.', { chapter: 'rhythm' });
add('r.record', 'Record 20', 'Rhythm', 6, 5, '06 · Rhythm', 'Target weighting of the week: 20%.',
  'One take a week keeps the ear honest about the hands.', { chapter: 'rhythm' });
add('r.air', 'Broadcast 15', 'Rhythm', 6, 5, '06 · Rhythm', 'Target weighting of the week: 15%.',
  'Out the door, but the door is not the work.', { chapter: 'rhythm' });
add('r.rest', 'Rest 10', 'Rhythm', 6, 4, '06 · Rhythm', 'Target weighting of the week: 10%.',
  'Deliberately left empty. The next week needs the gap.', { chapter: 'rhythm' });
add('r.legal', 'Legal scores only', 'Rhythm', 6, 5, '06 · Rhythm', 'Not a place for performance-teaching services or illegal sheet-music sharing.',
  'Copyrighted scores and recordings travel by legal channels only.', { chapter: 'rhythm' });
['r.practice', 'r.rep', 'r.record', 'r.air', 'r.rest', 'r.legal'].forEach((c) => link('ch.rhythm', c, 'contains'));

/* ── 07 · install ───────────────────────────────────────────────── */
add('i.manifest', 'Manifest', 'Install', 7, 5, '07 · Install', 'site.webmanifest plus a lilac P monogram.',
  'Add to Home Screen or install as an app; it opens in a standalone window.', { chapter: 'install', href: '/helena-piano/site.webmanifest' });
add('i.nows', 'No service worker', 'Install', 7, 4, '07 · Install', 'No service worker, so nothing is trapped in a cache.',
  'The page you open is always the current one.', { chapter: 'install' });
add('i.icon', 'P Monogram', 'Install', 7, 4, '07 · Install', 'icons/icon-192|512.png.',
  'A lilac P — a mark you can find on a small screen.', { chapter: 'install' });
add('i.eco', 'S21 Ecosystem', 'Install', 7, 5, '07 · Install', 'S21 Phone · Log · Faith · Piano · MetalCare, the same family.',
  'One name, different rooms; cross over from the eco-bar.', { chapter: 'install', href: 'https://helena751107.github.io/helena_phone/' });
['i.manifest', 'i.nows', 'i.icon', 'i.eco'].forEach((c) => link('ch.install', c, 'contains'));

/* ── cross-relations: the studio logic ─────────────────────────── */
[['z.practice', 'm.practice'], ['z.practice', 's.warm'], ['z.practice', 'c.minutes'], ['z.practice', 'r.practice'],
 ['z.rep', 'm.rep'], ['z.rep', 'r.rep'], ['z.rep', 'c.piece'],
 ['z.record', 'm.record'], ['z.record', 's.take'], ['z.record', 'r.record'],
 ['z.air', 'm.youtube'], ['z.air', 'g.youtube'], ['z.air', 'r.air'], ['z.air', 's.air'],
 ['m.practice', 'm.rep'], ['m.rep', 'm.record'], ['m.record', 'm.youtube'], ['m.youtube', 'm.archive'],
 ['s.warm', 'c.minutes'], ['s.work', 'c.block'], ['s.take', 'g.s21'], ['s.shape', 'c.craft'],
 ['s.air', 'g.youtube'], ['s.air', 'g.pages'], ['s.take', 's.shape'],
 ['c.block', 'c.next'], ['c.piece', 'c.next'], ['c.etiquette', 'c.name'], ['c.etiquette', 'i.eco'],
 ['c.name', 'g.youtube'], ['c.name', 'g.pages'], ['c.craft', 'g.pages'],
 ['r.practice', 'z.practice'], ['r.rep', 'z.rep'], ['r.record', 'z.record'], ['r.air', 'z.air'],
 ['r.legal', 'm.rep'], ['r.rest', 'c.next'],
 ['g.youtube', 'm.archive'], ['g.pages', 'i.manifest'], ['g.s21', 'i.eco'],
 ['i.nows', 'g.pages'], ['i.eco', HUB], ['i.manifest', HUB], ['i.manifest', 'i.nows'],
 ['c.craft', HUB], ['r.legal', HUB]
].forEach(([a, b]) => link(a, b, 'support'));

/* ── deterministic layout: chapter ring, entities orbiting their chapter ── */
const chapterOf = {};
SECTIONS.forEach((ch, i) => { chapterOf[ch] = i; });
const chapters = ['ch.pillars', 'ch.map', 'ch.method', 'ch.channels', 'ch.session', 'ch.rhythm', 'ch.install'];
const byId = new Map(N.map((n) => [n.id, n]));
const chapterPos = {};
N.forEach((n) => {
  const ch = n.chapter;
  if (n.id === HUB) { n.pos = [0, 46, 0]; return; }
  if (n.id.startsWith('ch.')) {
    const k = chapters.indexOf(n.id), a = (k / chapters.length) * Math.PI * 2 - Math.PI / 2;
    n.pos = [Math.cos(a) * 330, 36 + Math.sin(k * 1.7) * 38, Math.sin(a) * 330];
    chapterPos[n.chapter] = n.pos;
  }
});
const counts = {};
N.forEach((n) => { if (!n.id.startsWith('ch.') && n.id !== HUB) counts[n.chapter] = (counts[n.chapter] || 0) + 1; });
const seen = {};
N.forEach((n) => {
  if (n.id === HUB || n.id.startsWith('ch.')) return;
  const base = chapterPos[n.chapter] || [0, 0, 0];
  const k = (seen[n.chapter] = (seen[n.chapter] || 0) + 1) - 1;
  const a = k * 2.399963 + chapterOf[n.chapter] * 0.7;
  const r = 74 + (k % 3) * 26;
  const y = Math.sin(k * 1.3 + 0.6) * 46 + (k % 2 ? 16 : -12);
  n.pos = [base[0] + Math.cos(a) * r, base[1] + y, base[2] + Math.sin(a) * r];
});

export const NODES = N;
export const LINKS = L.filter((l) => byId.has(l.source) && byId.has(l.target));
export const CHAPTER_IDS = chapters;
export const chapterIndex = (id) => SECTIONS.indexOf(String(id || '').replace(/^ch\./, ''));
export const stats = {
  nodes: NODES.length,
  relations: LINKS.length,
  chapters: chapters.length,
  sources: new Set(NODES.map((n) => n.ref)).size
};
