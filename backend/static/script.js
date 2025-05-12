document.addEventListener('DOMContentLoaded', () => {
    
    // DOM Elements - Matrix Inputs
    const matrixAInputs = document.getElementById('matrixAInputs');
    const matrixBInputs = document.getElementById('matrixBInputs');
    const matrixMultAInputs = document.getElementById('matrixMultAInputs');
    const matrixMultBInputs = document.getElementById('matrixMultBInputs');
    const matrixDetInputs = document.getElementById('matrixDetInputs');
    const matrixInvInputs = document.getElementById('matrixInvInputs'); // Added for Inverse
    const matrixGaussAInputs = document.getElementById('matrixGaussAInputs'); // For Gaussian Elimination Matrix A
    const vectorGaussBInputs = document.getElementById('vectorGaussBInputs'); // For Gaussian Elimination Vector b
    const matrixGaussJordanAInputs = document.getElementById('matrixGaussJordanAInputs'); // For Gauss-Jordan Elimination Matrix A
    const vectorGaussJordanBInputs = document.getElementById('vectorGaussJordanBInputs'); // For Gauss-Jordan Elimination Vector b
    const matrixLuAInputs = document.getElementById('matrixLuAInputs'); // For LU Factorization Matrix A
    
    // Additional check to ensure determinant inputs element is found
    if (!matrixDetInputs) {
        console.error('matrixDetInputs element not found in DOM');
        // Try finding it with a different selector
        const detInputs = document.querySelector('#determinant .matrix-inputs');
        if (detInputs) {
            detInputs.id = 'matrixDetInputs'; // Ensure it has the correct ID
        }
    }
    
    const rowsASelector = document.getElementById('rowsA');
    const colsASelector = document.getElementById('colsA');
    const rowsBSelector = document.getElementById('rowsB');
    const colsBSelector = document.getElementById('colsB');
    const rowsMultASelector = document.getElementById('rowsMultA');
    const colsMultASelector = document.getElementById('colsMultA');
    const rowsMultBSelector = document.getElementById('rowsMultB');
    const colsMultBSelector = document.getElementById('colsMultB');
    const dimensionDetSelector = document.getElementById('dimensionDet');
    const dimensionInvSelector = document.getElementById('dimensionInv'); // Added for Inverse
    const dimensionGaussASelector = document.getElementById('dimensionGaussA'); // For Gaussian A
    const dimensionGaussBDisplay = document.getElementById('dimensionGaussBDisplay'); // To display b's dimension
    const dimensionGaussJordanASelector = document.getElementById('dimensionGaussJordanA'); // For Gauss-Jordan A
    const dimensionGaussJordanBDisplay = document.getElementById('dimensionGaussJordanBDisplay'); // To display Gauss-Jordan b's dimension
    const dimensionLuASelector = document.getElementById('dimensionLuA'); // For LU Factorization A

    // DOM Elements - Operation Buttons
    const addButton = document.getElementById('addButton');
    const subtractButton = document.getElementById('subtractButton');
    const multiplyButton = document.getElementById('multiplyButton');
    const determinantButton = document.getElementById('determinantButton');
    const inverseButton = document.getElementById('inverseButton'); // Added for Inverse
    const solveGaussianButton = document.getElementById('solveGaussianButton'); // For Gaussian Elimination
    const solveGaussJordanButton = document.getElementById('solveGaussJordanButton'); // For Gauss-Jordan Elimination
    const luFactorizationButton = document.getElementById('luFactorizationButton'); // For LU Factorization

    // DOM Elements - Results Display
    const resultMatrixDiv = document.getElementById('resultMatrix');
    const resultMultMatrixDiv = document.getElementById('resultMultMatrix');
    const resultDeterminantDiv = document.getElementById('resultDeterminant'); // Corrected ID from determinantValueDiv
    const resultInverseMatrixDiv = document.getElementById('resultInverseMatrix'); // Added for Inverse
    const resultGaussianSolutionDiv = document.getElementById('resultGaussianSolution'); // For Gaussian Elimination
    const resultGaussJordanRrefDiv = document.getElementById('resultGaussJordanRref'); // For Gauss-Jordan RREF
    const resultGaussJordanSolutionDiv = document.getElementById('resultGaussJordanSolution'); // For Gauss-Jordan Solution
    const resultLuLMatrixDiv = document.getElementById('resultLuLMatrix'); // For LU Factorization Matrix L
    const resultLuUMatrixDiv = document.getElementById('resultLuUMatrix'); // For LU Factorization Matrix U
    const stepsDisplay = document.getElementById('stepsDisplay');
    const stepsMultDisplay = document.getElementById('stepsMultDisplay');
    const stepsDetDisplay = document.getElementById('stepsDetDisplay');
    const stepsInvDisplay = document.getElementById('stepsInvDisplay'); // Added for Inverse
    const stepsGaussianDisplay = document.getElementById('stepsGaussianDisplay'); // For Gaussian Elimination
    const stepsGaussJordanDisplay = document.getElementById('stepsGaussJordanDisplay'); // For Gauss-Jordan
    const stepsLuDisplay = document.getElementById('stepsLuDisplay'); // For LU Factorization
    const errorDisplay = document.getElementById('errorDisplay');
    const errorMultDisplay = document.getElementById('errorMultDisplay');
    const errorDetDisplay = document.getElementById('errorDetDisplay');
    const errorInvDisplay = document.getElementById('errorInvDisplay'); // Added for Inverse
    const errorGaussianDisplay = document.getElementById('errorGaussianDisplay'); // For Gaussian Elimination
    const errorGaussJordanDisplay = document.getElementById('errorGaussJordanDisplay'); // For Gauss-Jordan
    const errorLuDisplay = document.getElementById('errorLuDisplay'); // For LU Factorization
    const loader = document.getElementById('loader');
    const multiplicationLoader = document.getElementById('multiplicationLoader');
    const determinantLoader = document.getElementById('determinantLoader');
    const inverseLoader = document.getElementById('inverseLoader'); // Added for Inverse
    const gaussianLoader = document.getElementById('gaussianLoader'); // For Gaussian Elimination
    const gaussJordanLoader = document.getElementById('gaussJordanLoader'); // For Gauss-Jordan
    const luLoader = document.getElementById('luLoader'); // For LU Factorization
    const multiplicationDimensionHint = document.getElementById('multiplicationDimensionHint');
    
    // DOM Elements - UI Controls
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    const themeToggle = document.querySelector('.theme-toggle');
    const copyResultBtn = document.getElementById('copyResult');
    const copyMultResultBtn = document.getElementById('copyMultResult');
    const copyDetResultBtn = document.getElementById('copyDetResult');
    const copyInvResultBtn = document.getElementById('copyInvResult'); // Added for Inverse
    const copyGaussianResultBtn = document.getElementById('copyGaussianResult'); // For Gaussian Elimination
    const copyGaussJordanRrefResultBtn = document.getElementById('copyGaussJordanRrefResult'); // For Gauss-Jordan RREF 
    const copyGaussJordanSolutionResultBtn = document.getElementById('copyGaussJordanSolutionResult'); // For Gauss-Jordan Solution
    const copyLuLResultBtn = document.getElementById('copyLuLResult'); // For LU Matrix L
    const copyLuUResultBtn = document.getElementById('copyLuUResult'); // For LU Matrix U
    
    // For 3D effect on matrices
    const matrixWrappers = document.querySelectorAll('.matrix-wrapper');

    // Helper function to convert digit to Unicode subscript
    function toSubscript(digit) {
        const subscripts = "₀₁₂₃₄₅₆₇₈₉";
        return String(digit).split('').map(char => subscripts[parseInt(char)] || char).join('');
    }

    // Initialize UI
    initializeUI();
    
    function initializeUI() {
        // Initialize tabs
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Skip if clicking on an already active tab
                if (button.classList.contains('active')) return;
                
                // Remove active class from all tabs
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab
                button.classList.add('active');
                
                // Show corresponding content
                const tabId = button.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');

                // If switching to multiplication tab, update dimension hints
                if (tabId === 'multiplication') {
                    updateMultiplicationDimensionHint();
                    // Add 3D effect to matrix wrappers
                    document.querySelectorAll('#multiplication .matrix-wrapper').forEach(wrapper => {
                        wrapper.classList.add('mult-3d');
                    });
                }
                
                // If switching to determinant tab, apply 3D effect if applicable
                if (tabId === 'determinant') {
                    document.querySelectorAll('#determinant .matrix-wrapper').forEach(wrapper => {
                        // wrapper.classList.add('det-3d'); // Example: can add specific 3d class if needed
                    });
                    
                    const detDimension = parseInt(dimensionDetSelector.value);
                    if (matrixDetInputs && matrixDetInputs.childElementCount === 0) {
                        generateMatrixInputs(matrixDetInputs, detDimension, detDimension, 'Det');
                    }
                }

                // If switching to inverse tab, initialize inputs
                if (tabId === 'inverse') {
                    document.querySelectorAll('#inverse .matrix-wrapper').forEach(wrapper => {
                        // wrapper.classList.add('inv-3d'); // Example: can add specific 3d class if needed
                    });
                    const invDimension = parseInt(dimensionInvSelector.value);
                    if (matrixInvInputs && matrixInvInputs.childElementCount === 0) {
                        generateMatrixInputs(matrixInvInputs, invDimension, invDimension, 'Inv');
                    }
                }

                // If switching to Gaussian elimination tab, initialize inputs
                if (tabId === 'gaussian-elimination') {
                    const gaussDim = parseInt(dimensionGaussASelector.value);
                    if (matrixGaussAInputs && matrixGaussAInputs.childElementCount === 0) {
                        generateMatrixInputs(matrixGaussAInputs, gaussDim, gaussDim, 'Agauss');
                    }
                    if (vectorGaussBInputs && vectorGaussBInputs.childElementCount === 0) {
                        generateVectorInputs(vectorGaussBInputs, gaussDim, 'bgauss');
                    }
                    updateGaussianDimensionDisplay();
                }
                
                // If switching to Gauss-Jordan tab, initialize inputs
                if (tabId === 'gauss-jordan') {
                    const gaussJordanDim = parseInt(dimensionGaussJordanASelector.value);
                    if (matrixGaussJordanAInputs && matrixGaussJordanAInputs.childElementCount === 0) {
                        generateMatrixInputs(matrixGaussJordanAInputs, gaussJordanDim, gaussJordanDim, 'Agj');
                    }
                    if (vectorGaussJordanBInputs && vectorGaussJordanBInputs.childElementCount === 0) {
                        generateVectorInputs(vectorGaussJordanBInputs, gaussJordanDim, 'bgj');
                    }
                    updateGaussJordanDimensionDisplay();
                }

                // If switching to LU factorization tab, initialize inputs
                if (tabId === 'lu-factorization') {
                    const luDim = parseInt(dimensionLuASelector.value);
                    if (matrixLuAInputs && matrixLuAInputs.childElementCount === 0) {
                        generateMatrixInputs(matrixLuAInputs, luDim, luDim, 'A_lu');
                    }
                }
            });
        });
        
        // Initialize theme toggle
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
        
        themeToggle.addEventListener('click', toggleTheme);
        
        // Initialize copy buttons
        if (copyResultBtn) {
            copyResultBtn.addEventListener('click', () => copyResultToClipboard(resultMatrixDiv, copyResultBtn));
        }
        if (copyMultResultBtn) {
            copyMultResultBtn.addEventListener('click', () => copyResultToClipboard(resultMultMatrixDiv, copyMultResultBtn));
        }
        if (copyDetResultBtn) {
            // Assuming determinant result is displayed in resultDeterminantDiv now, not a scalar specific div
            // If resultDeterminantDiv contains a table, use copyResultToClipboard
            // If it's a scalar value directly in resultDeterminantDiv, a modified copyScalar might be needed
            copyDetResultBtn.addEventListener('click', () => copyScalarResultToClipboard(resultDeterminantDiv.textContent, copyDetResultBtn)); 
        }
        if (copyInvResultBtn) { // Added for Inverse
            copyInvResultBtn.addEventListener('click', () => copyResultToClipboard(resultInverseMatrixDiv, copyInvResultBtn));
        }
        if (copyGaussianResultBtn) {
            copyGaussianResultBtn.addEventListener('click', () => copyGaussianSolutionToClipboard(resultGaussianSolutionDiv, copyGaussianResultBtn));
        }
        if (copyGaussJordanRrefResultBtn) {
            copyGaussJordanRrefResultBtn.addEventListener('click', () => copyResultToClipboard(resultGaussJordanRrefDiv, copyGaussJordanRrefResultBtn));
        }
        if (copyGaussJordanSolutionResultBtn) {
            copyGaussJordanSolutionResultBtn.addEventListener('click', () => copyGaussianSolutionToClipboard(resultGaussJordanSolutionDiv, copyGaussJordanSolutionResultBtn));
        }
        if (copyLuLResultBtn) {
            copyLuLResultBtn.addEventListener('click', () => copyResultToClipboard(resultLuLMatrixDiv, copyLuLResultBtn));
        }
        if (copyLuUResultBtn) {
            copyLuUResultBtn.addEventListener('click', () => copyResultToClipboard(resultLuUMatrixDiv, copyLuUResultBtn));
        }
        
        // Generate initial matrix inputs
        generateMatrixInputs(matrixAInputs, parseInt(rowsASelector.value), parseInt(colsASelector.value), 'A');
        generateMatrixInputs(matrixBInputs, parseInt(rowsBSelector.value), parseInt(colsBSelector.value), 'B');
        generateMatrixInputs(matrixMultAInputs, parseInt(rowsMultASelector.value), parseInt(colsMultASelector.value), 'A');
        generateMatrixInputs(matrixMultBInputs, parseInt(rowsMultBSelector.value), parseInt(colsMultBSelector.value), 'B');
        
        // Generate determinant matrix (square)
        const detDimension = parseInt(dimensionDetSelector.value);
        
        if (matrixDetInputs) {
            generateMatrixInputs(matrixDetInputs, detDimension, detDimension, 'Det'); // Changed prefix to 'Det'
        } else {
            console.error('matrixDetInputs element not found!');
        }

        // Generate inverse matrix (square)
        const invDimension = parseInt(dimensionInvSelector.value);
     
        if (matrixInvInputs) {
            generateMatrixInputs(matrixInvInputs, invDimension, invDimension, 'Inv');
        } else {
            console.error('matrixInvInputs element not found!');
        }

        // Generate Gaussian elimination inputs
        const gaussADimension = parseInt(dimensionGaussASelector.value);
        if (matrixGaussAInputs) {
            generateMatrixInputs(matrixGaussAInputs, gaussADimension, gaussADimension, 'Agauss');
        }
        if (vectorGaussBInputs) {
            generateVectorInputs(vectorGaussBInputs, gaussADimension, 'bgauss');
        }
        updateGaussianDimensionDisplay();
        
        // Generate LU Factorization Matrix A inputs
        const luADimension = parseInt(dimensionLuASelector.value);
        if (matrixLuAInputs) {
            generateMatrixInputs(matrixLuAInputs, luADimension, luADimension, 'A_lu');
        }
        
        // Set up event listeners for dimension selectors
        rowsASelector.addEventListener('change', () => updateMatrixDimensions(matrixAInputs, rowsASelector, colsASelector, 'A'));
        colsASelector.addEventListener('change', () => updateMatrixDimensions(matrixAInputs, rowsASelector, colsASelector, 'A'));
        rowsBSelector.addEventListener('change', () => updateMatrixDimensions(matrixBInputs, rowsBSelector, colsBSelector, 'B'));
        colsBSelector.addEventListener('change', () => updateMatrixDimensions(matrixBInputs, rowsBSelector, colsBSelector, 'B'));
        
        rowsMultASelector.addEventListener('change', () => {
            updateMatrixDimensions(matrixMultAInputs, rowsMultASelector, colsMultASelector, 'A');
            updateMultiplicationDimensionHint();
        });
        colsMultASelector.addEventListener('change', () => {
            updateMatrixDimensions(matrixMultAInputs, rowsMultASelector, colsMultASelector, 'A');
            updateMultiplicationDimensionHint();
        });
        rowsMultBSelector.addEventListener('change', () => {
            updateMatrixDimensions(matrixMultBInputs, rowsMultBSelector, colsMultBSelector, 'B');
            updateMultiplicationDimensionHint();
        });
        colsMultBSelector.addEventListener('change', () => {
            updateMatrixDimensions(matrixMultBInputs, rowsMultBSelector, colsMultBSelector, 'B');
            updateMultiplicationDimensionHint();
        });
        
        // Set up event listener for determinant dimension selector (square matrix)
        dimensionDetSelector.addEventListener('change', () => {
            const dimension = parseInt(dimensionDetSelector.value);
            generateMatrixInputs(matrixDetInputs, dimension, dimension, 'Det'); // Changed prefix to 'Det'
        });

        // Set up event listener for inverse dimension selector (square matrix)
        dimensionInvSelector.addEventListener('change', () => {
            const dimension = parseInt(dimensionInvSelector.value);
            generateMatrixInputs(matrixInvInputs, dimension, dimension, 'Inv');
        });

        // Set up event listener for Gaussian A dimension selector
        dimensionGaussASelector.addEventListener('change', () => {
            const dimension = parseInt(dimensionGaussASelector.value);
            generateMatrixInputs(matrixGaussAInputs, dimension, dimension, 'Agauss');
            generateVectorInputs(vectorGaussBInputs, dimension, 'bgauss'); // Also update vector b
            updateGaussianDimensionDisplay();
        });
        
        // Set up event listener for Gauss-Jordan A dimension selector
        dimensionGaussJordanASelector.addEventListener('change', () => {
            const dimension = parseInt(dimensionGaussJordanASelector.value);
            generateMatrixInputs(matrixGaussJordanAInputs, dimension, dimension, 'Agj');
            generateVectorInputs(vectorGaussJordanBInputs, dimension, 'bgj'); // Also update vector b
            updateGaussJordanDimensionDisplay();
        });

        // Set up event listener for LU A dimension selector
        dimensionLuASelector.addEventListener('change', () => {
            const dimension = parseInt(dimensionLuASelector.value);
            generateMatrixInputs(matrixLuAInputs, dimension, dimension, 'A_lu');
        });
        
        // Set up event listeners for calculation buttons
        addButton.addEventListener('click', () => performOperation('add'));
        subtractButton.addEventListener('click', () => performOperation('subtract'));
        multiplyButton.addEventListener('click', () => performMultiplication());
        determinantButton.addEventListener('click', () => calculateDeterminant());
        inverseButton.addEventListener('click', () => calculateInverse()); // Added for Inverse
        solveGaussianButton.addEventListener('click', () => solveSystemGaussian()); // Added for Gaussian
        solveGaussJordanButton.addEventListener('click', () => solveSystemGaussJordan()); // Added for Gauss-Jordan
        if (luFactorizationButton) { // Check if button exists
            luFactorizationButton.addEventListener('click', () => {
                calculateLUFactorization();
            });
        } else {
            console.error('LU Factorization button not found!'); // DEBUG
        }
        
        // Initial dimension hint update
        updateMultiplicationDimensionHint();
        
        // Check if determinant tab is active at page load and ensure matrix is generated
        const activeTab = document.querySelector('.tab-button.active');
        if (activeTab && activeTab.getAttribute('data-tab') === 'determinant') {
            const detDim = parseInt(dimensionDetSelector.value);
            // Check if matrixDetInputs exists and has no children before generating
            if (matrixDetInputs && matrixDetInputs.childElementCount === 0) {
                 generateMatrixInputs(matrixDetInputs, detDim, detDim, 'Det'); // Changed prefix to 'Det'
            }
        }
        // Check if inverse tab is active at page load and ensure matrix is generated
        if (activeTab && activeTab.getAttribute('data-tab') === 'inverse') {
            const invDim = parseInt(dimensionInvSelector.value);
            if (matrixInvInputs && matrixInvInputs.childElementCount === 0) {
                generateMatrixInputs(matrixInvInputs, invDim, invDim, 'Inv');
            }
        }
        // Check if Gaussian elimination tab is active at page load
        if (activeTab && activeTab.getAttribute('data-tab') === 'gaussian-elimination') {
            const gaussDim = parseInt(dimensionGaussASelector.value);
            if (matrixGaussAInputs && matrixGaussAInputs.childElementCount === 0) {
                generateMatrixInputs(matrixGaussAInputs, gaussDim, gaussDim, 'Agauss');
            }
            if (vectorGaussBInputs && vectorGaussBInputs.childElementCount === 0) {
                generateVectorInputs(vectorGaussBInputs, gaussDim, 'bgauss');
            }
            updateGaussianDimensionDisplay();
        }
        
        // Check if Gauss-Jordan tab is active at page load
        if (activeTab && activeTab.getAttribute('data-tab') === 'gauss-jordan') {
            const gaussJordanDim = parseInt(dimensionGaussJordanASelector.value);
            if (matrixGaussJordanAInputs && matrixGaussJordanAInputs.childElementCount === 0) {
                generateMatrixInputs(matrixGaussJordanAInputs, gaussJordanDim, gaussJordanDim, 'Agj');
            }
            if (vectorGaussJordanBInputs && vectorGaussJordanBInputs.childElementCount === 0) {
                generateVectorInputs(vectorGaussJordanBInputs, gaussJordanDim, 'bgj');
            }
            updateGaussJordanDimensionDisplay();
        }
        // Check if LU Factorization tab is active at page load
        if (activeTab && activeTab.getAttribute('data-tab') === 'lu-factorization') {
            const luDim = parseInt(dimensionLuASelector.value);
            if (matrixLuAInputs && matrixLuAInputs.childElementCount === 0) {
                generateMatrixInputs(matrixLuAInputs, luDim, luDim, 'A_lu');
            }
        }
    }
    
    function updateMultiplicationDimensionHint() {
        const colsA = parseInt(colsMultASelector.value);
        const rowsB = parseInt(rowsMultBSelector.value);
        const hintSpan = multiplicationDimensionHint.querySelector('span');
        
        // Reset classes
        multiplicationDimensionHint.classList.remove('warning', 'valid');
        
        if (colsA === rowsB) {
            multiplicationDimensionHint.classList.add('valid');
            hintSpan.innerHTML = `Para multiplicar A×B: las columnas de A (${colsA}) son iguales a las filas de B (${rowsB}) <i class="fas fa-check"></i>`;
            multiplyButton.disabled = false;
        } else {
            multiplicationDimensionHint.classList.add('warning');
            hintSpan.innerHTML = `Para multiplicar A×B: las columnas de A (${colsA}) deben ser iguales a las filas de B (${rowsB}) <i class="fas fa-exclamation-triangle"></i>`;
            multiplyButton.disabled = true;
        }
        
        // Add animation effect
        multiplicationDimensionHint.classList.remove('step-highlight');
        void multiplicationDimensionHint.offsetWidth; // Force reflow
        multiplicationDimensionHint.classList.add('step-highlight');
    }
    
    function updateMatrixDimensions(container, rowsSelector, colsSelector, matrixName) {
        const rows = parseInt(rowsSelector.value);
        const cols = parseInt(colsSelector.value);
        generateMatrixInputs(container, rows, cols, matrixName);
    }
    
    function toggleTheme() {
        document.body.classList.toggle('dark-theme');
        const currentTheme = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
        localStorage.setItem('theme', currentTheme);
    }
    
    async function copyResultToClipboard(matrixDiv, copyBtn) {
        const table = matrixDiv.querySelector('table');
        if (!table) return;
        
        try {
            // Create a text representation of the matrix
            let matrixText = '';
            const rows = table.querySelectorAll('tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                const rowValues = Array.from(cells).map(cell => cell.textContent);
                matrixText += rowValues.join('\t') + '\n';
            });
            
            await navigator.clipboard.writeText(matrixText);
            
            // Visual feedback
            copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    }

    function generateMatrixInputs(container, rows, cols, matrixName) {
        container.innerHTML = '';
        container.style.gridTemplateColumns = `repeat(${cols}, auto)`;
        
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                const input = document.createElement('input');
                input.type = 'text';
                input.classList.add('matrix-cell');
                
                let displayPrefix = matrixName;
                if (matrixName === 'Agauss' || matrixName === 'A') {
                    displayPrefix = 'A';
                } else if (matrixName === 'B') {
                    displayPrefix = 'B';
                } else if (matrixName === 'Det' || matrixName === 'Inv') {
                    displayPrefix = 'M';
                } else if (matrixName === 'A_lu') {
                    displayPrefix = 'A'; // For LU, matrix A is just 'A'
                }

                // Use displayPrefix and subscripts if it's one of the recognized types
                if (['A', 'B', 'M'].includes(displayPrefix)) {
                    input.placeholder = `${displayPrefix}${toSubscript(i + 1)}${toSubscript(j + 1)}`;
                } else {
                    // Fallback for any other matrixName or if modification is not desired for some
                    input.placeholder = `${matrixName}${i + 1}${j + 1}`;
                }
                
                // Add key navigation between cells
                input.dataset.row = i;
                input.dataset.col = j;
                input.addEventListener('keydown', handleMatrixInputKeydown);
                
                container.appendChild(input);
            }
        }
        
        // Auto-focus first cell for convenience
        if (container.querySelector('.matrix-cell')) {
            container.querySelector('.matrix-cell').focus();
        }
    }
    
    function handleMatrixInputKeydown(e) {
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        const container = e.target.parentElement;
        
        let rows, cols;
        
        // Handle different containers for different operations
        if (container.id === 'matrixAInputs') {
            rows = parseInt(rowsASelector.value);
            cols = parseInt(colsASelector.value);
        } else if (container.id === 'matrixBInputs') {
            rows = parseInt(rowsBSelector.value);
            cols = parseInt(colsBSelector.value);
        } else if (container.id === 'matrixMultAInputs') {
            rows = parseInt(rowsMultASelector.value);
            cols = parseInt(colsMultASelector.value);
        } else if (container.id === 'matrixMultBInputs') {
            rows = parseInt(rowsMultBSelector.value);
            cols = parseInt(colsMultBSelector.value);
        } else if (container.id === 'matrixDetInputs') {
            rows = cols = parseInt(dimensionDetSelector.value);
        } else if (container.id === 'matrixInvInputs') { // Added for Inverse
            rows = cols = parseInt(dimensionInvSelector.value);
        } else if (container.id === 'matrixGaussAInputs') { // Gaussian A
            rows = cols = parseInt(dimensionGaussASelector.value);
        } else if (container.id === 'vectorGaussBInputs') { // Gaussian B
            rows = parseInt(dimensionGaussASelector.value); // Vector b has N rows, 1 col
            cols = 1;
        } else if (container.id === 'matrixLuAInputs') { // LU Factorization A
            rows = cols = parseInt(dimensionLuASelector.value);
        } else {
            // Default fallback
            rows = cols = 2;
        }
        
        // Arrow key navigation
        if (e.key === 'ArrowRight' && col < cols - 1) {
            container.querySelector(`[data-row="${row}"][data-col="${col + 1}"]`)?.focus();
        } else if (e.key === 'ArrowLeft' && col > 0) {
            container.querySelector(`[data-row="${row}"][data-col="${col - 1}"]`)?.focus();
        } else if (e.key === 'ArrowDown' && row < rows - 1) {
            container.querySelector(`[data-row="${row + 1}"][data-col="${col}"]`)?.focus();
        } else if (e.key === 'ArrowUp' && row > 0) {
            container.querySelector(`[data-row="${row - 1}"][data-col="${col}"]`)?.focus();
        }
    }

    function getMatrixData(inputContainer, rows, cols) {
        const matrix = [];
        const inputs = inputContainer.getElementsByTagName('input');
        let inputIndex = 0;
        
        for (let i = 0; i < rows; i++) {
            const row = [];
            for (let j = 0; j < cols; j++) {
                // Trim whitespace and handle empty values
                let value = inputs[inputIndex]?.value?.trim() || '';
                row.push(value);
                inputIndex++;
            }
            matrix.push(row);
        }
        return matrix;
    }

    async function performMultiplication() {
        clearPreviousResults(stepsMultDisplay, resultMultMatrixDiv, errorMultDisplay);
        showLoader(multiplicationLoader, true);
        
        const rA = parseInt(rowsMultASelector.value);
        const cA = parseInt(colsMultASelector.value);
        const rB = parseInt(rowsMultBSelector.value);
        const cB = parseInt(colsMultBSelector.value);

        const matrixA = getMatrixData(matrixMultAInputs, rA, cA);
        const matrixB = getMatrixData(matrixMultBInputs, rB, cB);

        const payload = {
            matrix_a: matrixA,
            matrix_b: matrixB
        };

        try {
            const response = await fetch(`/operations/multiply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ocurrió un error al multiplicar las matrices');
            }

            const data = await response.json();

            // Add a small delay to show loader (for UX)
            await new Promise(resolve => setTimeout(resolve, 600));

            if (data.success) {
                displayResultMatrix(resultMultMatrixDiv, data.result, 'multiplication');
                formatAndDisplaySteps(stepsMultDisplay, data.steps, true);
            } else {
                displayError(errorMultDisplay, data.error || 'Ocurrió un error desconocido.');
            }
        } catch (error) {
            console.error('Error calling API:', error);
            displayError(errorMultDisplay, error.message || 'No se pudo conectar con el API o hubo un error en la respuesta.');
        } finally {
            showLoader(multiplicationLoader, false);
        }
    }

    async function performOperation(operation) {
        clearPreviousResults(stepsDisplay, resultMatrixDiv, errorDisplay);
        showLoader(loader, true);
        
        const rA = parseInt(rowsASelector.value);
        const cA = parseInt(colsASelector.value);
        const rB = parseInt(rowsBSelector.value);
        const cB = parseInt(colsBSelector.value);

        const matrixA = getMatrixData(matrixAInputs, rA, cA);
        const matrixB = getMatrixData(matrixBInputs, rB, cB);

        const payload = {
            matrix_a: matrixA,
            matrix_b: matrixB
        };

        try {
            const response = await fetch(`/operations/${operation}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ocurrió un error en la operación');
            }

            const data = await response.json();

            // Simulate a small delay to show loader (remove in production)
            await new Promise(resolve => setTimeout(resolve, 500));

            if (data.success) {
                displayResultMatrix(resultMatrixDiv, data.result);
                formatAndDisplaySteps(stepsDisplay, data.steps);
            } else {
                displayError(errorDisplay, data.error || 'Ocurrió un error desconocido.');
            }
        } catch (error) {
            console.error('Error calling API:', error);
            displayError(errorDisplay, error.message || 'No se pudo conectar con el API o hubo un error en la respuesta.');
        } finally {
            showLoader(loader, false);
        }
    }

    function showLoader(loaderElement, show) {
        loaderElement.style.display = show ? 'block' : 'none';
    }

    function displayResultMatrix(containerDiv, matrix, operation = null) {
        containerDiv.innerHTML = '';
        if (!matrix || matrix.length === 0) {
            containerDiv.textContent = 'No hay resultado para mostrar.';
            return;
        }
        
        const table = document.createElement('table');
        
        // Apply animation
        table.style.opacity = '0';
        table.style.transform = 'translateY(-10px)';
        
        matrix.forEach(rowData => {
            const tr = document.createElement('tr');
            rowData.forEach(cellData => {
                const td = document.createElement('td');
                td.textContent = cellData;
                // Add special animation for multiplication
                if (operation === 'multiplication') {
                    td.classList.add('calculation-highlight');
                    // Stagger the animation for each cell
                    setTimeout(() => {
                        td.classList.remove('calculation-highlight');
                    }, Math.random() * 1000 + 500);
                }
                tr.appendChild(td);
            });
            table.appendChild(tr);
        });
        
        containerDiv.appendChild(table);
        
        // Trigger animation
        setTimeout(() => {
            table.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            table.style.opacity = '1';
            table.style.transform = 'translateY(0)';
        }, 10);
    }

    function formatAndDisplaySteps(stepsContainer, steps, isMultiplication = false) {
        if (!steps || steps.length === 0) {
            stepsContainer.textContent = 'No hay pasos para mostrar.';
            return;
        }
        
        stepsContainer.innerHTML = '';
        let delay = 0;
        const stepIncrement = isMultiplication ? 200 : 100; // Longer delays for multiplication steps
        
        steps.forEach((step, index) => {
            const stepElement = document.createElement('div');
            stepElement.classList.add('step');
            
            // Special formatting for matrix representation in steps
            if (step.includes('|')) {
                stepElement.classList.add('matrix-step');
                
                // Replace spaces with non-breaking spaces for matrix formatting
                step = step.replace(/ {2,}/g, match => '&nbsp;'.repeat(match.length));
            }
            
            // Highlight calculation steps in multiplication
            if (isMultiplication && step.includes('Elemento C[')) {
                stepElement.classList.add('calculation-step');
            }
            
            stepElement.innerHTML = step;
            stepElement.style.opacity = '0';
            stepsContainer.appendChild(stepElement);
            
            // Staggered animation for steps
            setTimeout(() => {
                stepElement.style.transition = 'opacity 0.5s ease, transform 0.3s ease';
                stepElement.style.opacity = '1';
                
                // Add highlight animation for calculation steps
                if (isMultiplication && step.includes('Elemento C[')) {
                    stepElement.classList.add('step-highlight');
                    setTimeout(() => {
                        stepElement.classList.remove('step-highlight');
                    }, 800);
                }
            }, delay);
            
            delay += stepIncrement;
        });
    }

    function displayError(errorContainer, message) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
        
        // Add shake animation
        errorContainer.classList.add('shake');
        setTimeout(() => {
            errorContainer.classList.remove('shake');
        }, 500);
    }

    function clearPreviousResults(stepsContainer, resultContainer, errorContainer, additionalResultContainer = null) {
        if (stepsContainer) stepsContainer.innerHTML = '';
        if (resultContainer) resultContainer.innerHTML = '';
        if (additionalResultContainer) additionalResultContainer.innerHTML = ''; // For LU's second matrix
        if (errorContainer) {
            errorContainer.style.display = 'none';
            errorContainer.textContent = '';
        }
    }
    
    // New function for determinant calculation
    async function calculateDeterminant() {
        clearPreviousResults(stepsDetDisplay, resultDeterminantDiv, errorDetDisplay); //Ensure resultDeterminantDiv is cleared if it holds the scalar
        // If resultDeterminantDiv is for a matrix display, then the scalar display (determinantValueDiv) needs to be handled separately
        // For now, assuming resultDeterminantDiv will display the scalar value directly or it's handled by displayDeterminantResult
        showLoader(determinantLoader, true);
        
        const dimension = parseInt(dimensionDetSelector.value);
        const matrix = getMatrixData(matrixDetInputs, dimension, dimension);

        const payload = {
            matrix: matrix
        };

        try {
            const response = await fetch(`/operations/determinant`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ocurrió un error al calcular el determinante');
            }

            const data = await response.json();

            // Add a small delay to show loader (for UX)
            await new Promise(resolve => setTimeout(resolve, 800));

            if (data.success) {
                // Display determinant value with animation
                displayDeterminantResult(resultDeterminantDiv, data.result); // Pass resultDeterminantDiv
                formatAndDisplaySteps(stepsDetDisplay, data.steps, false); // isMultiplication is false for determinant
            } else {
                displayError(errorDetDisplay, data.error || 'Ocurrió un error desconocido.');
            }
        } catch (error) {
            console.error('Error calling API:', error);
            displayError(errorDetDisplay, error.message || 'No se pudo conectar con el API o hubo un error en la respuesta.');
        } finally {
            showLoader(determinantLoader, false);
        }
    }
    
    function displayDeterminantResult(resultDiv, result) { // Added resultDiv parameter
        resultDiv.innerHTML = ''; // Clear previous content
        
        // Apply animation - start with opacity 0
        resultDiv.style.opacity = '0';
        resultDiv.style.transform = 'scale(0.8)';
        
        // Add text content
        resultDiv.textContent = result;
        
        // Add class based on value for styling (optional, if CSS rules exist e.g. .zero, .nonzero)
        resultDiv.classList.remove('zero', 'nonzero'); // Clear previous classes
        if (result === '0' || parseFloat(result) === 0) {
            resultDiv.classList.add('zero');
        } else {
            resultDiv.classList.add('nonzero');
        }
        
        // Trigger animation
        setTimeout(() => {
            resultDiv.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            resultDiv.style.opacity = '1';
            resultDiv.style.transform = 'scale(1)';
        }, 10);
    }
    
    // New function for inverse calculation
    async function calculateInverse() {
        clearPreviousResults(stepsInvDisplay, resultInverseMatrixDiv, errorInvDisplay);
        showLoader(inverseLoader, true);
        
        const dimension = parseInt(dimensionInvSelector.value);
        const matrix = getMatrixData(matrixInvInputs, dimension, dimension);

        const payload = {
            matrix: matrix
        };

        try {
            const response = await fetch(`/operations/inverse`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ocurrió un error al calcular la inversa');
            }

            const data = await response.json();

            await new Promise(resolve => setTimeout(resolve, 800)); // UX delay

            if (data.success) {
                displayResultMatrix(resultInverseMatrixDiv, data.result, 'inverse');
                formatAndDisplaySteps(stepsInvDisplay, data.steps, false);
            } else {
                displayError(errorInvDisplay, data.error || 'Ocurrió un error desconocido.');
            }
        } catch (error) {
            console.error('Error calling API for inverse:', error);
            displayError(errorInvDisplay, error.message || 'No se pudo conectar con el API o hubo un error en la respuesta.');
        } finally {
            showLoader(inverseLoader, false);
        }
    }

    async function copyScalarResultToClipboard(text, copyBtn) {
        if (!text) return;
        
        try {
            await navigator.clipboard.writeText(text);
            
            // Visual feedback
            copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    }

    function generateVectorInputs(container, rows, vectorNamePrefix) {
        container.innerHTML = '';
        container.style.gridTemplateColumns = 'auto'; // Single column for vector

        for (let i = 0; i < rows; i++) {
            const input = document.createElement('input');
            input.type = 'text';
            input.classList.add('matrix-cell'); // Reuse matrix-cell styling
            
            if (vectorNamePrefix === 'bgauss') {
                input.placeholder = `b${toSubscript(i + 1)}`;
            } else {
                input.placeholder = `${vectorNamePrefix}${i + 1}`;
            }
            
            input.dataset.row = i;
            input.dataset.col = 0; // Always 0 for a vector
            input.addEventListener('keydown', handleMatrixInputKeydown); // Can reuse for up/down nav

            container.appendChild(input);
        }
        if (container.querySelector('.matrix-cell')) {
            container.querySelector('.matrix-cell').focus();
        }
    }

    function getVectorData(inputContainer, rows) {
        const vector = [];
        const inputs = inputContainer.getElementsByTagName('input');
        for (let i = 0; i < rows; i++) {
            let value = inputs[i]?.value?.trim() || '';
            vector.push(value);
        }
        return vector;
    }

    function updateGaussianDimensionDisplay() {
        const dimension = dimensionGaussASelector.value;
        dimensionGaussBDisplay.textContent = `${dimension}×1`;
    }
    
    function updateGaussJordanDimensionDisplay() {
        const dimension = dimensionGaussJordanASelector.value;
        dimensionGaussJordanBDisplay.textContent = `${dimension}×1`;
    }

    async function solveSystemGaussian() {
        clearPreviousResults(stepsGaussianDisplay, resultGaussianSolutionDiv, errorGaussianDisplay);
        showLoader(gaussianLoader, true);

        const n = parseInt(dimensionGaussASelector.value);
        const matrixA = getMatrixData(matrixGaussAInputs, n, n);
        const vectorB = getVectorData(vectorGaussBInputs, n);

        const payload = {
            matrix_a: matrixA,
            vector_b: vectorB
        };

        try {
            const response = await fetch(`/operations/solve_system_gaussian`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            // Handle HTTP errors before trying to parse JSON
            if (!response.ok) {
                let errorMsg = `Error del servidor: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.detail || errorMsg; 
                } catch (e) {
                    // If JSON parsing fails, use the initial status message
                    console.warn('Could not parse error response as JSON.');
                }
                throw new Error(errorMsg);
            }

            const data = await response.json();
            await new Promise(resolve => setTimeout(resolve, 600)); // UX Delay

            if (data.success) {
                if (data.result.solution_vector) {
                    // Display solution_vector as a column matrix
                    const solutionMatrix = data.result.solution_vector.map(val => [val]);
                    displayResultMatrix(resultGaussianSolutionDiv, solutionMatrix, 'gaussian');
                } else {
                    // Display message (no solution, infinite solutions)
                    resultGaussianSolutionDiv.innerHTML = `<div class="determinant-result">${data.result.message}</div>`;
                }
                formatAndDisplaySteps(stepsGaussianDisplay, data.steps, false);
            } else {
                displayError(errorGaussianDisplay, data.error || 'Ocurrió un error desconocido.');
            }
        } catch (error) {
            console.error('Error calling Gaussian elimination API:', error);
            displayError(errorGaussianDisplay, error.message || 'No se pudo conectar con el API o hubo un error en la respuesta.');
        } finally {
            showLoader(gaussianLoader, false);
        }
    }

    async function solveSystemGaussJordan() {
        clearPreviousResults(stepsGaussJordanDisplay, resultGaussJordanSolutionDiv, errorGaussJordanDisplay, resultGaussJordanRrefDiv);
        showLoader(gaussJordanLoader, true);

        const n = parseInt(dimensionGaussJordanASelector.value);
        const matrixA = getMatrixData(matrixGaussJordanAInputs, n, n);
        const vectorB = getVectorData(vectorGaussJordanBInputs, n);

        const payload = {
            matrix_a: matrixA,
            vector_b: vectorB
        };

        try {
            const response = await fetch(`/operations/gauss_jordan_elimination`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            // Handle HTTP errors before trying to parse JSON
            if (!response.ok) {
                let errorMsg = `Error del servidor: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.detail || errorMsg; 
                } catch (e) {
                    // If JSON parsing fails, use the initial status message
                    console.warn('Could not parse error response as JSON.');
                }
                throw new Error(errorMsg);
            }

            const data = await response.json();
            await new Promise(resolve => setTimeout(resolve, 600)); // UX Delay

            if (data.success) {
                // Display RREF matrix
                if (data.result.rref_matrix) {
                    displayResultMatrix(resultGaussJordanRrefDiv, data.result.rref_matrix, 'gauss-jordan');
                    
                    // Apply highlight to pivots in RREF matrix
                    setTimeout(() => {
                        highlightPivotsInRref(resultGaussJordanRrefDiv);
                    }, 800);
                }

                // Display solution if available
                if (data.result.solution_vector) {
                    // Display solution_vector as a column matrix
                    const solutionMatrix = data.result.solution_vector.map(val => [val]);
                    displayResultMatrix(resultGaussJordanSolutionDiv, solutionMatrix, 'gauss-jordan');
                } else {
                    // Display message (no solution, infinite solutions)
                    resultGaussJordanSolutionDiv.innerHTML = `<div class="determinant-result">${data.result.message}</div>`;
                }
                
                formatAndDisplaySteps(stepsGaussJordanDisplay, data.steps, false);
            } else {
                // Even when success is false, we may still have RREF matrix to display
                if (data.result && data.result.rref_matrix) {
                    displayResultMatrix(resultGaussJordanRrefDiv, data.result.rref_matrix, 'gauss-jordan');
                    setTimeout(() => {
                        highlightPivotsInRref(resultGaussJordanRrefDiv);
                    }, 800);
                }
                
                // Display message for no solution
                resultGaussJordanSolutionDiv.innerHTML = `<div class="determinant-result">${data.result ? data.result.message : 'Sistema sin solución'}</div>`;
                
                // Display steps and error message
                formatAndDisplaySteps(stepsGaussJordanDisplay, data.steps, false);
                displayError(errorGaussJordanDisplay, data.error || 'Ocurrió un error desconocido.');
            }
        } catch (error) {
            console.error('Error calling Gauss-Jordan elimination API:', error);
            displayError(errorGaussJordanDisplay, error.message || 'No se pudo conectar con el API o hubo un error en la respuesta.');
        } finally {
            showLoader(gaussJordanLoader, false);
        }
    }
    
    // Function to highlight pivots in RREF matrix
    function highlightPivotsInRref(matrixContainer) {
        const table = matrixContainer.querySelector('table');
        if (!table) return;
        
        const rows = table.querySelectorAll('tr');
        const numRows = rows.length;
        const numCols = rows[0].querySelectorAll('td').length - 1; // Excluding the last column (b vector)
        
        let pivotCol = 0;
        
        // For each row, find the pivot column (first non-zero element)
        for (let i = 0; i < numRows && pivotCol < numCols; i++) {
            const cells = rows[i].querySelectorAll('td');
            
            // Find pivot column (first non-zero element in this row)
            while (pivotCol < numCols) {
                const cellValue = cells[pivotCol].textContent;
                if (cellValue === '1' || cellValue === '1.0') {
                    // This is a pivot element
                    cells[pivotCol].classList.add('pivot-highlight');
                    pivotCol++;
                    break;
                }
                pivotCol++;
            }
        }
    }

    async function copyGaussianSolutionToClipboard(solutionDiv, copyBtn) {
        let textToCopy = '';
        const table = solutionDiv.querySelector('table');

        if (table) { // It's a matrix (solution vector)
            const rows = table.querySelectorAll('tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                const rowValues = Array.from(cells).map(cell => cell.textContent);
                textToCopy += rowValues.join('\t') + '\n'; // Assuming single column for solution vector
            });
        } else {
            // It's a message (no solution / infinite solutions)
            const messageDiv = solutionDiv.querySelector('.determinant-result'); // Using similar class for message display
            if (messageDiv) {
                textToCopy = messageDiv.textContent;
            }
        }

        if (!textToCopy) return;

        try {
            await navigator.clipboard.writeText(textToCopy.trim());
            copyBtn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy Gaussian solution: ', err);
        }
    }

    // LU Factorization
    async function calculateLUFactorization() {
        // Check if critical display elements are present
        if (!luLoader || !stepsLuDisplay || !resultLuLMatrixDiv || !resultLuUMatrixDiv || !errorLuDisplay) {
            console.error('One or more LU display elements are missing! Check IDs: luLoader, stepsLuDisplay, resultLuLMatrixDiv, resultLuUMatrixDiv, errorLuDisplay');
            alert('Error: UI elements for LU Factorization are missing. Please check the console.');
            return; // Stop further execution
        }

        clearPreviousResults(stepsLuDisplay, resultLuLMatrixDiv, errorLuDisplay, resultLuUMatrixDiv);
        showLoader(luLoader, true);

        const dimension = parseInt(dimensionLuASelector.value);
        const matrixA = getMatrixData(matrixLuAInputs, dimension, dimension);

        const payload = {
            matrix: matrixA
        };

        try {
            const response = await fetch(`/operations/lu_factorization`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Ocurrió un error al calcular la factorización LU');
            }

            const data = await response.json();
            await new Promise(resolve => setTimeout(resolve, 600)); // UX Delay

            if (data.success) {
                if (data.result && data.result.matrix_l && data.result.matrix_u) {
                    displayResultMatrix(resultLuLMatrixDiv, data.result.matrix_l, 'lu_l');
                    displayResultMatrix(resultLuUMatrixDiv, data.result.matrix_u, 'lu_u');
                } else {
                    // Should not happen if success is true and backend guarantees result structure
                    displayError(errorLuDisplay, 'Respuesta exitosa pero faltan matrices L/U.'); 
                }
                formatAndDisplaySteps(stepsLuDisplay, data.steps, false);
            } else {
                // Clear matrix displays if LU fails (e.g. pivot error)
                resultLuLMatrixDiv.innerHTML = '';
                resultLuUMatrixDiv.innerHTML = '';
                displayError(errorLuDisplay, data.error || 'Ocurrió un error desconocido durante la factorización LU.');
            }
        } catch (error) {
            console.error('Error calling LU Factorization API:', error);
            displayError(errorLuDisplay, error.message || 'No se pudo conectar con el API o hubo un error en la respuesta.');
        } finally {
            showLoader(luLoader, false);
        }
    }
}); 

// Extra safety check to ensure determinant inputs are generated
window.addEventListener('load', () => {
    const matrixDetInputs = document.getElementById('matrixDetInputs');
    const dimensionDetSelector = document.getElementById('dimensionDet');
    
    if (matrixDetInputs && dimensionDetSelector && matrixDetInputs.childElementCount === 0) {
        const detDimension = parseInt(dimensionDetSelector.value) || 2;
        
        // Clear and regenerate inputs
        matrixDetInputs.innerHTML = '';
        matrixDetInputs.style.gridTemplateColumns = `repeat(${detDimension}, auto)`;
        
        for (let i = 0; i < detDimension; i++) {
            for (let j = 0; j < detDimension; j++) {
                const input = document.createElement('input');
                input.type = 'text';
                input.classList.add('matrix-cell');
                input.placeholder = `Det${i + 1}${j + 1}`; // Changed prefix to 'Det'
                
                // Add key navigation data attributes
                input.dataset.row = i;
                input.dataset.col = j;
                
                matrixDetInputs.appendChild(input);
            }
        }
    }

    // Safety check for inverse inputs on window load
    const matrixInvInputsElement = document.getElementById('matrixInvInputs');
    const dimensionInvSelectorElement = document.getElementById('dimensionInv');

    if (matrixInvInputsElement && dimensionInvSelectorElement && matrixInvInputsElement.childElementCount === 0) {
        const invDimension = parseInt(dimensionInvSelectorElement.value) || 2;
        generateMatrixInputs(matrixInvInputsElement, invDimension, invDimension, 'Inv');
    }

    // Safety check for LU inputs on window load
    const matrixLuAInputsElement = document.getElementById('matrixLuAInputs');
    const dimensionLuASelectorElement = document.getElementById('dimensionLuA');

    if (matrixLuAInputsElement && dimensionLuASelectorElement && matrixLuAInputsElement.childElementCount === 0) {
        const luDimension = parseInt(dimensionLuASelectorElement.value) || 2;
        generateMatrixInputs(matrixLuAInputsElement, luDimension, luDimension, 'A_lu');
    }
}); 

// Tab overflow menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabOverflowMenu = document.querySelector('.tab-overflow-menu');
    const tabs = document.querySelector('.tabs');
    
    if (tabOverflowMenu) {
        tabOverflowMenu.addEventListener('click', function() {
            // Create a dropdown menu with tab options
            let dropdownMenu = document.querySelector('.tab-dropdown');
            
            if (dropdownMenu) {
                // Toggle the menu if it already exists
                dropdownMenu.classList.toggle('show-dropdown');
                return;
            }
            
            // Create the dropdown menu
            dropdownMenu = document.createElement('div');
            dropdownMenu.className = 'tab-dropdown';
            
            // Add all tab options
            const tabButtons = document.querySelectorAll('.tab-button');
            tabButtons.forEach(button => {
                const tabOption = document.createElement('div');
                tabOption.className = 'tab-option';
                tabOption.innerHTML = button.innerHTML;
                
                if (button.classList.contains('active')) {
                    tabOption.classList.add('active');
                }
                
                tabOption.addEventListener('click', function() {
                    const tabId = button.getAttribute('data-tab');
                    activateTab(tabId);
                    dropdownMenu.classList.remove('show-dropdown');
                });
                
                dropdownMenu.appendChild(tabOption);
            });
            
            // Add the dropdown to the page
            document.querySelector('.tabs-container').appendChild(dropdownMenu);
            dropdownMenu.classList.add('show-dropdown');
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function closeDropdown(e) {
                if (!e.target.closest('.tab-dropdown') && !e.target.closest('.tab-overflow-menu')) {
                    const dropdown = document.querySelector('.tab-dropdown');
                    if (dropdown && dropdown.classList.contains('show-dropdown')) {
                        dropdown.classList.remove('show-dropdown');
                    }
                }
            });
        });
    }
    
    // Function to activate a tab
    function activateTab(tabId) {
        // Deactivate all tabs
        document.querySelectorAll('.tab-button').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        // Activate the selected tab
        const selectedTab = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
        const selectedContent = document.getElementById(tabId);
        
        if (selectedTab) selectedTab.classList.add('active');
        if (selectedContent) selectedContent.classList.add('active');
    }
}); 