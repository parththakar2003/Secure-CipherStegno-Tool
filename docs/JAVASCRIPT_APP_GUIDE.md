# JavaScript Application Guide - Secure CipherStegno Tool

## Overview

The `src/web/static/js/app.js` file is a production-ready, comprehensive JavaScript application that provides the user interface for the Secure CipherStegno Tool web platform. It implements modern ES6+ JavaScript patterns with full error handling, input validation, and seamless API integration.

**File Statistics:**
- **Lines of Code**: 1,112
- **Functions**: 31
- **Size**: ~32KB
- **JavaScript Version**: ES6+ (async/await, arrow functions, template literals)
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)

---

## Table of Contents

1. [Architecture & Structure](#architecture--structure)
2. [Configuration](#configuration)
3. [Initialization](#initialization)
4. [Tab Navigation](#tab-navigation)
5. [Operation Switching](#operation-switching)
6. [Form Field Management](#form-field-management)
7. [Cryptography Operations](#cryptography-operations)
8. [Steganography Operations](#steganography-operations)
9. [Security Tools](#security-tools)
10. [Utility Functions](#utility-functions)
11. [API Communication](#api-communication)
12. [Error Handling](#error-handling)
13. [Testing & Debugging](#testing--debugging)

---

## Architecture & Structure

The application is organized into logical sections with clear separation of concerns:

```
app.js
├── Configuration & Constants
│   ├── CONFIG (API base URL, timeouts, toast duration)
│   └── ALGORITHM_CONFIG (field visibility rules per algorithm)
├── Initialization
│   ├── DOMContentLoaded event listener
│   ├── Tab navigation setup
│   ├── Operation switching setup
│   ├── Algorithm selection handlers
│   └── Form validation setup
├── Tab Navigation (switchTab)
├── Operation Switching
│   ├── Cryptography operations (encrypt/decrypt)
│   └── Steganography operations (encode/decode)
├── Form Field Management
│   ├── updateFormFieldsForAlgorithm
│   └── validatePasswordField
├── Cryptography Operations
│   ├── performEncryption
│   ├── performDecryption
│   ├── displayEncryptionResult
│   └── displayDecryptionResult
├── Steganography Operations
│   ├── performEncode
│   ├── performDecode
│   ├── displayEncodeResult
│   └── displayDecodeResult
├── Security Tools
│   ├── validatePassword
│   ├── generatePassword
│   ├── calculateHash
│   ├── displayPasswordValidationResult
│   ├── displayGeneratedPassword
│   └── displayHashResult
├── Utility Functions
│   ├── togglePassword
│   ├── copyToClipboard
│   ├── showToast
│   ├── showLoading
│   └── hideLoading
└── API Communication
    └── makeRequest
```

---

## Configuration

### CONFIG Object

```javascript
const CONFIG = {
  API_BASE_URL: '/api/v1',      // Base URL for all API endpoints
  TOAST_DURATION: 3000,          // Toast notification display time (ms)
  REQUEST_TIMEOUT: 30000,        // API request timeout (ms)
};
```

**Customization:**
- Modify `API_BASE_URL` for different server configurations
- Adjust `TOAST_DURATION` for user preference
- Increase `REQUEST_TIMEOUT` for large file operations

### ALGORITHM_CONFIG Object

Defines which form fields should be shown/hidden for each cryptographic algorithm:

```javascript
ALGORITHM_CONFIG = {
  encrypt: {
    caesar: { showFields: ['shift'], hideFields: ['key', 'iv'], requireKey: false },
    aes: { showFields: ['key'], hideFields: ['shift', 'iv'], requireKey: true },
    // ... more algorithms
  },
  decrypt: {
    // Similar structure for decryption
  }
}
```

**Fields:**
- `showFields`: Form fields to display
- `hideFields`: Form fields to hide
- `requireKey`: Whether key validation is required

**Adding New Algorithms:**
1. Add algorithm entry to both `encrypt` and `decrypt` sections
2. Specify which fields to show (correspond to HTML element IDs with pattern `{operation}-{field}-group`)
3. Set `requireKey` flag for validation

---

## Initialization

The application initializes on DOM load with the following sequence:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  initializeTabNavigation();           // Set up tab click handlers
  initializeOperationSwitching();      // Set up operation buttons
  initializeAlgorithmSelection();      // Set up algorithm change listeners
  initializeFormValidation();          // Set up real-time validation
  // ... additional setup
});
```

### Key Initialization Functions

#### `initializeTabNavigation()`
- Attaches click handlers to `.nav-link` elements
- Calls `switchTab()` when a tab is clicked
- Prevents default link behavior

#### `initializeOperationSwitching()`
- Handles encrypt/decrypt button switching
- Handles encode/decode button switching
- Calls appropriate operation switching functions

#### `initializeAlgorithmSelection()`
- Listens for algorithm selection changes
- Calls `updateFormFieldsForAlgorithm()` to show/hide fields

#### `initializeFormValidation()`
- Sets up real-time password field validation
- Provides visual feedback for weak passwords

---

## Tab Navigation

### switchTab(tabName)

Switches between main application tabs:

```javascript
switchTab('crypto');    // Show Cryptography tab
switchTab('stego');     // Show Steganography tab
switchTab('tools');     // Show Security Tools tab
switchTab('about');     // Show About tab
```

**What it does:**
1. Hides all tab content
2. Removes active state from all nav links
3. Shows selected tab
4. Marks nav link as active
5. Smooth scroll to new tab

**HTML Structure Expected:**
```html
<a class="nav-link" data-tab="crypto">Cryptography</a>
<div id="crypto-tab" class="tab-content"></div>
```

---

## Operation Switching

### switchCryptoOperation(operation)

Switches between encryption and decryption:

```javascript
switchCryptoOperation('encrypt');   // Show encryption form
switchCryptoOperation('decrypt');   // Show decryption form
```

### switchStegoOperation(operation)

Switches between encoding and decoding:

```javascript
switchStegoOperation('encode');     // Show encoding form
switchStegoOperation('decode');     // Show decoding form
```

**Features:**
- Updates button active state
- Shows/hides relevant sections
- Preserves form data during switching

---

## Form Field Management

### updateFormFieldsForAlgorithm(selectElement)

Dynamically shows/hides form fields based on selected algorithm:

```javascript
// When algorithm changes, this is called automatically
// Example: Selecting AES shows key field, hides shift field
```

**Algorithm-Specific Fields:**

| Algorithm | Required Fields | Optional Fields |
|-----------|-----------------|-----------------|
| Caesar | Shift | - |
| Vigenère | Key | - |
| AES | Key | IV (auto-generated) |
| RSA | - | Private Key (decrypt only) |
| ChaCha20 | Key | - |

### validatePasswordField(inputElement)

Validates password field in real-time:
- Minimum 4 characters for basic validation
- Adds/removes `invalid` CSS class
- Can be enhanced with custom validation rules

---

## Cryptography Operations

### performEncryption()

Encrypts text using selected algorithm:

```javascript
// Called by: onclick="performEncryption()"
// 1. Validates input (text must not be empty)
// 2. Validates required fields (key if required)
// 3. Sends POST request to /api/v1/encrypt
// 4. Displays result with ciphertext and IV (if applicable)
// 5. Shows success/error toast
```

**Request Format:**
```javascript
{
  text: "Plain text to encrypt",
  algorithm: "aes",
  key: "encryption_key",
  shift: 3  // for Caesar cipher
}
```

**Response Format:**
```javascript
{
  success: true,
  ciphertext: "encrypted_data",
  algorithm: "aes",
  iv: "initialization_vector"  // For AES
}
```

### performDecryption()

Decrypts ciphertext using selected algorithm:

```javascript
// Called by: onclick="performDecryption()"
// 1. Validates input (ciphertext must not be empty)
// 2. Validates required fields (key, IV for AES)
// 3. Sends POST request to /api/v1/decrypt
// 4. Displays plaintext result
// 5. Shows success/error toast
```

**Request Format:**
```javascript
{
  ciphertext: "encrypted_data",
  algorithm: "aes",
  key: "decryption_key",
  iv: "initialization_vector",  // Required for AES
  shift: 3  // for Caesar cipher
}
```

**Response Format:**
```javascript
{
  success: true,
  plaintext: "decrypted text",
  algorithm: "aes"
}
```

### displayEncryptionResult(response)

Displays encryption results in the UI:

**Features:**
- Shows algorithm used
- Displays ciphertext in textarea
- Shows IV if present (AES, ChaCha20)
- Handles RSA keys securely (public key only, private key not displayed)
- Auto-scrolls to result

### displayDecryptionResult(response)

Displays decryption results in the UI:

**Features:**
- Shows algorithm used
- Displays plaintext in textarea
- Provides copy-to-clipboard button
- Auto-scrolls to result

---

## Steganography Operations

### performEncode()

Hides a message in a cover file (image or audio):

```javascript
// Called by: onclick="performEncode()"
// 1. Validates cover file (must be PNG, BMP, or WAV)
// 2. Validates message (must not be empty)
// 3. Validates file type
// 4. Sends FormData POST request to /api/v1/stego/encode
// 5. Creates download link for output file
// 6. Shows message size and download button
```

**Request Format (FormData):**
```
- cover: File (PNG, BMP, or WAV)
- message: String (text to hide)
- compress: Boolean (compress message)
```

**Response Format:**
```javascript
{
  success: true,
  message_size: 1024,
  output: "base64_encoded_file_data",
  format: "png"  // or "bmp", "wav"
}
```

### performDecode()

Extracts a message from a stego file:

```javascript
// Called by: onclick="performDecode()"
// 1. Validates stego file (must be PNG, BMP, or WAV)
// 2. Validates file type
// 3. Sends FormData POST request to /api/v1/stego/decode
// 4. Displays extracted message
// 5. Shows copy-to-clipboard button
```

**Request Format (FormData):**
```
- stego_file: File (with hidden message)
- compressed: Boolean (whether message was compressed)
```

**Response Format:**
```javascript
{
  success: true,
  message: "extracted text"
}
```

### displayEncodeResult(response)

Displays encoding results and creates downloadable file:

**Features:**
- Shows message size
- Converts base64 data to blob
- Creates download link
- Sets appropriate filename

### displayDecodeResult(response)

Displays decoded message:

**Features:**
- Shows extracted text
- Provides copy-to-clipboard button
- Auto-scrolls to result

---

## Security Tools

### validatePassword()

Validates password strength:

```javascript
// Called by: onclick="validatePassword()"
// 1. Gets password from input
// 2. Sends POST request to /api/v1/tools/validate-password
// 3. Displays strength score and feedback
```

**Request Format:**
```javascript
{ password: "password_to_check" }
```

**Response Format:**
```javascript
{
  success: true,
  validation: {
    strength: "Strong",  // or "Weak", "Medium"
    score: 85,
    feedback: ["Contains uppercase", "Long enough"]
  }
}
```

### generatePassword()

Generates a strong random password:

```javascript
// Called by: onclick="generatePassword()"
// 1. Gets desired length
// 2. Sends POST request to /api/v1/tools/generate-password
// 3. Displays generated password and strength
```

**Request Format:**
```javascript
{ length: 16 }  // 8-64 characters
```

**Response Format:**
```javascript
{
  success: true,
  password: "GeneratedP@ssw0rd",
  strength: "Strong",
  score: 95
}
```

### calculateHash()

Calculates file hash:

```javascript
// Called by: onclick="calculateHash()"
// 1. Gets file and algorithm
// 2. Sends FormData POST request to /api/v1/tools/hash
// 3. Displays hash value
```

**Request Format (FormData):**
```
- file: File (any file type)
- algorithm: String ("md5", "sha1", "sha256", "sha512")
```

**Response Format:**
```javascript
{
  success: true,
  filename: "document.pdf",
  algorithm: "sha256",
  hash: "abc123def456..."
}
```

---

## Utility Functions

### togglePassword(fieldId, evt)

Toggles password field visibility:

```javascript
// HTML Usage:
// <button onclick="togglePassword('encrypt-key', event)">👁️</button>

// Features:
// - Changes input type between "password" and "text"
// - Updates button emoji (👁️ or 🙈)
// - No security risk (only changes display)
```

**Parameters:**
- `fieldId`: ID of password input element
- `evt`: Click event object (optional, for button feedback)

### copyToClipboard(elementId)

Copies text to clipboard with fallback:

```javascript
// HTML Usage:
// <button onclick="copyToClipboard('result-text')">Copy</button>

// Features:
// - Uses modern Clipboard API
// - Fallback for older browsers (textarea method)
// - Shows toast notification on success/failure
// - Handles both input values and text content
```

### showToast(message, type, duration)

Displays notification toast:

```javascript
showToast('✅ Operation successful!', 'success');  // Green toast
showToast('❌ Error occurred', 'error');           // Red toast
showToast('ℹ️ Information', 'info');              // Blue toast
showToast('⚠️ Warning', 'warning');               // Yellow toast

// Custom duration:
showToast('Quick notification', 'success', 1500);  // 1.5 seconds
```

**Parameters:**
- `message`: Text to display
- `type`: 'success', 'error', 'info', 'warning'
- `duration`: Display time in milliseconds (default: 3000ms)

**CSS Classes Required:**
```css
.toast              /* Base toast style */
.toast-success      /* Green background */
.toast-error        /* Red background */
.toast-info         /* Blue background */
.toast-warning      /* Yellow background */
.toast.show         /* Visible state */
```

### showLoading()

Shows loading overlay:

```javascript
showLoading();  // Shows spinner and "Processing..." message
```

**HTML Structure Expected:**
```html
<div id="loading-overlay" class="loading-overlay">
  <div class="spinner"></div>
  <p>Processing...</p>
</div>
```

### hideLoading()

Hides loading overlay:

```javascript
hideLoading();  // Hides overlay
```

---

## API Communication

### makeRequest(endpoint, method, data, isFormData)

Core API communication function with comprehensive error handling:

```javascript
// JSON Request Example:
const response = await makeRequest(
  '/api/v1/encrypt',
  'POST',
  { text: 'hello', algorithm: 'aes', key: 'key' }
);

// FormData Request Example:
const formData = new FormData();
formData.append('file', fileObject);
formData.append('algorithm', 'sha256');
const response = await makeRequest(
  '/api/v1/tools/hash',
  'POST',
  formData,
  true  // isFormData flag
);
```

**Features:**
- Automatic JSON serialization for object data
- FormData support with automatic content-type handling
- Request timeout management (30 seconds default)
- Comprehensive error handling
- Error message extraction from responses
- Browser compatibility

**Parameters:**
- `endpoint`: API endpoint URL
- `method`: HTTP method ('GET', 'POST', 'PUT', 'DELETE')
- `data`: Request payload (object or FormData)
- `isFormData`: Boolean flag for FormData requests

**Returns:**
- Promise resolving to parsed JSON response

**Throws:**
- Error with user-friendly message on failure

**Error Scenarios Handled:**
1. Network errors
2. Request timeouts
3. HTTP error responses
4. JSON parse errors
5. Server-returned error messages

---

## Error Handling

The application implements comprehensive error handling at multiple levels:

### Input Validation

```javascript
// Example: Encryption validation
if (!text) {
  throw new Error('Please enter text to encrypt');
}

if (config?.requireKey && !key) {
  throw new Error(`Key/Password is required for ${algorithm.toUpperCase()}`);
}
```

### API Error Handling

```javascript
try {
  const response = await makeRequest(endpoint, 'POST', payload);
  if (!response.success) {
    throw new Error(response.detail || 'Operation failed');
  }
  // Process success...
} catch (error) {
  showToast(`❌ ${error.message}`, 'error');
  console.error('Operation error:', error);
} finally {
  hideLoading();
}
```

### Network Error Handling

```javascript
// Timeout detection:
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

// Timeout error:
if (error.name === 'AbortError') {
  throw new Error(`Request timeout (${REQUEST_TIMEOUT / 1000}s)`);
}
```

### User Feedback

- Toast notifications for success/error messages
- Loading overlay for long-running operations
- Console logging for debugging
- Form validation feedback

---

## Testing & Debugging

### Browser Console Testing

```javascript
// Test encryption:
performEncryption();

// Test password validation:
validatePassword();

// Test API directly:
makeRequest('/api/v1/encrypt', 'POST', {
  text: 'test',
  algorithm: 'caesar',
  shift: 3
});

// View configuration:
console.log(CONFIG);
console.log(ALGORITHM_CONFIG);
```

### Debugging Tips

1. **Check Console Errors**: Browser DevTools → Console
2. **Network Inspection**: DevTools → Network tab to see API calls
3. **DOM Inspection**: DevTools → Elements to verify HTML structure
4. **Performance**: DevTools → Performance tab for optimization
5. **Console Logging**: Added to all async operations for tracing

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Toast not showing | Verify `#toast` element exists in HTML |
| Fields not toggling | Check `ALGORITHM_CONFIG` mapping |
| API calls failing | Verify `CONFIG.API_BASE_URL` is correct |
| File upload not working | Ensure FormData is used (`isFormData: true`) |
| Password toggle not working | Verify `event` parameter is passed |
| Results not scrolling | Check if element has proper ID matching pattern |

### Enabling Debug Mode

```javascript
// Add to console to enable detailed logging:
// Modify each function to add console.log statements

// Example modification:
async function performEncryption() {
  console.log('performEncryption called');
  console.log('Form values:', { text, algorithm, key });
  try {
    showLoading();
    // ... rest of function
  } catch (error) {
    console.error('Encryption error:', error);
    // ...
  }
}
```

---

## Security Considerations

### Input Validation
- All user inputs are validated before sending to API
- File types are validated on client side
- Password fields are treated securely

### Sensitive Data Handling
- RSA private keys are NOT displayed in the UI
- Passwords are only used in actual operations
- No sensitive data is logged to console in production

### API Security
- All requests use HTTPS in production
- CORS headers are configured on backend
- Request timeouts prevent hanging connections
- Error messages don't expose system details

### Frontend Security
- Content Security Policy compliant
- No inline event handlers with sensitive data
- Proper escaping of user-provided content
- FormData used for file uploads (prevents content-type manipulation)

---

## Performance Optimization

### Current Optimizations
- Lazy event listener binding
- Efficient DOM manipulation
- Request timeout management
- Blob creation optimization for large files

### Further Optimization Opportunities
- Implement request debouncing
- Add response caching
- Lazy-load modules
- Optimize DOM queries with caching
- Implement service workers for offline support

---

## Module System Support

The application exports functions for testing in module systems:

```javascript
// Node.js/Module system exports:
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    switchTab,
    switchCryptoOperation,
    switchStegoOperation,
    performEncryption,
    performDecryption,
    performEncode,
    performDecode,
    validatePassword,
    generatePassword,
    calculateHash,
    togglePassword,
    copyToClipboard,
    showToast,
    showLoading,
    hideLoading,
    makeRequest,
  };
}
```

---

## Contributing

When modifying `app.js`:

1. **Maintain Code Structure**: Follow existing section organization
2. **Add Documentation**: Update JSDoc comments for new functions
3. **Test Thoroughly**: Verify in browser DevTools
4. **Handle Errors**: Use try-catch with user-friendly messages
5. **Validate Inputs**: Check all user-provided data
6. **Keep It Secure**: Never expose sensitive information
7. **Use Modern JS**: ES6+ features are preferred
8. **Follow Patterns**: Match existing function patterns

---

## Browser Support

- ✅ Chrome/Chromium (v60+)
- ✅ Firefox (v55+)
- ✅ Safari (v11+)
- ✅ Edge (v79+)
- ⚠️ IE11 (limited support)

**Required APIs:**
- Fetch API
- Promise/async-await
- FormData
- Blob API
- URL.createObjectURL
- Clipboard API (with fallback)

---

## Version History

- **v3.1.0**: Production release with comprehensive documentation
- **v3.0.0**: Initial implementation with all core features

---

## License

MIT License - See LICENSE file in repository

---

## Support

For issues or questions:
1. Check browser console for errors
2. Review network requests in DevTools
3. Verify API server is running
4. Check backend logs for server-side errors
5. Open issue on GitHub repository

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JavaScript MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/)
- [Fetch API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [FormData API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/FormData)
