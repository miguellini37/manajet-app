/**
 * Manajet Search and Filter System
 * Provides instant client-side search for all tables
 */

// Initialize search on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeTableSearch();
});

/**
 * Initialize search functionality for all tables
 */
function initializeTableSearch() {
    const tables = document.querySelectorAll('table');

    tables.forEach(table => {
        if (!table.id) {
            table.id = 'table-' + Math.random().toString(36).substr(2, 9);
        }

        addSearchBox(table);
    });
}

/**
 * Add search box above a table
 */
function addSearchBox(table) {
    // Create search container
    const searchContainer = document.createElement('div');
    searchContainer.className = 'search-container';
    searchContainer.style.cssText = 'margin-bottom: 16px; display: flex; gap: 12px; align-items: center;';

    // Create search input
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = '🔍 Search...';
    searchInput.className = 'search-input';
    searchInput.style.cssText = `
        flex: 1;
        padding: 12px 16px;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        font-size: 15px;
        transition: all 0.3s;
    `;

    // Add focus effect
    searchInput.addEventListener('focus', function() {
        this.style.borderColor = '#6366f1';
        this.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.1)';
    });

    searchInput.addEventListener('blur', function() {
        this.style.borderColor = '#cbd5e1';
        this.style.boxShadow = 'none';
    });

    // Create results counter
    const resultsCounter = document.createElement('span');
    resultsCounter.className = 'results-counter';
    resultsCounter.style.cssText = `
        color: #64748b;
        font-size: 14px;
        min-width: 120px;
    `;

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const tbody = table.querySelector('tbody');
        if (!tbody) return;

        const rows = tbody.querySelectorAll('tr');
        let visibleCount = 0;

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const isVisible = text.includes(searchTerm);

            row.style.display = isVisible ? '' : 'none';
            if (isVisible) visibleCount++;
        });

        // Update counter
        const totalCount = rows.length;
        if (searchTerm) {
            resultsCounter.textContent = `${visibleCount} of ${totalCount} results`;
        } else {
            resultsCounter.textContent = `${totalCount} total`;
        }
    });

    // Initial count
    const tbody = table.querySelector('tbody');
    if (tbody) {
        const totalCount = tbody.querySelectorAll('tr').length;
        resultsCounter.textContent = `${totalCount} total`;
    }

    // Clear button
    const clearButton = document.createElement('button');
    clearButton.textContent = '✕ Clear';
    clearButton.className = 'btn-secondary';
    clearButton.style.cssText = 'padding: 8px 16px; display: none;';
    clearButton.onclick = function() {
        searchInput.value = '';
        searchInput.dispatchEvent(new Event('input'));
        this.style.display = 'none';
    };

    // Show/hide clear button
    searchInput.addEventListener('input', function() {
        clearButton.style.display = this.value ? 'inline-block' : 'none';
    });

    // Assemble search box
    searchContainer.appendChild(searchInput);
    searchContainer.appendChild(resultsCounter);
    searchContainer.appendChild(clearButton);

    // Insert before table
    table.parentNode.insertBefore(searchContainer, table);
}

/**
 * Advanced filtering by column
 */
function addColumnFilters(table) {
    const thead = table.querySelector('thead');
    if (!thead) return;

    const headerRow = thead.querySelector('tr');
    const headers = headerRow.querySelectorAll('th');

    // Create filter row
    const filterRow = document.createElement('tr');
    filterRow.className = 'filter-row';

    headers.forEach((header, index) => {
        const th = document.createElement('th');
        const select = document.createElement('select');
        select.style.cssText = 'width: 100%; padding: 4px; font-size: 12px;';

        // Get unique values for this column
        const tbody = table.querySelector('tbody');
        const values = new Set();

        tbody.querySelectorAll('tr').forEach(row => {
            const cell = row.cells[index];
            if (cell) {
                values.add(cell.textContent.trim());
            }
        });

        // Add "All" option
        const allOption = document.createElement('option');
        allOption.value = '';
        allOption.textContent = 'All';
        select.appendChild(allOption);

        // Add unique values
        Array.from(values).sort().forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value;
            select.appendChild(option);
        });

        // Filter on change
        select.addEventListener('change', function() {
            filterTable(table);
        });

        th.appendChild(select);
        filterRow.appendChild(th);
    });

    thead.appendChild(filterRow);
}

/**
 * Filter table based on column filters
 */
function filterTable(table) {
    const filterRow = table.querySelector('.filter-row');
    if (!filterRow) return;

    const filters = filterRow.querySelectorAll('select');
    const tbody = table.querySelector('tbody');

    tbody.querySelectorAll('tr').forEach(row => {
        let shouldShow = true;

        filters.forEach((filter, index) => {
            if (filter.value) {
                const cellText = row.cells[index]?.textContent.trim();
                if (cellText !== filter.value) {
                    shouldShow = false;
                }
            }
        });

        row.style.display = shouldShow ? '' : 'none';
    });
}

/**
 * Export table to CSV
 */
function exportToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId) || document.querySelector('table');
    if (!table) return;

    const rows = [];

    // Get headers
    const headers = [];
    table.querySelectorAll('thead th').forEach(th => {
        headers.push(th.textContent.trim());
    });
    rows.push(headers.join(','));

    // Get visible rows only
    table.querySelectorAll('tbody tr').forEach(tr => {
        if (tr.style.display !== 'none') {
            const cells = [];
            tr.querySelectorAll('td').forEach(td => {
                // Clean up cell text and handle commas
                let text = td.textContent.trim();
                text = text.replace(/"/g, '""'); // Escape quotes
                if (text.includes(',') || text.includes('"')) {
                    text = `"${text}"`;
                }
                cells.push(text);
            });
            rows.push(cells.join(','));
        }
    });

    // Create and download file
    const csvContent = rows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Add export button to page
 */
function addExportButton(table, filename) {
    const button = document.createElement('button');
    button.className = 'btn btn-secondary';
    button.innerHTML = '📥 Export to CSV';
    button.style.cssText = 'margin-bottom: 16px;';
    button.onclick = function() {
        exportToCSV(table.id, filename);
    };

    table.parentNode.insertBefore(button, table.parentNode.firstChild);
}
