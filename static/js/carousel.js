let slides = document.querySelectorAll(".slide");
let index = 0;

setInterval(() => {
    slides.forEach(slide => slide.classList.remove("active"));
    slides[index].classList.add("active");
    index = (index + 1) % slides.length;
}, 3000);
