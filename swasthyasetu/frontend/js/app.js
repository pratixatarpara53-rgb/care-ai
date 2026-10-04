/**
 * SwasthyaSetu AI – Main Application Logic
 * Handles navigation, API calls, and UI rendering
 */

const API_BASE = "/api";

// ── Navigation ──────────────────────────────────────────────────

function showSection(id) {
  document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const section = document.getElementById(id);
  if (section) section.classList.add('active');
  const navBtn = document.querySelector(`.nav-btn[data-section="${id}"]`);
  if (navBtn) navBtn.classList.add('active');
  window.scrollTo(0, 0);
  if (id === 'section-dashboard') loadDashboard();
  if (id === 'section-followup') loadFollowups();
}

document.addEventListener('DOMContentLoaded', () => {
  // Navigation buttons
  document.querySelectorAll('.nav-btn[data-section]').forEach(btn => {
    btn.addEventListener('click', () => showSection(btn.getAttribute('data-section')));
  });

  // Forms
  setupForms();
  showSection('section-home');
});

// ── Toast Notifications ─────────────────────────────────────────

function showToast(message, type = '') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  // v3 CSS uses: .toast-success / .toast-error / .toast-info
  toast.className = 'toast' + (type ? ' toast-' + type : '');
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// ── Generic API helper ──────────────────────────────────────────

async function apiFetch(endpoint, method = 'GET', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  const resp = await fetch(`${API_BASE}${endpoint}`, opts);
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${resp.status}`);
  }
  return resp.json();
}

// ── Set loading state on button ─────────────────────────────────

function setLoading(btnId, loadingText, isLoading) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.disabled = isLoading;
  if (isLoading) {
    btn._origText = btn.innerHTML;
    btn.innerHTML = `<span class="loading"></span>${loadingText}`;
  } else {
    btn.innerHTML = btn._origText || btn.innerHTML;
  }
}

// ── Response box display ────────────────────────────────────────

function showResponse(boxId, content, type = '') {
  const box = document.getElementById(boxId);
  if (!box) return;
  box.className = `response-box visible ${type}`;
  box.innerHTML = content;
}

function hideResponse(boxId) {
  const box = document.getElementById(boxId);
  if (box) box.classList.remove('visible');
}

// ═══════════════════════════════════════════════════════════════
// Agent 1 – Health Guidance
// ═══════════════════════════════════════════════════════════════

function setupForms() {
  // ── Health Guidance Form ──
  const guidanceForm = document.getElementById('form-guidance');
  if (guidanceForm) {
    guidanceForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const question = document.getElementById('inp-question').value.trim();
      const language = document.getElementById('inp-lang').value;
      const patient_name = document.getElementById('inp-patient-guidance').value.trim();
      if (!question) return showToast('Please enter a health question.', 'error');

      setLoading('btn-guidance', t('guidanceLoading'), true);
      hideResponse('response-guidance');

      try {
        const data = await apiFetch('/health-guidance', 'POST', { question, language, patient_name });
        const html = `
          <div style="margin-bottom:.75rem;">
            <strong>💬 ${data.question}</strong>
          </div>
          <div style="white-space:pre-wrap;line-height:1.8;">${escapeHtml(data.response)}</div>
          <div style="margin-top:1rem;padding:.75rem;background:rgba(0,0,0,.04);border-radius:8px;font-size:.83rem;color:var(--text-muted);">
            ⚠️ <em>${escapeHtml(data.disclaimer)}</em>
          </div>`;
        showResponse('response-guidance', html, '');
      } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
      } finally {
        setLoading('btn-guidance', '', false);
      }
    });
  }

  // ── Risk Screening Form ──
  const riskForm = document.getElementById('form-risk');
  if (riskForm) {
    riskForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const symptoms = document.getElementById('inp-symptoms').value.trim();
      const age = document.getElementById('inp-age').value.trim();
      const gender = document.getElementById('inp-gender').value;
      const patient_name = document.getElementById('inp-patient-risk').value.trim();
      if (!symptoms) return showToast('Please describe your symptoms.', 'error');

      setLoading('btn-risk', t('riskLoading'), true);
      hideResponse('response-risk');

      try {
        const data = await apiFetch('/risk-screening', 'POST', { symptoms, age, gender, patient_name });
        const level = (data.risk_level || 'MODERATE').toLowerCase();
        const badgeColor = { low: '#166534', moderate: '#92400e', urgent: '#991b1b' }[level] || '#1e293b';
        const badgeBg   = { low: '#dcfce7', moderate: '#fef3c7', urgent: '#fee2e2' }[level] || '#f1f5f9';
        const emergencyHtml = data.is_emergency ? `
          <div style="background:#7f1d1d;color:#fff;padding:1rem;border-radius:8px;margin:1rem 0;font-size:1.1rem;font-weight:700;">
            🚨 EMERGENCY: Call 108 immediately or go to the nearest hospital!
          </div>` : '';

        const html = `
          ${emergencyHtml}
          <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:1rem;flex-wrap:wrap;">
            <span style="font-weight:700;">Risk Level:</span>
            <span style="background:${badgeBg};color:${badgeColor};padding:.3rem 1rem;border-radius:20px;font-weight:700;font-size:.9rem;text-transform:uppercase;">
              ${data.risk_level}
            </span>
          </div>
          <div style="white-space:pre-wrap;line-height:1.8;">${escapeHtml(data.raw_response)}</div>
          <div style="margin-top:1rem;padding:.75rem;background:rgba(0,0,0,.05);border-radius:8px;font-size:.83rem;color:var(--text-muted);">
            ⚠️ <em>${escapeHtml(data.disclaimer)}</em>
          </div>`;
        showResponse('response-risk', html, level);
        // Store risk level for navigation
        window._lastRiskLevel = data.risk_level;
        window._lastSymptoms  = symptoms;
      } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
      } finally {
        setLoading('btn-risk', '', false);
      }
    });

    // Go to navigation button
    const goNavBtn = document.getElementById('btn-go-navigation');
    if (goNavBtn) {
      goNavBtn.addEventListener('click', () => {
        if (window._lastSymptoms)  document.getElementById('inp-nav-symptoms').value = window._lastSymptoms;
        if (window._lastRiskLevel) document.getElementById('inp-nav-risk').value      = window._lastRiskLevel;
        showSection('section-navigation');
      });
    }
  }

  // ── Care Navigation Form ──
  const navForm = document.getElementById('form-navigation');
  if (navForm) {
    navForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const symptoms    = document.getElementById('inp-nav-symptoms').value.trim();
      const risk_level  = document.getElementById('inp-nav-risk').value;
      const location    = document.getElementById('inp-nav-location').value.trim();
      const patient_name = document.getElementById('inp-patient-nav').value.trim();
      if (!symptoms) return showToast('Please describe your health concern.', 'error');

      setLoading('btn-navigation', t('navLoading'), true);
      hideResponse('response-navigation');

      try {
        const data = await apiFetch('/care-navigation', 'POST', { symptoms, risk_level, location, patient_name });
        const p = data.recommended_pathway;
        const isEmergency = p.key === 'EMERGENCY_SERVICES';

        // v3 CSS: .pathway-card .pc-icon
        const html = `
          <div class="pathway-card" style="border-color:${p.color || '#1a6b3c'};background:${hexToAlpha(p.color || '#1a6b3c', 0.06)};">
            <div class="pc-icon">${p.icon || '🏥'}</div>
            <h3 style="color:${p.color || '#1a6b3c'};">${escapeHtml(p.title)}</h3>
            <p>${escapeHtml(p.description)}</p>
            ${isEmergency ? '<p style="font-weight:700;color:#dc2626;">📞 Dial 108 for FREE ambulance anywhere in India!</p>' : ''}
            <hr style="margin:.75rem 0;border:none;border-top:1px solid rgba(0,0,0,.1);">
            <p><strong>Why this pathway?</strong><br>${escapeHtml(data.reason || '')}</p>
            ${data.next_steps ? `<p style="margin-top:.5rem;"><strong>Next Steps:</strong><br>${escapeHtml(data.next_steps)}</p>` : ''}
            <p style="margin-top:.75rem;font-size:.82rem;color:var(--text-muted);">ℹ️ ${escapeHtml(data.disclaimer)}</p>
          </div>`;
        showResponse('response-navigation', html, '');
      } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
      } finally {
        setLoading('btn-navigation', '', false);
      }
    });
  }

  // ── Follow-up Form ──
  const fuForm = document.getElementById('form-followup');
  if (fuForm) {
    fuForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const patient_name     = document.getElementById('fu-patient').value.trim();
      const concern          = document.getElementById('fu-concern').value.trim();
      const recommended_date = document.getElementById('fu-date').value;
      const notes            = document.getElementById('fu-notes').value.trim();
      const pathway          = document.getElementById('fu-pathway').value;
      const contact          = document.getElementById('fu-contact').value.trim();

      if (!patient_name || !concern) return showToast('Patient name and concern are required.', 'error');

      setLoading('btn-followup', t('fuLoading'), true);
      try {
        await apiFetch('/followup', 'POST', { patient_name, concern, recommended_date, notes, pathway, contact });
        showToast('Follow-up created successfully!', 'success');
        fuForm.reset();
        loadFollowups();
        const listTab = document.querySelector('.tab-btn[data-tab="tab-list"]');
        if (listTab) listTab.click();
      } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
      } finally {
        setLoading('btn-followup', '', false);
      }
    });
  }

  // ── Medicine Reminder Form ──
  const medForm = document.getElementById('form-medicine');
  if (medForm) {
    medForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const patient_name  = document.getElementById('med-patient').value.trim();
      const medicine_name = document.getElementById('med-name').value.trim();
      const reminder_time = document.getElementById('med-time').value.trim();
      const frequency     = document.getElementById('med-freq').value;
      const notes         = document.getElementById('med-notes').value.trim();

      if (!patient_name || !medicine_name || !reminder_time) {
        return showToast('Patient name, medicine name, and reminder time are required.', 'error');
      }

      setLoading('btn-medicine', 'Adding...', true);
      try {
        await apiFetch('/medicine-reminder', 'POST', { patient_name, medicine_name, reminder_time, frequency, notes });
        showToast('Medicine reminder added!', 'success');
        medForm.reset();
        loadMedicineReminders();
      } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
      } finally {
        setLoading('btn-medicine', '', false);
      }
    });
  }

  // ── HW Task Form ──
  const hwForm = document.getElementById('form-hw-task');
  if (hwForm) {
    hwForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const worker_name      = document.getElementById('hw-worker').value.trim();
      const task_description = document.getElementById('hw-task').value.trim();
      const patient_name     = document.getElementById('hw-patient').value.trim();
      const due_date         = document.getElementById('hw-due').value;
      const priority         = document.getElementById('hw-priority').value;

      if (!worker_name || !task_description) {
        return showToast('Worker name and task description are required.', 'error');
      }

      setLoading('btn-hw-task', 'Creating...', true);
      try {
        await apiFetch('/hw-tasks', 'POST', { worker_name, task_description, patient_name, due_date, priority });
        showToast('Task created!', 'success');
        hwForm.reset();
        loadHWTasks();
      } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
      } finally {
        setLoading('btn-hw-task', '', false);
      }
    });
  }
}

// ═══════════════════════════════════════════════════════════════
// Follow-up Data Loading
// ═══════════════════════════════════════════════════════════════

async function loadFollowups() {
  const listEl = document.getElementById('followup-list');
  if (!listEl) return;
  listEl.innerHTML = '<div class="skeleton" style="height:60px;margin-bottom:.5rem;"></div>'.repeat(3);
  try {
    const data = await apiFetch('/followup');
    renderFollowups(data.followups, listEl);
  } catch (e) {
    listEl.innerHTML = `<p class="text-muted">Unable to load follow-ups.</p>`;
  }
  loadMedicineReminders();
  loadHWTasks();
}

function renderFollowups(followups, container) {
  if (!followups || followups.length === 0) {
    container.innerHTML = `<p class="text-muted text-center" style="padding:2rem;">${t('noData')}</p>`;
    return;
  }
  // v3 CSS: .fu-item  |  .pill .pill-pending / .pill-completed
  container.innerHTML = followups.map(f => `
    <div class="fu-item">
      <div>
        <div class="fu-name">👤 ${escapeHtml(f.patient_name)}</div>
        <div style="font-size:.9rem;margin:.25rem 0;">${escapeHtml(f.concern)}</div>
        <div class="fu-date">📅 ${f.recommended_date} &nbsp;|&nbsp; 🏥 ${escapeHtml(f.pathway)}</div>
        ${f.notes ? `<div style="font-size:.82rem;color:var(--text-muted);margin-top:.2rem;">📝 ${escapeHtml(f.notes)}</div>` : ''}
      </div>
      <div style="display:flex;flex-direction:column;align-items:flex-end;gap:.5rem;flex-shrink:0;">
        <span class="pill pill-${f.status.toLowerCase()}">${f.status}</span>
        ${f.status === 'PENDING' ? `<button class="btn btn-sm btn-outline" onclick="completeFollowup('${f.id}')">${t('markDone')}</button>` : ''}
      </div>
    </div>
  `).join('');
}

async function completeFollowup(id) {
  try {
    await apiFetch(`/followup/${id}/complete`, 'PATCH');
    showToast('Follow-up marked as completed!', 'success');
    loadFollowups();
  } catch (e) {
    showToast('Error updating follow-up.', 'error');
  }
}

async function loadMedicineReminders() {
  const el = document.getElementById('medicine-list');
  if (!el) return;
  try {
    const data = await apiFetch('/medicine-reminder');
    if (!data.reminders.length) {
      el.innerHTML = `<p class="text-muted text-center" style="padding:2rem;">${t('noData')}</p>`;
      return;
    }
    // v3 CSS: .fu-item  |  .pill .pill-completed
    el.innerHTML = data.reminders.map(r => `
      <div class="fu-item">
        <div>
          <div class="fu-name">👤 ${escapeHtml(r.patient_name)}</div>
          <div style="font-size:.9rem;">💊 ${escapeHtml(r.medicine_name)}</div>
          <div class="fu-date">⏰ ${escapeHtml(r.reminder_time)} &nbsp;|&nbsp; ${escapeHtml(r.frequency)}</div>
          ${r.notes ? `<div style="font-size:.82rem;color:var(--text-muted);">📝 ${escapeHtml(r.notes)}</div>` : ''}
        </div>
        <span class="pill pill-completed">Active</span>
      </div>
    `).join('');
  } catch (e) {
    el.innerHTML = `<p class="text-muted">Unable to load reminders.</p>`;
  }
}

async function loadHWTasks() {
  const el = document.getElementById('hw-tasks-list');
  if (!el) return;
  try {
    const data = await apiFetch('/hw-tasks');
    if (!data.tasks.length) {
      el.innerHTML = `<p class="text-muted text-center" style="padding:2rem;">${t('noData')}</p>`;
      return;
    }
    // v3 CSS: .fu-item  |  .pill pill-pending/pill-completed
    el.innerHTML = data.tasks.map(task => `
      <div class="fu-item">
        <div>
          <div class="fu-name">👩‍⚕️ ${escapeHtml(task.worker_name)}</div>
          <div style="font-size:.9rem;">${escapeHtml(task.task_description)}</div>
          ${task.patient_name
            ? `<div class="fu-date">👤 ${escapeHtml(task.patient_name)} &nbsp;|&nbsp; 📅 ${task.due_date}</div>`
            : `<div class="fu-date">📅 ${task.due_date}</div>`}
        </div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:.5rem;">
          <span class="pill pill-${task.status.toLowerCase()}">${task.status}</span>
          <span class="risk-badge ${task.priority === 'HIGH' ? 'urgent' : 'low'}" style="font-size:.72rem;">${task.priority}</span>
        </div>
      </div>
    `).join('');
  } catch (e) {
    el.innerHTML = `<p class="text-muted">Unable to load tasks.</p>`;
  }
}

// ═══════════════════════════════════════════════════════════════
// Dashboard
// ═══════════════════════════════════════════════════════════════

async function loadDashboard() {
  try {
    const data = await apiFetch('/dashboard');
    renderDashboard(data);
  } catch (e) {
    showToast('Error loading dashboard.', 'error');
  }
}

function renderDashboard(data) {
  setText('dash-total',    data.total_requests);
  setText('dash-pending',  data.pending_followups);
  setText('dash-completed',data.completed_followups);
  setText('dash-total-fu', data.total_followups);

  const risk = data.risk_distribution || {};
  setText('dash-low',      risk.LOW      || 0);
  setText('dash-moderate', risk.MODERATE || 0);
  setText('dash-urgent',   risk.URGENT   || 0);

  // Risk bar chart
  const total = (risk.LOW || 0) + (risk.MODERATE || 0) + (risk.URGENT || 0) || 1;
  renderRiskBar('bar-low',      risk.LOW      || 0, total, '#22c55e');
  renderRiskBar('bar-moderate', risk.MODERATE || 0, total, '#f59e0b');
  renderRiskBar('bar-urgent',   risk.URGENT   || 0, total, '#ef4444');

  // Upcoming appointments
  const upEl = document.getElementById('upcoming-list');
  if (upEl) {
    const up = data.upcoming_appointments || [];
    if (!up.length) {
      upEl.innerHTML = `<p class="text-muted text-center" style="padding:1.5rem;">${t('noData')}</p>`;
    } else {
      upEl.innerHTML = up.map(f => `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:.6rem .5rem;border-bottom:1px solid var(--border);">
          <div>
            <div style="font-weight:600;font-size:.9rem;">👤 ${escapeHtml(f.patient_name)}</div>
            <div style="font-size:.8rem;color:var(--text-muted);">${escapeHtml(f.concern.substring(0,50))}${f.concern.length > 50 ? '...' : ''}</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:.85rem;font-weight:600;color:var(--secondary);">${f.recommended_date}</div>
            <div style="font-size:.75rem;color:var(--text-muted);">${escapeHtml(f.pathway)}</div>
          </div>
        </div>
      `).join('');
    }
  }

  // Recent interactions
  const intEl = document.getElementById('interactions-list');
  if (intEl) {
    const interactions = data.recent_interactions || [];
    if (!interactions.length) {
      intEl.innerHTML = `<p class="text-muted text-center" style="padding:1.5rem;">${t('noData')}</p>`;
    } else {
      intEl.innerHTML = `
        <div class="table-wrap">
          <table>
            <thead><tr><th>Time</th><th>Patient</th><th>Agent</th><th>Summary</th><th>Risk</th></tr></thead>
            <tbody>
              ${interactions.map(i => `
                <tr>
                  <td style="white-space:nowrap;font-size:.8rem;">${formatTime(i.timestamp)}</td>
                  <td style="font-size:.85rem;">${escapeHtml(i.patient_name)}</td>
                  <td style="font-size:.8rem;color:var(--text-muted);">${escapeHtml(i.agent_used.replace(' Agent',''))}</td>
                  <td style="font-size:.82rem;max-width:200px;">${escapeHtml(i.query_summary)}</td>
                  <td>${i.risk_level
                    ? `<span class="risk-badge ${i.risk_level.toLowerCase()}">${i.risk_level}</span>`
                    : '<span style="color:var(--text-light);font-size:.8rem;">–</span>'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>`;
    }
  }
}

function renderRiskBar(id, val, total, color) {
  const el = document.getElementById(id);
  if (!el) return;
  const pct = Math.round((val / total) * 100);
  el.innerHTML = `
    <div style="display:flex;align-items:center;gap:.75rem;">
      <div style="flex:1;background:var(--border);border-radius:4px;height:10px;overflow:hidden;">
        <div style="width:${pct}%;height:100%;background:${color};border-radius:4px;transition:.5s;"></div>
      </div>
      <span style="font-size:.85rem;font-weight:600;min-width:30px;text-align:right;">${val}</span>
    </div>`;
}

// ── Utilities ───────────────────────────────────────────────────

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function hexToAlpha(hex, alpha) {
  const r = parseInt(hex.slice(1,3), 16);
  const g = parseInt(hex.slice(3,5), 16);
  const b = parseInt(hex.slice(5,7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

function formatTime(isoStr) {
  if (!isoStr) return '';
  try {
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })
      + ' ' + d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  } catch { return isoStr.substring(0, 16); }
}
