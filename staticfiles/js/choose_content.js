 function toggleMenu() {
        const menu = document.getElementById("navbar-menu");
        const hamburger = document.getElementById("hamburger");

        menu.classList.toggle("active");
        hamburger.classList.toggle("open");

        // Optional: close on outside click
        document.addEventListener("click", function (event) {
            if (!event.target.closest(".navbar")) {
                menu.classList.remove("active");
                hamburger.classList.remove("open");
            }
        }, { once: true });
    }


//**********typeWriter and scroll progressbar****************//
const typingText = document.querySelector('.typing-text');
const username = typingText.dataset.username;
const welcome = `Welcome, ${username}!`;
let i = 0;

function typeWriter() {
    if (i < welcome.length) {
        typingText.innerHTML += welcome.charAt(i);
        i++;
        setTimeout(typeWriter, 80);
    }
}
typeWriter();



    const scrollProgress = document.getElementById("scrollProgress");

    window.addEventListener("scroll", () => {
        const scrollTop = window.scrollY;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrolled = (scrollTop / docHeight) * 100;
        scrollProgress.style.width = scrolled + "%";
    });



//***********************************************//
const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });


//**************************************//
 // Back to Top Button
    const backToTopButton = document.getElementById("backToTop");

    window.addEventListener("scroll", () => {
        if (window.scrollY > 300) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    });

    backToTopButton.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });



    // ***********************************************
// Disable Right Click
  document.addEventListener('contextmenu', event => event.preventDefault());

  // Disable Keyboard Shortcuts for Inspect Element
  document.addEventListener('keydown', function (event) {
      if (event.ctrlKey && (event.key === 'u' || event.key === 'U' || event.key === 's' || event.key === 'S' || event.key === 'p' || event.key === 'P')) {
          event.preventDefault();
      }
      if (event.ctrlKey && event.shiftKey && (event.key === 'I' || event.key === 'J' || event.key === 'C')) {
          event.preventDefault();
      }
      if (event.key === 'F12') {
          event.preventDefault();
      }
  });

  // Detect DevTools Opening (No alert, just logs)
  console.log('%c ', 'font-size: 1px; background: url() no-repeat;');
