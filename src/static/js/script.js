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

document.querySelectorAll('.appear').forEach(el => {
    observer.observe(el);
});

// Tooltip popup
const tooltip = document.getElementById('fixed-tooltip');
document.querySelectorAll('#skill-type').forEach(skill => {
    skill.addEventListener('mouseenter', () => {
        if(skill.dataset.tooltip == null)
            return;

        tooltip.textContent = skill.dataset.tooltip;
        tooltip.style.opacity = '1';
    });

    skill.addEventListener('mouseleave', () => {
        tooltip.style.opacity = '0';
    });

    skill.addEventListener('mousemove', (e) => {
        tooltip.style.top = `${e.clientY + 15}px`;
        tooltip.style.left = `${e.clientX + 15}px`;
    });
});

// Link pills
const link = document.querySelectorAll('#link');
document.querySelectorAll('#link').forEach(link => {
    const innerLink = link.querySelector('a');

    link.addEventListener('mouseenter', () => {
        innerLink.style.background = '#fff';
        innerLink.style.color = '#000';
    });

    link.addEventListener('mouseleave', () => {
        innerLink.style.background = '#097ae4';
        innerLink.style.color = '#fff';
    })
});

//Typewriter
const messages = [
    "software developer.",
    "backend developer.",
    "web developer."
]

const typewriter = document.querySelector('.typewriter');
let messageIndex = 0;
let charIndex = 0;
let isDeleting = false;

function typeLoop() {
    const currentMessage = messages[messageIndex];

    if(!isDeleting) {
        // textContent = first character
        typewriter.textContent = currentMessage.substring(0, charIndex + 1);
        // Increase character index by 1 (move to next character)
        charIndex++;

        // If character index equals length of current message
        if(charIndex === currentMessage.length) {
            isDeleting = true;
            setTimeout(typeLoop, 1500);
            return;
        }
    } else {
        // remove characters
        typewriter.textContent = currentMessage.substring(0, charIndex - 1);
        // Subtract 1 from character index
        charIndex--;

        if(charIndex === 0) {
            isDeleting = false;
            // Loop to next message
            messageIndex = (messageIndex + 1) % messages.length;
        }
    }
    const speed = isDeleting ? 50 : 100;
    setTimeout(typeLoop, speed);
}

document.addEventListener('DOMContentLoaded', () => {
    typeLoop();
});

// Contact Form
document.querySelector("#contact-form").addEventListener('submit', function(e) {
    e.preventDefault() // Prevent default form
    const formData = new FormData(this);

    fetch("/submit-form", {
        "method": "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const modalContent = document.getElementById("modalContent");

        if (data.success) {
            modalContent.innerHTML = `
                <p>Thank you for your message!</p>
                <p>I will respond to you as soon as possible.</p>
            `;
        } else {
            let errors = "";
            for(const field in data.errors) {
                data.errors[field].forEach(msg => {
                    errors += `<li>${msg}</li>`;
                });
            }
            modalContent.innerHTML = `
            <p>An error has occured:</p>
            <ul>${errors}</ul>`;
        }
        document.getElementById("successModal").style.display = "flex";
        document.querySelector("#contact-form").reset();
    });
});
