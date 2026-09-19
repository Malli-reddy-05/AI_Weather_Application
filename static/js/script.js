const form = document.querySelector("#search-form");
const cityInput = document.querySelector("#city");
const error = document.querySelector("#error");
const card = document.querySelector("#weather-card");
const button = form.querySelector("button");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();
  error.textContent = "";
  if (!city) {
    error.textContent = "Enter a city to see its weather.";
    return;
  }

  button.disabled = true;
  button.innerHTML = "Checking…";
  try {
    const response = await fetch("/api/weather", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ city }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to load weather.");
    showWeather(data);
  } catch (err) {
    error.textContent = err.message;
  } finally {
    button.disabled = false;
    button.innerHTML = "Check weather <span>→</span>";
  }
});

function showWeather(data) {
  document.querySelector("#place").textContent = [data.city, data.country].filter(Boolean).join(", ");
  document.querySelector("#condition").textContent = data.condition;
  document.querySelector("#temperature").textContent = data.temperature;
  document.querySelector("#description").textContent = data.description;
  document.querySelector("#feels-like").textContent = `${data.feels_like}°C`;
  document.querySelector("#humidity").textContent = `${data.humidity}%`;
  document.querySelector("#wind").textContent = `${data.wind_speed} km/h`;
  document.querySelector("#summary").textContent = data.summary;
  const icon = document.querySelector("#weather-icon");
  icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
  icon.alt = data.description;
  card.classList.remove("hidden");
}
