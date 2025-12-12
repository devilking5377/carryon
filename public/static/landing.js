// Utility functions
function byId(id) { return document.getElementById(id) }
function on(el, ev, fn) { if (el) el.addEventListener(ev, fn) }

// Navigation functions
function openWeb() { window.location.href = '/app' }
function downloadExtension() { window.location.href = '/download-extension' }

// Smooth scrolling for anchor links
function initSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// Navbar scroll effect
function initNavbarScroll() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;
  
  let lastScrollY = window.scrollY;

  window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;
    
    if (currentScrollY > 100) {
      navbar.style.background = 'rgba(255, 255, 255, 0.98)';
      navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
      navbar.style.background = 'rgba(255, 255, 255, 0.95)';
      navbar.style.boxShadow = 'none';
    }
    
    lastScrollY = currentScrollY;
  }, { passive: true });
}

// Mobile menu toggle
function initMobileMenu() {
  const toggle = byId('mobileMenuToggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-open');
      toggle.classList.toggle('active');
    });
  }
}

// Intersection Observer for animations
function initScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe elements for animation
  document.querySelectorAll('.feature-card, .step, .use-case, .pricing-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Hero demo animation
function initHeroDemo() {
  const demoText = document.querySelector('.demo-input .demo-text');
  const outputText = document.querySelector('.demo-output .demo-text');
  
  if (demoText && outputText) {
    // Initial state
    outputText.style.opacity = '0';
    outputText.style.transform = 'translateY(10px)';
    outputText.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    
    // Animate after delay
    setTimeout(() => {
      outputText.style.opacity = '1';
      outputText.style.transform = 'translateY(0)';
    }, 2000);
  }
}

// Stats counter animation
function initStatsCounter() {
  const stats = document.querySelectorAll('.stat-number');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const stat = entry.target;
        const finalValue = stat.textContent;
        
        if (finalValue === '100%') {
          animateCounter(stat, 0, 100, '%');
        } else if (finalValue === '0') {
          animateCounter(stat, 10, 0, '');
        }
        
        observer.unobserve(stat);
      }
    });
  });
  
  stats.forEach(stat => observer.observe(stat));
}

function animateCounter(element, start, end, suffix) {
  const duration = 2000;
  const startTime = performance.now();
  
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    const current = Math.floor(start + (end - start) * progress);
    element.textContent = current + suffix;
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}

// Button click handlers
function initButtonHandlers() {
  // Main CTA buttons
  const ctaButtons = [
    'openWeb', 'tryNowBtn', 'getStartedBtn', 'finalCTABtn'
  ];
  
  ctaButtons.forEach(id => {
    const btn = byId(id);
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openWeb();
      });
    }
  });
  
  // Extension download buttons
  const extensionButtons = [
    'downloadExt', 'downloadExtBtn', 'footerExtension'
  ];
  
  extensionButtons.forEach(id => {
    const btn = byId(id);
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        downloadExtension();
      });
    }
  });
}

// Theme detection and handling
function initThemeHandling() {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
  
  function updateTheme(e) {
    document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
  }
  
  prefersDark.addEventListener('change', updateTheme);
  updateTheme(prefersDark);
}

// Performance optimizations
function initPerformanceOptimizations() {
  // Lazy load images
  const images = document.querySelectorAll('img[data-src]');
  if (images.length > 0) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });
    
    images.forEach(img => imageObserver.observe(img));
  }
}

// Add button hover effects
function initButtonEffects() {
  const buttons = document.querySelectorAll('.btn');
  buttons.forEach(btn => {
    btn.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-2px)';
    });
    
    btn.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 CarryOn Summary landing page loaded');
  
  // Initialize all features
  initSmoothScrolling();
  initNavbarScroll();
  initMobileMenu();
  initScrollAnimations();
  initHeroDemo();
  initStatsCounter();
  initButtonHandlers();
  initThemeHandling();
  initPerformanceOptimizations();
  initButtonEffects();
  
  // Add loading complete class
  document.body.classList.add('loaded');
  
  console.log('✅ All landing page features initialized');
});

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
  if (document.visibilityState === 'visible') {
    console.log('👀 Page is now visible');
  }
});

// Export functions for global access
window.CarryOnLanding = {
  openWeb,
  downloadExtension,
  byId,
  on
};