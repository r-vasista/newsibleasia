$(function () {
  $(".selectpicker").selectpicker();
});

// Function to handle theme toggle
function toggleTheme() {
  document.body.classList.toggle("dark-mode");
  // Update localStorage with the current theme preference
  if (document.body.classList.contains("dark-mode")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
}

// DOMContentLoaded event to initialize theme and add event listeners
document.addEventListener("DOMContentLoaded", function () {
  // Check if dark mode is already enabled in localStorage
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
  }

  // Select the theme toggle buttons
  const toggleButton = document.getElementById("theme-toggle");
  const themeSwitcher = document.getElementById("themeSwitcher");

  // Add event listeners for both buttons
  if (toggleButton) {
    toggleButton.addEventListener("click", toggleTheme);
  }

  if (themeSwitcher) {
    themeSwitcher.addEventListener("click", toggleTheme);
  }
});

// header pray times
document.addEventListener("DOMContentLoaded", function () {
  if (typeof moment !== "undefined" && typeof moment().iYear !== "undefined") {
    var islamicMonthsEnglish = [
      "Muharram",
      "Safar",
      "Rabi' al-awwal",
      "Rabi' al-thani",
      "Jumada al-awwal",
      "Jumada al-thani",
      "Rajab",
      "Sha'ban",
      "Ramadan",
      "Shawwal",
      "Dhu al-Qi'dah",
      "Dhu al-Hijjah",
    ];
    var islamicMonthNumber = moment().iMonth();
    var islamicDate =
      moment().format("iD") +
      " " +
      islamicMonthsEnglish[islamicMonthNumber] +
      " " +
      moment().format("iYYYY") +
      " AH";
    var islamicDateElement = document.getElementById("islamic-date");
    if (islamicDateElement) {
      islamicDateElement.textContent = islamicDate;
    } else {
      console.warn("Islamic date element not found!");
    }
  } else {
    console.error("Moment-Hijri is not loaded.");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  function updateNextPrayerTime() {
    // URL to fetch prayer times for Dubai from Aladhan API
    var url =
      "http://api.aladhan.com/v1/timingsByCity?city=Dubai&country=UAE&method=2";

    // Fetch prayer times data
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        if (data && data.data && data.data.timings) {
          var timings = data.data.timings;
          var prayerTimes = [
            { name: "Fajr", time: timings.Fajr },
            { name: "Dhuhr", time: timings.Dhuhr },
            { name: "Asr", time: timings.Asr },
            { name: "Maghrib", time: timings.Maghrib },
            { name: "Isha", time: timings.Isha },
          ];

          var now = new Date();
          var currentTime = now.getHours() * 60 + now.getMinutes();

          // Find the next prayer time
          var nextPrayer = prayerTimes.find((prayer) => {
            var [hours, minutes] = prayer.time.split(":").map(Number);
            var prayerTime = hours * 60 + minutes;
            return prayerTime > currentTime;
          });

          // If no upcoming prayer, use the first prayer of the next day
          if (!nextPrayer) {
            nextPrayer = prayerTimes[0];
          }

          // Calculate remaining time
          var [prayerHours, prayerMinutes] = nextPrayer.time
            .split(":")
            .map(Number);
          var prayerTimeInMinutes = prayerHours * 60 + prayerMinutes;
          var remainingMinutes = prayerTimeInMinutes - currentTime;
          var remainingHours = Math.floor(remainingMinutes / 60);
          remainingMinutes = remainingMinutes % 60;

          // Calculate remaining seconds
          var nowInMinutes = now.getMinutes();
          var secondsUntilNextMinute = 60 - now.getSeconds();
          var remainingTime =
            (remainingHours * 60 + remainingMinutes) * 60 +
            secondsUntilNextMinute;

          // Format remaining time as HH:MM:SS
          var hours = String(Math.floor(remainingTime / 3600)).padStart(2, "0");
          var minutes = String(
            Math.floor((remainingTime % 3600) / 60)
          ).padStart(2, "0");
          var seconds = String(remainingTime % 60).padStart(2, "0");

          var formattedRemainingTime = `${hours}:${minutes}:${seconds}`;

          // Update HTML with the upcoming prayer time and remaining time
          document.getElementById(
            "prayer-time"
          ).textContent = `${nextPrayer.name} ${nextPrayer.time}`;
          document.getElementById(
            "remaining-time"
          ).textContent = `${formattedRemainingTime}`;
        } else {
          console.error("Prayer times data is not available.");
        }
      })
      .catch((error) => {
        console.error("Error fetching prayer times:", error);
      });
  }

  // Update next prayer time and remaining time on page load
  updateNextPrayerTime();

  // Refresh prayer time and remaining time every second (1000 milliseconds)
  setInterval(updateNextPrayerTime, 1000);
});

// Function to get current day, date, month, and year
const getFormattedDate = () => {
  const options = {
    weekday: "short",
    day: "2-digit",
    month: "short",
    year: "numeric",
  };
  const today = new Date();
  return today.toLocaleDateString("en-US", options);
};

// Set the date dynamically
document.getElementById("currentDate").innerText = getFormattedDate();

// featchers section
// Fetch Prayer Times
async function fetchPrayerTimes() {
  const city = document.getElementById("prayer-city").value;
  const apiUrl = `https://api.aladhan.com/v1/timingsByCity?city=${city}&country=&method=2`;

  try {
    const response = await fetch(apiUrl);
    const data = await response.json();

    if (data.code === 200) {
      const timings = data.data.timings;
      const location = data.data.meta.timezone;

      // Update location
      document.getElementById(
        "prayer-location"
      ).innerText = `Location: ${city} (${location})`;

      // Clear prayer times list
      const prayerTimesList = document.getElementById("prayer-times-list");
      prayerTimesList.innerHTML = "";

      // Render prayer times into cards
      const prayerNames = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"];
      prayerNames.forEach((prayer, index) => {
        const card = document.createElement("div");
        card.className = `prayer-card ${
          index === 4 ? "bottom-card" : ""
        } col-sm-12 col-md-5`;
        card.innerHTML = `
                        <h4>${prayer}</h4>
                        <p>${timings[prayer]}</p>
                    `;
        prayerTimesList.appendChild(card);
      });
    } else {
      alert("Unable to fetch prayer times. Please try again.");
    }
  } catch (error) {
    console.error(error);
    alert("Error fetching prayer times.");
  }
}

// Fetch Weather
async function fetchWeather() {
  const city = document.getElementById("weather-city").value;
  const apiKey = "bc4704ae1b004cc3bff91834242311";
  const apiUrl = `https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${city}&days=5`;

  try {
    const response = await fetch(apiUrl);
    const data = await response.json();

    if (data.error) {
      alert(data.error.message);
    } else {
      // Update current weather
      document.getElementById("weather-location").innerText =
        data.location.name;
      document.getElementById("weather-condition").innerText =
        data.current.condition.text;
      document.getElementById(
        "weather-temp"
      ).innerText = `${data.current.temp_c}°C`;
      document.getElementById(
        "weather-range"
      ).innerText = `${data.forecast.forecastday[0].day.mintemp_c}°C / ${data.forecast.forecastday[0].day.maxtemp_c}°C`;
      document.getElementById(
        "weather-wind"
      ).innerText = `${data.current.wind_kph} kph`;
      document.getElementById(
        "weather-humidity"
      ).innerText = `${data.current.humidity}%`;
      document.getElementById(
        "weather-precipitation"
      ).innerText = `${data.current.precip_mm} mm`;
      document.getElementById(
        "weather-icon"
      ).src = `https:${data.current.condition.icon}`;

      // Update forecast
      const forecastHtml = data.forecast.forecastday
        .map(
          (day) => `
                    <div>
                        <p>${new Date(day.date).toLocaleDateString("en-US", {
                          weekday: "short",
                        })}</p>
                        <p>${day.day.mintemp_c}°C / ${day.day.maxtemp_c}°C</p>
                        <img src="https:${day.day.condition.icon}" alt="${
            day.day.condition.text
          }" class="img-fluid">
                    </div>`
        )
        .join("");
      document.getElementById("weather-forecast").innerHTML = forecastHtml;
    }
  } catch (error) {
    console.error(error);
    alert("Error fetching weather data.");
  }
}

// Load default data on page load
window.onload = () => {
  fetchPrayerTimes();
  fetchWeather();
};

// API credentials
const clientId = "ehvHgNtFRwV3OxYF54EsxTgjXVUrKXNj";
const clientSecret = "wVAfrTG5BVsGZzQf";

// Function to get access token
async function getAccessToken() {
  const response = await fetch(
    "https://test.api.amadeus.com/v1/security/oauth2/token",
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "client_credentials",
        client_id: clientId,
        client_secret: clientSecret,
      }),
    }
  );
  const data = await response.json();
  return data.access_token;
}

// Function to search flights
async function searchFlights(accessToken, origin, destination, departureDate) {
  const response = await fetch(
    `https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=${origin}&destinationLocationCode=${destination}&departureDate=${departureDate}&adults=1`,
    {
      headers: { Authorization: `Bearer ${accessToken}` },
    }
  );
  return response.json();
}

// Handle form submission
document
  .getElementById("flightSearchForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;
    const departureDate = document.getElementById("departureDate").value;

    const accessToken = await getAccessToken();
    const flightData = await searchFlights(
      accessToken,
      origin,
      destination,
      departureDate
    );

    const flightsList = document.getElementById("flightsList");
    flightsList.innerHTML = "";

    if (flightData.data) {
      flightData.data.forEach((flight) => {
        const price = flight.price.total;
        const airline = flight.validatingAirlineCodes[0];
        const listItem = document.createElement("li");
        listItem.className = "list-group-item";
        listItem.innerHTML = `
                        <span>Airline: ${airline}</span>
                        <span>Price: $${price}</span>
                    `;
        flightsList.appendChild(listItem);
      });
    } else {
      flightsList.innerHTML =
        '<li class="list-group-item text-center">No results found.</li>';
    }
  });

function scrollLeft(uniqueSliderId) {
  const container = document.getElementById(uniqueSliderId);
  container.scrollBy({ left: -100, behavior: "smooth" });
}

function scrollRight(uniqueSliderId) {
  const container = document.getElementById(uniqueSliderId);
  container.scrollBy({ left: 100, behavior: "smooth" });
}

// universel js for share  start
function scrollLeft(postsId) {
  const container = document.getElementById(`shareSlider-${postsId}`);
  container.scrollBy({ left: -100, behavior: "smooth" });
}

function scrollRight(postsId) {
  const container = document.getElementById(`shareSlider-${postsId}`);
  container.scrollBy({ left: 100, behavior: "smooth" });
}

function copyLink(slug) {
  const link = `${window.location.origin}/${slug}`;
  navigator.clipboard
    .writeText(link)
    .then(() => alert("Link copied to clipboard!"))
    .catch((err) => console.error("Failed to copy link: ", err));
}
// universel js for share end
