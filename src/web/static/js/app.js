/**
 * Secure CipherStegno Tool - Web Interface Application
 * Modern JavaScript (ES6+) Frontend Application
 * 
 * @version 3.1.0
 * @author Parth Thakar
 * @license MIT
 * 
 * This module handles:
 * - Tab navigation between Cryptography, Steganography, Security Tools, and About
 * - Operation switching (encrypt/decrypt, encode/decode)
 * - Dynamic form field visibility based on algorithm selection
 * - API communication with FastAPI backend at /api/v1/
 * - User-friendly toast notifications and loading states
 */

// ============================================================================
// CONFIGURATION & CONSTANTS
// ============================================================================

const CONFIG = {
  API_BASE_URL: '/api/v1',
  TOAST_DURATION: 3000,
  REQUEST_TIMEOUT: 30000, // 30 seconds
};

/**
 * Algorithm configuration mapping
 * Defines which form fields should be visible/hidden for each algorithm
 */
const ALGORITHM_CONFIG = {
  encrypt: {
    caesar: {
      showFields: ['shift'],
      hideFields: ['key', 'iv'],
      requireKey: false,
    },
    vigenere: {
      showFields: ['key'],
      hideFields: ['shift', 'iv'],
      requireKey: true,
    },
    playfair: {
      showFields: ['key'],
      hideFields: ['shift', 'iv'],
      requireKey: true,
    },
    railfence: {
      showFields: ['shift'],
      hideFields: ['key', 'iv'],
      requireKey: false,
      description: 'Number of rails for Rail Fence cipher',
    },
    aes: {
      showFields: ['key'],
      hideFields: ['shift', 'iv'],
      requireKey: true,
    },
    blowfish: {
      showFields: ['key'],
      hideFields: ['shift', 'iv'],
      requireKey: true,
    },
    des3: {
      showFields: ['key'],
      hideFields: ['shift', 'iv'],
      requireKey: true,
    },
    chacha20: {
      showFields: ['key'],
      hideFields: ['shift', 'iv'],
      requireKey: true,
    },
    rsa: {
      showFields: [],
      hideFields: ['shift', 'key', 'iv'],
      requireKey: false,
    },
  },
  decrypt: {
    caesar: {
      showFields: ['shift'],
      hideFields: ['key', 'iv', 'private_key'],
      requireKey: false,
    },
    vigenere: {
      showFields: ['key'],
      hideFields: ['shift', 'iv', 'private_key'],
      requireKey: true,
    },
    playfair: {
      showFields: ['key'],
      hideFields: ['shift', 'iv', 'private_key'],
      requireKey: true,
    },
    railfence: {
      showFields: ['shift'],
      hideFields: ['key', 'iv', 'private_key'],
      requireKey: false,
    },
    aes: {
      showFields: ['key', 'iv'],
      hideFields: ['shift', 'private_key'],
      requireKey: true,
    },
    blowfish: {
      showFields: ['key'],
      hideFields: ['shift', 'iv', 'private_key'],
      requireKey: true,
    },
    des3: {
      showFields: ['key'],
      hideFields: ['shift', 'iv', 'private_key'],
      requireKey: true,
    },
    chacha20: {
      showFields: ['key'],
      hideFields: ['shift', 'iv', 'private_key'],
      requireKey: true,
    },
    rsa: {
      showFields: ['private_key'],
      hideFields: ['shift', 'key', 'iv'],
      requireKey: false,
    },
  },
};

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize the application
 * Called when the DOM is fully loaded
 */
document.addEventListener('DOMContentLoaded', () => {
  initializeTabNavigation();
  initializeOperationSwitching();
  initializeAlgorithmSelection();
  initializeFormValidation();
  
  // Prevent form submission on Enter for textareas
  document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && e.ctrlKey) {
        e.preventDefault();
        // Let button click handlers manage submission
      }
    });
  });
});

/**
 * Initialize tab navigation functionality
 */
function initializeTabNavigation() {
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const tabName = link.getAttribute('data-tab');
      switchTab(tabName);
    });
  });
}

/**
 * Initialize operation switching (encrypt/decrypt, encode/decode)
 */
function initializeOperationSwitching() {
  // Cryptography operations
  const cryptoOpButtons = document.querySelectorAll('#crypto-tab .op-btn');
  cryptoOpButtons.forEach(button => {
    button.addEventListener('click', () => {
      const operation = button.getAttribute('data-op');
      switchCryptoOperation(operation);
    });
  });
  
  // Steganography operations
  const stegoOpButtons = document.querySelectorAll('#stego-tab .op-btn');
  stegoOpButtons.forEach(button => {
    button.addEventListener('click', () => {
      const operation = button.getAttribute('data-op');
      switchStegoOperation(operation);
    });
  });
}

/**
 * Initialize algorithm selection change handlers
 */
function initializeAlgorithmSelection() {
  const algorithmSelects = document.querySelectorAll('select[id*="algorithm"]');
  
  algorithmSelects.forEach(select => {
    select.addEventListener('change', () => {
      updateFormFieldsForAlgorithm(select);
    });
  });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
  // Add real-time validation hints if needed
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach(input => {
    input.addEventListener('change', () => {
      validatePasswordField(input);
    });
  });
}

// ============================================================================
// TAB NAVIGATION
// ============================================================================

/**
 * Switch between main tabs (Cryptography, Steganography, Security Tools, About)
 * @param {string} tabName - The tab identifier
 */
function switchTab(tabName) {
  // Hide all tabs
  const allTabs = document.querySelectorAll('.tab-content');
  allTabs.forEach(tab => tab.classList.remove('active'));
  
  // Remove active state from all nav links
  const allNavLinks = document.querySelectorAll('.nav-link');
  allNavLinks.forEach(link => link.classList.remove('active'));
  
  // Show selected tab
  const selectedTab = document.getElementById(`${tabName}-tab`);
  if (selectedTab) {
    selectedTab.classList.add('active');
  }
  
  // Mark nav link as active
  const activeNavLink = document.querySelector(`[data-tab="${tabName}"]`);
  if (activeNavLink) {
    activeNavLink.classList.add('active');
  }
}

// ============================================================================
// OPERATION SWITCHING
// ============================================================================

/**
 * Switch between encryption and decryption operations
 * @param {string} operation - 'encrypt' or 'decrypt'
 */
function switchCryptoOperation(operation) {
  const encryptSection = document.getElementById('encrypt-section');
  const decryptSection = document.getElementById('decrypt-section');
  const cryptoButtons = document.querySelectorAll('#crypto-tab .op-btn');
  
  // Update button states
  cryptoButtons.forEach(btn => btn.classList.remove('active'));
  document.querySelector(`#crypto-tab .op-btn[data-op="${operation}"]`)?.classList.add('active');
  
  // Show/hide sections
  if (operation === 'encrypt') {
    encryptSection.style.display = 'block';
    decryptSection.style.display = 'none';
  } else {
    encryptSection.style.display = 'none';
    decryptSection.style.display = 'block';
  }
}

/**
 * Switch between encoding and decoding operations
 * @param {string} operation - 'encode' or 'decode'
 */
function switchStegoOperation(operation) {
  const encodeSection = document.getElementById('encode-section');
  const decodeSection = document.getElementById('decode-section');
  const stegoButtons = document.querySelectorAll('#stego-tab .op-btn');
  
  // Update button states
  stegoButtons.forEach(btn => btn.classList.remove('active'));
  document.querySelector(`#stego-tab .op-btn[data-op="${operation}"]`)?.classList.add('active');
  
  // Show/hide sections
  if (operation === 'encode') {
    encodeSection.style.display = 'block';
    decodeSection.style.display = 'none';
  } else {
    encodeSection.style.display = 'none';
    decodeSection.style.display = 'block';
  }
}

// ============================================================================
// FORM FIELD MANAGEMENT
// ============================================================================

/**
 * Update form field visibility based on selected algorithm
 * @param {HTMLSelectElement} selectElement - The algorithm select element
 */
function updateFormFieldsForAlgorithm(selectElement) {
  const algorithm = selectElement.value;
  const sectionId = selectElement.id.includes('encrypt') ? 'encrypt' : 'decrypt';
  const operation = sectionId.replace('-algorithm', '');
  
  // Get configuration for this algorithm
  const config = ALGORITHM_CONFIG[operation]?.[algorithm];
  
  if (!config) {
    console.warn(`No configuration found for ${operation} - ${algorithm}`);
    return;
  }
  
  // Hide all optional fields
  ['key', 'shift', 'iv', 'private_key'].forEach(field => {
    const fieldGroup = document.getElementById(`${sectionId}-${field}-group`);
    if (fieldGroup) {
      fieldGroup.style.display = 'none';
    }
  });
  
  // Show required fields
  config.showFields.forEach(field => {
    const fieldGroup = document.getElementById(`${sectionId}-${field}-group`);
    if (fieldGroup) {
      fieldGroup.style.display = 'block';
    }
  });
}

/**
 * Validate a password field
 * @param {HTMLInputElement} inputElement - The password input element
 */
function validatePasswordField(inputElement) {
  const value = inputElement.value;
  
  // Add validation feedback (can be enhanced with real-time feedback)
  if (value.length < 4 && value.length > 0) {
    inputElement.classList.add('invalid');
  } else {
    inputElement.classList.remove('invalid');
  }
}

// ============================================================================
// CRYPTOGRAPHY OPERATIONS
// ============================================================================

/**
 * Perform encryption operation
 * Validates input, sends request to backend, and displays result
 */
async function performEncryption() {
  try {
    showLoading();
    
    // Get form values
    const text = document.getElementById('encrypt-text').value.trim();
    const algorithm = document.getElementById('encrypt-algorithm').value;
    const key = document.getElementById('encrypt-key')?.value || '';
    const shift = parseInt(document.getElementById('encrypt-shift')?.value || '3');
    
    // Validation
    if (!text) {
      throw new Error('Please enter text to encrypt');
    }
    
    // Check if key is required but missing
    const config = ALGORITHM_CONFIG.encrypt[algorithm];
    if (config?.requireKey && !key) {
      throw new Error(`Key/Password is required for ${algorithm.toUpperCase()} encryption`);
    }
    
    // AES always generates and returns IV - no validation needed here
    // The backend will include IV in response for AES encryption
    
    // Prepare request
    const payload = {
      text,
      algorithm,
      ...(key && { key }),
      ...(shift && { shift }),
    };
    
    // Make API request
    const response = await makeRequest(`${CONFIG.API_BASE_URL}/encrypt`, 'POST', payload);
    
    if (!response.success) {
      throw new Error(response.detail || 'Encryption failed');
    }
    
    // Display result
    displayEncryptionResult(response);
    showToast('✅ Encryption successful!', 'success');
    
  } catch (error) {
    showToast(`❌ ${error.message}`, 'error');
    console.error('Encryption error:', error);
  } finally {
    hideLoading();
  }
}

/**
 * Perform decryption operation
 * Validates input, sends request to backend, and displays result
 */
async function performDecryption() {
  try {
    showLoading();
    
    // Get form values
    const ciphertext = document.getElementById('decrypt-text').value.trim();
    const algorithm = document.getElementById('decrypt-algorithm').value;
    const key = document.getElementById('decrypt-key')?.value || '';
    const iv = document.getElementById('decrypt-iv')?.value || '';
    const shift = parseInt(document.getElementById('decrypt-shift')?.value || '3');
    const privateKey = document.getElementById('decrypt-private-key')?.value || '';
    
    // Validation
    if (!ciphertext) {
      throw new Error('Please enter ciphertext to decrypt');
    }
    
    // Check if key is required but missing
    const config = ALGORITHM_CONFIG.decrypt[algorithm];
    if (config?.requireKey && !key && !privateKey) {
      throw new Error(`Key/Password or Private Key is required for ${algorithm.toUpperCase()} decryption`);
    }
    
    // For AES, IV is required
    if (algorithm === 'aes' && !iv) {
      throw new Error('IV (Initialization Vector) is required for AES decryption');
    }
    
    // Prepare request
    const payload = {
      ciphertext,
      algorithm,
      ...(key && { key }),
      ...(iv && { iv }),
      ...(shift && { shift }),
      ...(privateKey && { private_key: privateKey }),
    };
    
    // Make API request
    const response = await makeRequest(`${CONFIG.API_BASE_URL}/decrypt`, 'POST', payload);
    
    if (!response.success) {
      throw new Error(response.detail || 'Decryption failed');
    }
    
    // Display result
    displayDecryptionResult(response);
    showToast('✅ Decryption successful!', 'success');
    
  } catch (error) {
    showToast(`❌ ${error.message}`, 'error');
    console.error('Decryption error:', error);
  } finally {
    hideLoading();
  }
}

/**
 * Display encryption result in the UI
 * @param {Object} response - Response from encryption API
 */
function displayEncryptionResult(response) {
  const resultBox = document.getElementById('encrypt-result');
  const algoSpan = document.getElementById('encrypt-result-algo');
  const resultText = document.getElementById('encrypt-result-text');
  const ivGroup = document.getElementById('encrypt-result-iv');
  const keysGroup = document.getElementById('encrypt-result-keys');
  
  // Clear previous results
  resultText.value = '';
  
  // Display algorithm
  algoSpan.textContent = response.algorithm.toUpperCase();
  
  // Display ciphertext
  resultText.value = response.ciphertext;
  
  // Display IV if present (for AES, etc.)
  if (response.iv) {
    document.getElementById('encrypt-iv-value').textContent = response.iv;
    ivGroup.style.display = 'block';
  } else {
    ivGroup.style.display = 'none';
  }
  
  // Display RSA keys if present
  // NOTE: For security, we do NOT display private keys in the UI
  // Users should handle RSA keys securely through secure download mechanisms
  if (response.public_key) {
    document.getElementById('encrypt-public-key').textContent = response.public_key.substring(0, 50) + '...';
    keysGroup.style.display = 'block';
  } else {
    keysGroup.style.display = 'none';
  }
  
  // Hide private key display for security (even though field exists in HTML)
  if (response.private_key) {
    const privateKeySpan = document.getElementById('encrypt-private-key');
    if (privateKeySpan) {
      privateKeySpan.textContent = '[DOWNLOAD FROM SECURE CHANNEL]';
    }
  }
  
  // Show result box
  resultBox.style.display = 'block';
  
  // Scroll to result
  resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Display decryption result in the UI
 * @param {Object} response - Response from decryption API
 */
function displayDecryptionResult(response) {
  const resultBox = document.getElementById('decrypt-result');
  const algoSpan = document.getElementById('decrypt-result-algo');
  const resultText = document.getElementById('decrypt-result-text');
  
  // Display algorithm
  algoSpan.textContent = response.algorithm.toUpperCase();
  
  // Display plaintext
  resultText.value = response.plaintext || '';
  
  // Show result box
  resultBox.style.display = 'block';
  
  // Scroll to result
  resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ============================================================================
// STEGANOGRAPHY OPERATIONS
// ============================================================================

/**
 * Perform steganography encoding (hide message in file)
 * Validates input, sends request with FormData, and provides download
 */
async function performEncode() {
  try {
    showLoading();
    
    // Get form values
    const coverFile = document.getElementById('cover-file').files[0];
    const message = document.getElementById('hide-message').value.trim();
    const compress = document.getElementById('compress-message').checked;
    
    // Validation
    if (!coverFile) {
      throw new Error('Please select a cover file (PNG, BMP, or WAV)');
    }
    
    if (!message) {
      throw new Error('Please enter a message to hide');
    }
    
    // Validate file type
    const validTypes = ['image/png', 'image/bmp', 'audio/wav'];
    if (!validTypes.includes(coverFile.type) && !coverFile.name.match(/\.(png|bmp|wav)$/i)) {
      throw new Error('Only PNG, BMP, and WAV files are supported');
    }
    
    // Prepare FormData
    const formData = new FormData();
    formData.append('cover', coverFile);
    formData.append('message', message);
    formData.append('compress', compress);
    
    // Make API request
    const response = await makeRequest(
      `${CONFIG.API_BASE_URL}/stego/encode`,
      'POST',
      formData,
      true // isFormData flag
    );
    
    if (!response.success) {
      throw new Error(response.detail || 'Encoding failed');
    }
    
    // Display result and create download link
    displayEncodeResult(response);
    showToast('✅ Message hidden successfully!', 'success');
    
  } catch (error) {
    showToast(`❌ ${error.message}`, 'error');
    console.error('Encode error:', error);
  } finally {
    hideLoading();
  }
}

/**
 * Perform steganography decoding (extract message from file)
 * Validates input, sends request with FormData, and displays message
 */
async function performDecode() {
  try {
    showLoading();
    
    // Get form values
    const stegoFile = document.getElementById('stego-file').files[0];
    const compressed = document.getElementById('decompress-message').checked;
    
    // Validation
    if (!stegoFile) {
      throw new Error('Please select a stego file (PNG, BMP, or WAV)');
    }
    
    // Validate file type
    const validTypes = ['image/png', 'image/bmp', 'audio/wav'];
    if (!validTypes.includes(stegoFile.type) && !stegoFile.name.match(/\.(png|bmp|wav)$/i)) {
      throw new Error('Only PNG, BMP, and WAV files are supported');
    }
    
    // Prepare FormData
    const formData = new FormData();
    formData.append('stego_file', stegoFile);
    formData.append('compressed', compressed);
    
    // Make API request
    const response = await makeRequest(
      `${CONFIG.API_BASE_URL}/stego/decode`,
      'POST',
      formData,
      true // isFormData flag
    );
    
    if (!response.success) {
      throw new Error(response.detail || 'Decoding failed');
    }
    
    // Display result
    displayDecodeResult(response);
    showToast('✅ Message extracted successfully!', 'success');
    
  } catch (error) {
    showToast(`❌ ${error.message}`, 'error');
    console.error('Decode error:', error);
  } finally {
    hideLoading();
  }
}

/**
 * Display steganography encoding result
 * Efficiently converts base64-encoded blob to proper format and creates download
 * @param {Object} response - Response from encode API
 */
function displayEncodeResult(response) {
  const resultBox = document.getElementById('encode-result');
  const messageSizeSpan = document.getElementById('encode-message-size');
  const downloadLink = document.getElementById('encode-download');
  
  // Display message size
  messageSizeSpan.textContent = response.message_size || 0;
  
  // Create blob from base64-encoded output
  try {
    const binaryString = atob(response.output);
    const bytes = new Uint8Array(binaryString.length);
    
    // Convert binary string to bytes
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    
    // Create blob with appropriate MIME type
    const mimeType = `image/${response.format}`;
    const blob = new Blob([bytes], { type: mimeType });
  
    // Create object URL and set download link
    const url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = `stego_output.${response.format}`;
    
    // Show result box
    resultBox.style.display = 'block';
    
    // Scroll to result
    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (error) {
    console.error('Error decoding base64 output:', error);
    showToast('Error processing encoded file. Invalid base64 data.', 'error');
    hideLoading();
  }
}

/**
 * Display steganography decoding result
 * @param {Object} response - Response from decode API
 */
function displayDecodeResult(response) {
  const resultBox = document.getElementById('decode-result');
  const resultText = document.getElementById('decode-result-text');
  
  // Display extracted message
  resultText.value = response.message || '';
  
  // Show result box
  resultBox.style.display = 'block';
  
  // Scroll to result
  resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ============================================================================
// SECURITY TOOLS
// ============================================================================

/**
 * Validate password strength
 * Sends password to backend for validation and displays feedback
 */
async function validatePassword() {
  try {
    showLoading();
    
    // Get password
    const password = document.getElementById('validate-password').value;
    
    // Validation
    if (!password) {
      throw new Error('Please enter a password to validate');
    }
    
    // Make API request
    const response = await makeRequest(
      `${CONFIG.API_BASE_URL}/tools/validate-password`,
      'POST',
      { password }
    );
    
    if (!response.success) {
      throw new Error(response.detail || 'Validation failed');
    }
    
    // Display result
    displayPasswordValidationResult(response.validation);
    showToast('✅ Validation complete!', 'success');
    
  } catch (error) {
    showToast(`❌ ${error.message}`, 'error');
    console.error('Password validation error:', error);
  } finally {
    hideLoading();
  }
}

/**
 * Generate strong password
 * Requests password generation from backend and displays result
 */
async function generatePassword() {
  try {
    showLoading();
    
    // Get length
    const length = parseInt(document.getElementById('password-length').value) || 16;
    
    // Validation
    if (length < 8 || length > 64) {
      throw new Error('Password length must be between 8 and 64 characters');
    }
    
    // Make API request
    const response = await makeRequest(
      `${CONFIG.API_BASE_URL}/tools/generate-password`,
      'POST',
      { length }
    );
    
    if (!response.success) {
      throw new Error(response.detail || 'Generation failed');
    }
    
    // Display result
    displayGeneratedPassword(response);
    showToast('✅ Password generated successfully!', 'success');
    
  } catch (error) {
    showToast(`❌ ${error.message}`, 'error');
    console.error('Password generation error:', error);
  } finally {
    hideLoading();
  }
}

/**
 * Calculate file hash
 * Sends file to backend for hashing and displays result
 */
async function calculateHash() {
  try {
    showLoading();
    
    // Get file and algorithm
    const file = document.getElementById('hash-file').files[0];
    const algorithm = document.getElementById('hash-algorithm').value;
    
    // Validation
    if (!file) {
      throw new Error('Please select a file to hash');
    }
    
    // Prepare FormData
    const formData = new FormData();
    formData.append('file', file);
    formData.append('algorithm', algorithm);
    
    // Make API request
    const response = await makeRequest(
      `${CONFIG.API_BASE_URL}/tools/hash`,
      'POST',
      formData,
      true // isFormData flag
    );
    
    if (!response.success) {
      throw new Error(response.detail || 'Hash calculation failed');
    }
    
    // Display result
    displayHashResult(response);
    showToast('✅ Hash calculated successfully!', 'success');
    
  } catch (error) {
    showToast(`❌ ${error.message}`, 'error');
    console.error('Hash calculation error:', error);
  } finally {
    hideLoading();
  }
}

/**
 * Display password validation result
 * @param {Object} validation - Validation result object
 */
function displayPasswordValidationResult(validation) {
  const resultBox = document.getElementById('password-validation-result');
  const strengthSpan = document.getElementById('password-strength');
  const scoreSpan = document.getElementById('password-score');
  const feedbackDiv = document.getElementById('password-feedback');
  
  // Display strength and score
  strengthSpan.textContent = validation.strength || 'Unknown';
  scoreSpan.textContent = validation.score || 0;
  
  // Color code the strength
  strengthSpan.className = `strength-${(validation.strength || 'weak').toLowerCase()}`;
  
  // Display feedback
  if (validation.feedback && Array.isArray(validation.feedback)) {
    feedbackDiv.innerHTML = validation.feedback
      .map(fb => `<p>• ${fb}</p>`)
      .join('');
  } else if (validation.feedback) {
    feedbackDiv.innerHTML = `<p>${validation.feedback}</p>`;
  }
  
  // Show result box
  resultBox.style.display = 'block';
}

/**
 * Display generated password
 * @param {Object} response - Response from password generation API
 */
function displayGeneratedPassword(response) {
  const resultBox = document.getElementById('generated-password-result');
  const passwordInput = document.getElementById('generated-password');
  const strengthSpan = document.getElementById('generated-strength');
  
  // Display password
  passwordInput.value = response.password || '';
  
  // Display strength
  strengthSpan.textContent = response.strength || 'Unknown';
  strengthSpan.className = `strength-${(response.strength || 'unknown').toLowerCase()}`;
  
  // Show result box
  resultBox.style.display = 'block';
}

/**
 * Display hash calculation result
 * @param {Object} response - Response from hash calculation API
 */
function displayHashResult(response) {
  const resultBox = document.getElementById('hash-result');
  const algoSpan = document.getElementById('hash-algo');
  const hashInput = document.getElementById('hash-value');
  
  // Display algorithm
  algoSpan.textContent = response.algorithm.toUpperCase();
  
  // Display hash
  hashInput.value = response.hash || '';
  
  // Show result box
  resultBox.style.display = 'block';
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Toggle password field visibility
 * @param {string} fieldId - ID of the password input element
 * @param {Event} evt - Click event from button (optional)
 */
function togglePassword(fieldId, evt) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  
  const currentType = field.getAttribute('type');
  const newType = currentType === 'password' ? 'text' : 'password';
  field.setAttribute('type', newType);
  
  // Update button visual feedback (optional)
  const button = evt?.target;
  if (button) {
    button.textContent = newType === 'password' ? '👁️' : '🙈';
  }
}

/**
 * Copy text to clipboard
 * @param {string} elementId - ID of the element containing text to copy
 */
function copyToClipboard(elementId) {
  const element = document.getElementById(elementId);
  if (!element) return;
  
  try {
    // Get text content
    const text = element.value || element.textContent;
    
    // Copy to clipboard
    navigator.clipboard.writeText(text)
      .then(() => {
        showToast('📋 Copied to clipboard!', 'success');
      })
      .catch(() => {
        // Fallback for older browsers
        fallbackCopyToClipboard(text);
      });
      
  } catch (error) {
    showToast('❌ Failed to copy to clipboard', 'error');
    console.error('Copy error:', error);
  }
}

/**
 * Fallback copy to clipboard for older browsers
 * @param {string} text - Text to copy
 */
function fallbackCopyToClipboard(text) {
  try {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast('📋 Copied to clipboard!', 'success');
  } catch (error) {
    showToast('❌ Failed to copy to clipboard', 'error');
  }
}

/**
 * Show notification toast
 * @param {string} message - Message to display
 * @param {string} type - Toast type: 'success', 'error', 'info', 'warning'
 * @param {number} duration - Display duration in milliseconds
 */
function showToast(message, type = 'info', duration = CONFIG.TOAST_DURATION) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  
  // Set message and type
  toast.textContent = message;
  toast.className = `toast toast-${type} show`;
  
  // Auto-hide after duration
  setTimeout(() => {
    toast.classList.remove('show');
  }, duration);
}

/**
 * Show loading overlay
 */
function showLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.style.display = 'flex';
  }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
  const overlay = document.getElementById('loading-overlay');
  if (overlay) {
    overlay.style.display = 'none';
  }
}

// ============================================================================
// API COMMUNICATION
// ============================================================================

/**
 * Make HTTP request to API
 * Handles JSON and FormData requests with proper headers and error handling
 * 
 * @param {string} endpoint - API endpoint URL
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {Object|FormData} data - Request payload (optional)
 * @param {boolean} isFormData - Whether data is FormData (default: false)
 * @returns {Promise<Object>} Response JSON
 * @throws {Error} If request fails or times out
 */
async function makeRequest(endpoint, method = 'GET', data = null, isFormData = false) {
  try {
    // Prepare request options
    const options = {
      method,
      headers: {},
    };
    
    // Add request timeout
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), CONFIG.REQUEST_TIMEOUT);
    options.signal = controller.signal;
    
    // Handle data
    if (data) {
      if (isFormData) {
        // FormData (don't set Content-Type, browser will set it with boundary)
        options.body = data;
      } else {
        // JSON data
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(data);
      }
    }
    
    // Make request
    const response = await fetch(endpoint, options);
    
    // Clear timeout
    clearTimeout(timeout);
    
    // Check if response is ok
    if (!response.ok) {
      // Try to parse error message from response
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch (e) {
        // Response is not JSON, use status text
      }
      
      throw new Error(errorMessage);
    }
    
    // Parse and return response
    return await response.json();
    
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error(`Request timeout (${CONFIG.REQUEST_TIMEOUT / 1000}s)`);
    }
    throw error;
  }
}

// ============================================================================
// EXPORT FOR TESTING (Node.js / Module systems)
// ============================================================================

// If running in Node.js or module system, export functions
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    // Tab navigation
    switchTab,
    
    // Operation switching
    switchCryptoOperation,
    switchStegoOperation,
    
    // Cryptography
    performEncryption,
    performDecryption,
    
    // Steganography
    performEncode,
    performDecode,
    
    // Security tools
    validatePassword,
    generatePassword,
    calculateHash,
    
    // Utilities
    togglePassword,
    copyToClipboard,
    showToast,
    showLoading,
    hideLoading,
    makeRequest,
  };
}
