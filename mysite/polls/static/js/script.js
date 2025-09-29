var swiper = new Swiper(".mySwiper", {
  slidesPerView: 3,
  spaceBetween: 20,
  navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
  // pagination: { el: ".swiper-pagination", clickable: true }, // se quiser bolinhas
  breakpoints: {
    0:    { slidesPerView: 1 },
    576:  { slidesPerView: 2 },
    992:  { slidesPerView: 3 }
  }
});
