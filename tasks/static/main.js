const scrollRevealOption = {
    distance: "50px",
    origin: "buttom",
    duration: 1000,
};

ScrollReveal().reveal(".header_image img",{
    ...scrollRevealOption,
    origin: "right",
})
