chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    let result = tab.url.startsWith("https")
      ? "✅ Ce site semble sûr."
      : "⚠️ Ce site peut être risqué.";

    chrome.storage.local.set({ detectionResult: result }, () => {
      console.log("Résultat sauvegardé :", result);
    });
  }
});
