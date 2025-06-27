const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('visibile');
            observer.unobserve(entry.target);
        }
    });
});

document.querySelectorAll('.slide-in').forEach(el => {
    observer.observe(el);
});