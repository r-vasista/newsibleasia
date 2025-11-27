// Function to handle theme toggle
function toggleTheme() {
  document.body.classList.toggle("dark-mode");
  if (document.body.classList.contains("dark-mode")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
  }

  const toggleButton = document.getElementById("theme-toggle");
  const themeSwitcher = document.getElementById("themeSwitcher");

  if (toggleButton) {
    toggleButton.addEventListener("click", toggleTheme);
  }

  if (themeSwitcher) {
    themeSwitcher.addEventListener("click", toggleTheme);
  }
});

// Universal scroll left/right functions
function scrollLeft(uniqueSliderId) {
  const container = document.getElementById(uniqueSliderId);
  container.scrollBy({ left: -100, behavior: "smooth" });
}

function scrollRight(uniqueSliderId) {
  const container = document.getElementById(uniqueSliderId);
  container.scrollBy({ left: 100, behavior: "smooth" });
}

// Universal JS for share
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
