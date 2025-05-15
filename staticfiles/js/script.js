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
    const toggleButton = document.querySelector(SELECTORS.DARK_MODE_TOGGLE);
    
    if (!toggleButton) {
      console.error("ake.fx: Dark mode toggle button not found");
      return;
    }
    
    const body = document.body;
    const icon = toggleButton.querySelector('i');
    
    if (!icon) {
      console.error("ake.fx: Icon element not found inside toggle button");
      return;
    }
    
    // Check for saved preference or system preference
    const savedDarkMode = localStorage.getItem(STORAGE_KEYS.DARK_MODE);
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Apply initial mode
    if (savedDarkMode === DARK_MODE_VALUES.ENABLED || 
        (savedDarkMode === null && prefersDarkMode)) {
      applyDarkMode(body, icon, true);
    } else {
      applyDarkMode(body, icon, false);
    }
    
    // Toggle dark mode on button click
    toggleButton.addEventListener('click', () => {
      const isDarkModeActive = body.classList.contains(CLASSES.DARK_MODE);
      applyDarkMode(body, icon, !isDarkModeActive);
      
      // Save preference to localStorage
      localStorage.setItem(
        STORAGE_KEYS.DARK_MODE, 
        !isDarkModeActive ? DARK_MODE_VALUES.ENABLED : DARK_MODE_VALUES.DISABLED
      );
    });
    
    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      // Only apply if user hasn't set a preference
      if (localStorage.getItem(STORAGE_KEYS.DARK_MODE) === null) {
        applyDarkMode(body, icon, e.matches);
      }
    });
    
    console.log("ake.fx: Dark mode functionality initialized");
  }
  
  /**
   * Apply dark mode or light mode
   * @param {HTMLElement} body - The document body element
   * @param {HTMLElement} icon - The toggle button icon element
   * @param {boolean} isDarkMode - Whether to apply dark mode
   */
  function applyDarkMode(body, icon, isDarkMode) {
    if (isDarkMode) {
      body.classList.add(CLASSES.DARK_MODE);
      updateDarkModeIcon(icon, true);
    } else {
      body.classList.remove(CLASSES.DARK_MODE);
      updateDarkModeIcon(icon, false);
    }
  }
  
  /**
   * Update dark mode toggle button icon
   * @param {HTMLElement} icon - The icon element
   * @param {boolean} isDarkMode - Current dark mode state
   */
  function updateDarkModeIcon(icon, isDarkMode) {
    if (isDarkMode) {
      icon.classList.remove(ICONS.MOON);
      icon.classList.add(ICONS.SUN);
    } else {
      icon.classList.remove(ICONS.SUN);
      icon.classList.add(ICONS.MOON);
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
})();