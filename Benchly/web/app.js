const defaultServer = "http://127.0.0.1:5000";

const serverInput = document.getElementById("serverUrl");
const refreshButton = document.getElementById("refreshBtn");
const leaderboardBody = document.querySelector("#leaderboard tbody");
const statsContainer = document.getElementById("stats");

function formatTimestamp(ts) {
  try {
    const d = new Date(ts);
    return d.toLocaleString();
  } catch {
    return ts;
  }
}

function renderStats(rows) {
  statsContainer.innerHTML = "";
  if (!rows || rows.length === 0) {
    statsContainer.textContent = "No data available.";
    return;
  }

  const latest = rows[0];
  const results = latest.payload?.results || {};

  const cards = [
    { title: "Machine", value: latest.machine_id },
    { title: "Score", value: latest.score?.toFixed(2) ?? "-" },
    { title: "Submitted", value: formatTimestamp(latest.created_at) },
    { title: "CPU (s)", value: results.cpu?.duration_s?.toFixed(3) ?? "-" },
    { title: "RAM (s)", value: results.ram?.duration_s?.toFixed(3) ?? "-" },
    { title: "Disk Write (s)", value: results.disk?.write_seconds?.toFixed(3) ?? "-" },
    { title: "Disk Read (s)", value: results.disk?.read_seconds?.toFixed(3) ?? "-" },
  ];

  for (const card of cards) {
    const elem = document.createElement("div");
    elem.className = "card";

    const title = document.createElement("div");
    title.className = "card-title";
    title.textContent = card.title;

    const value = document.createElement("div");
    value.className = "card-value";
    value.textContent = card.value;

    elem.appendChild(title);
    elem.appendChild(value);
    statsContainer.appendChild(elem);
  }
}

function renderLeaderboard(rows) {
  leaderboardBody.innerHTML = "";

  if (!rows || rows.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 6;
    td.textContent = "No results yet";
    tr.appendChild(td);
    leaderboardBody.appendChild(tr);
    return;
  }

  for (let idx = 0; idx < rows.length; idx += 1) {
    const row = rows[idx];
    const tr = document.createElement("tr");

    const addCell = (value) => {
      const td = document.createElement("td");
      td.textContent = value;
      tr.appendChild(td);
    };

    const results = row.payload?.results || {};

    addCell(idx + 1);
    addCell(row.machine_id);
    addCell(row.score?.toFixed(2) ?? "-");
    addCell(formatTimestamp(row.created_at));
    addCell((results.cpu?.duration_s ?? "-").toFixed ? results.cpu.duration_s.toFixed(3) : "-");
    addCell((results.ram?.duration_s ?? "-").toFixed ? results.ram.duration_s.toFixed(3) : "-");
    addCell((results.disk?.write_seconds ?? "-").toFixed ? results.disk.write_seconds.toFixed(3) : "-");
    addCell((results.disk?.read_seconds ?? "-").toFixed ? results.disk.read_seconds.toFixed(3) : "-");

    leaderboardBody.appendChild(tr);
  }
}

async function fetchLeaderboard() {
  const serverUrl = serverInput.value.trim() || defaultServer;
  const endpoint = serverUrl.replace(/\/+$/, "") + "/leaderboard";

  const resp = await fetch(endpoint);
  if (!resp.ok) {
    throw new Error(`Server returned ${resp.status}`);
  }
  return resp.json();
}

async function refresh() {
  refreshButton.disabled = true;
  try {
    const payload = await fetchLeaderboard();
    const rows = payload.results || [];
    renderStats(rows);
    renderLeaderboard(rows);
  } catch (err) {
    console.error(err);
    statsContainer.textContent = "Failed to load data. Check server URL and try again.";
  } finally {
    refreshButton.disabled = false;
  }
}

refreshButton.addEventListener("click", refresh);

window.addEventListener("load", () => {
  serverInput.value = defaultServer;
  refresh();
});
