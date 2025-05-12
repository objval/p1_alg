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
        
        // Always use dark theme
        document.body.classList.add('dark-theme');
        
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

        // Initialize presets
        initializePresets();
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
    
    // Theme toggle function removed
    
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

    // Matrix Presets functionality
    function initializePresets() {
        // Basic Operations presets
        const presetButtons = document.querySelectorAll('.preset-btn');
        if (presetButtons.length > 0) {
            presetButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const presetType = button.getAttribute('data-preset');
                    applyPreset(presetType);
                    
                    // Add animation effect to the button
                    button.classList.add('active');
                    setTimeout(() => {
                        button.classList.remove('active');
                    }, 500);
                });
            });
        }
        
        // Multiplication presets
        const multPresetButtons = document.querySelectorAll('.preset-btn-mult');
        if (multPresetButtons.length > 0) {
            multPresetButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const presetType = button.getAttribute('data-preset');
                    applyMultiplicationPreset(presetType);
                    
                    button.classList.add('active');
                    setTimeout(() => {
                        button.classList.remove('active');
                    }, 500);
                    
                    // Update dimension hint after applying preset
                    setTimeout(() => {
                        updateMultiplicationDimensionHint();
                    }, 100);
                });
            });
        }
        
        // Determinant presets
        const detPresetButtons = document.querySelectorAll('.preset-btn-det');
        if (detPresetButtons.length > 0) {
            detPresetButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const presetType = button.getAttribute('data-preset');
                    applyDeterminantPreset(presetType);
                    
                    button.classList.add('active');
                    setTimeout(() => {
                        button.classList.remove('active');
                    }, 500);
                });
            });
        }
        
        // Inverse presets
        const invPresetButtons = document.querySelectorAll('.preset-btn-inv');
        if (invPresetButtons.length > 0) {
            invPresetButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const presetType = button.getAttribute('data-preset');
                    applyInversePreset(presetType);
                    
                    button.classList.add('active');
                    setTimeout(() => {
                        button.classList.remove('active');
                    }, 500);
                });
            });
        }

        // Gaussian elimination presets
        const gaussPresetButtons = document.querySelectorAll('.preset-btn-gauss');
        if (gaussPresetButtons.length > 0) {
            gaussPresetButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const presetType = button.getAttribute('data-preset');
                    applyGaussianPreset(presetType);
                    
                    button.classList.add('active');
                    setTimeout(() => {
                        button.classList.remove('active');
                    }, 500);
                });
            });
        }

        // Gauss-Jordan presets
        const gjPresetButtons = document.querySelectorAll('.preset-btn-gj');
        if (gjPresetButtons.length > 0) {
            gjPresetButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const presetType = button.getAttribute('data-preset');
                    applyGaussJordanPreset(presetType);
                    
                    button.classList.add('active');
                    setTimeout(() => {
                        button.classList.remove('active');
                    }, 500);
                });
            });
        }

        // LU factorization presets
        const luPresetButtons = document.querySelectorAll('.preset-btn-lu');
        if (luPresetButtons.length > 0) {
            luPresetButtons.forEach(button => {
                button.addEventListener('click', () => {
                    const presetType = button.getAttribute('data-preset');
                    applyLUPreset(presetType);
                    
                    button.classList.add('active');
                    setTimeout(() => {
                        button.classList.remove('active');
                    }, 500);
                });
            });
        }
    }

    function applyPreset(presetType) {
        // Get current matrix dimensions
        const rowsA = parseInt(document.getElementById('rowsA').value);
        const colsA = parseInt(document.getElementById('colsA').value);
        const rowsB = parseInt(document.getElementById('rowsB').value);
        const colsB = parseInt(document.getElementById('colsB').value);
        
        // Get input containers
        const matrixAInputs = document.getElementById('matrixAInputs');
        const matrixBInputs = document.getElementById('matrixBInputs');
        
        if (!matrixAInputs || !matrixBInputs) return;
        
        // Clear existing values first
        const allInputs = [...matrixAInputs.querySelectorAll('input'), ...matrixBInputs.querySelectorAll('input')];
        allInputs.forEach(input => input.value = '');
        
        // Apply different presets based on type
        switch (presetType) {
            case 'identity':
                applyIdentityMatrices(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB);
                break;
            case 'simple':
                applySimpleTestCase(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB);
                break;
            case 'fractions':
                applyFractionsTestCase(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB);
                break;
            case 'negatives':
                applyNegativesTestCase(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB);
                break;
            case 'random':
                applyRandomMatrices(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB);
                break;
        }
        
        // Trigger animation effect to highlight the changes
        highlightMatrixChanges(matrixAInputs);
        highlightMatrixChanges(matrixBInputs);
    }

    function highlightMatrixChanges(matrixContainer) {
        const inputs = matrixContainer.querySelectorAll('input');
        inputs.forEach((input, index) => {
            // Apply staggered animation to each cell
            setTimeout(() => {
                input.classList.add('preset-applied');
                setTimeout(() => {
                    input.classList.remove('preset-applied');
                }, 800);
            }, index * 50);
        });
    }

    function applyIdentityMatrices(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Set Matrix A to identity matrix
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsA; j++) {
                const index = i * colsA + j;
                inputsA[index].value = i === j ? '1' : '0';
            }
        }
        
        // Set Matrix B to identity matrix
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < rowsB; i++) {
            for (let j = 0; j < colsB; j++) {
                const index = i * colsB + j;
                inputsB[index].value = i === j ? '1' : '0';
            }
        }
    }

    function applySimpleTestCase(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Test case with simple integers
        const valuesA = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ];
        
        const valuesB = [
            [2, 3, 4, 5],
            [6, 7, 8, 9],
            [10, 11, 12, 13],
            [14, 15, 16, 17]
        ];
        
        // Apply values to Matrix A
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsA; j++) {
                if (i < valuesA.length && j < valuesA[0].length) {
                    const index = i * colsA + j;
                    inputsA[index].value = valuesA[i][j];
                }
            }
        }
        
        // Apply values to Matrix B
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < rowsB; i++) {
            for (let j = 0; j < colsB; j++) {
                if (i < valuesB.length && j < valuesB[0].length) {
                    const index = i * colsB + j;
                    inputsB[index].value = valuesB[i][j];
                }
            }
        }
    }

    function applyFractionsTestCase(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Test case with fractions
        const valuesA = [
            ['1/2', '2/3', '3/4', '1/5'],
            ['1/3', '1/4', '1/5', '1/6'],
            ['2/3', '3/4', '4/5', '5/6'],
            ['1/6', '1/7', '1/8', '1/9']
        ];
        
        const valuesB = [
            ['1/3', '1/4', '1/5', '1/6'],
            ['2/3', '3/4', '4/5', '5/6'],
            ['1/2', '2/3', '3/4', '4/5'],
            ['3/5', '4/7', '5/9', '6/11']
        ];
        
        // Apply values to Matrix A
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsA; j++) {
                if (i < valuesA.length && j < valuesA[0].length) {
                    const index = i * colsA + j;
                    inputsA[index].value = valuesA[i][j];
                }
            }
        }
        
        // Apply values to Matrix B
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < rowsB; i++) {
            for (let j = 0; j < colsB; j++) {
                if (i < valuesB.length && j < valuesB[0].length) {
                    const index = i * colsB + j;
                    inputsB[index].value = valuesB[i][j];
                }
            }
        }
    }

    function applyNegativesTestCase(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Test case with negative values
        const valuesA = [
            [-1, -2, -3, -4],
            [-5, -6, -7, -8],
            [-9, -10, -11, -12],
            [-13, -14, -15, -16]
        ];
        
        const valuesB = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ];
        
        // Apply values to Matrix A
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsA; j++) {
                if (i < valuesA.length && j < valuesA[0].length) {
                    const index = i * colsA + j;
                    inputsA[index].value = valuesA[i][j];
                }
            }
        }
        
        // Apply values to Matrix B
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < rowsB; i++) {
            for (let j = 0; j < colsB; j++) {
                if (i < valuesB.length && j < valuesB[0].length) {
                    const index = i * colsB + j;
                    inputsB[index].value = valuesB[i][j];
                }
            }
        }
    }

    function applyRandomMatrices(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Generate random integer values between -10 and 10
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < inputsA.length; i++) {
            inputsA[i].value = Math.floor(Math.random() * 21) - 10;
        }
        
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < inputsB.length; i++) {
            inputsB[i].value = Math.floor(Math.random() * 21) - 10;
        }
    }

    // Function to apply multiplication presets
    function applyMultiplicationPreset(presetType) {
        // Get current matrix dimensions
        const rowsA = parseInt(document.getElementById('rowsMultA').value);
        const colsA = parseInt(document.getElementById('colsMultA').value);
        const rowsB = parseInt(document.getElementById('rowsMultB').value);
        const colsB = parseInt(document.getElementById('colsMultB').value);
        
        const matrixAInputs = document.getElementById('matrixMultAInputs');
        const matrixBInputs = document.getElementById('matrixMultBInputs');
        
        if (!matrixAInputs || !matrixBInputs) return;
        
        // Clear existing values
        const allInputs = [...matrixAInputs.querySelectorAll('input'), ...matrixBInputs.querySelectorAll('input')];
        allInputs.forEach(input => input.value = '');
        
        // For some presets we need to adjust dimensions for compatibility
        let needToAdjustDimensions = false;
        
        switch (presetType) {
            case 'identity':
                // Ensure square matrices of same dimension
                if (rowsA !== colsA || rowsB !== colsB || colsA !== rowsB) {
                    document.getElementById('rowsMultA').value = 3;
                    document.getElementById('colsMultA').value = 3;
                    document.getElementById('rowsMultB').value = 3;
                    document.getElementById('colsMultB').value = 3;
                    
                    generateMatrixInputs(matrixAInputs, 3, 3, 'A');
                    generateMatrixInputs(matrixBInputs, 3, 3, 'B');
                    needToAdjustDimensions = true;
                }
                
                applyIdentityMatricesForMultiplication(matrixAInputs, matrixBInputs, 
                    needToAdjustDimensions ? 3 : rowsA, 
                    needToAdjustDimensions ? 3 : colsA, 
                    needToAdjustDimensions ? 3 : rowsB, 
                    needToAdjustDimensions ? 3 : colsB);
                break;
                
            case 'simple':
                // Ensure A is 2x3 and B is 3x2 for a classic multiplication example
                if (rowsA !== 2 || colsA !== 3 || rowsB !== 3 || colsB !== 2) {
                    document.getElementById('rowsMultA').value = 2;
                    document.getElementById('colsMultA').value = 3;
                    document.getElementById('rowsMultB').value = 3;
                    document.getElementById('colsMultB').value = 2;
                    
                    generateMatrixInputs(matrixAInputs, 2, 3, 'A');
                    generateMatrixInputs(matrixBInputs, 3, 2, 'B');
                    needToAdjustDimensions = true;
                }
                
                applySimpleMultiplicationCase(matrixAInputs, matrixBInputs);
                break;
                
            case 'matrix-vector':
                // Matrix × Vector: make B a column vector
                if (colsB !== 1) {
                    document.getElementById('colsMultB').value = 1;
                    generateMatrixInputs(matrixBInputs, rowsB, 1, 'B');
                }
                
                // Ensure A columns = B rows for compatibility
                if (colsA !== rowsB) {
                    document.getElementById('colsMultA').value = rowsB;
                    generateMatrixInputs(matrixAInputs, rowsA, rowsB, 'A');
                    needToAdjustDimensions = true;
                }
                
                applyMatrixVectorCase(matrixAInputs, matrixBInputs, 
                    rowsA, 
                    needToAdjustDimensions ? rowsB : colsA, 
                    rowsB, 1);
                break;
                
            case 'special':
                // Apply a special case with interesting properties (e.g., rotation matrix)
                if (rowsA !== 2 || colsA !== 2 || rowsB !== 2 || colsB !== 2) {
                    document.getElementById('rowsMultA').value = 2;
                    document.getElementById('colsMultA').value = 2;
                    document.getElementById('rowsMultB').value = 2;
                    document.getElementById('colsMultB').value = 2;
                    
                    generateMatrixInputs(matrixAInputs, 2, 2, 'A');
                    generateMatrixInputs(matrixBInputs, 2, 2, 'B');
                    needToAdjustDimensions = true;
                }
                
                applySpecialMultiplicationCase(matrixAInputs, matrixBInputs);
                break;
                
            case 'random':
                // Ensure dimensions are compatible for multiplication
                if (colsA !== rowsB) {
                    document.getElementById('rowsMultB').value = colsA;
                    generateMatrixInputs(matrixBInputs, colsA, colsB, 'B');
                    needToAdjustDimensions = true;
                }
                
                applyRandomMultiplicationMatrices(matrixAInputs, matrixBInputs, 
                    rowsA, colsA, 
                    needToAdjustDimensions ? colsA : rowsB, colsB);
                break;
        }
        
        // Highlight the changes
        highlightMatrixChanges(matrixAInputs);
        highlightMatrixChanges(matrixBInputs);
    }

    // Function to apply determinant presets
    function applyDeterminantPreset(presetType) {
        const dimension = parseInt(document.getElementById('dimensionDet').value);
        const matrixInputs = document.getElementById('matrixDetInputs');
        
        if (!matrixInputs) return;
        
        // Clear existing values
        const inputs = matrixInputs.querySelectorAll('input');
        inputs.forEach(input => input.value = '');
        
        switch (presetType) {
            case 'identity':
                applyIdentityMatrixForDeterminant(matrixInputs, dimension);
                break;
            
            case 'singular':
                applySingularMatrixForDeterminant(matrixInputs, dimension);
                break;
            
            case 'triangular':
                applyTriangularMatrixForDeterminant(matrixInputs, dimension);
                break;
            
            case 'symmetric':
                applySymmetricMatrixForDeterminant(matrixInputs, dimension);
                break;
            
            case 'random':
                applyRandomMatrixForDeterminant(matrixInputs, dimension);
                break;
        }
        
        // Highlight the changes
        highlightMatrixChanges(matrixInputs);
    }

    // Helper functions for multiplication presets
    function applyIdentityMatricesForMultiplication(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Apply identity matrices
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsA; j++) {
                const index = i * colsA + j;
                inputsA[index].value = i === j ? '1' : '0';
            }
        }
        
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < rowsB; i++) {
            for (let j = 0; j < colsB; j++) {
                const index = i * colsB + j;
                inputsB[index].value = i === j ? '1' : '0';
            }
        }
    }

    function applySimpleMultiplicationCase(matrixAInputs, matrixBInputs) {
        // 2x3 and 3x2 matrices for showcasing matrix multiplication
        const valuesA = [
            [1, 2, 3],
            [4, 5, 6]
        ];
        
        const valuesB = [
            [7, 8],
            [9, 10],
            [11, 12]
        ];
        
        // Apply to Matrix A (2x3)
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < 2; i++) {
            for (let j = 0; j < 3; j++) {
                const index = i * 3 + j;
                inputsA[index].value = valuesA[i][j];
            }
        }
        
        // Apply to Matrix B (3x2)
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 2; j++) {
                const index = i * 2 + j;
                inputsB[index].value = valuesB[i][j];
            }
        }
    }

    function applyMatrixVectorCase(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Fill matrix A with sequential values
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < rowsA; i++) {
            for (let j = 0; j < colsA; j++) {
                const index = i * colsA + j;
                inputsA[index].value = i + j + 1;
            }
        }
        
        // Fill vector B with ones
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < rowsB; i++) {
            inputsB[i].value = '1';
        }
    }

    function applySpecialMultiplicationCase(matrixAInputs, matrixBInputs) {
        // Rotation matrix (90 degrees) for A
        const valuesA = [
            [0, -1],
            [1, 0]
        ];
        
        // Matrix with vector to rotate
        const valuesB = [
            [1, 2],
            [3, 4]
        ];
        
        // Apply to Matrix A
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < 2; i++) {
            for (let j = 0; j < 2; j++) {
                const index = i * 2 + j;
                inputsA[index].value = valuesA[i][j];
            }
        }
        
        // Apply to Matrix B
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < 2; i++) {
            for (let j = 0; j < 2; j++) {
                const index = i * 2 + j;
                inputsB[index].value = valuesB[i][j];
            }
        }
    }

    function applyRandomMultiplicationMatrices(matrixAInputs, matrixBInputs, rowsA, colsA, rowsB, colsB) {
        // Generate random integers between -5 and 5
        const inputsA = matrixAInputs.querySelectorAll('input');
        for (let i = 0; i < inputsA.length; i++) {
            inputsA[i].value = Math.floor(Math.random() * 11) - 5;
        }
        
        const inputsB = matrixBInputs.querySelectorAll('input');
        for (let i = 0; i < inputsB.length; i++) {
            inputsB[i].value = Math.floor(Math.random() * 11) - 5;
        }
    }

    // Helper functions for determinant presets
    function applyIdentityMatrixForDeterminant(matrixInputs, dimension) {
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = i === j ? '1' : '0';
            }
        }
    }

    function applySingularMatrixForDeterminant(matrixInputs, dimension) {
        // Create a singular matrix (with determinant 0)
        // Method: Create a matrix where one row is a multiple of another row
        
        // First fill with random values
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = Math.floor(Math.random() * 10) + 1;
            }
        }
        
        // Then make the last row a multiple of the first row
        for (let j = 0; j < dimension; j++) {
            const multiplier = 2; // A simple multiple
            const firstRowIndex = j;
            const lastRowIndex = (dimension - 1) * dimension + j;
            
            inputs[lastRowIndex].value = multiplier * parseInt(inputs[firstRowIndex].value);
        }
    }

    function applyTriangularMatrixForDeterminant(matrixInputs, dimension) {
        // Create an upper triangular matrix (zeros below diagonal)
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = j >= i ? Math.floor(Math.random() * 9) + 1 : '0';
            }
        }
    }

    function applySymmetricMatrixForDeterminant(matrixInputs, dimension) {
        // Create a symmetric matrix (M[i][j] = M[j][i])
        const inputs = matrixInputs.querySelectorAll('input');
        
        // First fill upper triangular part with random values
        for (let i = 0; i < dimension; i++) {
            for (let j = i; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = Math.floor(Math.random() * 9) + 1;
            }
        }
        
        // Then mirror values to make it symmetric
        for (let i = 1; i < dimension; i++) {
            for (let j = 0; j < i; j++) {
                const sourceIndex = j * dimension + i;
                const targetIndex = i * dimension + j;
                inputs[targetIndex].value = inputs[sourceIndex].value;
            }
        }
    }

    function applyRandomMatrixForDeterminant(matrixInputs, dimension) {
        // Generate random integers for determinant calculation
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = Math.floor(Math.random() * 19) - 9; // Values between -9 and 9
        }
    }

    // Function to apply inverse matrix presets
    function applyInversePreset(presetType) {
        const dimension = parseInt(document.getElementById('dimensionInv').value);
        const matrixInputs = document.getElementById('matrixInvInputs');
        
        if (!matrixInputs) return;
        
        // Clear existing values
        const inputs = matrixInputs.querySelectorAll('input');
        inputs.forEach(input => input.value = '');
        
        switch (presetType) {
            case 'identity':
                // Identity matrix (its inverse is itself)
                applyIdentityMatrixForInverse(matrixInputs, dimension);
                break;
            
            case 'simple':
                // Simple invertible matrix
                applySimpleInvertibleMatrix(matrixInputs, dimension);
                break;
            
            case 'diagonal':
                // Diagonal matrix with non-zero elements
                applyDiagonalMatrix(matrixInputs, dimension);
                break;
            
            case 'orthogonal':
                // Orthogonal matrix (its transpose is its inverse)
                applyOrthogonalMatrix(matrixInputs, dimension);
                break;
            
            case 'random':
                // Random invertible matrix
                applyRandomInvertibleMatrix(matrixInputs, dimension);
                break;
        }
        
        // Highlight the changes
        highlightMatrixChanges(matrixInputs);
    }

    // Function to apply Gaussian elimination presets
    function applyGaussianPreset(presetType) {
        const dimension = parseInt(document.getElementById('dimensionGaussA').value);
        const matrixAInputs = document.getElementById('matrixGaussAInputs');
        const vectorBInputs = document.getElementById('vectorGaussBInputs');
        
        if (!matrixAInputs || !vectorBInputs) return;
        
        // Clear existing values
        matrixAInputs.querySelectorAll('input').forEach(input => input.value = '');
        vectorBInputs.querySelectorAll('input').forEach(input => input.value = '');
        
        switch (presetType) {
            case 'identity':
                // Identity matrix with simple b vector
                applyIdentitySystemForGauss(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'simple':
                // Simple system with integer solutions
                applySimpleSystemForGauss(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'consistent':
                // System with unique solution
                applyConsistentSystemForGauss(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'inconsistent':
                // System with no solution
                applyInconsistentSystemForGauss(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'random':
                // Random system
                applyRandomSystemForGauss(matrixAInputs, vectorBInputs, dimension);
                break;
        }
        
        // Highlight the changes
        highlightMatrixChanges(matrixAInputs);
        highlightMatrixChanges(vectorBInputs);
    }

    // Function to apply Gauss-Jordan presets
    function applyGaussJordanPreset(presetType) {
        const dimension = parseInt(document.getElementById('dimensionGaussJordanA').value);
        const matrixAInputs = document.getElementById('matrixGaussJordanAInputs');
        const vectorBInputs = document.getElementById('vectorGaussJordanBInputs');
        
        if (!matrixAInputs || !vectorBInputs) return;
        
        // Clear existing values
        matrixAInputs.querySelectorAll('input').forEach(input => input.value = '');
        vectorBInputs.querySelectorAll('input').forEach(input => input.value = '');
        
        switch (presetType) {
            case 'identity':
                // Identity matrix with simple b vector
                applyIdentitySystemForGaussJordan(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'simple':
                // Simple system with integer solutions
                applySimpleSystemForGaussJordan(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'unique':
                // System with unique solution
                applyUniqueSystemForGaussJordan(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'infinite':
                // System with infinite solutions
                applyInfiniteSystemForGaussJordan(matrixAInputs, vectorBInputs, dimension);
                break;
            
            case 'random':
                // Random system
                applyRandomSystemForGaussJordan(matrixAInputs, vectorBInputs, dimension);
                break;
        }
        
        // Highlight the changes
        highlightMatrixChanges(matrixAInputs);
        highlightMatrixChanges(vectorBInputs);
    }

    // Helper functions for inverse presets
    function applyIdentityMatrixForInverse(matrixInputs, dimension) {
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = i === j ? '1' : '0';
            }
        }
    }

    function applySimpleInvertibleMatrix(matrixInputs, dimension) {
        // Create a simple invertible matrix
        const matrices = {
            1: [[2]],
            2: [
                [1, 2],
                [3, 4]
            ],
            3: [
                [1, 0, 2],
                [2, 1, 0],
                [0, 3, 1]
            ],
            4: [
                [1, 0, 0, 1],
                [1, 2, 0, 0],
                [0, 1, 3, 0],
                [0, 0, 1, 4]
            ]
        };

        const matrix = matrices[dimension] || matrices[2];
        const inputs = matrixInputs.querySelectorAll('input');
        
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = matrix[i][j];
            }
        }
    }

    function applyDiagonalMatrix(matrixInputs, dimension) {
        // Diagonal matrix with random non-zero elements
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                if (i === j) {
                    // Non-zero random value for diagonal elements
                    inputs[index].value = Math.floor(Math.random() * 8) + 1; // 1 to 8
                } else {
                    inputs[index].value = '0';
                }
            }
        }
    }

    function applyOrthogonalMatrix(matrixInputs, dimension) {
        // For 2x2, we can use a rotation matrix
        if (dimension === 2) {
            const inputs = matrixInputs.querySelectorAll('input');
            // Rotation matrix (30 degrees)
            const cos = Math.sqrt(3)/2;
            const sin = 0.5;
            
            inputs[0].value = cos.toFixed(3);
            inputs[1].value = sin.toFixed(3);
            inputs[2].value = (-sin).toFixed(3);
            inputs[3].value = cos.toFixed(3);
            return;
        }
        
        // For larger dimensions, start with identity and add some structure
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                if (i === j) {
                    inputs[index].value = '1';
                } else if (i === j + 1 || i + 1 === j) {
                    inputs[index].value = '0.5';
                } else {
                    inputs[index].value = '0';
                }
            }
        }
    }

    function applyRandomInvertibleMatrix(matrixInputs, dimension) {
        const inputs = matrixInputs.querySelectorAll('input');
        
        // Start with identity to ensure invertibility
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = i === j ? '1' : '0';
            }
        }
        
        // Add random elements but keep matrix invertible by keeping determinant non-zero
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                if (i !== j) {  // Keep diagonal dominant
                    const index = i * dimension + j;
                    inputs[index].value = Math.floor(Math.random() * 7) - 3; // -3 to 3
                }
            }
        }
    }

    // Helper functions for Gaussian elimination presets
    function applyIdentitySystemForGauss(matrixInputs, vectorInputs, dimension) {
        // Identity matrix with b vector of sequential numbers
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = i === j ? '1' : '0';
            }
        }
        
        // b vector with sequential values
        const bInputs = vectorInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            bInputs[i].value = i + 1;
        }
    }

    function applySimpleSystemForGauss(matrixInputs, vectorInputs, dimension) {
        // Simple system with integer coefficients
        const systems = {
            1: {
                A: [[2]],
                b: [4]
            },
            2: {
                A: [
                    [1, 1],
                    [2, 3]
                ],
                b: [5, 13]
            },
            3: {
                A: [
                    [1, 1, 1],
                    [2, 3, 1],
                    [1, 1, 2]
                ],
                b: [6, 10, 8]
            },
            4: {
                A: [
                    [1, 1, 1, 1],
                    [1, 2, 3, 4],
                    [4, 3, 2, 1],
                    [1, 3, 3, 1]
                ],
                b: [10, 20, 30, 40]
            }
        };

        const system = systems[dimension] || systems[2];
        
        // Fill matrix A
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = system.A[i][j];
            }
        }
        
        // Fill vector b
        const bInputs = vectorInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            bInputs[i].value = system.b[i];
        }
    }

    function applyConsistentSystemForGauss(matrixInputs, vectorInputs, dimension) {
        // Create a consistent system with nice solutions (all 1s)
        const inputs = matrixInputs.querySelectorAll('input');
        const bInputs = vectorInputs.querySelectorAll('input');
        
        // Start with random values for matrix A
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = Math.floor(Math.random() * 5) + 1; // 1 to 5
            }
        }
        
        // Set b to be the sum of columns (ensures x = [1,1,...,1] is a solution)
        for (let i = 0; i < dimension; i++) {
            let sum = 0;
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                sum += parseInt(inputs[index].value);
            }
            bInputs[i].value = sum;
        }
    }

    function applyInconsistentSystemForGauss(matrixInputs, vectorInputs, dimension) {
        // Create an inconsistent system (no solution)
        if (dimension < 2) return;
        
        const inputs = matrixInputs.querySelectorAll('input');
        const bInputs = vectorInputs.querySelectorAll('input');
        
        // Make first two rows proportional
        for (let j = 0; j < dimension; j++) {
            inputs[j].value = j + 1; // First row
            inputs[dimension + j].value = 2 * (j + 1); // Second row (proportional to first)
        }
        
        // Fill other rows with random values if dimension > 2
        for (let i = 2; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = Math.floor(Math.random() * 5) + 1;
            }
        }
        
        // Make system inconsistent by setting different b values for proportional rows
        bInputs[0].value = 10;
        bInputs[1].value = 15; // Should be 20 for consistency with the 2x factor
        
        // Random values for other b elements
        for (let i = 2; i < dimension; i++) {
            bInputs[i].value = Math.floor(Math.random() * 20) + 1;
        }
    }

    function applyRandomSystemForGauss(matrixInputs, vectorInputs, dimension) {
        // Random system
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].value = Math.floor(Math.random() * 10) - 5; // -5 to 4
        }
        
        const bInputs = vectorInputs.querySelectorAll('input');
        for (let i = 0; i < bInputs.length; i++) {
            bInputs[i].value = Math.floor(Math.random() * 20) - 10; // -10 to 9
        }
    }

    // Helper functions for Gauss-Jordan presets
    function applyIdentitySystemForGaussJordan(matrixInputs, vectorInputs, dimension) {
        // Same as Gaussian
        applyIdentitySystemForGauss(matrixInputs, vectorInputs, dimension);
    }

    function applySimpleSystemForGaussJordan(matrixInputs, vectorInputs, dimension) {
        // Same as Gaussian
        applySimpleSystemForGauss(matrixInputs, vectorInputs, dimension);
    }

    function applyUniqueSystemForGaussJordan(matrixInputs, vectorInputs, dimension) {
        // Similar to consistent system for Gaussian
        applyConsistentSystemForGauss(matrixInputs, vectorInputs, dimension);
    }

    function applyInfiniteSystemForGaussJordan(matrixInputs, vectorInputs, dimension) {
        // Create a system with infinite solutions
        if (dimension < 2) return;
        
        const inputs = matrixInputs.querySelectorAll('input');
        const bInputs = vectorInputs.querySelectorAll('input');
        
        // Clear first
        inputs.forEach(input => input.value = '0');
        bInputs.forEach(input => input.value = '0');
        
        // Create a matrix with linearly dependent rows
        // First row: all 1s
        for (let j = 0; j < dimension; j++) {
            inputs[j].value = '1';
        }
        
        // Second row: 2 times first row
        for (let j = 0; j < dimension; j++) {
            inputs[dimension + j].value = '2';
        }
        
        // Fill remaining rows to be linearly independent from first row
        for (let i = 2; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                if (j < i) {
                    inputs[index].value = Math.floor(Math.random() * 5) + 1;
                } else if (j === i) {
                    inputs[index].value = '1';
                }
            }
        }
        
        // Set b values to be consistent with the linear dependency
        bInputs[0].value = dimension;
        bInputs[1].value = 2 * dimension;
        
        // Set other b values
        for (let i = 2; i < dimension; i++) {
            bInputs[i].value = i + 1;
        }
    }

    function applyRandomSystemForGaussJordan(matrixInputs, vectorInputs, dimension) {
        // Same as Gaussian
        applyRandomSystemForGauss(matrixInputs, vectorInputs, dimension);
    }

    // Function to apply LU factorization presets
    function applyLUPreset(presetType) {
        const dimension = parseInt(document.getElementById('dimensionLuA').value);
        const matrixInputs = document.getElementById('matrixLuAInputs');
        
        if (!matrixInputs) return;
        
        // Clear existing values
        const inputs = matrixInputs.querySelectorAll('input');
        inputs.forEach(input => input.value = '');
        
        switch (presetType) {
            case 'identity':
                // Identity matrix
                applyIdentityMatrixForLU(matrixInputs, dimension);
                break;
            
            case 'simple':
                // Simple matrix with known LU factorization
                applySimpleMatrixForLU(matrixInputs, dimension);
                break;
            
            case 'triangular':
                // Upper triangular matrix (U = A, L = I)
                applyTriangularMatrixForLU(matrixInputs, dimension);
                break;
            
            case 'diagonal':
                // Diagonal matrix with random values
                applyDiagonalMatrixForLU(matrixInputs, dimension);
                break;
            
            case 'random':
                // Random matrix
                applyRandomMatrixForLU(matrixInputs, dimension);
                break;
        }
        
        // Highlight the changes
        highlightMatrixChanges(matrixInputs);
    }

    // Helper functions for LU factorization presets
    function applyIdentityMatrixForLU(matrixInputs, dimension) {
        // Identity matrix - will yield L = U = I
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = i === j ? '1' : '0';
            }
        }
    }

    function applySimpleMatrixForLU(matrixInputs, dimension) {
        // Create a simple matrix with known LU factorization
        const matrices = {
            1: [[2]],
            2: [
                [2, 1],
                [6, 4]
            ],
            3: [
                [4, 2, 1],
                [8, 7, 2],
                [4, 2, 5]
            ],
            4: [
                [4, 2, 1, 1],
                [8, 8, 2, 3],
                [4, 6, 6, 4],
                [2, 4, 2, 8]
            ]
        };

        const matrix = matrices[dimension] || matrices[2];
        const inputs = matrixInputs.querySelectorAll('input');
        
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                inputs[index].value = matrix[i][j];
            }
        }
    }

    function applyTriangularMatrixForLU(matrixInputs, dimension) {
        // Upper triangular matrix (U = A, L = I)
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                if (j >= i) {
                    inputs[index].value = Math.floor(Math.random() * 9) + 1;
                } else {
                    inputs[index].value = '0';
                }
            }
        }
    }

    function applyDiagonalMatrixForLU(matrixInputs, dimension) {
        // Diagonal matrix (trivial LU factorization)
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                if (i === j) {
                    inputs[index].value = Math.floor(Math.random() * 9) + 1;
                } else {
                    inputs[index].value = '0';
                }
            }
        }
    }

    function applyRandomMatrixForLU(matrixInputs, dimension) {
        // Generate random integers - avoiding zero entries on the diagonal to help with pivots
        const inputs = matrixInputs.querySelectorAll('input');
        for (let i = 0; i < dimension; i++) {
            for (let j = 0; j < dimension; j++) {
                const index = i * dimension + j;
                // For diagonal elements, use values 1-9 to avoid singular matrices
                if (i === j) {
                    inputs[index].value = Math.floor(Math.random() * 9) + 1;
                } else {
                    // For non-diagonal elements, use values -5 to 5
                    inputs[index].value = Math.floor(Math.random() * 11) - 5;
                }
            }
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