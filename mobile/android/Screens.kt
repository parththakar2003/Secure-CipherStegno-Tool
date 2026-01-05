package com.cipherstegno.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.cipherstegno.service.CryptoService
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CryptoScreen() {
    var selectedAlgorithm by remember { mutableStateOf("caesar") }
    var inputText by remember { mutableStateOf("") }
    var outputText by remember { mutableStateOf("") }
    var keyText by remember { mutableStateOf("") }
    var shiftValue by remember { mutableStateOf(3f) }
    var isEncrypting by remember { mutableStateOf(true) }
    var isLoading by remember { mutableStateOf(false) }
    
    val cryptoService = remember { CryptoService() }
    val scope = rememberCoroutineScope()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text(
            "Cryptography",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // Algorithm selection
        SingleChoiceSegmentedButtonRow(modifier = Modifier.fillMaxWidth()) {
            listOf("caesar", "vigenere", "aes", "rsa").forEachIndexed { index, algo ->
                SegmentedButton(
                    selected = selectedAlgorithm == algo,
                    onClick = { selectedAlgorithm = algo },
                    shape = SegmentedButtonDefaults.itemShape(index, 4)
                ) {
                    Text(algo.uppercase())
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Mode selection
        Row(modifier = Modifier.fillMaxWidth()) {
            FilterChip(
                selected = isEncrypting,
                onClick = { isEncrypting = true },
                label = { Text("Encrypt") },
                modifier = Modifier.weight(1f).padding(end = 8.dp)
            )
            FilterChip(
                selected = !isEncrypting,
                onClick = { isEncrypting = false },
                label = { Text("Decrypt") },
                modifier = Modifier.weight(1f)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Input text
        OutlinedTextField(
            value = inputText,
            onValueChange = { inputText = it },
            label = { Text("Input Text") },
            modifier = Modifier
                .fillMaxWidth()
                .height(150.dp),
            maxLines = 6
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Key/Password field
        if (selectedAlgorithm == "caesar") {
            Text("Shift Value: ${shiftValue.toInt()}")
            Slider(
                value = shiftValue,
                onValueChange = { shiftValue = it },
                valueRange = 1f..25f,
                steps = 23
            )
        } else {
            OutlinedTextField(
                value = keyText,
                onValueChange = { keyText = it },
                label = { Text("Key/Password") },
                modifier = Modifier.fillMaxWidth()
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Process button
        Button(
            onClick = {
                scope.launch {
                    isLoading = true
                    try {
                        outputText = if (isEncrypting) {
                            cryptoService.encryptAES(inputText, keyText).getOrThrow().ciphertext
                        } else {
                            "Decryption result" // Implement decrypt
                        }
                    } catch (e: Exception) {
                        outputText = "Error: ${e.message}"
                    }
                    isLoading = false
                }
            },
            modifier = Modifier.fillMaxWidth(),
            enabled = !isLoading && inputText.isNotEmpty()
        ) {
            if (isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(20.dp),
                    color = MaterialTheme.colorScheme.onPrimary
                )
                Spacer(modifier = Modifier.width(8.dp))
            }
            Text(if (isEncrypting) "Encrypt" else "Decrypt")
        }
        
        // Output
        if (outputText.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedCard(
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Output", style = MaterialTheme.typography.titleMedium)
                        TextButton(onClick = {
                            // Copy to clipboard
                        }) {
                            Text("Copy")
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(outputText)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SteganographyScreen() {
    var messageText by remember { mutableStateOf("") }
    var isEncoding by remember { mutableStateOf(true) }
    var resultMessage by remember { mutableStateOf("") }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text(
            "Steganography",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // Mode selection
        Row(modifier = Modifier.fillMaxWidth()) {
            FilterChip(
                selected = isEncoding,
                onClick = { isEncoding = true },
                label = { Text("Hide Message") },
                modifier = Modifier.weight(1f).padding(end = 8.dp)
            )
            FilterChip(
                selected = !isEncoding,
                onClick = { isEncoding = false },
                label = { Text("Extract Message") },
                modifier = Modifier.weight(1f)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Image selection placeholder
        OutlinedCard(
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp),
            onClick = { /* Open image picker */ }
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = androidx.compose.ui.Alignment.Center
            ) {
                Text("Tap to select image")
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        if (isEncoding) {
            OutlinedTextField(
                value = messageText,
                onValueChange = { messageText = it },
                label = { Text("Message to Hide") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp),
                maxLines = 5
            )
            
            Spacer(modifier = Modifier.height(16.dp))
        }
        
        Button(
            onClick = { /* Process steganography */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(if (isEncoding) "Hide Message" else "Extract Message")
        }
        
        if (resultMessage.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedCard(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Result", style = MaterialTheme.typography.titleMedium)
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(resultMessage)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ToolsScreen() {
    var passwordInput by remember { mutableStateOf("") }
    var passwordStrength by remember { mutableStateOf("") }
    var generatedPassword by remember { mutableStateOf("") }
    var passwordLength by remember { mutableStateOf(16f) }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text(
            "Security Tools",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // Password Validator
        OutlinedCard(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Password Validator", style = MaterialTheme.typography.titleMedium)
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = passwordInput,
                    onValueChange = { passwordInput = it },
                    label = { Text("Enter password") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(8.dp))
                Button(
                    onClick = { /* Validate password */ },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Validate")
                }
                if (passwordStrength.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(passwordStrength, style = MaterialTheme.typography.bodySmall)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Password Generator
        OutlinedCard(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Password Generator", style = MaterialTheme.typography.titleMedium)
                Spacer(modifier = Modifier.height(8.dp))
                Text("Length: ${passwordLength.toInt()}")
                Slider(
                    value = passwordLength,
                    onValueChange = { passwordLength = it },
                    valueRange = 8f..32f,
                    steps = 23
                )
                Button(
                    onClick = { /* Generate password */ },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Generate")
                }
                if (generatedPassword.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(generatedPassword, style = MaterialTheme.typography.bodyMedium)
                        TextButton(onClick = { /* Copy */ }) {
                            Text("Copy")
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen() {
    var apiEndpoint by remember { mutableStateOf("https://api.cipherstegno.com") }
    var enableBiometrics by remember { mutableStateOf(true) }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text(
            "Settings",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // API Settings
        OutlinedCard(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("API Settings", style = MaterialTheme.typography.titleMedium)
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedTextField(
                    value = apiEndpoint,
                    onValueChange = { apiEndpoint = it },
                    label = { Text("API Endpoint") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Security Settings
        OutlinedCard(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Security", style = MaterialTheme.typography.titleMedium)
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Biometric Authentication")
                    Switch(
                        checked = enableBiometrics,
                        onCheckedChange = { enableBiometrics = it }
                    )
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // About
        OutlinedCard(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("About", style = MaterialTheme.typography.titleMedium)
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Version")
                    Text("3.1.0", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Button(
            onClick = { /* Sign out */ },
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.error
            )
        ) {
            Text("Sign Out")
        }
    }
}
