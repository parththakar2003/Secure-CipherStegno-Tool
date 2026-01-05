package com.cipherstegno.service

import android.content.Context
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity
import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import javax.crypto.spec.IvParameterSpec
import android.util.Base64
import java.security.MessageDigest

// MARK: - Biometric Service
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

// MARK: - Crypto Service
class CryptoService {
    
    data class EncryptResult(
        val ciphertext: String,
        val iv: String
    )
    
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
    
    // AES-256 Decryption
    fun decryptAES(ciphertext: String, iv: String, password: String): Result<String> {
        return try {
            val key = generateAESKey(password)
            val cipher = Cipher.getInstance("AES/CBC/PKCS5Padding")
            val ivSpec = IvParameterSpec(Base64.decode(iv, Base64.DEFAULT))
            cipher.init(Cipher.DECRYPT_MODE, key, ivSpec)
            
            val decrypted = cipher.doFinal(Base64.decode(ciphertext, Base64.DEFAULT))
            Result.success(String(decrypted))
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
                char.isDigit() -> {
                    ((char.toString().toInt() + shift) % 10).toString()[0]
                }
                else -> char
            }
        }.joinToString("")
    }
    
    fun decryptCaesar(text: String, shift: Int): String {
        return encryptCaesar(text, 26 - shift)
    }
    
    // Vigenere Cipher
    fun encryptVigenere(text: String, key: String): String {
        if (key.isEmpty() || !key.all { it.isLetter() }) {
            throw IllegalArgumentException("Key must contain only letters")
        }
        
        val upperKey = key.toUpperCase()
        var keyIndex = 0
        
        return text.map { char ->
            if (char.isLetter()) {
                val base = if (char.isUpperCase()) 'A' else 'a'
                val shift = upperKey[keyIndex % upperKey.length] - 'A'
                keyIndex++
                ((char - base + shift) % 26 + base.toInt()).toChar()
            } else {
                char
            }
        }.joinToString("")
    }
    
    fun decryptVigenere(text: String, key: String): String {
        if (key.isEmpty() || !key.all { it.isLetter() }) {
            throw IllegalArgumentException("Key must contain only letters")
        }
        
        val upperKey = key.toUpperCase()
        var keyIndex = 0
        
        return text.map { char ->
            if (char.isLetter()) {
                val base = if (char.isUpperCase()) 'A' else 'a'
                val shift = upperKey[keyIndex % upperKey.length] - 'A'
                keyIndex++
                ((char - base - shift + 26) % 26 + base.toInt()).toChar()
            } else {
                char
            }
        }.joinToString("")
    }
    
    private fun generateAESKey(password: String): SecretKeySpec {
        val digest = MessageDigest.getInstance("SHA-256")
        val hash = digest.digest(password.toByteArray())
        return SecretKeySpec(hash, "AES")
    }
}

// MARK: - Steganography Service
class SteganographyService {
    
    // Placeholder for image steganography
    // In production, implement LSB encoding/decoding
    
    fun encode(imageBytes: ByteArray, message: String): ByteArray {
        // Implement LSB encoding
        return imageBytes
    }
    
    fun decode(imageBytes: ByteArray): String {
        // Implement LSB decoding
        return ""
    }
}

// MARK: - API Client
class ApiClient {
    companion object {
        private const val BASE_URL = "https://api.cipherstegno.com/api/v1"
    }
    
    // API methods would use Retrofit here
    // This is a simplified placeholder
    
    suspend fun encrypt(
        text: String,
        algorithm: String,
        key: String?,
        shift: Int?
    ): Result<String> {
        // In production, make API call
        return Result.success("encrypted_text")
    }
    
    suspend fun decrypt(
        ciphertext: String,
        algorithm: String,
        key: String?,
        shift: Int?,
        iv: String?
    ): Result<String> {
        // In production, make API call
        return Result.success("decrypted_text")
    }
    
    suspend fun validatePassword(password: String): Result<PasswordValidation> {
        // API call
        return Result.success(PasswordValidation("Medium", 5, listOf()))
    }
    
    suspend fun generatePassword(length: Int): Result<GeneratedPassword> {
        // API call
        return Result.success(GeneratedPassword("P@ssw0rd!123", "Strong", 7))
    }
    
    data class PasswordValidation(
        val strength: String,
        val score: Int,
        val feedback: List<String>
    )
    
    data class GeneratedPassword(
        val password: String,
        val strength: String,
        val score: Int
    )
}

// MARK: - Secure Storage
class SecureStorage(private val context: Context) {
    private val prefs = context.getSharedPreferences("secure_prefs", Context.MODE_PRIVATE)
    
    fun saveToken(token: String) {
        prefs.edit().putString("api_token", token).apply()
    }
    
    fun getToken(): String? {
        return prefs.getString("api_token", null)
    }
    
    fun clearToken() {
        prefs.edit().remove("api_token").apply()
    }
}
