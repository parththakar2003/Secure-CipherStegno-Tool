package com.cipherstegno

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.cipherstegno.service.BiometricService
import com.cipherstegno.ui.theme.SecureCipherStegnoTheme
import com.cipherstegno.ui.screens.*

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            SecureCipherStegnoTheme {
                val biometricService = remember { BiometricService(this) }
                var isAuthenticated by remember { mutableStateOf(false) }
                
                LaunchedEffect(Unit) {
                    if (biometricService.canAuthenticate(this@MainActivity)) {
                        biometricService.authenticate { success ->
                            isAuthenticated = success
                        }
                    } else {
                        isAuthenticated = true
                    }
                }
                
                if (isAuthenticated) {
                    MainScreen()
                } else {
                    AuthenticationScreen(biometricService)
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen() {
    var selectedTab by remember { mutableStateOf(0) }
    
    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Icon(Icons.Filled.Lock, "Crypto") },
                    label = { Text("Crypto") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Icon(Icons.Filled.Image, "Stego") },
                    label = { Text("Stego") }
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    icon = { Icon(Icons.Filled.Build, "Tools") },
                    label = { Text("Tools") }
                )
                NavigationBarItem(
                    selected = selectedTab == 3,
                    onClick = { selectedTab = 3 },
                    icon = { Icon(Icons.Filled.Settings, "Settings") },
                    label = { Text("Settings") }
                )
            }
        }
    ) { paddingValues ->
        Box(modifier = Modifier.padding(paddingValues)) {
            when (selectedTab) {
                0 -> CryptoScreen()
                1 -> SteganographyScreen()
                2 -> ToolsScreen()
                3 -> SettingsScreen()
            }
        }
    }
}

@Composable
fun AuthenticationScreen(biometricService: BiometricService) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally
    ) {
        Icon(
            Icons.Filled.Lock,
            contentDescription = "Lock",
            modifier = Modifier.size(80.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Text(
            "Secure CipherStegno",
            style = MaterialTheme.typography.headlineLarge
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            "Authenticate to continue",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Button(
            onClick = {
                biometricService.authenticate { success ->
                    // Handle authentication result
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Icon(Icons.Filled.Fingerprint, "Authenticate")
            Spacer(modifier = Modifier.width(8.dp))
            Text("Authenticate")
        }
    }
}
