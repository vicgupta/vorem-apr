document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Function to set theme
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        updateThemeIcon(theme);
        localStorage.setItem('theme', theme);
    }
    
    // Check for saved theme preference or use system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
        setTheme(savedTheme);
    } else if (systemPrefersDark) {
        setTheme('dark');
    } else {
        setTheme('light');
    }
    
    // Theme toggle click handler
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }
    
    // Update theme icon based on current theme
    function updateThemeIcon(theme) {
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.innerHTML = '☀️';
                if (themeToggle) {
                    themeToggle.title = 'Switch to light theme';
                }
            } else {
                themeIcon.innerHTML = '🌙';
                if (themeToggle) {
                    themeToggle.title = 'Switch to dark theme';
                }
            }
        }
    }
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        // Only apply system theme if no saved preference
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            setTheme(newTheme);
        }
    });
}); 