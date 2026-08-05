// admin/cms.js
document.addEventListener('DOMContentLoaded', () => {
  // Wait for Decap CMS to fully render the list and top bar
  setTimeout(() => {
    const addListBtn = document.querySelector('.cms-list .cms-list-add');
    const topBarButtons = document.querySelector('.cms-topbar__buttons');
    
    // Find the Preview button by its text content for robustness
    const previewBtn = Array.from(topBarButtons?.querySelectorAll('button') || [])
      .find(btn => btn.textContent.includes('Preview'));

    if (addListBtn && topBarButtons && previewBtn) {
      // Insert the "Add" button right after the Preview button
      topBarButtons.insertBefore(addListBtn, previewBtn.nextSibling);
    }
  }, 10000); // Increase timeout if your CMS loads slower
});
