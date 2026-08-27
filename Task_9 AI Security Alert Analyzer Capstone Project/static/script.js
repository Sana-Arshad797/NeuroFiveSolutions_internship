// script.js
// Handles user interaction, calls the Flask backend, and renders results.

const alertInput = document.getElementById("alert-input");
const charCount = document.getElementById("char-count");
const analyzeBtn = document.getElementById("analyze-btn");
const exampleBtn = document.getElementById("example-btn");
const errorBox = document.getElementById("error-box");
const loadingBox = document.getElementById("loading-box");
const resultsSection = document.getElementById("results");

const resultSeverity = document.getElementById("result-severity");
const resultThreatType = document.getElementById("result-threat-type");
const resultConfidence = document.getElementById("result-confidence");
const resultSummary = document.getElementById("result-summary");
const resultIndicators = document.getElementById("result-indicators");
const resultActions = document.getElementById("result-actions");

const EXAMPLE_ALERT =
  "Endpoint detection alert: powershell.exe was launched by winword.exe " +
  "on host FIN-LAPTOP-07 at 14:32 UTC. The PowerShell command line was " +
  "base64-encoded and included the flag '-enc'. The process then attempted " +
  "an outbound HTTPS connection to an IP address not previously seen on " +
  "this host. No further activity has been confirmed yet.";

// --- Character counter -----------------------------------------------------

alertInput.addEventListener("input", () => {
  charCount.textContent = alertInput.value.length;
});

// --- Example button ---------------------------------------------------------

exampleBtn.addEventListener("click", () => {
  alertInput.value = EXAMPLE_ALERT;
  charCount.textContent = alertInput.value.length;
  hideError();
});

// --- Analyze button ----------------------------------------------------------

analyzeBtn.addEventListener("click", async () => {
  const alertText = alertInput.value.trim();

  hideError();
  hideResults();

  if (alertText.length < 10) {
    showError("Please enter at least 10 characters describing the alert.");
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ alert: alertText }),
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      showError(data.error || "Something went wrong while analyzing the alert.");
      return;
    }

    renderResults(data.analysis);
  } catch (err) {
    showError("Could not reach the server. Please check your connection and try again.");
  } finally {
    setLoading(false);
  }
});

// --- Helpers -----------------------------------------------------------------

function setLoading(isLoading) {
  analyzeBtn.disabled = isLoading;
  loadingBox.classList.toggle("hidden", !isLoading);
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function hideError() {
  errorBox.textContent = "";
  errorBox.classList.add("hidden");
}

function hideResults() {
  resultsSection.classList.add("hidden");
}

function severityClass(severity) {
  switch ((severity || "").toLowerCase()) {
    case "low":
      return "severity-low";
    case "medium":
      return "severity-medium";
    case "high":
      return "severity-high";
    case "critical":
      return "severity-critical";
    default:
      return "";
  }
}

function renderList(container, items) {
  container.innerHTML = "";

  if (!items || items.length === 0) {
    const li = document.createElement("li");
    li.textContent = "None identified from the provided information.";
    container.appendChild(li);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    container.appendChild(li);
  });
}

function renderResults(analysis) {
  resultSeverity.textContent = analysis.severity;
  resultSeverity.className = "severity-badge " + severityClass(analysis.severity);

  resultThreatType.textContent = analysis.threat_type;
  resultConfidence.textContent = `${analysis.confidence}%`;
  resultSummary.textContent = analysis.summary;

  renderList(resultIndicators, analysis.indicators);
  renderList(resultActions, analysis.recommended_actions);

  resultsSection.classList.remove("hidden");
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}
