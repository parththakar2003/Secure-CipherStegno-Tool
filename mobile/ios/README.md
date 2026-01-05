# iOS Application for Secure CipherStegno Tool

## Overview
Native iOS application built with Swift and SwiftUI for secure cryptography and steganography operations.

## Features
- Native iOS interface with SwiftUI
- Face ID / Touch ID authentication
- iCloud Keychain integration
- Share extension for files
- Widget support for quick access
- Camera integration for instant encryption
- QR code support for key exchange

## Requirements
- iOS 14.0+
- Xcode 14.0+
- Swift 5.7+

## Project Structure
```
SecureCipherStegno-iOS/
├── SecureCipherStegno/
│   ├── App/
│   │   ├── SecureCipherStegnoApp.swift
│   │   └── ContentView.swift
│   ├── Views/
│   │   ├── CryptoView.swift
│   │   ├── SteganographyView.swift
│   │   ├── ToolsView.swift
│   │   └── SettingsView.swift
│   ├── Models/
│   │   ├── CryptoService.swift
│   │   ├── SteganographyService.swift
│   │   └── User.swift
│   ├── Services/
│   │   ├── APIClient.swift
│   │   ├── BiometricAuth.swift
│   │   └── KeychainService.swift
│   ├── Utils/
│   │   ├── Extensions.swift
│   │   └── Constants.swift
│   └── Resources/
│       ├── Assets.xcassets
│       └── Info.plist
├── SecureCipherStegnoTests/
├── SecureCipherStegnoUITests/
└── Widgets/
    └── QuickAccessWidget/
```

## Key Components

### 1. SecureCipherStegnoApp.swift
```swift
import SwiftUI

@main
struct SecureCipherStegnoApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .onAppear {
                    BiometricAuth.shared.authenticate()
                }
        }
    }
}

class AppState: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
}
```

### 2. CryptoService.swift
```swift
import Foundation
import CryptoKit

class CryptoService {
    static let shared = CryptoService()
    
    // AES-256 Encryption
    func encryptAES(text: String, password: String) -> Result<String, Error> {
        // Implementation connects to backend API
        // or uses local CryptoKit
    }
    
    // RSA Encryption
    func encryptRSA(text: String, publicKey: String) -> Result<String, Error> {
        // RSA implementation
    }
    
    // Caesar Cipher
    func encryptCaesar(text: String, shift: Int) -> String {
        // Caesar implementation
    }
}
```

### 3. BiometricAuth.swift
```swift
import LocalAuthentication

class BiometricAuth {
    static let shared = BiometricAuth()
    
    func authenticate(completion: @escaping (Bool) -> Void) {
        let context = LAContext()
        var error: NSError?
        
        if context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) {
            context.evaluatePolicy(
                .deviceOwnerAuthenticationWithBiometrics,
                localizedReason: "Authenticate to access Secure CipherStegno"
            ) { success, error in
                DispatchQueue.main.async {
                    completion(success)
                }
            }
        }
    }
}
```

### 4. APIClient.swift
```swift
import Foundation

class APIClient {
    static let shared = APIClient()
    private let baseURL = "https://api.cipherstegno.com/api/v1"
    
    func encrypt(
        text: String,
        algorithm: String,
        key: String?
    ) async throws -> EncryptResponse {
        // API call to backend
    }
    
    func steganographyEncode(
        image: UIImage,
        message: String
    ) async throws -> Data {
        // Upload and encode
    }
}
```

## Build & Run

```bash
# Clone repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git

# Open iOS project
cd mobile/ios
open SecureCipherStegno.xcodeproj

# Install dependencies (if using CocoaPods)
pod install
open SecureCipherStegno.xcworkspace

# Or using Swift Package Manager (SPM)
# Dependencies are managed in Xcode
```

## Dependencies

### Swift Package Manager
```swift
dependencies: [
    .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),
    .package(url: "https://github.com/kishikawakatsumi/KeychainAccess.git", from: "4.2.2")
]
```

## Features Implementation Status

- [x] Basic UI structure
- [x] Biometric authentication framework
- [x] API client setup
- [x] Caesar cipher implementation
- [x] Keychain integration
- [ ] Full cryptography implementation
- [ ] Steganography implementation
- [ ] Share extension
- [ ] Widgets
- [ ] Camera integration
- [ ] QR code scanning
- [ ] App Store submission

## Security Features

- **Biometric Authentication**: Face ID / Touch ID
- **Keychain Storage**: Secure key storage in iOS Keychain
- **App Transport Security**: HTTPS only
- **Data Protection**: File-level encryption
- **Certificate Pinning**: SSL pinning for API calls
- **Secure Enclave**: Hardware-backed key storage

## Screenshots

(Screenshots will be added after UI implementation)

## App Store

Coming soon to the Apple App Store

## License

MIT License - See main repository LICENSE file
