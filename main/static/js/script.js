/**
 * ake.fx - Main JavaScript File
 * Includes dark mode functionality, navbar handlers, and alert auto-dismissal
 */

// IIFE to avoid global scope pollution
(function() {
  'use strict';
  
  console.log("ake.fx: Script loaded");
  
  // DOM elements and constants
  const SELECTORS = {
    DARK_MODE_TOGGLE: '#toggle-dark-mode',
    NAV_LINKS: '.nav-link',
    NAVBAR_COLLAPSE: '.navbar-collapse',
    ALERTS: '.alert:not(.alert-permanent)',
    CURRENT_PAGE_LINKS: '.navbar-nav .nav-link'
  };
  
  const CLASSES = {
    DARK_MODE: 'dark-mode',
    SHOW: 'show',
    ACTIVE: 'active'
  };
  
  const STORAGE_KEYS = {
    DARK_MODE: 'darkMode'
  };
  
  const DARK_MODE_VALUES = {
    ENABLED: 'enabled',
    DISABLED: 'disabled'
  };
  
  const ICONS = {
    MOON: 'fa-moon',
    SUN: 'fa-sun'
  };
  
  /**
   * Initialize navbar functionality
   * Close navbar when clicking on links in mobile view
   */
  function initializeNavbar() {
    const navLinks = document.querySelectorAll(SELECTORS.NAV_LINKS);
    const navbarCollapse = document.querySelector(SELECTORS.NAVBAR_COLLAPSE);
    
    if (!navLinks.length || !navbarCollapse) return;
    
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (navbarCollapse.classList.contains(CLASSES.SHOW)) {
          navbarCollapse.classList.remove(CLASSES.SHOW);
        }
      });
    });
    
    // Mark current page as active
    markCurrentPageActive();
    
    console.log("ake.fx: Navbar handlers initialized");
  }
  
  /**
   * Mark the current page link as active
   */
  function markCurrentPageActive() {
    const currentPage = window.location.pathname;
    const links = document.querySelectorAll(SELECTORS.CURRENT_PAGE_LINKS);
    
    links.forEach(link => {
      const href = link.getAttribute('href');
      
      if (href === currentPage || 
          (currentPage.includes(href) && href !== '/')) {
        link.classList.add(CLASSES.ACTIVE);
      } else if (currentPage === '/' && href === '/') {
        link.classList.add(CLASSES.ACTIVE);
      }
    });
  }
  
  /**
   * Initialize alert auto-dismissal
   * Fade out and remove alerts after specified time
   * @param {number} delay - Time in milliseconds before alerts fade out
   */
  function initializeAlerts(delay = 5000) {
    const alerts = document.querySelectorAll(SELECTORS.ALERTS);
    
    if (!alerts.length) return;
    
    setTimeout(() => {
      alerts.forEach(alert => {
        // Make sure the alert hasn't been manually closed
        if (document.body.contains(alert)) {
          // Add transition if not already present
          if (!alert.style.transition) {
            alert.style.transition = 'opacity 0.5s ease';
          }
          
          alert.style.opacity = '0';
          
          // Remove from DOM after fade completes
          setTimeout(() => {
            if (document.body.contains(alert)) {
              alert.remove();
            }
          }, 500);
        }
      });
    }, delay);
    
    console.log("ake.fx: Alert auto-dismissal initialized");
  }
  
  /**
   * Initialize dark mode functionality
   * Uses both localStorage and system preference
   */
  function initializeDarkMode() {
    const darkMode = localStorage.getItem('darkMode') === 'enabled';
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Apply initial theme
    if (darkMode || prefersDarkMode) {
        enableDarkMode();
    }
    
    // Theme toggle button
    const themeToggle = document.getElementById('toggle-dark-mode');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            if (document.body.classList.contains('dark-mode')) {
                disableDarkMode();
            } else {
                enableDarkMode();
            }
        });
    }
}

  function enableDarkMode() {
    document.body.classList.add('dark-mode');
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('darkMode', 'enabled');
    updateThemeIcon(true);
}

  function disableDarkMode() {
    document.body.classList.remove('dark-mode');
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('darkMode', 'disabled');
    updateThemeIcon(false);
}

  function updateThemeIcon(isDark) {
    const icon = document.querySelector('#toggle-dark-mode i');
    if (icon) {
        icon.className = isDark ? 'bi bi-sun' : 'bi bi-moon-stars';
    }
}

  /**
   * Initialize all functionality when DOM is ready
   */
  function initializeAll() {
    try {
      initializeNavbar();
      initializeAlerts();
      initializeDarkMode();
      console.log("ake.fx: All functionality initialized successfully");
    } catch (error) {
      console.error("ake.fx: Error initializing functionality:", error);
    }
  }
  
  /**
   * Check if document is loaded and initialize
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAll);
  } else {
    initializeAll();
  }
  
  /**
   * Toggle dark mode manually
   */
  function toggleDarkMode() {
    const body = document.body;
    const isDarkMode = body.classList.toggle('dark-mode');
    
    // Save preference
    localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
    
    // Update theme color meta tag
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.setAttribute('content', isDarkMode ? '#212529' : '#ffffff');
    }
  }

  // Check for saved dark mode preference
  document.addEventListener('DOMContentLoaded', () => {
    const darkModeSaved = localStorage.getItem('darkMode') === 'enabled';
    if (darkModeSaved) {
        document.body.classList.add('dark-mode');
    }
  });
})();