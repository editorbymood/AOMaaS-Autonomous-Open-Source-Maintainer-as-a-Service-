/**
 * Demo page functionality for AOMaaS
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize demo functionality
    initDemoPage();
});

function initDemoPage() {
    // Set up tab switching
    setupTabs();
    
    // Set up repository card buttons
    setupRepoButtons();
    
    // Set up opportunity buttons
    setupOpportunityButtons();
    
    // Set up implementation buttons
    setupImplementationButtons();
    
    // Fetch demo data from API
    fetchDemoData();
}

function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

function setupRepoButtons() {
    const repoButtons = document.querySelectorAll('.repo-card .btn');
    repoButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Get repository ID from parent card
            const repoId = button.closest('.repo-card').getAttribute('data-repo-id');
            
            // Switch to opportunities tab
            switchToTab('opportunities');
            
            // Highlight opportunities for this repository
            // In a real implementation, this would filter opportunities by repo
            console.log(`Showing opportunities for repository: ${repoId}`);
        });
    });
}

function setupOpportunityButtons() {
    const oppButtons = document.querySelectorAll('.opportunity-item .btn');
    oppButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Get opportunity ID from parent item
            const oppId = button.closest('.opportunity-item').getAttribute('data-opp-id');
            
            // Switch to implementations tab
            switchToTab('implementations');
            
            // Highlight implementations for this opportunity
            // In a real implementation, this would filter implementations by opportunity
            console.log(`Showing implementations for opportunity: ${oppId}`);
        });
    });
}

function setupImplementationButtons() {
    const implButtons = document.querySelectorAll('.implementation-item .btn');
    implButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Get implementation ID from parent item
            const implId = button.closest('.implementation-item').getAttribute('data-impl-id');
            
            // Simulate creating a PR
            console.log(`Creating PR for implementation: ${implId}`);
            
            // Show success message
            alert('Demo PR created successfully! In a real application, this would create a pull request.');
        });
    });
}

function switchToTab(tabId) {
    // Get all tab buttons and contents
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Remove active class from all buttons and contents
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Add active class to specified tab button and content
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

async function fetchDemoData() {
    try {
        // In a real implementation, these would be actual API calls
        // For demo purposes, we're just logging to console
        console.log('Fetching demo repositories...');
        // const repoResponse = await fetch('/api/v1/demo/repositories');
        // const repositories = await repoResponse.json();
        
        console.log('Fetching demo opportunities...');
        // const oppResponse = await fetch('/api/v1/demo/opportunities');
        // const opportunities = await oppResponse.json();
        
        console.log('Fetching demo implementations...');
        // const implResponse = await fetch('/api/v1/demo/implementations');
        // const implementations = await implResponse.json();
        
        console.log('Demo data loaded successfully');
    } catch (error) {
        console.error('Error fetching demo data:', error);
    }
}