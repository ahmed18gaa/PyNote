const menuButton = document.getElementById("menuButton");
const navLinks = document.getElementById("navLinks");
const macDownload = document.getElementById("macDownload");
const windowsDownload = document.getElementById("windowsDownload");

if (menuButton && navLinks) {
  menuButton.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });

  document.querySelectorAll("#navLinks a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
    });
  });
}

if (macDownload) {
  macDownload.href =
    "https://github.com/ahmed18gaa/PyNote/releases/download/v1.0.2/PyNote-1.0.2.dmg";
}

if (windowsDownload) {
  windowsDownload.href =
    "https://github.com/ahmed18gaa/PyNote/releases/download/v1.0.2/PyNote-1.0.2-Windows.zip";
}

// Uncomment and edit when the GitHub Release is ready:
// macDownload.href = "YOUR_MACOS_RELEASE_URL";
// windowsDownload.href = "YOUR_WINDOWS_RELEASE_URL";
