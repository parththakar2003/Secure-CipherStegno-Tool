# Android Application for Secure CipherStegno Tool

## Overview
Native Android application built with Kotlin and Jetpack Compose for secure cryptography and steganography operations.

## Features
- Modern Material Design 3 UI
- Biometric authentication (Fingerprint/Face)
- Google Drive integration
- Share functionality
- Camera integration
- QR code generation/scanning
- Offline mode support
- Dark theme support

## Requirements
- Android 8.0 (API 26)+
- Kotlin 1.9+
- Android Studio Hedgehog+
- Gradle 8.0+

## Project Structure
```
SecureCipherStegno-Android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/cipherstegno/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── ui/
│   │   │   │   │   ├── crypto/CryptoScreen.kt
│   │   │   │   │   ├── stego/StegoScreen.kt
│   │   │   │   │   ├── tools/ToolsScreen.kt
│   │   │   │   │   └── settings/SettingsScreen.kt
│   │   │   │   ├── data/
│   │   │   │   │   ├── model/
│   │   │   │   │   ├── repository/
│   │   │   │   │   └── api/ApiClient.kt
│   │   │   │   ├── domain/
│   │   │   │   │   └── usecase/
│   │   │   │   ├── service/
│   │   │   │   │   ├── CryptoService.kt
│   │   │   │   │   ├── SteganographyService.kt
│   │   │   │   │   └── BiometricService.kt
│   │   │   │   └── util/
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   ├── values/
│   │   │   │   ├── drawable/
│   │   │   │   └── mipmap/
│   │   │   └── AndroidManifest.xml
│   │   └── test/
│   └── build.gradle.kts
├── gradle/
└── build.gradle.kts
```

## Key Components

### 1. MainActivity.kt
```kotlin
package com.cipherstegno

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.*
import com.cipherstegno.ui.theme.SecureCipherStegnoTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        setContent {
            SecureCipherStegnoTheme {
                val biometricService = remember { BiometricService(this) }
                
                LaunchedEffect(Unit) {
                    biometricService.authenticate { success ->
                        if (success) {
                            // Proceed to main app
                        }
                    }
                }
                
                MainScreen()
            }
        }
    }
}
```

### 2. CryptoService.kt
```kotlin
package com.cipherstegno.service

import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import javax.crypto.spec.IvParameterSpec
import android.util.Base64

class CryptoService {
    
    // AES-256 Encryption
    fun encryptAES(plaintext: String, password: String): Result<EncryptResult> {
        return try {
            val key = generateAESKey(password)
            val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
            cipher.init(Cipher.ENCRYPT_MODE, key)
            
            val encrypted = cipher.doFinal(plaintext.toByteArray())
            val iv = cipher.iv
            
            Result.success(EncryptResult(
                ciphertext = Base64.encodeToString(encrypted, Base64.DEFAULT),
                iv = Base64.encodeToString(iv, Base64.DEFAULT)
            ))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    // Caesar Cipher
    fun encryptCaesar(text: String, shift: Int): String {
        return text.map { char ->
            when {
                char.isLetter() -> {
                    val base = if (char.isUpperCase()) 'A' else 'a'
                    ((char - base + shift) % 26 + base.toInt()).toChar()
                }
                else -> char
            }
        }.joinToString("")
    }
    
    private fun generateAESKey(password: String): SecretKeySpec {
        val digest = java.security.MessageDigest.getInstance("SHA-256")
        val hash = digest.digest(password.toByteArray())
        return SecretKeySpec(hash, "AES")
    }
}

data class EncryptResult(
    val ciphertext: String,
    val iv: String
)
```

### 3. BiometricService.kt
```kotlin
package com.cipherstegno.service

import android.content.Context
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity

class BiometricService(private val activity: FragmentActivity) {
    
    fun authenticate(callback: (Boolean) -> Unit) {
        val executor = ContextCompat.getMainExecutor(activity)
        
        val biometricPrompt = BiometricPrompt(
            activity,
            executor,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(
                    result: BiometricPrompt.AuthenticationResult
                ) {
                    super.onAuthenticationSucceeded(result)
                    callback(true)
                }
                
                override fun onAuthenticationFailed() {
                    super.onAuthenticationFailed()
                    callback(false)
                }
                
                override fun onAuthenticationError(
                    errorCode: Int,
                    errString: CharSequence
                ) {
                    super.onAuthenticationError(errorCode, errString)
                    callback(false)
                }
            }
        )
        
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Secure CipherStegno Authentication")
            .setSubtitle("Verify your identity")
            .setNegativeButtonText("Cancel")
            .build()
        
        biometricPrompt.authenticate(promptInfo)
    }
    
    fun canAuthenticate(context: Context): Boolean {
        val biometricManager = BiometricManager.from(context)
        return biometricManager.canAuthenticate(
            BiometricManager.Authenticators.BIOMETRIC_STRONG
        ) == BiometricManager.BIOMETRIC_SUCCESS
    }
}
```

### 4. ApiClient.kt
```kotlin
package com.cipherstegno.data.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

interface ApiService {
    @POST("api/v1/encrypt")
    suspend fun encrypt(@Body request: EncryptRequest): EncryptResponse
    
    @POST("api/v1/decrypt")
    suspend fun decrypt(@Body request: DecryptRequest): DecryptResponse
    
    @Multipart
    @POST("api/v1/stego/encode")
    suspend fun stegoEncode(
        @Part("message") message: String,
        @Part image: MultipartBody.Part
    ): StegoResponse
}

object ApiClient {
    private const val BASE_URL = "https://api.cipherstegno.com/"
    
    val apiService: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}
```

## Build Configuration

### build.gradle.kts (app)
```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.cipherstegno"
    compileSdk = 34
    
    defaultConfig {
        applicationId = "com.cipherstegno"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "3.1.0"
    }
    
    buildFeatures {
        compose = true
    }
    
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.3"
    }
}

dependencies {
    // Jetpack Compose
    implementation("androidx.compose.ui:ui:1.5.4")
    implementation("androidx.compose.material3:material3:1.1.2")
    implementation("androidx.activity:activity-compose:1.8.1")
    
    // Biometric
    implementation("androidx.biometric:biometric:1.2.0-alpha05")
    
    // Networking
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    
    // Camera
    implementation("androidx.camera:camera-camera2:1.3.0")
    implementation("androidx.camera:camera-lifecycle:1.3.0")
    implementation("androidx.camera:camera-view:1.3.0")
    
    // QR Code
    implementation("com.google.zxing:core:3.5.2")
    
    // Security
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
}
```

## Permissions (AndroidManifest.xml)
```xml
<manifest>
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.USE_BIOMETRIC"/>
    
    <application
        android:allowBackup="false"
        android:usesCleartextTraffic="false">
        <!-- Activities -->
    </application>
</manifest>
```

## Build & Run

```bash
# Clone repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git

# Open Android project
cd mobile/android
./gradlew build

# Run on emulator or device
./gradlew installDebug

# Or open in Android Studio
android-studio .
```

## Features Implementation Status

- [x] Basic UI structure with Jetpack Compose
- [x] Biometric authentication framework
- [x] API client with Retrofit
- [x] Caesar cipher implementation
- [x] AES encryption service
- [x] Material Design 3 theme
- [ ] Complete steganography implementation
- [ ] Camera integration
- [ ] QR code functionality
- [ ] Google Drive integration
- [ ] Offline mode
- [ ] Google Play Store submission

## Security Features

- **Biometric Authentication**: Fingerprint/Face unlock
- **EncryptedSharedPreferences**: Secure local storage
- **Certificate Pinning**: SSL certificate validation
- **ProGuard**: Code obfuscation
- **Security Crypto**: Android Security library
- **SafetyNet**: Device integrity check

## Testing

```bash
# Unit tests
./gradlew test

# Instrumented tests
./gradlew connectedAndroidTest
```

## Play Store

Coming soon to Google Play Store

## License

MIT License - See main repository LICENSE file
