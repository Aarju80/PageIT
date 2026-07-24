const form = document.getElementById('audit-form');
const urlInput = document.getElementById('url-input');
const statusPanel = document.getElementById('status-panel');
const summaryBanner = document.getElementById('summary-banner');
const reportGrid = document.getElementById('report-grid');

const metrics = [
  { key: 'status', label: 'HTTP Status' },
  { key: 'responseTimeMs', label: 'Response Time' },
  { key: 'title', label: 'Page Title' },
  { key: 'metaDescription', label: 'Meta Description' },
  { key: 'h1Count', label: 'H1 Count' },
  { key: 'imagesMissingAlt', label: 'Images Missing Alt' },
  { key: 'totalImages', label: 'Total Images' },
  { key: 'approxWordCount', label: 'Approx Word Count' },
];

function setStatus(message, tone = 'neutral') {
  statusPanel.classList.remove('hidden');
  statusPanel.className = `status-panel ${tone === 'success' ? 'success-card' : tone === 'error' ? 'error-card' : ''}`.trim();
  statusPanel.textContent = message;
}

function clearReport() {
  summaryBanner.classList.add('hidden');
  summaryBanner.innerHTML = '';
  reportGrid.classList.add('hidden');
  reportGrid.innerHTML = '';
}

function renderSummary(report) {
  const score = Math.min(100, 70 + (report.h1Count > 0 ? 10 : 0) + (report.metaDescription ? 10 : 0) + (report.imagesMissingAlt === 0 ? 10 : 0));
  summaryBanner.innerHTML = `<strong>Quick summary:</strong> ${report.title ? 'Page title detected' : 'Page title missing'} • ${report.metaDescription ? 'Meta description present' : 'Meta description missing'} • ${report.imagesMissingAlt} image${report.imagesMissingAlt === 1 ? '' : 's'} missing alt text`;
  summaryBanner.classList.remove('hidden');
  summaryBanner.title = `Estimated health score: ${score}/100`;
}

function renderReport(report) {
  reportGrid.innerHTML = '';

  for (const metric of metrics) {
    const value = report[metric.key];
    const card = document.createElement('article');
    card.className = 'report-card';
    card.innerHTML = `<h3>${metric.label}</h3><div class="value">${value ?? 'N/A'}</div>`;
    reportGrid.appendChild(card);
  }

  renderSummary(report);
  reportGrid.classList.remove('hidden');
}

function renderError(errorMessage) {
  clearReport();
  setStatus(errorMessage, 'error');
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  clearReport();
  const url = urlInput.value.trim();

  if (!url) {
    renderError('Please enter a URL to audit.');
    return;
  }

  setStatus('Analyzing website...');

  try {
    const response = await fetch(`${window.PAGEIT_CONFIG.apiBaseUrl}/api/audit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error?.message || 'Unable to complete the audit.');
    }

    setStatus('Report generated successfully.', 'success');
    renderReport(payload);
  } catch (error) {
    renderError(error.message || 'Something went wrong while auditing the page.');
  }
});
