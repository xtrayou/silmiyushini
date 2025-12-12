document.addEventListener('DOMContentLoaded', () => {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    // Select elements to animate
    const animatedElements = document.querySelectorAll('.portfolio, .portfolio-1a, .portfolio-22, .card, .card-1c, .card-25, .stunning-introduction, .front-end-developer-portfolio, .skills-technologies, .experience, .contact');
    
    animatedElements.forEach(el => {
        el.classList.add('hidden');
        observer.observe(el);
    });
});
