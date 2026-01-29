const form = document.getElementById("ai-form");
const results = document.getElementById("ai-results");

const mockRecommendations = () => [
  {
    name: "信州あさひ市",
    score: 92,
    summary: "保育料補助と医療費助成が充実。家賃支援と移住支援金も手厚い。",
    tags: ["子育て", "医療", "支援金"],
  },
  {
    name: "みなみ高原町",
    score: 88,
    summary: "教育支援と学童が豊富。空き家バンクと家賃補助が利用しやすい。",
    tags: ["教育", "家賃", "子育て"],
  },
  {
    name: "ひだまり湖市",
    score: 84,
    summary: "リモート対応求人が多く、就業支援が豊富。医療アクセスも良好。",
    tags: ["仕事", "医療", "教育"],
  },
];

const renderResults = (items) => {
  results.innerHTML = "";
  items.forEach((item) => {
    const card = document.createElement("div");
    card.className = "result-card";
    card.innerHTML = `
      <div class="result-head">
        <h3>${item.name}</h3>
        <span class="score">マッチ度 ${item.score}</span>
      </div>
      <p>${item.summary}</p>
      <div class="badge-row">
        ${item.tags.map((tag) => `<span>${tag}</span>`).join("")}
      </div>
    `;
    results.appendChild(card);
  });
};

const readForm = (formEl) => {
  const data = new FormData(formEl);
  const services = data.getAll("service");
  return {
    family: data.get("family"),
    budget: data.get("budget"),
    work: data.get("work"),
    services,
    note: data.get("note") || "",
  };
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = readForm(form);
  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (result.recommendations) {
      renderResults(result.recommendations);
      return;
    }
  } catch (error) {
    // Fall back to mock recommendations.
  }

  renderResults(mockRecommendations(payload));
});

renderResults(mockRecommendations());
