// Case Viewer — minimal JS (~50 lines)
(function () {
  'use strict';

  function flash(msg) {
    const n = document.createElement('div');
    n.textContent = msg;
    n.className = 'fixed top-4 right-4 z-50 bg-brand-navy text-white px-4 py-2 rounded-md shadow-lg text-sm';
    document.body.appendChild(n);
    setTimeout(() => n.remove(), 2000);
  }

  // Copy link buttons
  document.querySelectorAll('[data-copy-link]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        flash('Link copied');
      } catch (e) {
        flash('Copy failed — please copy the URL manually');
      }
    });
  });

  // Preview modal
  const modal = document.getElementById('preview-modal');
  const frame = document.getElementById('preview-frame');
  const title = document.getElementById('preview-title');

  function openPreview(url, name) {
    if (!modal || !frame) return;
    frame.src = url;
    if (title) title.textContent = name || 'Preview';
    modal.classList.remove('hidden');
    modal.classList.add('flex', 'open');
  }
  function closePreview() {
    if (!modal || !frame) return;
    frame.src = 'about:blank';
    modal.classList.add('hidden');
    modal.classList.remove('flex', 'open');
  }

  document.querySelectorAll('[data-preview]').forEach((btn) => {
    btn.addEventListener('click', () => openPreview(btn.dataset.preview, btn.dataset.title));
  });
  document.querySelectorAll('[data-close-preview]').forEach((btn) => btn.addEventListener('click', closePreview));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closePreview(); });
  if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) closePreview(); });

  // Request-doc buttons → fire WF-CP-02 (placeholder: just confirm)
  document.querySelectorAll('[data-request-doc]').forEach((btn) => {
    btn.addEventListener('click', () => {
      flash('Request sent for: ' + btn.dataset.requestDoc);
    });
  });

  // Auto-scroll timeline to latest
  const tl = document.getElementById('timeline-list');
  if (tl) tl.scrollTop = tl.scrollHeight;
})();
