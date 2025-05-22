
(async function () {
  const url = window.location.href;
  console.log("🔍 URL visitée :", url);

  try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ url })
      });

      const result = await response.json();
      console.log("✅ Résultat reçu du serveur :", result);

      if (result.label === "phishing") {
          alert("⚠️ Attention : ce site est potentiellement un site de phishing !");
      } else {
          console.log("🟢 Site considéré comme sûr.");
      }

  } catch (error) {
      console.error("❌ Erreur lors de la détection :", error);
  }
})();


