// AOMaaS - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // Initialize components
  initDemoForm();
  initAnimations();
  setupNavigation();
});

/**
 * Initialize the demo form functionality
 */
function initDemoForm() {
  const demoForm = document.getElementById('demo-form');
  const repoInput = document.getElementById('repo-input');
  const analyzeButton = document.getElementById('analyze-button');
  const demoResults = document.getElementById('demo-results');
  const loadingIndicator = document.getElementById('loading-indicator');
  
  if (!demoForm) return;
  
  demoForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const repoUrl = repoInput.value.trim();
    if (!repoUrl) {
      showError('Please enter a valid repository URL');
      return;
    }
    
    // Show loading state
    loadingIndicator.style.display = 'flex';
    analyzeButton.disabled = true;
    demoResults.innerHTML = '';
    
    try {
      // Call the API to analyze the repository
      const response = await fetch('/api/v1/repositories/mine-opportunities', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repository_url: repoUrl,
          provider_type: detectProviderType(repoUrl)
        })
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      
      const data = await response.json();
      displayResults(data);
    } catch (error) {
      showError('An error occurred while analyzing the repository. Please try again.');
      console.error('Error:', error);
    } finally {
      // Hide loading state
      loadingIndicator.style.display = 'none';
      analyzeButton.disabled = false;
    }
  });
  
  /**
   * Display the analysis results
   */
  function displayResults(data) {
    demoResults.innerHTML = '';
    
    if (!data.opportunities || data.opportunities.length === 0) {
      demoResults.innerHTML = '<div class="no-results">No maintenance opportunities found in this repository.</div>';
      return;
    }
    
    // Create results header
    const resultsHeader = document.createElement('div');
    resultsHeader.className = 'results-header';
    resultsHeader.innerHTML = `
      <h3>Maintenance Opportunities</h3>
      <p>Found ${data.opportunities.length} opportunities for improvement</p>
    `;
    demoResults.appendChild(resultsHeader);
    
    // Create results list
    const resultsList = document.createElement('div');
    resultsList.className = 'results-list';
    
    data.opportunities.forEach((opportunity, index) => {
      const opportunityCard = document.createElement('div');
      opportunityCard.className = 'opportunity-card';
      opportunityCard.innerHTML = `
        <div class="opportunity-header">
          <div class="opportunity-type">${opportunity.type || 'Improvement'}</div>
          <div class="opportunity-priority ${getPriorityClass(opportunity.priority)}">${opportunity.priority || 'Medium'}</div>
        </div>
        <h4 class="opportunity-title">${opportunity.title || 'Unnamed Opportunity'}</h4>
        <p class="opportunity-description">${opportunity.description || 'No description provided'}</p>
        <div class="opportunity-meta">
          <span class="opportunity-location">${opportunity.location || 'Repository-wide'}</span>
          <span class="opportunity-effort">${getEffortLabel(opportunity.effort_estimate)}</span>
        </div>
      `;
      resultsList.appendChild(opportunityCard);
    });
    
    demoResults.appendChild(resultsList);
  }
  
  /**
   * Show an error message
   */
  function showError(message) {
    demoResults.innerHTML = `<div class="error-message">${message}</div>`;
  }
  
  /**
   * Get the CSS class for a priority level
   */
  function getPriorityClass(priority) {
    switch (priority?.toLowerCase()) {
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return 'priority-medium';
    }
  }
  
  /**
   * Get a human-readable effort label
   */
  function getEffortLabel(effort) {
    if (!effort) return 'Unknown effort';
    
    switch (effort.toLowerCase()) {
      case 'small': return 'Small effort (< 1 hour)';
      case 'medium': return 'Medium effort (1-4 hours)';
      case 'large': return 'Large effort (> 4 hours)';
      default: return effort;
    }
  }
  
  /**
   * Detect the provider type from the repository URL
   */
  function detectProviderType(url) {
    if (url.includes('github.com')) {
      return 'github';
    } else if (url.includes('gitlab.com')) {
      return 'gitlab';
    } else {
      return 'github'; // Default to GitHub
    }
  }
}

/**
 * Initialize scroll and reveal animations
 */
function initAnimations() {
  // Reveal elements on scroll
  const revealElements = document.querySelectorAll('.reveal');
  
  if (revealElements.length > 0) {
    const revealOnScroll = function() {
      for (let i = 0; i < revealElements.length; i++) {
        const windowHeight = window.innerHeight;
        const elementTop = revealElements[i].getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < windowHeight - elementVisible) {
          revealElements[i].classList.add('active');
        }
      }
    };
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Check on load
  }
  
  // Animate code typing effect
  const codeElements = document.querySelectorAll('.code-content');
  
  codeElements.forEach(codeElement => {
    const codeLines = codeElement.querySelectorAll('.code-line');
    
    codeLines.forEach((line, index) => {
      line.style.opacity = '0';
      
      setTimeout(() => {
        line.style.transition = 'opacity 0.5s ease-in-out';
        line.style.opacity = '1';
      }, 500 + (index * 100));
    });
  });
}

/**
 * Setup navigation functionality
 */
function setupNavigation() {
  // Smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  
  anchorLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80, // Offset for fixed header
          behavior: 'smooth'
        });
      }
    });
  });
}