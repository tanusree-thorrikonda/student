/**
 * EduPulse - Student Management System
 * Core Client-Side Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    initClientSearch();
    initAlertAutoDismiss();
    initTableSorting();
});

/* ==========================================================================
   REAL-TIME CLIENT-SIDE TABLE SEARCH FILTER
   ========================================================================== */
function initClientSearch() {
    const searchInput = document.getElementById('searchInput');
    const studentsTable = document.getElementById('studentsTable');
    
    if (!searchInput || !studentsTable) return;

    const tableRows = studentsTable.querySelectorAll('tbody tr.student-row');

    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase().trim();
        
        tableRows.forEach(row => {
            // Read columns text content (Student ID, Name, Email, Major)
            const idText = row.querySelector('.badge-id')?.textContent.toLowerCase() || '';
            const nameText = row.querySelector('.student-name-col')?.textContent.toLowerCase() || '';
            const emailText = row.cells[2]?.textContent.toLowerCase() || '';
            const majorText = row.querySelector('.badge-major')?.textContent.toLowerCase() || '';
            
            // Show row if query matches any column, else hide it
            if (idText.includes(searchTerm) || 
                nameText.includes(searchTerm) || 
                emailText.includes(searchTerm) || 
                majorText.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });

        // Optional: show a 'No matching results' row if everything is hidden
        const visibleRows = Array.from(tableRows).filter(row => row.style.display !== 'none');
        let noMatchRow = document.getElementById('noMatchRow');

        if (visibleRows.length === 0) {
            if (!noMatchRow) {
                noMatchRow = document.createElement('tr');
                noMatchRow.id = 'noMatchRow';
                noMatchRow.innerHTML = `
                    <td colspan="6" style="text-align: center; padding: 40px; color: var(--text-muted);">
                        <i class="fa-solid fa-magnifying-glass-minus" style="font-size: 24px; margin-bottom: 8px; display: block; opacity: 0.5;"></i>
                        No students match your live search. Press Enter to search on server.
                    </td>
                `;
                studentsTable.querySelector('tbody').appendChild(noMatchRow);
            }
        } else {
            if (noMatchRow) {
                noMatchRow.remove();
            }
        }
    });
}

/* ==========================================================================
   MODAL DELETE CONFIRMATION HANDLER
   ========================================================================== */
let activeDeleteForm = null;

/**
 * Triggered on submit of student delete forms.
 * Prevents default submit, grabs student name, and displays custom modal dialog.
 */
function confirmDelete(event, studentName) {
    event.preventDefault(); // Stop form submission
    activeDeleteForm = event.currentTarget; // Store form reference
    
    const modal = document.getElementById('deleteModal');
    const nameSpan = document.getElementById('deleteStudentName');
    
    if (modal && nameSpan) {
        nameSpan.textContent = studentName;
        modal.classList.add('show');
        
        // Add event listener to confirm delete button
        const confirmBtn = document.getElementById('confirmDeleteBtn');
        if (confirmBtn) {
            // Clear existing listeners to avoid multiple submissions
            const newConfirmBtn = confirmBtn.cloneNode(true);
            confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
            
            newConfirmBtn.addEventListener('click', () => {
                if (activeDeleteForm) {
                    activeDeleteForm.submit();
                }
            });
        }
    }
    
    return false;
}

/**
 * Closes the active confirmation modal dialog.
 */
function closeModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
        modal.classList.remove('show');
    }
    activeDeleteForm = null;
}

// Close modal if user clicks outside of the glass card content
window.addEventListener('click', (event) => {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        closeModal();
    }
});

/* ==========================================================================
   AUTO DISMISS ALERTS
   ========================================================================== */
function initAlertAutoDismiss() {
    const alerts = document.querySelectorAll('.alerts-container .alert');
    alerts.forEach(alert => {
        // Auto-fade out alerts after 5 seconds
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
}

/* ==========================================================================
   INTERACTIVE CLIENT-SIDE TABLE COLUMN SORTING
   ========================================================================== */
function initTableSorting() {
    const studentsTable = document.getElementById('studentsTable');
    if (!studentsTable) return;

    const headers = studentsTable.querySelectorAll('thead th[data-sort]');
    const tbody = studentsTable.querySelector('tbody');

    headers.forEach(header => {
        header.addEventListener('click', () => {
            const sortKey = header.getAttribute('data-sort');
            const sortType = header.getAttribute('data-type') || 'string';
            const currentDir = header.getAttribute('data-dir') || 'desc';
            const newDir = currentDir === 'asc' ? 'desc' : 'asc';

            // Clear previous sorting directions on all headers
            headers.forEach(h => {
                h.removeAttribute('data-dir');
                const icon = h.querySelector('.sort-icon');
                if (icon) {
                    icon.className = 'fa-solid fa-sort sort-icon';
                }
            });

            // Set new direction on clicked header
            header.setAttribute('data-dir', newDir);
            const icon = header.querySelector('.sort-icon');
            if (icon) {
                icon.className = newDir === 'asc' 
                    ? 'fa-solid fa-sort-up sort-icon active' 
                    : 'fa-solid fa-sort-down sort-icon active';
            }

            // Get row elements
            const rows = Array.from(tbody.querySelectorAll('tr.student-row'));

            // Sort rows
            rows.sort((rowA, rowB) => {
                let valA = getCellValue(rowA, sortKey);
                let valB = getCellValue(rowB, sortKey);

                if (sortType === 'number') {
                    valA = parseFloat(valA) || 0;
                    valB = parseFloat(valB) || 0;
                } else {
                    valA = valA.toLowerCase();
                    valB = valB.toLowerCase();
                }

                if (valA < valB) return newDir === 'asc' ? -1 : 1;
                if (valA > valB) return newDir === 'asc' ? 1 : -1;
                return 0;
            });

            // Re-append sorted rows to body
            rows.forEach(row => tbody.appendChild(row));
            
            // Re-append noMatchRow if it exists and is currently visible
            const noMatchRow = document.getElementById('noMatchRow');
            if (noMatchRow) {
                tbody.appendChild(noMatchRow);
            }
        });
    });
}

function getCellValue(row, sortKey) {
    if (sortKey === 'id') {
        return row.querySelector('.badge-id')?.textContent.trim() || '';
    } else if (sortKey === 'name') {
        return row.querySelector('.student-name-col')?.textContent.trim() || '';
    } else if (sortKey === 'email') {
        return row.cells[2]?.textContent.trim() || '';
    } else if (sortKey === 'major') {
        return row.querySelector('.badge-major')?.textContent.trim() || '';
    } else if (sortKey === 'gpa') {
        return row.querySelector('.gpa-badge')?.textContent.trim() || '';
    }
    return '';
}
