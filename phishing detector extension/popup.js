document.addEventListener('DOMContentLoaded', function () {
  let currentTabUrl = '';

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    currentTabUrl = tabs[0].url;
    document.getElementById('currentUrl').textContent = currentTabUrl;
  });

  document.getElementById('checkBtn').addEventListener('click', function () {
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: currentTabUrl })
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById('result').textContent =
          data.prediction === 'phishing'
            ? "⚠️ Site suspect détecté !"
            : "✅ Ce site semble sûr.";
      })
      .catch(error => {
        console.error("Erreur :", error);
        document.getElementById('result').textContent = "Erreur de connexion avec l'API.";
      });
  });
});