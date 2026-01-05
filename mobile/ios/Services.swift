import Foundation
import LocalAuthentication
import Security

// MARK: - Biometric Authentication
class BiometricAuthManager: ObservableObject {
    @Published var isAuthenticated = false
    
    func authenticate() {
        let context = LAContext()
        var error: NSError?
        
        if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
            let reason = "Authenticate to access Secure CipherStegno"
            
            context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { success, error in
                DispatchQueue.main.async {
                    if success {
                        self.isAuthenticated = true
                    } else {
                        print("Authentication failed: \(error?.localizedDescription ?? "Unknown error")")
                    }
                }
            }
        } else {
            // Biometric not available, allow access
            isAuthenticated = true
        }
    }
}

// MARK: - Keychain Service
class KeychainService {
    static let shared = KeychainService()
    
    private let service = "com.cipherstegno.app"
    
    func saveToken(_ token: String) {
        let data = Data(token.utf8)
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: "apiToken",
            kSecValueData as String: data
        ]
        
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }
    
    func getToken() -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: "apiToken",
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        if status == errSecSuccess,
           let data = result as? Data,
           let token = String(data: data, encoding: .utf8) {
            return token
        }
        return nil
    }
    
    func deleteToken() {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: "apiToken"
        ]
        SecItemDelete(query as CFDictionary)
    }
}

// MARK: - Crypto Service
class CryptoService {
    static let shared = CryptoService()
    
    func encrypt(text: String, algorithm: String, key: String?, shift: Int) async throws -> String {
        switch algorithm {
        case "caesar":
            return encryptCaesar(text, shift: shift)
        case "vigenere":
            guard let key = key, !key.isEmpty else {
                throw CryptoError.invalidKey
            }
            return try await APIClient.shared.encrypt(text: text, algorithm: algorithm, key: key, shift: nil)
        case "aes", "rsa":
            guard let key = key, !key.isEmpty else {
                throw CryptoError.invalidKey
            }
            return try await APIClient.shared.encrypt(text: text, algorithm: algorithm, key: key, shift: nil)
        default:
            throw CryptoError.unsupportedAlgorithm
        }
    }
    
    func decrypt(text: String, algorithm: String, key: String?, shift: Int) async throws -> String {
        switch algorithm {
        case "caesar":
            return decryptCaesar(text, shift: shift)
        default:
            guard let key = key, !key.isEmpty else {
                throw CryptoError.invalidKey
            }
            return try await APIClient.shared.decrypt(ciphertext: text, algorithm: algorithm, key: key, shift: nil, iv: nil)
        }
    }
    
    private func encryptCaesar(_ text: String, shift: Int) -> String {
        return text.map { char in
            if char.isLetter {
                let base = char.isUppercase ? Character("A").asciiValue! : Character("a").asciiValue!
                let shifted = (char.asciiValue! - base + UInt8(shift)) % 26 + base
                return Character(UnicodeScalar(shifted))
            }
            return char
        }.reduce("") { $0 + String($1) }
    }
    
    private func decryptCaesar(_ text: String, shift: Int) -> String {
        return encryptCaesar(text, shift: 26 - shift)
    }
}

// MARK: - Steganography Service
class SteganographyService {
    static let shared = SteganographyService()
    
    func encode(image: UIImage, message: String) async throws -> UIImage {
        // For production, call API or implement LSB locally
        return try await APIClient.shared.stegoEncode(image: image, message: message)
    }
    
    func decode(image: UIImage) async throws -> String {
        return try await APIClient.shared.stegoDecode(image: image)
    }
}

// MARK: - API Client
class APIClient {
    static let shared = APIClient()
    
    private let baseURL = "https://api.cipherstegno.com/api/v1"
    
    struct EncryptRequest: Codable {
        let text: String
        let algorithm: String
        let key: String?
        let shift: Int?
    }
    
    struct EncryptResponse: Codable {
        let success: Bool
        let ciphertext: String
        let iv: String?
    }
    
    struct DecryptRequest: Codable {
        let ciphertext: String
        let algorithm: String
        let key: String?
        let shift: Int?
        let iv: String?
    }
    
    struct DecryptResponse: Codable {
        let success: Bool
        let plaintext: String
    }
    
    struct PasswordValidationResponse: Codable {
        let success: Bool
        let validation: ValidationResult
        
        struct ValidationResult: Codable {
            let strength: String
            let score: Int
            let feedback: [String]
        }
    }
    
    struct PasswordGenerationResponse: Codable {
        let success: Bool
        let password: String
        let strength: String
        let score: Int
    }
    
    func encrypt(text: String, algorithm: String, key: String?, shift: Int?) async throws -> String {
        let url = URL(string: "\(baseURL)/encrypt")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = EncryptRequest(text: text, algorithm: algorithm, key: key, shift: shift)
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(EncryptResponse.self, from: data)
        return response.ciphertext
    }
    
    func decrypt(ciphertext: String, algorithm: String, key: String?, shift: Int?, iv: String?) async throws -> String {
        let url = URL(string: "\(baseURL)/decrypt")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = DecryptRequest(ciphertext: ciphertext, algorithm: algorithm, key: key, shift: shift, iv: iv)
        request.httpBody = try JSONEncoder().encode(body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(DecryptResponse.self, from: data)
        return response.plaintext
    }
    
    func validatePassword(_ password: String) async throws -> (strength: String, score: Int) {
        let url = URL(string: "\(baseURL)/tools/validate-password")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["password": password]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(PasswordValidationResponse.self, from: data)
        return (response.validation.strength, response.validation.score)
    }
    
    func generatePassword(length: Int) async throws -> (password: String, strength: String) {
        let url = URL(string: "\(baseURL)/tools/generate-password")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["length": length]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let response = try JSONDecoder().decode(PasswordGenerationResponse.self, from: data)
        return (response.password, response.strength)
    }
    
    func stegoEncode(image: UIImage, message: String) async throws -> UIImage {
        // Implement multipart form data upload
        let url = URL(string: "\(baseURL)/stego/encode")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        
        // Add message
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"message\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(message)\r\n".data(using: .utf8)!)
        
        // Add image
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"cover\"; filename=\"image.png\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/png\r\n\r\n".data(using: .utf8)!)
        body.append(image.pngData()!)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let (data, _) = try await URLSession.shared.data(for: request)
        
        // For simplicity, return original image (in production, decode base64 response)
        if let resultImage = UIImage(data: data) {
            return resultImage
        }
        return image
    }
    
    func stegoDecode(image: UIImage) async throws -> String {
        let url = URL(string: "\(baseURL)/stego/decode")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"stego_file\"; filename=\"image.png\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/png\r\n\r\n".data(using: .utf8)!)
        body.append(image.pngData()!)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let (data, _) = try await URLSession.shared.data(for: request)
        
        if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
           let message = json["message"] as? String {
            return message
        }
        throw CryptoError.decodingFailed
    }
}

// MARK: - Errors
enum CryptoError: Error, LocalizedError {
    case invalidKey
    case unsupportedAlgorithm
    case decodingFailed
    
    var errorDescription: String? {
        switch self {
        case .invalidKey:
            return "Invalid or missing key"
        case .unsupportedAlgorithm:
            return "Unsupported algorithm"
        case .decodingFailed:
            return "Failed to decode message"
        }
    }
}
