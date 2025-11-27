// topnew js start
// Ticker scroll function
function scrollTicker(id, direction) {
  const ticker = document.getElementById(id);
  ticker.style.animationPlayState = "paused";

  const currentTransform = getComputedStyle(ticker).transform;
  let xOffset = 0;

  if (currentTransform !== "none") {
    const matrix = new DOMMatrix(currentTransform);
    xOffset = matrix.m41;
  }

  const scrollAmount = 50 * direction;
  ticker.style.transform = `translateX(${xOffset + scrollAmount}px)`;

  setTimeout(() => {
    ticker.style.animationPlayState = "running";
  }, 5000);
}

function pauseTicker(id) {
  const ticker = document.getElementById(id);
  if (ticker) {
    ticker.style.animationPlayState = "paused";
  }
}

function resumeTicker(id) {
  const ticker = document.getElementById(id);
  if (ticker) {
    ticker.style.animationPlayState = "running";
  }
}



// Swiper Initializations
document.addEventListener("DOMContentLoaded", function () {
  // Hide specific slide
  const hiddenSlide = document.querySelector(
    '.swiper-slide[data-swiper-slide-index="2"]'
  );
  if (hiddenSlide) hiddenSlide.style.display = "none";

  // Thumbnail swiper
  const thumbSwiper = new Swiper(".thumb-swiper", {
    slidesPerView: 4,
    spaceBetween: 10,
    watchSlidesProgress: true,
    breakpoints: {
      576: { slidesPerView: 3 },
      768: { slidesPerView: 4 },
      992: { slidesPerView: 5 },
      1200: { slidesPerView: 6 },
    },
  });

  // Main Swiper
  const mainSwiper = new Swiper(".main-swiper", {
    loop: true,
    spaceBetween: 10,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    autoplay: {
      delay: 4000,
      disableOnInteraction: false,
    },
    thumbs: {
      swiper: thumbSwiper,
    },
  });

  // Trending Swiper
  const trendingThumb = new Swiper(".trending-thumb-swiper", {
    slidesPerView: 4,
    spaceBetween: 10,
    watchSlidesProgress: true,
  });

  const trendingSwiper = new Swiper(".trending-swiper", {
    loop: true,
    navigation: {
      nextEl: ".trending-next",
      prevEl: ".trending-prev",
    },
    autoplay: {
      delay: 4000,
      disableOnInteraction: false,
    },
    thumbs: {
      swiper: trendingThumb,
    },
  });
});

// artical js start
let mainSlider;
  let slides;
  let slideCount;
  let currentSlideIndex = 0;
  let autoSlideInterval;

  function goToArticleSlide(index) {
    mainSlider.style.transition = 'transform 0.6s ease';
    mainSlider.style.transform = `translateX(-${index * 100}%)`;
    currentSlideIndex = index;
  }

  function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
      currentSlideIndex++;
      if (currentSlideIndex >= slideCount) {
        currentSlideIndex = 0;
      }
      goToArticleSlide(currentSlideIndex);
    }, 5000);
  }

  document.addEventListener('DOMContentLoaded', function () {
    mainSlider = document.getElementById('articleSliderMain');
    slides = mainSlider.querySelectorAll('.article-slide-item');
    slideCount = slides.length;

    startAutoSlide();
  });
// news js start
document.addEventListener("DOMContentLoaded", function () {
    const thumbs = document.querySelectorAll('.thumb');
    const mainImage = document.getElementById('mainImage');
  
    if (!mainImage) return; // Optional safety check
  
    let isSliding = false;
  
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        if (isSliding) return;
  
        const newSrc = thumb.getAttribute('data-image');
  
        // If the same image, do nothing
        if (mainImage.src.includes(newSrc)) return;
  
        isSliding = true;
  
        // Preload the new image
        const imgPreload = new Image();
        imgPreload.src = newSrc;
  
        imgPreload.onload = () => {
          // Slide current image to left
          mainImage.style.transform = 'translateX(-100%)';
  
          // Wait for slide-out to complete
          setTimeout(() => {
            // Instantly move new image from the right without transition
            mainImage.style.transition = 'none';
            mainImage.src = newSrc;
            mainImage.style.transform = 'translateX(100%)';
  
            // Force reflow to apply transform
            void mainImage.offsetWidth;
  
            // Slide new image into view
            mainImage.style.transition = 'transform 0.5s ease-in-out';
            mainImage.style.transform = 'translateX(0)';
  
            // Reset flag after animation
            setTimeout(() => {
              isSliding = false;
            }, 500);
          }, 500);
        };
      });
    });
  });

  // news2_left js start
  
  // video js start
  document.addEventListener("DOMContentLoaded", function () {
    const swiper = new Swiper(".mySwiper", {
      slidesPerView: 1,
      spaceBetween: 30,
      loop: true,
      speed: 800,
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      breakpoints: {
        768: { slidesPerView: 4 },
        1024: { slidesPerView: 5 }
      }
    });
  });
  
// bp-logo js start
  const brandSlider = document.getElementById("brandSlider");
  const brandTrack = document.getElementById("brandTrack");

  brandSlider.addEventListener("mouseover", () => {
    brandTrack.classList.add("paused");
  });

  brandSlider.addEventListener("mouseout", () => {
    brandTrack.classList.remove("paused");
  });