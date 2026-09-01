import pathlib, re

HERE = pathlib.Path(__file__).parent
SRC = HERE / "home.html"
OUT = HERE / "pages"
OUT.mkdir(exist_ok=True)

src = SRC.read_text()

# Extract shared <head> content: everything from <title> through </style>
m = re.search(r'(.*?</style>)', src, re.S)
HEAD = m.group(1)

# ---------------------------------------------------------------------------
# Outbound links. Paste a URL in as it becomes available and rebuild - that is
# the only edit needed. A blank string renders a muted "coming soon" chip
# instead of a link, so the live site never ships a dead href="#".
#
# Google Forms need the RESPONDER link (Send -> link tab), which looks like
# /forms/d/e/1FAIpQLS.../viewform. An /edit link only works for the form owner.
# ---------------------------------------------------------------------------
REGISTER_HREF = "https://docs.google.com/forms/d/e/1FAIpQLScOa7TmpL-l7saAUh3yhFERfoQ56vIgvfBP2k9fAFf3bHbGrg/viewform"
USAW_HREF     = "https://www.usawmembership.com/login"
STORE_HREF    = ""   # team store - paste the shop URL here
SPONSOR_HREF  = "https://docs.google.com/forms/d/e/1FAIpQLSdJ6Hfl9D3JLc9kIt5DNIEoDrtCxOUjEuzjYAUBcYPKpY8NPg/viewform"
# NB: that form has a File Upload question, so Google forces responders to sign in
# to a Google account. Removing the upload question is what lifts that.
PAYMENT_HREF  = ""   # dues / payment portal


def pending_link(href, label, pending_label, style=""):
    """A button when we have a URL, a muted non-clickable chip when we don't."""
    style_attr = f' style="{style}"' if style else ""
    if href:
        return (f'<a class="btn" href="{href}" target="_blank" rel="noopener"'
                f'{style_attr}>{label}</a>')
    return (f'<span class="btn is-pending" aria-disabled="true"'
            f'{style_attr}>{pending_label}</span>')

DIVIDER = '<div class="claw-divider" role="presentation"><svg class="rake-svg" viewBox="0 0 64 46" width="128" height="42" aria-hidden="true"><path class="pA" transform="translate(4,13.0)" d="M-0.15,0.0 L-0.53,1.43 L-1.12,2.86 L-1.25,4.29 L-1.27,5.71 L-1.18,7.14 L-1.56,8.57 L-1.58,10.0 L-1.4,11.43 L-1.35,12.86 L-1.12,14.29 L-0.87,15.71 L-0.93,17.14 L-0.78,18.57 L-0.15,20.0 L0.15,20.0 L1.19,18.57 L1.71,17.14 L2.0,15.71 L2.53,14.29 L2.97,12.86 L3.15,11.43 L3.38,10.0 L3.32,8.57 L2.8,7.14 L2.68,5.71 L2.37,4.29 L1.9,2.86 L0.93,1.43 L0.15,0.0 Z"/><path class="pB" transform="translate(18,6.0)" d="M-0.15,0.0 L-1.08,2.43 L-0.83,4.86 L-0.89,7.29 L-1.54,9.71 L-1.09,12.14 L-1.07,14.57 L-1.39,17.0 L-1.2,19.43 L-1.51,21.86 L-1.08,24.29 L-1.45,26.71 L-0.94,29.14 L-0.86,31.57 L-0.15,34.0 L0.15,34.0 L1.53,31.57 L2.24,29.14 L3.32,26.71 L3.43,24.29 L4.22,21.86 L4.13,19.43 L4.39,17.0 L3.99,14.57 L3.79,12.14 L3.89,9.71 L2.76,7.29 L2.13,4.86 L1.75,2.43 L0.15,0.0 Z"/><path class="pC" transform="translate(32,0.0)" d="M-0.15,0.0 L-1.4,3.29 L-1.9,6.57 L-2.21,9.86 L-1.96,13.14 L-2.43,16.43 L-2.42,19.71 L-2.52,23.0 L-2.25,26.29 L-2.19,29.57 L-2.18,32.86 L-1.81,36.14 L-1.61,39.43 L-0.86,42.71 L-0.15,46.0 L0.15,46.0 L1.17,42.71 L2.22,39.43 L2.68,36.14 L3.27,32.86 L3.45,29.57 L3.61,26.29 L3.92,23.0 L3.79,19.71 L3.69,16.43 L3.06,13.14 L3.08,9.86 L2.51,6.57 L1.71,3.29 L0.15,0.0 Z"/><path class="pB" transform="translate(46,6.0)" d="M-0.15,0.0 L-1.6,2.43 L-2.55,4.86 L-2.85,7.29 L-3.89,9.71 L-3.8,12.14 L-4.32,14.57 L-4.06,17.0 L-4.37,19.43 L-3.77,21.86 L-3.71,24.29 L-3.18,26.71 L-2.51,29.14 L-1.44,31.57 L-0.15,34.0 L0.15,34.0 L0.77,31.57 L1.21,29.14 L1.31,26.71 L1.37,24.29 L1.07,21.86 L1.45,19.43 L1.06,17.0 L1.4,14.57 L1.1,12.14 L1.54,9.71 L0.98,7.29 L1.25,4.86 L0.93,2.43 L0.15,0.0 Z"/><path class="pA" transform="translate(60,13.0)" d="M-0.15,0.0 L-1.06,1.43 L-2.04,2.86 L-2.5,4.29 L-2.52,5.71 L-3.19,7.14 L-3.22,8.57 L-2.93,10.0 L-3.41,11.43 L-2.82,12.86 L-2.57,14.29 L-2.25,15.71 L-1.84,17.14 L-0.91,18.57 L-0.15,20.0 L0.15,20.0 L0.51,18.57 L1.06,17.14 L1.13,15.71 L1.16,14.29 L1.2,12.86 L1.66,11.43 L1.13,10.0 L1.47,8.57 L1.57,7.14 L1.11,5.71 L1.38,4.29 L1.26,2.86 L0.66,1.43 L0.15,0.0 Z"/></svg></div>'

def nav(active=""):
    return f'''<div class="bg-texture" aria-hidden="true"></div>

<header class="nav">
  <div class="nav-inner">
    <a class="brand" href="{{{{HOME_URL}}}}#home">
      <img src="data:image/webp;base64,__BADGE_B64__" alt="O-Town Wrestling Club badge">
      <span class="brand-text">
        <span class="big">O-TOWN</span>
        <span class="small">Wrestling Club</span>
      </span>
    </a>
    <nav class="links" id="navLinks">
      <a href="{{{{HOME_URL}}}}#home">Home</a>
      <a href="{{{{ABOUT_URL}}}}">About Us</a>
      <a href="{{{{HOME_URL}}}}#gallery">Gallery</a>
      <a href="{{{{HOME_URL}}}}#schedule">Schedule</a>
      <a href="{{{{SPONSORS_URL}}}}">Sponsors</a>
      <a href="{{{{STORE_URL}}}}">Store</a>
      <a href="{{{{CONTACT_URL}}}}">Contact Us</a>
    </nav>
    <a class="btn" href="{REGISTER_HREF}" target="_blank" rel="noopener"><span class="cta-long">Register Now</span><span class="cta-short">Register</span></a>
    <button class="nav-toggle" id="navToggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="navLinks"><span></span></button>
  </div>
</header>

<script>
(function(){{
  var header = document.querySelector('header.nav');
  var btn = document.getElementById('navToggle');
  if (!header || !btn) return;
  function setOpen(open){{
    header.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }}
  btn.addEventListener('click', function(){{
    setOpen(!header.classList.contains('open'));
  }});
  document.getElementById('navLinks').addEventListener('click', function(e){{
    if (e.target.tagName === 'A') setOpen(false);
  }});
  document.addEventListener('keydown', function(e){{
    if (e.key === 'Escape') setOpen(false);
  }});
}})();
</script>
'''

FOOTER = '''<footer>
  <div class="wrap">
    <div class="footer-cols">
      <div>
        <div class="footer-brand">
          <img src="data:image/webp;base64,__BADGE_B64__" alt="O-Town Wrestling Club badge">
          <span>O-Town Wrestling Club &middot; Mat Cats</span>
        </div>
        <p class="footer-tagline">Claws up, guns out. Youth and Jr/Sr High wrestling in Onalaska, Texas &mdash; ages 5 and up, no experience required.</p>
      </div>
      <div>
        <h4>Find Us</h4>
        <p>1885 FM 3459<br>Onalaska, TX 77360</p>
        <a href="tel:+18326065517" target="_top">832-606-5517</a>
        <a href="mailto:otownwrestlingclub@gmail.com" target="_top">otownwrestlingclub@gmail.com</a>
      </div>
      <div>
        <h4>Club</h4>
        <a href="{{ABOUT_URL}}">About Us</a>
        <a href="{{HANDBOOK_URL}}">Club Handbook</a>
        <a href="{{HOME_URL}}#schedule">Practice Schedule</a>
        <a href="{{SPONSORS_URL}}">Sponsors</a>
        <a href="{{STORE_URL}}">Team Store</a>
        <a href="{{CONTACT_URL}}">Contact Us</a>
      </div>
    </div>
    <div class="footer-inner">
      <div class="footer-meta">&copy; 2026 O-Town Wrestling Club &middot; All Rights Reserved</div>
      <a class="btn" href="''' + REGISTER_HREF + '''" target="_blank" rel="noopener">Register For The Season</a>
    </div>
  </div>
</footer>

<script>
(function(){
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    els.forEach(function(el){ el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if (entry.isIntersecting){
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  els.forEach(function(el, i){
    el.style.transitionDelay = Math.min(i % 4, 3) * 70 + 'ms';
    io.observe(el);
  });
})();
</script>
'''

ABOUT_SECTION = '''<section class="band" id="about-content">
  <div class="wrap">
    <div class="section-head">
      <div class="eyebrow label">Coaching Staff</div>
      <h2>THE CLAWS BEHIND <span class="accent">THE CATS</span></h2>
      <p class="deck">The coaches in the room every Wednesday and Thursday night, and the standard they hold the Mat Cats to.</p>
    </div>
    <div class="coach-grid">
      <div class="coach-card reveal">
        <div class="avatar">D</div>
        <span class="role-badge">Director</span>
        <h3 class="placeholder">Coach Announced Soon</h3>
        <p class="placeholder">Full staff bios go up before the season opener. Reach out any time in the meantime &mdash; we&rsquo;re happy to talk through the program.</p>
      </div>
      <div class="coach-card reveal">
        <div class="avatar">H</div>
        <span class="role-badge">Head Coach</span>
        <h3 class="placeholder">Coach Announced Soon</h3>
        <p class="placeholder">Full staff bios go up before the season opener. Reach out any time in the meantime &mdash; we&rsquo;re happy to talk through the program.</p>
      </div>
      <div class="coach-card reveal">
        <div class="avatar">A</div>
        <span class="role-badge">Assistant Coach</span>
        <h3 class="placeholder">Coach Announced Soon</h3>
        <p class="placeholder">Full staff bios go up before the season opener. Reach out any time in the meantime &mdash; we&rsquo;re happy to talk through the program.</p>
      </div>
    </div>
  </div>
</section>
'''

CONTACT_SECTION = '''<section class="band alt" id="contact-content">
  <div class="wrap">
    <div class="contact-panel">
      <div class="contact-map">
        <iframe src="https://maps.google.com/maps?q=1885+FM+3459,+Onalaska,+TX+77360&z=15&output=embed" title="Map to O-Town Wrestling Club" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        <a class="map-caption" href="https://maps.google.com/?q=1885+FM+3459,+Onalaska,+TX+77360" target="_blank" rel="noopener">1885 FM 3459, Onalaska, TX 77360 &middot; Get Directions</a>
      </div>
      <div class="contact-info">
        <div class="contact-row">
          <div class="icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 21s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg></div>
          <div>
            <div class="label">Practice Location</div>
            <div class="value">1885 FM 3459<br>Onalaska, TX 77360</div>
            <a class="contact-directions" href="https://maps.google.com/?q=1885+FM+3459,+Onalaska,+TX+77360" target="_blank" rel="noopener">
              Get Directions
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M7 7h10v10"/></svg>
            </a>
          </div>
        </div>
        <div class="contact-row">
          <div class="icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v4a2 2 0 0 1-2 2C9.5 21 3 14.5 3 6a2 2 0 0 1 2-2Z"/></svg></div>
          <div>
            <div class="label">Call Or Text</div>
            <a class="value" href="tel:+18326065517" target="_top">832-606-5517</a>
          </div>
        </div>
        <div class="contact-row">
          <div class="icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="4" width="20" height="16" rx="1.5"/><path d="m3 6 9 7 9-7"/></svg></div>
          <div>
            <div class="label">Email</div>
            <a class="value" href="mailto:otownwrestlingclub@gmail.com" target="_top">otownwrestlingclub@gmail.com</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

HANDBOOK_SECTION = '''<section class="band" id="handbook-content">
  <div class="wrap hb-layout">

    <nav class="hb-toc" aria-label="Handbook contents">
      <h4>Contents</h4>
      <a href="#hb-1">1. Who We Are</a>
      <a href="#hb-2">2. Season &amp; Practice</a>
      <a href="#hb-3">3. Before Your First Practice</a>
      <a href="#hb-4">4. What To Wear &amp; Bring</a>
      <a href="#hb-5">5. Health &amp; Skin Checks</a>
      <a href="#hb-6">6. Weight &amp; Nutrition</a>
      <a href="#hb-7">7. Your First Tournament</a>
      <a href="#hb-8">8. How Scoring Works</a>
      <a href="#hb-9">9. Code Of Conduct</a>
      <a href="#hb-10">10. Staying In Touch</a>
      <a href="#hb-11">11. Common Questions</a>
    </nav>

    <div>

      <section class="hb-sec reveal" id="hb-1">
        <h2><span class="n">01</span>WHO WE ARE</h2>
        <p>O-Town Wrestling Club is a youth and junior/senior high wrestling club based in Onalaska, Texas. We are open to <strong>anyone age 5 and up</strong>, with no experience required and no tryout to get through. First-year beginners and returning competitors train in the same room, grouped by age and worked at their own level.</p>
        <p>Wrestling asks more of a kid than most sports. There is no bench to hide on and no teammate to pass to &mdash; when the whistle blows it is one wrestler against one wrestler. That is exactly why it builds what it builds: conditioning, composure, and the specific kind of confidence that only comes from being tested and finding out you can handle it.</p>
        <p>Our job is to teach the sport safely, fairly, and well. Your wrestler&rsquo;s job is to show up and work. This handbook covers what to expect from both sides.</p>
      </section>

      <section class="hb-sec reveal" id="hb-2">
        <h2><span class="n">02</span>SEASON &amp; PRACTICE</h2>
        <p>The folkstyle season runs from <strong>September through April</strong>. Practices are held on <strong>Wednesdays and Thursdays</strong> at the club mat room, 1885 FM 3459, Onalaska, TX 77360.</p>
        <dl class="hb-rows">
          <div class="hb-row"><dt>Youth</dt><dd>6:00 &ndash; 7:30 PM, Wednesday &amp; Thursday</dd></div>
          <div class="hb-row"><dt>Jr / Sr High</dt><dd>4:00 &ndash; 5:30 PM, Wednesday &amp; Thursday</dd></div>
        </dl>
        <p>The live practice calendar on the <a href="{{HOME_URL}}#schedule" style="color:var(--rose);">schedule page</a> is the authority on dates. Cancellations &mdash; weather, holidays, facility closures &mdash; are marked in red there as soon as we know about them, so check it before you drive out if you are unsure.</p>
        <h3>Attendance</h3>
        <p>Wrestling is a skill sport built by repetition. Kids who come consistently improve quickly; kids who come occasionally tend to stall out and get frustrated, which is the most common reason a first-year wrestler quits. We are not going to bench anyone for missing practice, but we will be honest with you: consistency is most of the result.</p>
        <p>If your wrestler will be out for an extended stretch &mdash; injury, another sport, family reasons &mdash; let a coach know so we can plan their return sensibly rather than dropping them back into full contact cold.</p>
      </section>

      <section class="hb-sec reveal" id="hb-3">
        <h2><span class="n">03</span>BEFORE YOUR FIRST PRACTICE</h2>
        <p>Two things have to be in place before your wrestler takes the mat: club registration and a current USA Wrestling card. Come by, meet the coaches, and see the room any practice night &mdash; but get the card sorted before their first session, because it is what insures them on the mat.</p>
        <h3>Coming to your first session</h3>
        <ul>
          <li>Show up a few minutes early and introduce yourself to a coach.</li>
          <li>Wear a t&#8209;shirt and shorts. No singlet or special gear to buy up front.</li>
          <li>Bring water.</li>
          <li>Have the USA Wrestling card number with you.</li>
        </ul>
        <h3>To join the club</h3>
        <ul>
          <li><strong>Club registration.</strong> Complete the registration form linked throughout this site.</li>
          <li><strong>USA Wrestling membership.</strong> <strong>Required for every wrestler, for practices as well as tournaments.</strong> The card carries the athlete insurance that covers mat time, so it has to be current before your wrestler steps on the mat &mdash; not just before their first competition. Purchased directly from USA Wrestling, not from the club. Keep the card number somewhere you can find it; you will need it at every tournament entry.</li>
          <li><strong>Season dues.</strong> Contact the club for current rates and payment options.</li>
        </ul>
        <div class="hb-note">
          <strong>A note on the physical</strong>
          <p>Requirements vary by event and by school district. Some tournaments and most school-affiliated programs require a current sports physical on file. If your wrestler is also competing for a school team, follow that program&rsquo;s requirements &mdash; they are usually the stricter of the two.</p>
        </div>
      </section>

      <section class="hb-sec reveal" id="hb-4">
        <h2><span class="n">04</span>WHAT TO WEAR &amp; BRING</h2>
        <h3>Practice</h3>
        <ul>
          <li><strong>Athletic t&#8209;shirt and shorts.</strong> Avoid zippers, buttons, snaps, and pockets &mdash; they catch fingers and tear mats. Compression shorts or leggings work well.</li>
          <li><strong>Wrestling shoes</strong> once your wrestler is committed. They protect ankles and grip the mat far better than sneakers. Street shoes are never worn on the mat.</li>
          <li><strong>Headgear</strong> to protect the ears. Not optional once live wrestling starts.</li>
          <li><strong>Water bottle</strong> with a name on it.</li>
          <li><strong>Mouthguard</strong> if your wrestler has braces.</li>
        </ul>
        <h3>Competition</h3>
        <ul>
          <li><strong>Singlet</strong>, or the two&#8209;piece alternative where the event allows it. Check the specific tournament&rsquo;s rules.</li>
          <li>Wrestling shoes and headgear.</li>
          <li>Warm&#8209;ups, a towel, and a change of clothes for after weigh&#8209;ins.</li>
          <li>Food and water for a long day &mdash; see section 7.</li>
        </ul>
        <h3>Grooming</h3>
        <ul>
          <li><strong>Fingernails and toenails cut short.</strong> Officials check, and long nails are the most common source of scratches on the mat.</li>
          <li>Long hair tied back or contained in a hair cover.</li>
          <li>No jewelry, including earrings. Take them out before you come.</li>
        </ul>
      </section>

      <section class="hb-sec reveal" id="hb-5">
        <h2><span class="n">05</span>HEALTH &amp; SKIN CHECKS</h2>
        <p>This is the section parents new to wrestling most often skip and most often regret skipping. Wrestling involves constant skin&#8209;to&#8209;skin and skin&#8209;to&#8209;mat contact, which makes skin infections the sport&rsquo;s most common non&#8209;orthopedic problem. They are also almost entirely preventable.</p>
        <h3>The routine that prevents nearly all of it</h3>
        <ul>
          <li><strong>Shower right after every practice</strong> &mdash; not later that evening. Soap and water, all over.</li>
          <li><strong>Wash practice clothes after every single session.</strong> Not twice a week.</li>
          <li>Wipe down headgear, kneepads, and shoes regularly.</li>
          <li>Never share towels, water bottles, or gear.</li>
        </ul>
        <h3>If something shows up on the skin</h3>
        <p>Tell a coach and see a doctor promptly. Ringworm, impetigo, and herpes gladiatorum are the usual suspects, and all three are treatable and contagious &mdash; the sooner they are handled, the less mat time your wrestler loses and the less likely it spreads to teammates.</p>
        <p>At tournaments, wrestlers are visually checked for skin conditions before they are allowed to compete. A wrestler with an untreated or undocumented condition <strong>will be turned away at the door</strong>, regardless of how far you drove. If your wrestler is being treated for something, bring a signed physician&rsquo;s note stating the diagnosis, the treatment, and that they are cleared to compete.</p>
        <div class="hb-note">
          <strong>Keep a kid home when</strong>
          <p>They have a fever, are actively vomiting, or have an open or draining skin lesion that has not been seen by a doctor. Nobody wins when one sick wrestler puts the whole room out for a week.</p>
        </div>
        <h3>Injuries</h3>
        <p>Report every injury to a coach the day it happens, however minor it looks. Small things that get trained through become big things. If a doctor restricts your wrestler in any way, tell us what the restriction is and we will work within it rather than guess.</p>
      </section>

      <section class="hb-sec reveal" id="hb-6">
        <h2><span class="n">06</span>WEIGHT &amp; NUTRITION</h2>
        <div class="hb-note">
          <strong>We do not cut weight at this club</strong>
          <p>Not for youth wrestlers, and not for the sake of a bracket. A growing athlete who is dehydrated or underfed does not wrestle better &mdash; they wrestle slower, they get hurt more, and they burn out on the sport. If you ever hear otherwise from anyone, come talk to a coach.</p>
        </div>
        <p>Wrestlers compete in weight classes so that they face opponents of similar size. The right approach for a young athlete is simple: <strong>eat normally, train hard, and wrestle at the weight you naturally are.</strong> Bodies change a lot across a season at these ages, and the classes are wide enough to absorb that.</p>
        <h3>Practical eating around competition</h3>
        <ul>
          <li>A real meal the night before, and breakfast the morning of. Hungry wrestlers gas out in the third period.</li>
          <li>Drink water throughout the day, not all at once between matches.</li>
          <li>Pack food you know they will actually eat. Tournament concession stands are unpredictable and expensive.</li>
          <li>Something light and familiar between matches beats a big meal.</li>
        </ul>
      </section>

      <section class="hb-sec reveal" id="hb-7">
        <h2><span class="n">07</span>YOUR FIRST TOURNAMENT</h2>
        <p>Nobody is entered in a bracket before they are ready for one. When a coach thinks your wrestler is prepared, we will tell you, and the decision to go is yours.</p>
        <p>We compete on the <strong>TX&#8209;USAW South Region</strong> circuit &mdash; events around Spring, Bryan, Katy, and the surrounding area, with state&#8209;level tournaments later in the season. The event list lives on the <a href="{{HOME_URL}}#schedule" style="color:var(--rose);">schedule page</a>.</p>
        <h3>How the day actually goes</h3>
        <dl class="hb-rows">
          <div class="hb-row"><dt>Weigh&#8209;ins</dt><dd>Early, and usually well before wrestling starts. Get there when the event says to, not when you think matches begin.</dd></div>
          <div class="hb-row"><dt>Skin check</dt><dd>Happens at or near weigh&#8209;in. See section 5.</dd></div>
          <div class="hb-row"><dt>Bracketing</dt><dd>Wrestlers are grouped by age and weight after weigh&#8209;ins, so brackets are not posted until then.</dd></div>
          <div class="hb-row"><dt>Wrestling</dt><dd>Multiple mats run at once. Listen for your wrestler&rsquo;s mat and bout number being called.</dd></div>
          <div class="hb-row"><dt>Duration</dt><dd>Expect most of a day. Matches are short; the waiting between them is not.</dd></div>
        </dl>
        <h3>What to bring</h3>
        <ul>
          <li>Everything from the competition list in section 4.</li>
          <li>Food, water, and snacks for the whole day.</li>
          <li>Folding chairs. Gym seating runs out fast.</li>
          <li>Cash for admission and concessions &mdash; not every event takes cards.</li>
          <li>Something to keep a kid occupied between matches.</li>
        </ul>
        <div class="hb-note">
          <strong>Expect to lose some matches</strong>
          <p>Nearly every wrestler loses early and often in their first season, including the ones who go on to be very good. That is the sport working as designed, not a sign your kid is in the wrong place. What matters is what they do at the next practice.</p>
        </div>
      </section>

      <section class="hb-sec reveal" id="hb-8">
        <h2><span class="n">08</span>HOW SCORING WORKS</h2>
        <p>Folkstyle is the style wrestled in American schools and clubs, and it rewards control. A match is won by pin, by accumulating more points than your opponent, or by technical superiority if the point gap gets large enough.</p>
        <h3>The fastest way to win</h3>
        <p>A <strong>pin</strong> &mdash; also called a fall &mdash; holds both of the opponent&rsquo;s shoulders to the mat for long enough for the official to count it. A pin ends the match instantly no matter what the score is.</p>
        <h3>Points</h3>
        <dl class="hb-rows">
          <div class="hb-row"><dt>Takedown &mdash; 3</dt><dd>From neutral, taking the opponent down and establishing control.</dd></div>
          <div class="hb-row"><dt>Escape &mdash; 1</dt><dd>Getting out from underneath and back to a neutral, facing position.</dd></div>
          <div class="hb-row"><dt>Reversal &mdash; 2</dt><dd>Going from underneath straight to being the one in control.</dd></div>
          <div class="hb-row"><dt>Near fall &mdash; 2 to 4</dt><dd>Holding the opponent&rsquo;s shoulders near the mat without a pin. The longer the hold, the more points.</dd></div>
          <div class="hb-row"><dt>Penalty points</dt><dd>Awarded to the opponent for illegal holds, stalling, and other infractions.</dd></div>
        </dl>
        <p>Matches run several short periods, with the exact length varying by age division. Wrestlers start neutral and then alternate starting positions.</p>
        <div class="hb-note">
          <strong>Rules change</strong>
          <p>Point values and period lengths get revised periodically &mdash; the takedown moved from 2 points to 3 in recent seasons. <a href="https://www.usawrestling.org/" target="_blank" rel="noopener" style="color:var(--rose);">USA Wrestling</a> publishes the current rulebook, and it governs at sanctioned events. When in doubt, the official on the mat is right.</p>
        </div>
      </section>

      <section class="hb-sec reveal" id="hb-9">
        <h2><span class="n">09</span>CODE OF CONDUCT</h2>
        <h3>Wrestlers</h3>
        <ul>
          <li>Show up on time and ready to work.</li>
          <li>Listen the first time. Mat time is short.</li>
          <li>Take care of your practice partner. They are the reason you improve.</li>
          <li>Shake hands before and after every match, win or lose, and shake the opposing coach&rsquo;s hand.</li>
          <li>No trash talk, no celebrating over a beaten opponent, no arguing with officials.</li>
          <li>Losing is allowed. Quitting mid&#8209;match is not.</li>
        </ul>
        <h3>Parents &amp; spectators</h3>
        <ul>
          <li><strong>Let the coaches coach.</strong> A wrestler hearing instructions from two directions hears neither. Cheer as loud as you want &mdash; just do not coach from the stands.</li>
          <li><strong>Leave the officials alone.</strong> They are often volunteers, calls will not always go your way, and no official has ever reversed a decision because a parent shouted.</li>
          <li>Be a good guest in someone else&rsquo;s gym. Clean up your space.</li>
          <li>Support every wrestler in the room, not only your own.</li>
          <li>The car ride home is the moment a kid decides whether they love this sport. &ldquo;I loved watching you wrestle&rdquo; goes a long way further than a breakdown of their mistakes.</li>
        </ul>
        <div class="hb-note">
          <strong>The short version</strong>
          <p>Conduct that embarrasses the club, abuses an official, or makes the room unsafe for kids ends a family&rsquo;s participation. We have never expected to need this paragraph and would rather never use it.</p>
        </div>
      </section>

      <section class="hb-sec reveal" id="hb-10">
        <h2><span class="n">10</span>STAYING IN TOUCH</h2>
        <p>The <a href="{{HOME_URL}}#schedule" style="color:var(--rose);">practice calendar</a> on this site is kept current and is the fastest way to confirm whether a session is on. Cancellations show up there in red.</p>
        <dl class="hb-rows">
          <div class="hb-row"><dt>Call or text</dt><dd><a href="tel:+18326065517" target="_top" style="color:var(--rose);">832-606-5517</a></dd></div>
          <div class="hb-row"><dt>Email</dt><dd><a href="mailto:otownwrestlingclub@gmail.com" target="_top" style="color:var(--rose);">otownwrestlingclub@gmail.com</a></dd></div>
          <div class="hb-row"><dt>Mat room</dt><dd>1885 FM 3459, Onalaska, TX 77360</dd></div>
        </dl>
        <p>If something is not working for your family &mdash; the schedule, the cost, how your wrestler is being coached &mdash; tell us early. Almost everything is fixable if we hear about it.</p>
      </section>

      <section class="hb-sec reveal" id="hb-11">
        <h2><span class="n">11</span>COMMON QUESTIONS</h2>
        <h3>My child has never wrestled. Is it too late to start?</h3>
        <p>No. Most of our wrestlers started with no experience, and beginners are the majority of any youth room. Kids who start later often catch up quickly because they are more coordinated when they begin.</p>
        <h3>Is wrestling safe?</h3>
        <p>It is a full&#8209;contact sport and injuries happen, as in any sport. What makes wrestling comparatively safe is that there are no projectiles, no high&#8209;speed collisions, and every athlete is matched by age and weight. Beginners spend their first sessions learning stance, motion, and how to fall properly before any live wrestling.</p>
        <h3>Does my child have to compete?</h3>
        <p>No. Plenty of kids practice all season for the conditioning, the skills, and the room, and never enter a tournament. Competing is available when your wrestler wants it and a coach agrees they are ready.</p>
        <h3>How much does it cost?</h3>
        <p>Season dues plus a USA Wrestling membership, and shoes and headgear once your wrestler commits. Contact us for current dues.</p>
        <h3>What if we can only make one practice a week?</h3>
        <p>Come to the one. One practice a week beats none, and we would rather have your wrestler in the room part time than not at all.</p>
        <h3>My child wants to quit mid&#8209;season.</h3>
        <p>Very common, usually around the first hard loss or the first tough practice. Talk to a coach before you make the call &mdash; it is often a fixable thing like a mismatched partner or a skill they are stuck on, and pushing through it is where most of the growth in this sport actually lives.</p>
      </section>

    </div>
  </div>
</section>
'''

SPONSOR_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
STORE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 2 3 7v13a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V7l-3-5Z"/><path d="M3 7h18M8 11a4 4 0 0 0 8 0"/></svg>'

def sponsor_cards(n):
    cards = []
    for i in range(n):
        cards.append(f'''      <div class="info-card reveal">
        <div class="icon-circle">{SPONSOR_ICON}</div>
        <h3>Your Name Here</h3>
        <p>Sponsorship spot open</p>
      </div>''')
    return "\n".join(cards)

def store_cards(items):
    cards = []
    for name in items:
        cards.append(f'''      <div class="info-card reveal">
        <div class="icon-circle">{STORE_ICON}</div>
        <h3>{name}</h3>
        <p>Opening soon</p>
        <div class="price">$--</div>
      </div>''')
    return "\n".join(cards)

def set_title(page_html, title):
    # No '^' anchor: the shared head starts with the charset meta, not <title>,
    # so anchoring silently matched nothing and every page shipped the same title.
    out, n = re.subn(r'<title>.*?</title>', f'<title>{title}</title>', page_html, count=1)
    if n != 1:
        raise SystemExit(f"set_title matched {n} times for {title!r} - expected 1")
    return out

ABOUT_PAGE = HEAD + "\n" + nav("about") + f'''
<section class="page-header">
  <div class="wrap">
    <a class="back-home" href="{{HOME_URL}}#home"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>Back To Home</a>
    <div class="eyebrow label">O-Town Wrestling Club</div>
    <h1>ABOUT <span class="accent">US</span></h1>
    <p class="deck">Where the Mat Cats are made &mdash; our coaching staff, our story, and what we&rsquo;re building in Onalaska.</p>
    <a class="btn" href="{{HANDBOOK_URL}}" style="margin-top:1.8rem;">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="17" height="17"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/></svg>
      View Club Handbook
    </a>
  </div>
</section>

{DIVIDER}

{ABOUT_SECTION}
{FOOTER}'''
ABOUT_PAGE = set_title(ABOUT_PAGE, "About Us &middot; O-Town Mat Cats")

CONTACT_PAGE = HEAD + "\n" + nav("contact") + f'''
<section class="page-header">
  <div class="wrap">
    <a class="back-home" href="{{HOME_URL}}#home"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>Back To Home</a>
    <div class="eyebrow label">Get In Touch</div>
    <h1>CONTACT <span class="accent">THE CLUB</span></h1>
    <p class="deck">Questions about registration, practice, or the season? Reach out any way that works.</p>
  </div>
</section>

{DIVIDER}

{CONTACT_SECTION}
{FOOTER}'''
CONTACT_PAGE = set_title(CONTACT_PAGE, "Contact Us &middot; O-Town Mat Cats")

SPONSORS_PAGE = HEAD + "\n" + nav("sponsors") + f'''
<section class="page-header">
  <div class="wrap">
    <a class="back-home" href="{{HOME_URL}}#home"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>Back To Home</a>
    <div class="eyebrow label">Back The Cats</div>
    <h1>OUR <span class="accent">SPONSORS</span></h1>
    <p class="deck">Local businesses and families keep this club on the mat &mdash; covering singlets, tournament entries, and travel for kids who might not otherwise get to compete.</p>
    {pending_link(SPONSOR_HREF, "Become A Sponsor", "Sponsor Form Coming Soon", style="margin-top:1.8rem;")}
  </div>
</section>

{DIVIDER}

<section class="band" id="sponsors-content">
  <div class="wrap">
    <div class="section-head reveal">
      <div class="eyebrow label">Founding Season</div>
      <h2>SPOTS <span class="accent">STILL OPEN</span></h2>
      <p class="deck">2026&ndash;27 is our first season. Sponsors who come in now get their name on the mat from day one.</p>
    </div>
    <div class="info-grid">
{sponsor_cards(6)}
    </div>
  </div>
</section>
{FOOTER}'''
SPONSORS_PAGE = set_title(SPONSORS_PAGE, "Our Sponsors &middot; O-Town Mat Cats")

STORE_PAGE = HEAD + "\n" + nav("store") + f'''
<section class="page-header">
  <div class="wrap">
    <a class="back-home" href="{{HOME_URL}}#home"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>Back To Home</a>
    <div class="eyebrow label">Gear Up</div>
    <h1>CLUB <span class="accent">STORE</span></h1>
    <p class="deck">O-Town Mat Cats apparel and gear. The shop opens ahead of the first tournament &mdash; tees, singlets, hoodies, and sideline gear.</p>
    {pending_link(STORE_HREF, "Shop The Store", "Shop Opening Soon", style="margin-top:1.8rem;")}
  </div>
</section>

{DIVIDER}

<section class="band" id="store-content">
  <div class="wrap">
    <div class="info-grid">
{store_cards(["Mat Cats Tee", "Practice Singlet", "Competition Singlet", "Zip Hoodie", "Trucker Hat", "Water Bottle"])}
    </div>
  </div>
</section>
{FOOTER}'''
STORE_PAGE = set_title(STORE_PAGE, "Club Store &middot; O-Town Mat Cats")

HANDBOOK_PAGE = HEAD + "\n" + nav("handbook") + f'''
<section class="page-header">
  <div class="wrap">
    <a class="back-home" href="{{ABOUT_URL}}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>Back To About Us</a>
    <div class="eyebrow label">2026&ndash;27 Season</div>
    <h1>CLUB <span class="accent">HANDBOOK</span></h1>
    <p class="deck">Everything a new Mat Cats family needs &mdash; practice, gear, health, tournaments, and what we expect from each other.</p>
  </div>
</section>

{DIVIDER}

{HANDBOOK_SECTION}
{FOOTER}'''
HANDBOOK_PAGE = set_title(HANDBOOK_PAGE, "Club Handbook &middot; O-Town Mat Cats")

(OUT / "about.html").write_text(ABOUT_PAGE)
(OUT / "contact.html").write_text(CONTACT_PAGE)
(OUT / "sponsors.html").write_text(SPONSORS_PAGE)
(OUT / "store.html").write_text(STORE_PAGE)
(OUT / "handbook.html").write_text(HANDBOOK_PAGE)

print("wrote 5 page templates")
