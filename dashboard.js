// CPU chart
const cpuCtx = document.getElementById('cpu-chart').getContext('2d');
const cpuChart = new Chart(cpuCtx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'CPU Usage (%)',
      data: [],
      borderWidth: 2,
      fill: false,
      tension: 0.3,
      pointRadius: 2
    }]
  },
  options: {
    responsive: true,
    animation: false,
    scales: { y: { beginAtZero: true, max: 100 } }
  }
});

// Net chart
const netCtx = document.getElementById('net-chart').getContext('2d');
const netChart = new Chart(netCtx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      { label: 'Download (KB/s)', data: [], borderWidth: 2, fill: false, tension: 0.3, pointRadius: 2 },
      { label: 'Upload (KB/s)', data: [], borderWidth: 2, fill: false, tension: 0.3, pointRadius: 2 }
    ]
  },
  options: {
    responsive: true,
    animation: false,
    scales: { y: { beginAtZero: true } }
  }
});

function addPoint(chart, label, values) {
  chart.data.labels.push(label);
  if (!Array.isArray(values)) values = [values];
  for (let i = 0; i < values.length; i++) {
    chart.data.datasets[i].data.push(values[i]);
  }
  // keep last 60 points
  if (chart.data.labels.length > 60) {
    chart.data.labels.shift();
    chart.data.datasets.forEach(ds => ds.data.shift());
  }
  chart.update();
}

// Poll CPU
async function pollCPU() {
  try {
    const r = await fetch('/api/cpu_usage');
    const j = await r.json();
    const label = new Date().toLocaleTimeString();
    addPoint(cpuChart, label, j.cpu);
    const kpi = document.getElementById('cpu-kpi');
    if (kpi) kpi.textContent = `${j.cpu} %`;
  } catch (e) {
    console.error('CPU poll failed', e);
  }
}

// Poll Network
async function pollNetwork() {
  try {
    const r = await fetch('/api/network/speed');
    const j = await r.json();
    const label = new Date().toLocaleTimeString();
    addPoint(netChart, label, [j.download_kbps, j.upload_kbps]);
    const dl = document.getElementById('dl-kpi');
    const ul = document.getElementById('ul-kpi');
    const ts = document.getElementById('total-sent');
    const tr = document.getElementById('total-recv');
    if (dl) dl.textContent = `${j.download_kbps} KB/s`;
    if (ul) ul.textContent = `${j.upload_kbps} KB/s`;
    if (ts) ts.textContent = `${j.total_sent_mb} MB`;
    if (tr) tr.textContent = `${j.total_recv_mb} MB`;
  } catch (e) {
    console.error('Network poll failed', e);
  }
}

// USB Alert
async function fetchUsbAlert() {
  try {
    const r = await fetch('/api/usb_alert');
    const j = await r.json();
    const alertDiv = document.getElementById('usb-alert');
    if (j && j.device) {
      alertDiv.innerHTML = `
        <strong>USB Alert:</strong> New device <strong>${j.device}</strong> detected at ${j.timestamp}.
      `;
      alertDiv.style.display = 'block';
    }
  } catch (e) {
    console.error('USB alert poll failed', e);
  }
}

// Kick off
setInterval(pollCPU, 1000);
setInterval(pollNetwork, 1000);
setInterval(fetchUsbAlert, 10000);
pollCPU();
pollNetwork();
fetchUsbAlert();
