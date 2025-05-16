// static/js/theme-toggle.js

document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    const currentTheme = localStorage.getItem('theme') || 'light';
  
    // Apply saved theme
    html.setAttribute('data-theme', currentTheme);
    updateIcons(currentTheme);
  
    // Handle toggle click
    toggle.addEventListener('click', () => {
      const newTheme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateIcons(newTheme);
    });
  
    function updateIcons(theme) {
      if (theme === 'dark') {
        toggle.classList.remove('bi-moon');
        toggle.classList.add('bi-sun');
      } else {
        toggle.classList.remove('bi-sun');
        toggle.classList.add('bi-moon');
      }
    }
  });
  